import socket

socket_client = socket.socket()
socket_client.connect(('127.0.0.1', 7788))

while 1:
    cmd = input("Please input cmd:")
    if not cmd: continue
    elif cmd == 'q': break
    socket_client.send(cmd.encode('utf-8'))
    data = socket_client.recv(1024)
    print('recv:', data.decode())

socket_client.close()