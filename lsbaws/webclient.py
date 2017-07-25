import socket

# 创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立链接
s.connect(('127.0.0.1', 8888))


print(s.recv(1024).decode('utf-8'))

for data in [b'hans', b'tes', b'sry']:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))

s.send(b'exit')
s.close()
