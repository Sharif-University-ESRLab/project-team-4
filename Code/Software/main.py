from arduino_serial import *
from plotter import live_plotter

# plot live data
live_plotter()
# close serial port
ser.close()
