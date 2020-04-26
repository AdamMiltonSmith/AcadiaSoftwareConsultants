import csv
import glob
import json
import os

import kivy
import matplotlib.pyplot as plt
import pandas


class Graph:
    """
    Author: adamg, jacobb
    """
    def __init__(self, data_file: str, image_file: str, start_date, end_date):
        """
        Author: adamg
        """
        data = pandas.read_csv(data_file)
        self.output_image = image_file

        self.start_date = start_date
        self.end_date = end_date

        data = data.drop(["Unnamed: 0", "Unnamed: 0.1"], axis = 1)

        self.plot_graph(data)

# Plots the elements read from csvInput
    def plot_graph(self, df: pandas.DataFrame) -> plt.plot:
        """
        Author: adamg, jacobb
        """
        color_data = {}

        with open('resources/colors.json') as f:
            color_data = json.load(f)

        dict_of_regions = {k: v for k, v in df.groupby('trackId')}

        for k in dict_of_regions:
            plt.plot('latitude', 'h_li_diff',
                     data=dict_of_regions[k], marker='', color=color_data[str(k)], linewidth=1, label = k)
        #plt.plot(csv_input[0], csv_input[1])
        plt.title(f"{self.output_image}\n({self.start_date}-{self.end_date})")
        plt.legend(loc = "upper right", prop={'size': 6})
        plt.ylabel('Elevation (Meters)')
        plt.xlabel('Latitude (Degrees)')
        plt.savefig('resources/graph_images/' + self.output_image, dpi=1000)
        plt.close()

def create_graph(input_file: str, output_file: str, start_date, end_date) -> Graph:
    """
    Author: adamg
    """

    return Graph(input_file, output_file, start_date, end_date)

if __name__ == "__main__":
    Graph("resources/csv_data_collection/test/change_in_height.csv", 'foo.png', '2018-02-12', '2019-02-12')
