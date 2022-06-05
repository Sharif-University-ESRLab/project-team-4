import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from arduino_serial import adc_inputs, pwm_queues, buffer_lock, NUM
import numpy as np
from matplotlib.widgets import CheckButtons
import json, os


# Time between graph frames in milli seconds.
INTERVAL = 200  

# plots colors
colors = ["salmon", "grey", "yellow", "lightgreen", "orange", "pink", "cyan", "plum"]

# initialization of buttons related to different channels
save_buttons = [] * NUM
transfer_buttons = [] * NUM
visibility_buttons = [] * NUM

# index of the element to save values after that
save_start_index = [0] * NUM

# a list of boolean values, True if the corresponding channel is visible
visible_diagrams = [True] # only first diagram is visible in the beginning
visible_diagrams.extend([False] * (NUM - 1))

# initializing the figure to plot
fig = plt.figure(figsize=(10, 8))
axes = [None] * NUM
axes[0] = fig.add_subplot(label=str(0))
fig.tight_layout()


# wrapper function for saving values of the input channels
def save(channel):
    def func(label):
        save_file_name = f"values_{int(channel) + 1}.txt"
        
        # button pressed to start saving
        if save_buttons[channel].get_status()[0]:
            save_start_index[channel] = len(adc_inputs[channel])
        
        # butten pressed to stop saving values and write saved ones to the file
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


# wrapper function to transfer saved values to arduino to show them on the LEDs
def transfer_to_arduino(channel):
    def func(label):
        save_file_name = f"values_{int(channel) + 1}.txt"
        
        # button pressed to start transfering to arduino
        if transfer_buttons[channel].get_status()[0]:
            vals = []
            f = open(save_file_name, "r")
            if os.stat(save_file_name).st_size != 0:
                vals.extend(json.loads(f.read()))
            f.close()
            with buffer_lock:
                pwm_queues[channel].queue.clear()
                # send saved values to pwm_queues 
                [pwm_queues[channel].put(i) for i in vals]
        
        # button pressed to stop transfering to arduino 
        else:
            with buffer_lock:
                # clear pwm_queues to show nothing on the LEDs (turn them off)
                pwm_queues[channel].queue.clear()

    return func


# set the diagram of the channel to be visible
def set_visible(channel):
    def func(label):
        # button pressed to show diagram of the channel
        if visibility_buttons[channel].get_status()[0]:
            visible_diagrams[channel] = True
            axes[channel] = fig.add_subplot(sum(visible_diagrams), 1, sum(visible_diagrams), label=str(channel))
            for i in range(len(visible_diagrams)):
                if visible_diagrams[i]:
                    axes[i].change_geometry(sum(visible_diagrams), 1, sum(visible_diagrams[:i + 1]))
        
        # button pressed to hide diagram of the channel
        else:
            visible_diagrams[channel] = False
            fig.delaxes(axes[channel])
            axes[channel] = None
            for i in range(len(visible_diagrams)):
                if visible_diagrams[i]:
                    axes[i].change_geometry(sum(visible_diagrams), 1, sum(visible_diagrams[:i + 1]))

    return func


# plot live data, define buttons of channels and their functionalities
def live_plotter():
    ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL)

    for i in range(NUM):
        save_label = ["save{}".format(i + 1)]
        observe_label = ["observe{}".format(i + 1)]
        visible_label = ["visible{}".format(i + 1)]

        # x position, y position, width and height
        save_ax = plt.axes([np.linspace(0.05, 0.9, 8)[i], 0.16, 0.1, 0.08], frame_on=False)
        observe_ax = plt.axes(
            [np.linspace(0.05, 0.9, 8)[i], 0.08, 0.1, 0.08], frame_on=False
        )
        visible_ax = plt.axes([np.linspace(0.05, 0.9, 8)[i], 0, 0.1, 0.08], frame_on=False)
        save_buttons.append(CheckButtons(save_ax, save_label, [False]))
        transfer_buttons.append(CheckButtons(observe_ax, observe_label, [False]))
        visibility_buttons.append(CheckButtons(visible_ax, visible_label, [True if i == 0 else False]))

        # set colors for buttons
        save_buttons[-1].rectangles[0].set_facecolor(colors[i])
        transfer_buttons[-1].rectangles[0].set_facecolor(colors[i])
        visibility_buttons[-1].rectangles[0].set_facecolor(colors[i])

        # clear content of values file
        save_file_name = "values_{}.txt".format(i + 1)
        open(save_file_name, "w").close()

        # buttons functionalities
        save_buttons[i].on_clicked(save(i))
        transfer_buttons[i].on_clicked(transfer_to_arduino(i))
        visibility_buttons[i].on_clicked(set_visible(i))

    # add some space between subplots and to the right of the rightmost ones
    plt.subplots_adjust(bottom=0.24, hspace=1)
    plt.show()


# animating each input data
def animate(_):
    for i in range(NUM):
        if visible_diagrams[i]:
            with buffer_lock:
                input_copy = adc_inputs[i][-400:].copy()
            if len(input_copy) == 0:
                continue
            axes[i].cla()
            axes[i].set_ylim(-100, 1100)
            axes[i].set_xlim(0, 410)
            axes[i].plot(input_copy, color=colors[i])
            axes[i].title.set_text("{}th Input".format(i + 1))
