import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from arduino_serial import adc_inputs, pwm_queues, buffer_lock, NUM
import numpy as np
from matplotlib.widgets import CheckButtons
import json, os

INTERVAL = 100  # Time between graph frames in milli seconds.

fig, axes = plt.subplots(2, 4, figsize=(15, 6))
fig.tight_layout()
colors = ["red", "black", "yellow", "green", "orange", "pink", "cyan", "purple"]

save_buttons = [] * NUM
transfer_buttons = [] * NUM
save_start_index = [0] * NUM


def save(channel):
    def func(label):
        save_file_name = f"values_{int(channel)+1}.txt"
        # print("---------------------------------", save_file_name, "--------------------------------")
        if save_buttons[channel].get_status()[0]:
            save_start_index[channel] = len(adc_inputs[channel])
        else:
            vals = []
            f = open(save_file_name, "r")
            if os.stat(save_file_name).st_size != 0:
                vals.extend(json.loads(f.read()))
            f.close()
            vals.extend(adc_inputs[channel][save_start_index[channel]:])
            f = open(save_file_name, "w")
            f.write(json.dumps(vals))
            f.close()

    return func


def transfer_to_arduino(channel):
    def func(label):
        save_file_name = f"values_{int(channel)+1}.txt"
        if transfer_buttons[channel].get_status()[0]:
            vals = []
            f = open(save_file_name, "r")
            if os.stat(save_file_name).st_size != 0:
                vals.extend(json.loads(f.read()))
            f.close()
            with buffer_lock:
                pwm_queues[channel].queue.clear()
                [pwm_queues[channel].put(i) for i in vals]
        else:
            with buffer_lock:
                pwm_queues[channel].queue.clear()

    return func


# plot live data
def live_plotter():
    # set buttons x and y
    save_xy = [
        (0.185, 0.75),
        (0.43, 0.75),
        (0.675, 0.75),
        (0.92, 0.75),
        (0.185, 0.25),
        (0.43, 0.25),
        (0.675, 0.25),
        (0.92, 0.25),
    ]
    observe_xy = [
        (0.185, 0.7),
        (0.43, 0.7),
        (0.675, 0.7),
        (0.92, 0.7),
        (0.185, 0.2),
        (0.43, 0.2),
        (0.675, 0.2),
        (0.92, 0.2),
    ]

    ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL)

    for i in range(NUM):
        save_label = ["save"]
        observe_label = ["observe"]

        # x position, y position, width and height
        save_ax = plt.axes([save_xy[i][0], save_xy[i][1], 0.1, 0.1], frame_on=False)
        observe_ax = plt.axes(
            [observe_xy[i][0], observe_xy[i][1], 0.1, 0.1], frame_on=False
        )

        save_buttons.append(CheckButtons(save_ax, save_label, [False]))
        transfer_buttons.append(CheckButtons(observe_ax, observe_label, [False]))

        # clear content of values file
        save_file_name = "values_{}.txt".format(i + 1)
        open(save_file_name, "w").close()

        # buttons functionalities
        save_buttons[i].on_clicked(save(i))
        transfer_buttons[i].on_clicked(transfer_to_arduino(i))

    # add some space between subplots and to the right of the rightmost ones
    plt.subplots_adjust(wspace=0.6, right=0.92)
    plt.show()


# animating each input data
def animate(i):
    with buffer_lock:
        inputs_copy = []
        for i in range(NUM):
            inputs_copy.append(adc_inputs[i].copy())
            if len(inputs_copy[i]) == 0:
                continue
            axes[i // 4, i % 4].cla()
            axes[i // 4, i % 4].set_ylim(-100, 1100)
            axes[i // 4, i % 4].set_xlim(
                0, np.power(np.e, int(np.log(len(inputs_copy[i]))) + 1)
            )
            axes[i // 4, i % 4].plot(inputs_copy[i], color=colors[i])
            axes[i // 4, i % 4].title.set_text("{}th Input".format(i + 1))
