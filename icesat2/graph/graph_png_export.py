import csv
import glob
import os

import kivy
import matplotlib.pyplot as plt
#from kivy.core.window import Window
#from kivy.garden.graph import Graph, MeshLinePlot
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import pandas

class Graph:
    def __init__(self, data_file: str, image_file: str, start_date, end_date):
        data = pandas.read_csv(data_file)
        self.output_image = image_file

        self.start_date = start_date
        self.end_date = end_date

        self.plot_graph((data['latitude'].tolist(),
                    data['h_li_diff'].tolist()))

# Plots the elements read from csvInput
    def plot_graph(self, csv_input: list) -> plt.plot:
        plt.plot(csv_input[0], csv_input[1])
        plt.title(f"{self.output_image}\n({self.start_date}-{self.end_date})")
        plt.ylabel('Elevation (Meters)')
        plt.xlabel('Latitude (Degrees)')
        plt.savefig('resources/graph_images/' + self.output_image, dpi=1000)
        plt.close()

def create_graph(input_file: str, output_file: str, start_date, end_date) -> Graph:
    return Graph(input_file, output_file, start_date, end_date)

if __name__ == "__main__":
    Graph("resources/csv_data_collection/test/change_in_height.csv", 'foo.png', '2018-02-12', '2019-02-12')
