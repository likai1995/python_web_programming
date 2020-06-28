import socket
import multiprocessing
import threading

def read_msg(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if data:  # 正常接收数据
                print('收到{}:数据{}'.format(addr,data.decode()))
                conn.send(data)
            else:  # 收到空消息，关闭
                print('close:{}'.format(addr))
                break
        except Exception as e:
            print(e)
            break
    conn.close()

if __name__ == '__main__':
    #建立tcp套接字
    server = socket.socket()
    #设置端口复用
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #给套接字绑定地址与端口
    server.bind(('127.0.0.1', 9988))
    #设置为监听套接字，已连接队列最大为5
    server.listen(5)
    while True:
        print('-------主进程,等待连接------')
        #阻塞在accept，等待客户端连接
        conn, addr = server.accept()
        print('创建一个新的进程，和客户端{}通信'.format(addr))
        #建立客户端子进程
        client = multiprocessing.Process(target=read_msg, args=(conn, addr))
        # client = threading.Thread(target=readable, args=((conn, addr)))
        # p.start()
        client.start()
    #关闭套接字
    server.close()
