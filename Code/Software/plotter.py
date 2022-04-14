import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from arduino_serial import *

# for hiding buttons
mpl.rcParams["toolbar"] = "None"
INTERVAL = 100  # Time between graph frames in milli seconds.
optimal_frequency = (INTERVAL // SAMPLE_DELAY) * 2


# plot live data
def live_plotter():
    ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL)
    plt.tight_layout()
    plt.show()


# animating each input data
def animate(i):
    with buffer_lock:
        inputs_copy = adc_inputs.copy()
    if len(inputs_copy) == 0:
        return
    plt.cla()
    plt.ylim(-100, 1100)
    plt.plot(inputs_copy[-1000:])
    # plt.plot(inputs_copy)
    # # clear axis
    # plt.cla()
    # # plot data
    # plt.scatter(len(inputs_copy) - 1, inputs_copy[-1])
    # # show the data on the plot
    # plt.text(len(inputs_copy) - 1, inputs_copy[-1] + 2, "{}".format(inputs_copy[-1]))
