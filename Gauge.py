"""
This project is for gauge
"""
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
import re


def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])


class Gauge:
    def __init__(self):
        self.run_complete = -1
        self.run_error = 0
        self.data = ""
        self.fft_y = []
        self.mode = 0
        self.wait = 0
        self.send = 0

    # Gauge Run
    def Gauge_Run(self):
        # self.Calculation_Function()
        pass

    # Data calculation
    def Calculation_Function(self):
        self.fft_y = abs(fft(self.data))

    # Data decoder
    def Data_Decoder(self):
        try:
            start_index = re.search(':', self.data).start()
            self.data = self.data[start_index:]
            end_index = re.search('\r\n', self.data).start()
            self.data = self.data[1:end_index]   # we chose start index and end index clip
            self.data = self.data.split(',')
            # self.data = [encode(i) for i in self.data]
            # self.data = [i.replace(' ', '') for i in self.data]
            self.data = [int(i) for i in self.data]
            self.fft_y = abs(fft(self.data))
            self.run_complete = 0
            # else:
            #     print('error')
            #     self.run_error = 1

        except:
            print('error')
            self.run_error = 1
            pass


def main():
    print("Hello! This is a project of gauge!")


if __name__ == "__main__":
    main()












