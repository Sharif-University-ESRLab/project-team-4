from arduino_serial import *
from plotter import live_plotter

# a thread for reading data from arduino and showing saved values on LED
start_read_adc_thread()
# plot live data
live_plotter()
