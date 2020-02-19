from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
import csv

def read_data(file_name: str) -> list:
    """Reads from CSV file and adds them to a list csvInput"""
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_input = []
        for row in csv_reader:
            for element in row:
                csv_input.append(int(element))
        return csv_input

def plot_graph(csv_input: list) -> plt.plot:
    """Plots the elements read from csvInput"""
    plt.plot(csv_input)
    plt.title('IGLOO TESTS')
    plt.ylabel('Y Axis')
    plt.xlabel('X Axis')
    plt.savefig('icesat2\\graph\\graph_png\\foo.png', dpi = 100)
