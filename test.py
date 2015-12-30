#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep

import serial

if __name__ == '__main__':

    t = serial.Serial('/dev/ttyUSB0', 115200)

    while True:
        t.write(b'#0 P2200 #1 P2200 T2000 \r')
        sleep(1000)
        t.write(b'#0 P800 #1 P800 T2000 \r')
        sleep(1000)
