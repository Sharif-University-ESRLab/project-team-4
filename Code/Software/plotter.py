import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from arduino_serial import adc_inputs, pwm_queues, buffer_lock
import numpy as np
from matplotlib.widgets import CheckButtons
import json, os

# for hiding buttons
mpl.rcParams["toolbar"] = "None"
INTERVAL = 100  # Time between graph frames in milli seconds.
CURRENT_CHANNEL = 3

fig = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
ax = plt.subplot(121)

# x position, y position, width and height
save_button = CheckButtons(plt.axes([0.5, 0.001, 0.5, 0.5], frame_on=False), ["save"], [False])
transfer_button = CheckButtons(plt.axes([0.5, 0.5, 0.5, 0.5], frame_on=False), ["observe saved data"], [False])

save_file_name = 'values_{}.txt'.format(CURRENT_CHANNEL)
# clear content of values file
open(save_file_name, 'w').close()

save_start_index = 0


def save(label):
    global save_start_index
    if save_button.get_status()[0]:
        save_start_index = len(adc_inputs[CURRENT_CHANNEL])
    else:
        vals = []
        f = open(save_file_name, 'r')
        if os.stat(save_file_name).st_size != 0:
            vals.extend(json.loads(f.read()))
        f.close()
        vals.extend(adc_inputs[CURRENT_CHANNEL][save_start_index:])
        f = open(save_file_name, 'w')
        f.write(json.dumps(vals))
        f.close()


def transfer_to_arduino(label):
    if transfer_button.get_status()[0]:
        vals = []
        f = open(save_file_name, 'r')
        if os.stat(save_file_name).st_size != 0:
            vals.extend(json.loads(f.read()))
        f.close()
        with buffer_lock:
            pwm_queues[CURRENT_CHANNEL].queue.clear()
            [pwm_queues[CURRENT_CHANNEL].put(i) for i in vals]
    else:
        with buffer_lock:
            pwm_queues[CURRENT_CHANNEL].queue.clear()


# plot live data
def live_plotter():
    ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL)
    plt.tight_layout()

    save_button.on_clicked(save)
    transfer_button.on_clicked(transfer_to_arduino)

    plt.show()


# animating each input data
def animate(i):
    global ax
    with buffer_lock:
        inputs_copy = adc_inputs[CURRENT_CHANNEL].copy()
    if len(inputs_copy) == 0:
        return
    ax.cla()
    ax.set_ylim(-100, 1100)
    ax.set_xlim(0, np.power(np.e, int(np.log(len(inputs_copy))) + 1))
    ax.plot(inputs_copy)
    # plt.plot(inputs_copy)
    # # clear axis
    # plt.cla()
    # # plot data
    # plt.scatter(len(inputs_copy) - 1, inputs_copy[-1])
    # # show the data on the plot
    # plt.text(len(inputs_copy) - 1, inputs_copy[-1] + 2, "{}".format(inputs_copy[-1]))
