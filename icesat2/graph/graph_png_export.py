from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
import csv

# Reads from CSV file and adds them to a list csvInput
def read_data(file_name: str) -> list:
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_input = []
        for row in csv_reader:
            for element in row:
                csv_input.append(int(element))
        return csv_input

# Plots the elements read from csvInput
def plot_graph(csv_input: list, file_name: str) -> plt.plot:
    plt.plot(csv_input)
    plt.title(file_name)
    plt.ylabel('Y Axis')
    plt.xlabel('X Axis')
    plt.savefig('resources\\graph_images\\' + file_name, dpi = 100)