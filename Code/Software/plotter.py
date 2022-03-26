import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from arduino_serial import read_adc

# for hiding buttons
mpl.rcParams["toolbar"] = "None"

inputs = []

# plot live data
def live_plotter():
    ani = FuncAnimation(plt.gcf(), animate, 1000)
    plt.tight_layout()
    plt.show()


# animating each input data
def animate(i):
    # get data
    inputs.append(read_adc())
    # print(inputs[-1])
    # clear axis
    plt.cla()
    # plot data
    plt.plot(inputs)
    plt.scatter(len(inputs) - 1, inputs[-1])
    # show the data on the plot
    plt.text(len(inputs) - 1, inputs[-1] + 2, "{}".format(inputs[-1]))
