# This is a project about WiFi server

import sys
import socket
import threading
'''
AF_INET: 基于IPv4协议的网络
SOCK_STREAM(默认)，基于TCP协议
SOCK_STREAM:基于TCP协议
使用多协程的方式处理多个客户端的数据
'''
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socks = []

def Server_Init():
    print("Hello this is Server!")
    ip_address = input("Please input the Server ip address:")
    ip_port = int(input("Please input the Server ip port:"))
    global  Server_ip
    Server_ip = (ip_address, ip_port)
    Server.bind(Server_ip)
    Server.listen(5)             # Maximum connections 5



def Server_Monitoring():
    while True:
        print("Enter monitoring state......")
        print("Waiting for client {}".format(len(socks) + 1))
        conn, addr =  Server.accept()
        conn.setblocking(0)
        socks.append(conn)
        print("Find the client {}".format(len(socks) + 1))
        print(addr)


def Server_Handle():              # Creat a child thread
    while True:
        for conn in socks:
            try:  # Check the client whether breaks
                client_data = conn.recv(1024)
            except Exception as e:
                continue
            if not client_data:
                socks.remove(conn)
                print("The client has closed")
                continue

            if client_data == b'close server\r\n':
                print("Close the Server")
                Server.close()
                print("Server has closed!\r\n")
                sys.exit(0)

            elif client_data == b'close client\r\n':
                print("Close the Client")
            print(client_data.decode("utf-8"))
            conn.send('Server reply content\r\n'.encode("utf-8"))  # Reply a message to client


t = threading.Thread(target = Server_Handle)     # child threading

def main():
    Server_Init()
    Server_Monitoring()


if __name__ == "__main__":
    t.start()
    main()
