import socket

socket_client = socket.socket()
#连接套接字 ,与服务器连接
socket_client.connect(('127.0.0.1', 9988))

while True:
       cmd = input("请输入：:")
       if not cmd: 
           continue
       #客户端输入信息为‘EXIT’，断开连接
       elif cmd == 'EXIT':
           break
       #将输入信息发给服务器，并用utf-8进行编码
       socket_client.send(cmd.encode('utf-8'))
       #接受返回的数据
       data = socket_client.recv(1024)
       print('收到服务器返回数据：%s' % data.decode())

#关闭套接字
socket_client.close()
