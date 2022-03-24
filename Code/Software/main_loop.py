from arduino_serial import *

for i in range(10):
    print(read_adc())

ser.close()
