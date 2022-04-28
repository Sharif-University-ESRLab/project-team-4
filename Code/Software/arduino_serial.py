import queue
import threading
import serial
import random
import time

NUM = 8
SAMPLE_DELAY = 10  # milli
buffer_lock = threading.Lock()
adc_inputs = [[] for _ in range(NUM)]
pwm_queues = [queue.Queue() for _ in range(NUM)]


####  REAL  ####
def read_adc(ser: serial.SerialBase):
    try:
        packet = ser.readline().strip().decode("utf-8")
        samples = packet.split('|')
        if len(samples) != (NUM + 1):
            return
        with buffer_lock:
            for i in range(NUM):
                if samples[i].isnumeric():
                    adc_inputs[i].append(int(samples[i]))
    except Exception as e:
        print(e)


def write_adc(ser: serial.SerialBase):
    packet = ''
    with buffer_lock:
        for i in range(NUM):
            if pwm_queues[i].empty():
                val = 0
            else:
                val = pwm_queues[i].get()
            packet += '{:4}|'.format(val)
    ser.write(str.encode('{}\n'.format(packet)))


def start_read_adc_thread():
    def continuous_read_adc():
        ser = serial.Serial(port='/dev/cu.usbmodem14201', baudrate=115200, timeout=1)
        while True:
            read_adc(ser)
            write_adc(ser)

    threading.Thread(target=continuous_read_adc).start()


####  FAKE   ####
# position_s = [random.randint(100, 900) for _ in range(NUM)]
# speed_s = [random.randint(-5, +5) for _ in range(NUM)]


# def read_adc():
#     time.sleep(SAMPLE_DELAY / 1000)
#     with buffer_lock:
#         for i in range(NUM):
#             speed_s[i] += random.randint(-3, 3)
#             speed_s[i] = min(speed_s[i], 6)
#             speed_s[i] = max(speed_s[i], -6)
#             position_s[i] += speed_s[i]
#             position_s[i] = min(position_s[i], 1024)
#             position_s[i] = max(position_s[i], 0)
#             adc_inputs[i].append(position_s[i])
#             pwm_queues[i].put(position_s[i])


# def write_adc():
#     with buffer_lock:
#         for i in range(NUM):
#             if pwm_queues[i].empty():
#                 val = 0
#             else:
#                 val = pwm_queues[i].get()
#             print('Output {}: {}'.format(i, val))


# def start_read_adc_thread():
#     def continuous_read_adc():
#         while True:
#             read_adc()
#             write_adc()

#     threading.Thread(target=continuous_read_adc).start()
