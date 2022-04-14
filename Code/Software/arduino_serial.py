import threading
import serial
import random
import time

SAMPLE_DELAY = 10  # milli
buffer_lock = threading.Lock()
adc_inputs = []


def read_adc(ser: serial.SerialBase):
    try:
        sample = ser.readline().strip()
        if sample.decode("utf-8").isnumeric():
            sample = int(sample)
            with buffer_lock:
                adc_inputs.append(sample)
    except Exception as e:
        print(e)


def start_read_adc_thread():
    def continuous_read_adc():
        ser = serial.Serial(port='/dev/cu.usbmodem14201', baudrate=115200, timeout=1)
        while True:
            read_adc(ser)

    threading.Thread(target=continuous_read_adc).start()

# fake (for test)
# x = 500
# s = 0
#
#
# def read_adc(ser):
#     global x, s
#     time.sleep(SAMPLE_DELAY / 1000)
#     s += random.randint(-3, 3)
#     s = min(s, 6)
#     s = max(s, -6)
#     x += s
#     x = min(x, 1024)
#     x = max(x, 0)
#     adc_inputs.append(x)
