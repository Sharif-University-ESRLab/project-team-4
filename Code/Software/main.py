from arduino_serial import *
from plotter import live_plotter

start_read_adc_thread()
# plot live data
live_plotter()
