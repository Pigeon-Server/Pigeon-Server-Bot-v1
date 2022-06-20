# Bot 主体
# by Pigeon Server Team
import asyncio
from module.qq_bot import QQ_bot
# from module.kaiheila_bot import kaiheila_bot
# asyncio.get_event_loop().run_until_complete(
#     asyncio.gather(QQ_bot(), kaiheila_bot())
# )
QQ_bot()
# kaiheila_bot()
# from multiprocessing import Process, Pool
# if __name__ == '__main__':
#     a = Pool(2)
#     a.apply_async(QQ_bot(), args=[])
#     a.apply_async(kaiheila_bot(), args=[])
#     # p = Process(target=QQ_bot(), args=())
#     # m = Process(target=kaiheila_bot(), args=())
#     a.close()
#     a.join()

