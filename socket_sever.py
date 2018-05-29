# -*- coding: UTF-8 -*-
import socket
import threading
import time
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('127.0.0.1',9999))

    s.listen(2)
    print("wait for connect")

    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()
        
def tcplink(sock,addr):
   

    while True:
        message = input("请发送你想要输入的命令:")
        sock.send(message.encode())
        '''
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send('Hello, %s!' % data)
        '''
    sock.close()
    print ('Connection closed.')

if __name__ == "__main__":
    main()
