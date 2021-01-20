# This is a project about WiFi server

import sys
import socket
import threading
import time
'''
AF_INET: 基于IPv4协议的网络
SOCK_STREAM(默认)，基于TCP协议
SOCK_STREAM:基于TCP协议
使用多协程的方式处理多个客户端的数据
'''

class Server:         # 第一个socket是包的名字
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.ip_address = '0,0,0,0,'
        self.ip_port = 0
        self.ip = ()
        self.number = 0
        self.socks = []

    def Server_Init(self):
        self.ip_address = input("Please input the Server ip address:")
        self.ip_port = int(input("Please input the Server ip port:"))
        self.number = int(input("Please input the number of listening Clients:"))
        self.ip = (self.ip_address, self.ip_port)
        self.socket.bind(self.ip)
        self.socket.listen(self.number)  # define maximum connections

    def Server_Monitoring(self):               # monitoring client
        tcheck = threading.Thread(target=self.Cheack_Heart)  # Heart threading
        tcheck.start()
        while True:
            print("Enter monitoring state......")
            print("Waiting for client {}".format(len(self.socks) + 1))
            c = client()
            c.conn, c.addr = self.socket.accept()
            c.time = time.time()
            self.socks.append(c)
            c.threading = threading.Thread(target=c.Handle)  # child threading
            c.threading.start()
            print("Find the client {}".format(len(self.socks)))
            print(c.addr)

    def Cheack_Heart(self):         # check all client heart
        while True:
            for c in self.socks:
                if (time.time() - c.time) > 5:
                    c.conn.close()
                    self.socks.remove(c)
                    print("{} users are offline".format(c.addr))

class client:                      # client class
    def __init__(self):
        self.time = 0
        self.message = 0
        self.conn = socket.socket()
        self.addr = 0
        self.threading = 0
    def Handle(self):  # Creat a child thread
        while True:
            try:  # Check the client whether breaks
                self.message = self.conn.recv(1024)
            except Exception as e:
                print("This threading has finished")
                break
            self.time = time.time()
            print(self.time)
            if self.message == b'close server\r\n':
                print("Close the Server")
                print("Server has closed!\r\n")
                sys.exit(0)

            elif self.message == b'close client\r\n':
                self.conn.close()
                print("Close the Client")
                break

            else:
                print(self.message.decode("utf-8"))
            self.conn.send('Server reply content\r\n'.encode("utf-8"))  # Reply a message to client







def main():
    s = Server()
    s.Server_Init()
    s.Server_Monitoring()

if __name__ == "__main__":
    print("Hello this is Server!")
    main()
