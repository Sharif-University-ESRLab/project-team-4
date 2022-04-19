import queue
import threading
import serial
import random
import time

SAMPLE_DELAY = 10  # milli
buffer_lock = threading.Lock()
adc_inputs = []
pwm_queue = queue.Queue()


####  REAL  ####
def read_adc(ser: serial.SerialBase):
    try:
        sample = ser.readline().strip()
        if sample.decode("utf-8").isnumeric():
            sample = int(sample)
            with buffer_lock:
                adc_inputs.append(sample)
                # pwm_queue.put(sample)  # Just for test
    except Exception as e:
        print(e)


def write_adc(ser: serial.SerialBase):
    with buffer_lock:
        if pwm_queue.empty():
            val = 0
        else:
            val = pwm_queue.get()
    ser.write(str.encode('{}\n'.format(val)))


def start_read_adc_thread():
    def continuous_read_adc():
        ser = serial.Serial(port='/dev/cu.usbmodem14201', baudrate=115200, timeout=1)
        while True:
            read_adc(ser)
            write_adc(ser)

    threading.Thread(target=continuous_read_adc).start()

####  FAKE   ####
# x = 500
# s = 0
#
#
# def read_adc():
#     global x, s
#     time.sleep(SAMPLE_DELAY / 1000)
#     s += random.randint(-3, 3)
#     s = min(s, 6)
#     s = max(s, -6)
#     x += s
#     x = min(x, 1024)
#     x = max(x, 0)
#     with buffer_lock:
#         adc_inputs.append(x)
#         # pwm_queue.put(x)  # Just for test
#
#
# def write_adc():
#     with buffer_lock:
#         if pwm_queue.empty():
#             val = 0
#         else:
#             val = pwm_queue.get()
#     print('Output: ', val)
#
#
# def start_read_adc_thread():
#     def continuous_read_adc():
#         while True:
#             read_adc()
#             write_adc()
#
#     threading.Thread(target=continuous_read_adc).start()
