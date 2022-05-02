#include <iostream>
#include <stdio.h>
#include <csignal>
#include <winsock2.h>
#include <ws2tcpip.h>
#define MIRAICPP_STATICLIB
#include <mirai.h>
using namespace std;
using namespace Cyan;

static int global_raw_output = 0; 
static int global_silent_mode = 0;
static int global_disable_colors = 0;
static int global_connection_alive = 1;
static int global_rsock;
static int global_wait_seconds = 0;

int main(int argc, char* argv[])
{
    MiraiBot bot; //创建机器人类，此类不能复制或者赋值
    SessionOptions opts = SessionOptions::FromCommandLine(argc, argv);//从命令行读取连接参数
    bot.Connect(opts);//连接mirai-api-http
    printf("机器人启动成功\n");
    //接收临时消息并回复
    bot.On<GroupMessage>(
        [](GroupMessage m)
        {
            m.Reply(m.MessageChain);
        });
    //自动重连
    bot.On<LostConnection>([&](LostConnection error)
    {
        printf(error.ErrorMessage.c_str(),"(", error.Code ,")\n");
        while (true)
        {
            try
            {   
                printf("尝试与 mirai-api-http 重新建立连接...\n");
                bot.Reconnect();
                break;
            }
            catch (const std::exception& ex)
            {
                printf(ex.what(),"\n");
            }
            MiraiBot::SleepSeconds(1);
        }
        printf("成功与 mirai-api-http 重新建立连接!\n");
    });
    //退出部分
    char exit;
    while ((exit = getchar()) != 'q');
    bot.Disconnect();//在退出前断开连接，不然会导致内存泄漏
}

//Rcon连接和命令发送部分
//定义结构体
struct rconpacket
{
	int size;
	int id;
	int cmd;
	char data[4096];
} rcon_packet;

void net_init_WSA(void)
{
	WSADATA wsadata;
	WORD version = MAKEWORD(2, 2);
	int err = WSAStartup(version, &wsadata);
	if (err != 0)
	{
		printf("WSAStartup失效。错误: %d。\n", err);
		exit(EXIT_FAILURE);
	}
}

void sighandler(int sig)
{
	if (sig == SIGINT)
	{
		putchar('\n');
	}
	global_connection_alive = 0;
}

void exit_proc(void)
{
	if (global_rsock != -1)
	{
		net_close(global_rsock);
	}
}

void net_close(int sd)
{
	closesocket(sd);
	WSACleanup();
}

int net_connect(const char *host, const char *port)
{
	int sendpacket;
	struct addrinfo hints;
	struct addrinfo *server_info, *p;
	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = IPPROTO_TCP;
	net_init_WSA();
	int ret = getaddrinfo(host, port, &hints, &server_info);
	if (ret != 0)
	{
		printf("名称解析失败。\n");
		printf("错误 %d: %s", ret, gai_strerror(ret));
		exit(EXIT_FAILURE);
	}
	for (p = server_info; p != NULL; p = p->ai_next)
	{
		sendpacket = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
		if (sendpacket == -1)
		{
			continue;
		}
		ret = connect(sendpacket, p->ai_addr, p->ai_addrlen);
		if (ret == -1)
		{
			net_close(sendpacket);
			continue;
		}
		break;
	}
	if (p == NULL)
	{
		printf("连接失败\n");
		freeaddrinfo(server_info);
		exit(EXIT_FAILURE);
	}
	freeaddrinfo(server_info);
	return sendpacket;
}

rconpacket *packet_build(int id, int cmd, char *s1)
{
	static rconpacket packet = {0, 0, 0, {0x00}};
	int len = strlen(s1);
	if (len >= 4096)
	{
		printf("警告：命令过长(%d)。命令的最大长度为: %d.\n", len, 4096 - 1);
		return NULL;
	}
	packet.size = sizeof(int) * 2 + len + 2;
	packet.id = id;
	packet.cmd = cmd;
	strncpy(packet.data, s1, 4096 - 1);
	return &packet;
}

int net_send_packet(int sd, rconpacket *packet)
{
	int len;
	int total = 0;
	int bytesleft;
	int ret = -1;
	bytesleft = len = packet->size + sizeof(int);
	while (total < len)
	{
		ret = send(sd, (char *)packet + total, bytesleft, 0);
		if (ret == -1)
		{
			break;
		}
		total += ret;
		bytesleft -= ret;
	}
	return ret == -1 ? -1 : 1;
}

int net_clean_incoming(int sd, int size)
{
	char tmp[size];
	int ret = recv(sd, tmp, size, 0);
	if (ret == 0)
	{
		printf("连接丢失\n");
		global_connection_alive = 0;
	}
	return ret;
}

rconpacket *net_recv_packet(int sd)
{
	int psize;
	static rconpacket packet = {0, 0, 0, {0x00}};
	int ret = recv(sd, (char *)&psize, sizeof(int), 0);
	if (ret == 0)
	{
		printf("连接丢失\n");
		global_connection_alive = 0;
		return NULL;
	}
	if (ret != sizeof(int))
	{
		printf("错误：无效的包大小(%d)。\n", ret);
		global_connection_alive = 0;
		return NULL;
	}
	if (psize < 10 || psize > 4096)
	{
		printf("错误：无效的包大小。(%d)包大小应当大于10小于%d.\n", psize, 4096);
		if (psize > 4096 || psize < 0)
			psize = 4096;
		net_clean_incoming(sd, psize);
		return NULL;
	}
	packet.size = psize;
	int received = 0;
	while (received < psize)
	{
		ret = recv(sd, (char *)&packet + sizeof(int) + received, psize - received, 0);
		if (ret == 0)
		{ 
			printf("连接丢失\n");
			global_connection_alive = 0;
			return NULL;
		}
		received += ret;
	}
	return &packet;
}

int rcon_auth(int sock, char *passwd)
{
	int ret;
	rconpacket *packet = packet_build(0xBADC0DE, 3, passwd);
	if (packet == NULL)
	{
		return 0;
	}
	ret = net_send_packet(sock, packet);
	if (!ret)
	{
		return 0;
	}
	packet = net_recv_packet(sock);
	if (packet == NULL)
	{
		return 0;
	}
	return packet->id == -1 ? 0 : 1;
}

int connectserver(char* host,char* pass,char* port)
{
    int terminal_mode = 0;
	int exit_code = EXIT_SUCCESS;
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	atexit(&exit_proc);
	signal(SIGABRT, &sighandler);
	signal(SIGTERM, &sighandler);
	signal(SIGINT, &sighandler);
	net_init_WSA();
	global_rsock = net_connect(host, port);
	if (rcon_auth(global_rsock, pass))
	{
        printf("验证成功\n");
        return 1;
	}
    else 
	{
		printf("身份验证失败\n");
		return -1;
	}
}



