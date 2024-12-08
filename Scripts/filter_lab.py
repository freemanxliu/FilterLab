import json
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def config_graph(axis, axis_config, id):
    axis[id].set_title(axis_config['title'])
    axis[id].set_xlabel(axis_config['x_label'])
    axis[id].set_ylabel(axis_config['y_label'])

    if axis_config['x_scales'] == 'function':
        axis[id].set_xscale('function', functions=(
            lambda x: np.interp(x, axis_config['x_ticks'],
                                np.linspace(0, 1, len(axis_config['x_ticks']))),
            lambda x: np.abs(x)))
    else:
        axis[id].set_xscale(axis_config['x_scales'])

    axis[id].set_xticks(axis_config['x_ticks'])
    axis[id].set_xticklabels(axis_config['x_labels'])


def plot_graph(axis, graph_data, axis_config, id):

    w = graph_data.iloc[:,0]
    r = graph_data.iloc[:,1]
    g = graph_data.iloc[:,2]
    b = graph_data.iloc[:,3]

    axis[id].clear()

    if axis_config["curve_type"] == "wr, wg, wb":  # color-match graph
        axis[id].plot(w, r, color='red', marker='o')
        axis[id].plot(w, g, color='green', marker='o')
        axis[id].plot(w, b, color='blue', marker='o')
    elif axis_config["curve_type"] == "rg":  # gamut graph
        axis[id].plot(r, g, color='red', marker='o')

        for i in range(len(r)):
            plt.text(r[i], g[i], f'({w[i]:.1f})', fontsize=9, ha='right')

    config_graph(axis, axis_config, id)

def plot_graphs():
    plt.draw()


def update():
    plot_graphs()

if __name__ == "__main__":

    fig, ax = plt.subplots(1, 2, figsize=(20, 8))
    # fig.tight_layout()

    root = tk.Tk()
    root.title("Filter Labs")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    image = Image.open('../Images/lenna.png')
    image_array = np.array(image)
    ax[0].imshow(image_array)
    ax[0].axis('off')
    ax[0].set_xlabel('X-label')
    ax[0].set_title('Image 1')

    frame = tk.Frame(root)

    with open('../Data/graph.json', 'r', encoding='utf-8') as file:
        graph_configs = json.load(file)
        graph_options = list(graph_configs.keys())

    left_graph = ttk.Combobox(root, values=graph_options)
    left_graph.current(0)
    left_graph.bind("<<ComboboxSelected>>", lambda x: update())
    left_graph.pack(side=tk.LEFT, padx=500, pady=10)

    right_graph = ttk.Combobox(root, values=graph_options)
    right_graph.current(1)
    right_graph.bind("<<ComboboxSelected>>", lambda x : update())
    right_graph.pack(side=tk.RIGHT, padx=500, pady=10)


    update()
    root.mainloop()
