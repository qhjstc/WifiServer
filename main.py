# This is a project about WiFi server

import sys
import socket
import asyncio
'''
AF_INET: 基于IPv4协议的网络
SOCK_STREAM(默认)，基于TCP协议
SOCK_STREAM:基于TCP协议
'''
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def main():
    print("Hello this is Server!")
    ip_address = input("Please input the Server ip address:")
    ip_port = int(input("Please input the Server ip port:"))
    Server_ip = (ip_address, ip_port)
    Server.bind(Server_ip)
    Server.listen(5)             # Maximum connections 5
    print("Enter monitoring state......")
    conn, addr = Server.accept()
    print("Find the client")
    print(addr)
    while 1:
        try:                      # Check the client whether breaks
            conn.settimeout(5)
            client_data = conn.recv(1024)
        except:
            print("The client has closed")
            print("Enter monitoring state......")  # Start connecting to the next client
            conn, addr = Server.accept()
            print("Find the client")
            print(addr)

        if client_data == b'close server\r\n':
            print("Close the Server")
            break
        if client_data == b'close client\r\n':
            print("Close the Client")
        print(client_data.decode("utf-8"))
        conn.send('Server reply content\r\n'.encode("utf-8"))    # Reply a message to client

    Server.close()

if __name__ == "__main__":
    main()