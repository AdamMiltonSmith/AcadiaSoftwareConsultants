from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
import csv

# Reads data from a CSV file and adds all members to csv_input.
# Currently reads all members will need to get specific data later.
def read_data(file_name: str) -> list:
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_input = []
        for row in csv_reader:
            for element in row:
                csv_input.append(int(element))
        return csv_input

#   Takes a list and plots each value in it as a point where the x value
# is the position in the list and the y value is the value of the element.
# After the graph is created it is stored in foo.png. Later this will need
# a unique name for each graph.
def plot_graph(csv_input: list) -> plt.plot:
    plt.plot(csv_input)
    plt.title('IGLOO TESTS')
    plt.ylabel('Y Axis')
    plt.xlabel('X Axis')
    plt.savefig('icesat2\\graph\\graph_images\\foo.png', dpi = 100)