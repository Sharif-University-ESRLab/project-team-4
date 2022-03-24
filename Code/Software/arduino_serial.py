import serial
import random
import time

ser = serial.Serial(port='/dev/cu.usbmodem14201', baudrate=9600, timeout=5)


def read_adc():
    return int(ser.readline().strip())

# fake (for test)
# def read_adc():
#     time.sleep(1)
#     return random.randint(0, 1023)
