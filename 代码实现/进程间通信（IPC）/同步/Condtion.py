import threading
import time
"""
condition提供了多线程通信机制，condition注重等待，lock注重上锁，都用于线程间的同步
acquire() —  线程锁，注意线程条件变量Condition中的所有相关函数使用必须在acquire() /release() 内部操作；
release() — 释放锁，注意线程条件变量Condition中的所有相关函数使用必须在acquire() /release() 内部操作；
wait(timeout) —  线程挂起(阻塞状态)，直到收到一个notify通知或者超时才会被唤醒继续运行（超时参数默认不设置，可选填，类型是浮点数，单位是秒）。wait()必须在已获得Lock前提下才能调用，否则会触发RuntimeError；
notify(n=1) —  通知其他线程，那些挂起的线程接到这个通知之后会开始运行，缺省参数，默认是通知一个正等待通知的线程,最多则唤醒n个等待的线程。notify()必须在已获得Lock前提下才能调用，否则会触发RuntimeError，notify()不会主动释放Lock；
notifyAll() —  如果wait状态线程比较多，notifyAll的作用就是通知所有线程；

利用条件变量解决生产者消费者问题
消费者从count中取数据，每次取完数据，通过notify唤醒生产者线程，释放锁，生产者获得锁，检查count,若count>1000,挂起，notify通知消费者，释放锁，消费者再次消费
"""
class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global count
        while True:
            if con.acquire():
                if count > 1000:
                    con.wait()
                else:
                    count = count+100
                    print("\n")
                    print('-----生产者线程%s启动-----' % self.name)
                    msg = self.name+' produce 100, count=' + str(count)
                    print(msg)
                con.notify()
                con.release()
                print('-----生产者线程%s关闭-----' % self.name)
                time.sleep(1)


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global count
        while True:
            if con.acquire():
                if count < 100:
                    con.wait()
                else:
                    count = count-30
                    print("\n")
                    print('-----消费者线程%s启动-----' % self.name)
                    msg = self.name+' consume 30, count='+str(count)
                    print(msg)
                con.notify()
                con.release()
                print('-----消费者线程%s关闭-----' % self.name)
                time.sleep(1)

count = 500
con = threading.Condition()

def test():
    for i in range(2):
        p = Producer()
        p.start()
    for i in range(5):
        c = Consumer()
        c.start()

if __name__ == '__main__':
    test()