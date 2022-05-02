#include <iostream>
#include <stdio.h>
#define MIRAICPP_STATICLIB
#include <include/mirai/MiraiBot.hpp>
using namespace std;
using namespace Cyan;
int main(int argc, char* argv[])
{
    MiraiBot bot; //创建机器人类，此类不能复制或者赋值
    SessionOptions opts = SessionOptions::FromCommandLine(argc, argv);//从命令行读取连接参数
    bot.Connect(opts);//连接mirai-api-http
    printf("机器人启动成功\n");
    //接收临时消息并回复
    bot.On<TempMessage>(
        [](TempMessage m)
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