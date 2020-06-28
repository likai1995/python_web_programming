from multiprocessing import Process, Lock
import time
import json
import os


def task(name, mutex):
    query_ticket(name)
    #互斥锁用来保护不同线程/进程间共享数据的完整性，保证任意时刻有且只有一个进程/线程处理临界区（加锁与解锁间的代码）内的数据
    mutex.acquire()
    buy_ticket(name)
    mutex.release()

#模拟抢票练习
def query_ticket(name):
    """
    余票查询函数
    :param name:查询者名字
    :return:
    """
    time.sleep(1)
    #使用db.txt模拟从数据库中读取数据
    with open('db.txt', 'r', encoding='utf-8') as f:
        d = json.load(f)
        print("[%s] 查询到的剩余票数 [%s]" % (name, d['count']))

def buy_ticket(name):
    """
    购票函数
    :param name:
    :return:
    """
    time.sleep(1)
    with open('db.txt', 'r', encoding='utf-8') as f:
        d = json.load(f)
        if d.get('count') > 0:
            d['count'] -= 1
            time.sleep(1)
            json.dump(d, open('db.txt', 'w', encoding='utf-8'))
            print("<%s> 购票成功" % name)
        else:
            print("没有多于的票, <%s> 购票失败" % name)


if __name__ == '__main__':
    mutex = Lock()
    print("开始抢票...")
    for i in range(5):
        p = Process(target=task, args=('客户%s' % i, mutex))
        p.start()
        """
        使用join将并发改成串行，但串行的是整个task函数，而互斥锁串行的可以是task程序的部分代码
        """
        p.join()
