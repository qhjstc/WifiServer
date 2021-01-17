# This is a project about WiFi server

import sys
import socket
'''
AF_INET: 基于IPv4协议的网络
SOCK_STREAM(默认)，基于TCP协议
SOCK_STREAM:基于TCP协议
'''
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def main():
    print("Hello this is Server!")
    # ip_address = input("Please input the Server ip address:")
    # ip_port = int(input("Please input the Server ip port:"))
    # Server_ip = (ip_address, ip_port)
    Server_ip = ('192.168.50.44', 8086)
    # print(ip_address)
    Server.bind(Server_ip)
    Server.listen(5)             # Maximum connections 5
    print("Enter monitoring state......")
    conn,addr = Server.accept()
    print("Find the client")
    print(addr)
    while 1:
        client_data = conn.recv(1024)
        if client_data == b'close server\r\n':
            print("Close the Server")
            break
        print(client_data.decode("utf-8"))
        conn.send('Server reply content\r\n'.encode("utf-8"))
    conn.close()

if __name__ == "__main__":
    main()