import threading
import random
import time

"""
信号量（semaphore）是线程间同步的一种机制，用于多线程中同步对共享资源的使用，用于表明当前的共享资源可以有多少个线程去并发读取。信号量可分为二值信号量（值为0或1）和计数信号量（初始化为任意非负值N的信号量），二值信号量类似于互斥锁。
在threading中，信号量有两个函数：
acquire函数：当线程要读取关联了信号量的共享资源时，必须先调用acquire，将信号量的值减一，如果值为非负，得到操作资源的权限，如果是负值，则线程被挂起，直到其他线程释放资源
release函数：当线程对共享资源操作完毕，通过release函数是释放，此时信号量的值加一，等待队列中排在最前面的线程会拿到权限
信号量与互斥锁与条件变量的关系：
1.互斥锁必须由给他上锁的线程解锁，但信号量的挂出不必由执行他等待过程的同一个消费者的问题线程执行，典型的是一个生产者和一个消费者的问题
2.互斥锁要么被锁住，要么被解开（二值状态，类似于二值信号量）
3.信号量内部有一个计数值，那么信号量的挂出总会被记录下来（值加一），但如果一个条件变量发送唤醒信号时，如果没有线程等待在该条件变量上时，那么该信号会丢失。

需要注意的地方，信号量同步机制只有在线程操作为原子操作时，才会没问题，即该线程在获得权限进行操作时，系统不能切换到另外一个线程去acquire获得权限
"""

class MyThread(threading.Thread):
    availableTables = ['A', 'B', 'C', 'D', 'E']

    def __init__(self, threadName, semaphore):
        self.interval = random.randrange(1, 6)
        self.semaphore = semaphore
        threading.Thread.__init__(self, name=threadName)

    def run(self):
        self.semaphore.acquire()
        # acquire a semaphore
        table = MyThread.availableTables.pop()
        print("%s entered;seated at table %s." % (self.getName(), table))
        time.sleep(self.interval)

        # free a table
        print("%s exiting,freeing table %s." % (self.getName(), table))
        MyThread.availableTables.append(table)

        self.semaphore.release()


mySemaphore = threading.Semaphore(4)


def Test():
    threads = []

    for i in range(1, 10):
        threads.append(MyThread("thread" + str(i), mySemaphore))

    for i in range(len(threads)):
        threads[i].start()


if __name__ == '__main__':
    Test()
