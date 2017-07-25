import socket
import time
import threading

HOST, PORT = '', 8888

# Socket时，AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6
# SOCK_STREAM指定使用面向流的TCP协议，这样，一个Socket对象就创建成功
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 监听端口
s.bind((HOST, PORT))
# listen()方法开始监听端口，传入的参数指定等待连接的最大数量
s.listen(1)
print ('Serving HTTP on port %s ...' % PORT)


def tcplink(sock, addr):
    print('accept new Connection from %s: %s... ' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s: %s clossed.' % addr)

# 服务器程序通过一个永久循环来接受来自客户端的连接
# accept()会等待并返回一个客户端的连接
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
