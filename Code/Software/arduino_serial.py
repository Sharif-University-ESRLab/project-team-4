import queue
import threading
import serial
import random
import time

# number of channels
NUM = 8

# time between sampling intervals
SAMPLE_DELAY = 50  # milli

# lock for reading and writing data in their respective queues
buffer_lock = threading.Lock()

# arrays of inputs and pwm outputs for each channel
adc_inputs = [[] for _ in range(NUM)]
pwm_queues = [queue.Queue() for _ in range(NUM)]


####  REAL  ####
# read data from input port in arduino
def read_adc(ser: serial.SerialBase):
    try:
        packet = ser.readline().strip().decode("utf-8")
        # seperate input data with |
        samples = packet.split("|")
        if len(samples) != (NUM + 1):
            return
        # get the buffer to save input values into
        with buffer_lock:
            for i in range(NUM):
                if samples[i].isnumeric():
                    adc_inputs[i].append(int(samples[i]))
    except Exception as e:
        print(e)


# write saved values to the serial port(pwm output)
def write_adc(ser: serial.SerialBase):
    packet = ""
    # get the buffer to put output values into
    with buffer_lock:
        for i in range(NUM):
            # if no value is available in the queue, so LED is off
            if pwm_queues[i].empty():
                val = 0
            else:
                val = pwm_queues[i].get()
            packet += "{:4}|".format(val)
    ser.write(str.encode("{}\n".format(packet)))


# define a thread for continuously reading and writing data from and to arduino
def start_read_adc_thread():
    # infinite loop to read and write
    def continuous_read_adc():
        ser = serial.Serial(port="/dev/cu.usbmodem14201", baudrate=115200, timeout=1)
        while True:
            read_adc(ser)
            write_adc(ser)

    # start a thread running above function
    threading.Thread(target=continuous_read_adc).start()


####  FAKE   ####
# # fake inputs initialization
# position_s = [random.randint(100, 900) for _ in range(NUM)]
# speed_s = [random.randint(-5, +5) for _ in range(NUM)]

# # create random inputs to plot
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


# # print saved values in the terminal, in case of having no input, prints 0
# def write_adc():
#     with buffer_lock:
#         for i in range(NUM):
#             if pwm_queues[i].empty():
#                 val = 0
#             else:
#                 val = pwm_queues[i].get()
#             print('Output {}: {}'.format(i, val))


# # define a thread for continuously reading and writing data
# def start_read_adc_thread():
#     def continuous_read_adc():
#         while True:
#             read_adc()
#             write_adc()

#     threading.Thread(target=continuous_read_adc).start()
