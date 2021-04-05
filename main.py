# This is a project about WiFi server

import sys
import socket
import threading
import time
import Gauge
from PySide2.QtWidgets import QApplication, QMainWindow, QTextBrowser
from PySide2.QtCore import Signal, QObject, QTimer
import gauge_ui
import numpy as np
'''
AF_INET: 基于IPv4协议的网络
SOCK_STREAM(默认)，基于TCP协议
SOCK_STREAM:基于TCP协议
使用多协程的方式处理多个客户端的数据
'''


# 第一个socket是包的名字
class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.ip_address = '0,0,0,0,'
        self.ip_port = 0
        self.ip = ()
        self.number = 0
        self.socks = []
        self.ga = Gauge.Gauge()

    # Server Init
    def Server_Init(self):
        # self.ip_address = input("Please input the Server ip address:")
        # self.ip_port = int(input("Please input the Server ip port:"))
        # self.number = int(input("Please input the number of listening Clients:"))
        self.ip_address = "192.168.43.177"
        self.ip_port = 8058
        self.number = 5
        self.ip = (self.ip_address, self.ip_port)
        self.socket.bind(self.ip)
        self.socket.listen(self.number)  # define maximum connections

    # monitoring client
    def Server_Monitoring(self):
        t_check = threading.Thread(target=self.Cheack_Heart)  # Heart threading
        t_check.start()
        t_ga = threading.Thread(target=self.Server_GaugeRun)
        t_ga.start()
        while True:
            print("Enter monitoring state......")
            print("Waiting for client ".format(len(self.socks) + 1))
            c = Client()
            c.conn, c.addr = self.socket.accept()
            c.time = time.time()
            self.socks.append(c)
            c.threading = threading.Thread(target=c.Client_Handle)  # child threading
            c.threading.start()
            print("Find the client {}".format(len(self.socks)))
            print(c.addr)

    # check all client heart
    def Cheack_Heart(self):
        while True:
            for c in self.socks:
                if (time.time() - c.time) > 100:
                    c.conn.close()
                    self.socks.remove(c)
                    print("{} users are offline".format(c.addr))

    def Server_GaugeRun(self):
        self.ga.Gauge_Run()
        while True:
            for c in self.socks:
                if c.receive_complete == 1 and self.ga.wait == 0:
                    self.ga.wait = self.ga.wait + 1
                    self.ga.data = c.message.decode('gb18030')
                    self.ga.Data_Decoder()

                if self.ga.send == 1:
                    c.send_state = self.ga.mode
                    self.ga.send = 0


# client class
class Client:
    def __init__(self):
        self.conn = socket.socket()
        self.addr = 0
        self.time = 0
        self.message = 0
        self.send_state = 0
        self.receive_complete = 0
        self.threading = 0
        self.wait = 1

    def Send(self):
        while True:
            if self.send_state != 0 and self.send_state != 'ok':
                try:
                    self.conn.send(('%s' % ((str(chr(0x3A)))+str(self.send_state))).encode("utf-8"))
                except:
                    pass
                else:
                    self.send_state = 0

    def Client_Handle(self):  # Creat a child thread
        time.sleep(3)
        send_message = threading.Thread(target=self.Send)
        send_message.start()
        while True:
            if self.receive_complete == 0:                         # Check free state
                try:  # Check the client whether breaks
                    self.message = self.conn.recv(4096)
                except Exception as e:
                    print("This threading has finished")
                    break
                # change some state signal
                self.receive_complete = 1
                self.wait = 0
                self.time = time.time()

                if self.message == b'close server\r\n':
                    print("Server has closed!\r\n")
                    sys.exit(0)

                elif self.message == b'close client\r\n':
                    self.conn.close()
                    print("Client has closed!")
                    break


# my signals class, it can emit graph refresh signal to main process
class MySignals(QObject):
    graph_refresh = Signal()


# gui class
class Gui:
    def __init__(self):
        self.app = QApplication([])
        self.mywin = gauge_ui.MyGraphWindows()
        self.s = Server()
        self.ms = MySignals()
        self.timer = 0
        self.curve1 = []
        self.curve2 = []

    def Gauge_Gui(self):
        self.s.Server_Init()

        # set signal connect
        self.ms.graph_refresh.connect(self.Win_Show)

        # set button connect
        self.mywin.start_button.clicked.connect(self.Start_main)
        self.mywin.button1.clicked.connect(lambda: self.Change_Show(1))
        self.mywin.button2.clicked.connect(lambda: self.Change_Show(2))
        self.mywin.button3.clicked.connect(lambda: self.Change_Show(3))
        self.mywin.button4.clicked.connect(lambda: self.Change_Show(4))
        self.mywin.button5.clicked.connect(lambda: self.Change_Show(5))
        self.mywin.button6.clicked.connect(lambda: self.Change_Show(6))
        self.Win_Show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.Show_Refresh)
        self.timer.start(50)
        self.mywin.show()
        self.app.exec_()
        sys.exit()

    def Change_Show(self, choice):
        self.s.ga.mode = choice
        self.s.ga.send = 1

    # Win show the graph
    def Win_Show(self):
        self.mywin.p1.setYRange(0, 4096, padding=0)
        self.curve1 = self.mywin.p1.plot(self.mywin.x, self.mywin.y, pen='g', clear=True)
        self.curve2 = self.mywin.p2.plot(self.mywin.x, self.mywin.y, pen='g', clear=True)

    def Show_Refresh(self):
        # if run_complete is 0, it will run the plot procession
        if self.s.ga.run_complete == 0:
            if self.s.ga.mode == 1:
                self.s.ga.Gauge_Run()
                self.mywin.x = np.linspace(0, len(self.s.ga.data) - 1, len(self.s.ga.data))
                self.mywin.y = self.s.ga.data
                self.curve1.setData(self.mywin.x, self.mywin.y)
                self.mywin.y = self.s.ga.fft_y[1:]
                self.curve2.setData(self.mywin.y)
                self.s.ga.run_complete = 1  # if run state is 1, the gauge will display the data
                for c in self.s.socks:
                    c.receive_complete = 0
                    self.s.ga.wait = 0
        # if the data processing occur error, it will also reset receive_complete
        elif self.s.ga.run_error == 1:
            for c in self.s.socks:
                c.receive_complete = 0
                self.s.ga.wait = 0

    def main(self):
        self.s.Server_Monitoring()

    # start main function
    def Start_main(self):
        main_threading = threading.Thread(target=self.main)
        main_threading.start()


if __name__ == "__main__":
    print("Hello this is Server!")
    g = Gui()
    g.Gauge_Gui()

