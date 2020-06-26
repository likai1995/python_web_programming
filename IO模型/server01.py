from multiprocessing import Process
from threading import Thread
import select
from socket import *


def recv_data(new_socket, client_info):
    print("客户端{}已经连接".format(client_info))
    # 接受数据
    raw_data = new_socket.recv(1024)
    if not raw_data: pass
    while raw_data:
        if raw_data == 'q':

            break
        else:
            print(f"收到来自{client_info}的数据：{raw_data.decode()}")
            new_socket.send(raw_data)
            raw_data = new_socket.recv(1024)

    print('客户端{}已断开连接'.format(client_info))
    new_socket.close()



def main1():
    """
    多进程并发阻塞
    利用进程把客户端和服务器进行管理，当有新的客户端连接到服务器时，就创建一个新的进程来管理，通过操作系统的调度，从而实现了并发的操作
    :return:
    """
    # 实例化socket对象
    socket_server = socket(AF_INET, SOCK_STREAM)
    # 设置端口复用
    socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 绑定IP地址和端口
    socket_server.bind(("", 7788))
    # 改主动为被动，监听客户端
    socket_server.listen(5)
    print("------主进程，开始连接------")
    while True:
        # 等待连接
        new_socket, client_info = socket_server.accept()
        p = Process(target=recv_data, args=(new_socket, client_info))
        p.start()
        # 多进程会复制父进程的内存空间，所以父进程中new_socket也必须关闭
        new_socket.close()


def main2():
    """
    多线程并发阻塞
    多线程和多进程类似，只是线程间共享内存空间，要注意变量的管理
    :return:
    """
    # 实例化socket对象
    socket_server = socket(AF_INET, SOCK_STREAM)
    # 设置端口复用
    socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 绑定IP地址和端口
    socket_server.bind(("", 7788))
    # 改主动为被动，监听客户端
    socket_server.listen(5)
    print("------主进程，开始连接------")
    while True:
        # 等待连接
        new_socket, client_info = socket_server.accept()
        p = Thread(target=recv_data, args=(new_socket, client_info))
        p.start()
        # 多线程共享一片内存区域，所以这里不用关闭
        # new_socket.close()


def main3():
    """
    在操作系统层面上，系统提供了一个select接口，它会轮询给定的文件描述符状态，
    如果其中有描述符的状态改变，select()就会返回有变化的文件描述符。
    利用select函数实现io多路复用，进程阻塞在select函数，而不是阻塞在recv函数

    优点：良好的跨平台支持

    缺点：
    1.监测的文件描述符数量有最大限制，Linux系统一般为1024，可以修改宏定义或者内核进行修改，但是会造成效率低下；
    2.对文件描述符采用轮询机制，每个文件描述符都会询问一遍，这样很消耗CPU时间
    3.select()和poll()将就绪的文件描述符告诉进程后，如果进程没有对其进行IO操作，
      那么下次调用select()和poll()的时候将再次报告这些文件描述符，
      所以它们一般不会丢失就绪的消息，这种方式称为水平触发（Level Triggered）
    :return:
    """
    socket_server = socket(AF_INET, SOCK_STREAM)
    #设置端口复用，sol_socket：通用套接字选项
    socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    socket_server.bind(("", 7788))
    socket_server.listen(5)
    #创建套接字列表
    socket_list = [socket_server]
    print('------主进程，开始连接------')
    while True:
        read_list, _, _ = select.select(socket_list, [], [])
        #print(len(socket_list), len(read_list))
        for sock in read_list:
            if sock == socket_server:
                new_socket, client_info = socket_server.accept()
                print("客户端{}已连接".format(client_info))
                socket_list.append(new_socket)
            else:
                raw_data = sock.recv(1024)
                if not raw_data: pass
                while raw_data:
                    if raw_data == 'q':
                        break
                    else:
                        print(f"收到来自{client_info}的数据：{raw_data.decode()}")
                        new_socket.send(raw_data)
                        raw_data = new_socket.recv(1024)
                print('客户端{}已断开'.format(client_info))
                sock.close()
                socket_list.remove(sock)


def main4():
    """
    epoll是对select和poll的改进（只在Linux系统存在）
    优点：
    1.文件描述符数目没有上限，最大数量取决于内存的大小（这一点poll同样实现）
    2.基于事件就绪通知方式：一旦被监听的某个文件描述符就绪，内核会采用类似于callback的回调机制，迅速激活这个文件描述符，而不是采用轮询的方式遍历整个描述符列表  
    3.维护就绪队列：当文件描述符就绪，就会被放到内核中的一个就绪队列中，这样调用epoll_weit获取就绪文件描述符的时候，只要取队列中的元素即可。
    4.事件触发机制包括水平触发和边缘触发，而select和poll只有水平触发
    """
    sock_server = socket(AF_INET, SOCK_STREAM)
    # 绑定IP和端口
    sock_server.bind(("", 7788))
    # 将主动模式设置为被动模式，监听连接
    sock_server.listen(5)
    # 创建epoll监测对象
    epoll = select.epoll()
    # print("未注册epoll对象：{}".format(epoll))
    # 注册主套接字,监控读状态
    epoll.register(sock_server.fileno(), select.EPOLLIN)
    # print("注册了主套接字后：{}".format(epoll))
    # 创建字典，保存套接字对象
    sock_dicts = {}
    # 创建字典，保存客户端信息
    client_dicts = {}
    while True:
        # print("所有套接字：{}".format(sock_dicts))
        # print("所有客户端信息：{}".format(client_dicts))
        # 程序阻塞在这，返回文件描述符有变化的对象
        poll_list = epoll.poll()
        # print("有变化的套接字：{}".format(poll_list))
        for sock_fileno, events in poll_list:
            # print("文件描述符：{}，事件：{}".format(sock_fileno, events))
            # 判断是否是主套接字
            if sock_fileno == sock_server.fileno():
                # 创建新套接字
                new_sock, client_info = sock_server.accept()
                print(f"客户端：{client_info}已连接")
                # 注册到epoll监测中
                epoll.register(new_sock.fileno(), select.EPOLLIN)
                # 添加到套接字字典当中
                sock_dicts[new_sock.fileno()] = new_sock
                client_dicts[new_sock.fileno()] = client_info
            else:
                # 接收消息
                raw_data = sock_dicts[sock_fileno].recv(1024)
                if raw_data:
                    print(f"来自{client_dicts[sock_fileno]}的数据：{raw_data.decode('gb2312')}")
                else:
                    # 关闭连接
                    sock_dicts[sock_fileno].close()
                    # 注销epoll监测对象
                    epoll.unregister(sock_fileno)
                    # 数据为空，则客户端断开连接，删除相关数据
                    del sock_dicts[sock_fileno]
                    del client_dicts[sock_fileno]


if __name__ == '__main__':
    main3()

