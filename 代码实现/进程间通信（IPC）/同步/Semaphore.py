import threading
import random
import time

"""
�ź�����semaphore�����̼߳�ͬ����һ�ֻ��ƣ����ڶ��߳���ͬ���Թ�����Դ��ʹ�ã����ڱ�����ǰ�Ĺ�����Դ�����ж��ٸ��߳�ȥ������ȡ���ź����ɷ�Ϊ��ֵ�ź�����ֵΪ0��1���ͼ����ź�������ʼ��Ϊ����Ǹ�ֵN���ź���������ֵ�ź��������ڻ�������
��threading�У��ź���������������
acquire���������߳�Ҫ��ȡ�������ź����Ĺ�����Դʱ�������ȵ���acquire�����ź�����ֵ��һ�����ֵΪ�Ǹ����õ�������Դ��Ȩ�ޣ�����Ǹ�ֵ�����̱߳�����ֱ�������߳��ͷ���Դ
release���������̶߳Թ�����Դ������ϣ�ͨ��release�������ͷţ���ʱ�ź�����ֵ��һ���ȴ�������������ǰ����̻߳��õ�Ȩ��
�ź����뻥���������������Ĺ�ϵ��
1.�����������ɸ����������߳̽��������ź����Ĺҳ�������ִ�����ȴ����̵�ͬһ�������ߵ������߳�ִ�У����͵���һ�������ߺ�һ�������ߵ�����
2.������Ҫô����ס��Ҫô���⿪����ֵ״̬�������ڶ�ֵ�ź�����
3.�ź����ڲ���һ������ֵ����ô�ź����Ĺҳ��ܻᱻ��¼������ֵ��һ���������һ�������������ͻ����ź�ʱ�����û���̵߳ȴ��ڸ�����������ʱ����ô���źŻᶪʧ��

��Ҫע��ĵط����ź���ͬ������ֻ�����̲߳���Ϊԭ�Ӳ���ʱ���Ż�û���⣬�����߳��ڻ��Ȩ�޽��в���ʱ��ϵͳ�����л�������һ���߳�ȥacquire���Ȩ��
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
