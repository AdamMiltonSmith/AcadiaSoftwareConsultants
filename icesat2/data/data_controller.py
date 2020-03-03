import os
import datetime
import re
import pandas as pd
import requests

from os import listdir
from os.path import isfile, join
from datetime import date

#csv format:
#   segment_id, longitude, latitude, height, quality, track_id, beam, file_name

min_x = '105.25'
min_y = '49.48'
max_x = '106.06'
max_y = '50.43'

path = "resources\\csv_data_collection"
class Data:
    day_delta = datetime.timedelta(days=1)
    file_name = "Untitled"

    def __init__(self, start_date=None, end_date=None, min_x=None, min_y=None, max_x=None, max_y=None, file_name=None, day_delta=None):
        self.start_date = start_date
        self.end_date = end_date

        self.avg_height = 0
        self.stdv = 0

        self.min_x = min_x
        self.min_y = min_y

        self.max_x = max_x
        self.max_y = max_y

        #this counts the number of csv files in the directory
        self.file_count = 0

        if(day_delta != None):
            self.day_delta = day_delta

        if(file_name != None):
            self.file_name = file_name

        self.path = "resources/csv_data_collection/" + self.file_name

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def get_data(self):
        """
        This function makes GET request to the api provided by openaltimetry
        and saves the results in a csv format
        """
        for i in range((self.end_date - self.start_date).days + 1):
            day = (self.start_date + i*self.day_delta)
            
            parameters = {'date': day.strftime('%Y-%m-%d'), 'minx': self.min_x, 'miny': self.min_y, 'maxx' : self.max_x, 'maxy': self.max_y, 'trackId': '705', 'client': 'jupyter', 'outputFormat': 'csv'}           
            url = "https://openaltimetry.org/data/api/icesat2/atl06"
            
            r = requests.get(url, params=parameters)
            write_file = self.path + "/" + self.file_name + day.strftime('%Y-%m-%d')
            
            with open(write_file, "w") as f:
                for line in r.text:
                    f.write(line)

        
        write_file = self.path + "/" + self.file_name + "object_info"

        """
        This chunk of code will save needed object info in plain txt
        This will help with allowing front-end interfaces fetch data objects
        Hopefully serialize in the future
        """
        with open(write_file, "w") as f:
            f.write(self.start_date.strftime('%Y-%m-%d') + ",")
            f.write(self.end_date.strftime('%Y-%m-%d') + ",")
            
            f.write(self.min_x + ",")
            f.write(self.min_y + ",")
            f.write(self.max_x + ",")
            f.write(self.max_y + ",")
    
    """
    get_height, will subtract height at lat x at time b from height at lat x from time a
    where a and b are start and end
    """
    def get_height_diff(self, start_date, end_date):
        start_file = self.path + "/" + self.file_name + '' + start_date
        end_file = self.path + "/" + self.file_name + '' + end_date

        return
    
    def get_differential(self):
        """This function will return a csv file the height differentials,
        the differential will be calculate useing all the dates
        This will be a bit harder to implement
        """
        return
    
    """
    This function will allow the front-end to create a data object
    with only an already existing name.
    Need to include error checks to ensure there are no runtime errors
    """
    def restore_members(self):
        write_file = self.path + "/" + self.file_name + "object_info"

        with open(write_file) as f:
            members = f.readline.split(',')
            self.start_date = members[0]
            self.end_date = members[1]
            
            self.min_x = members[2]
            self.min_y = members[3]
            self.max_x = members[4]
            self.max_y = members[5]


def createData(start_date, end_date, file_name, day_delta=None):
    data = Data(start_date, end_date, file_name, day_delta=None)

    return data

def fetchData(file_name):
    data = Data(None, None, file_name)
    data.restore_members()

    return data

