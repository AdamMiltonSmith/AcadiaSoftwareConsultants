import os
import datetime
import re
import pandas as pd
import requests

from os import listdir
from os.path import isfile, join
from datetime import date

from os import path

#csv format:
#   segment_id, longitude, latitude, height, quality, track_id, beam, file_name

min_x = '105.25'
min_y = '49.48'
max_x = '106.06'
max_y = '50.43'

DATA_DIR = "resources/csv_data_collection"
DEFAULT_PROJECT_NAME = "Untilted"

DEFAULT_REQUEST = 'segment_id,longitude,latitude,h_li,atl06_quality_summary,track_id,beam,file_name\n'

class Data:
    day_delta = datetime.timedelta(days=1)

    def __init__(self, start_date=None, end_date=None, min_x=None, min_y=None,
                 max_x=None, max_y=None, file_name=None, day_delta=None):
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

        if day_delta is not None:
            self.day_delta = day_delta

        if file_name is not None:
            self.file_name = file_name
        else:
            # looks for the first directory under DEFAULT_PROJECT_NAME (currently
            # Untitled) and adds numbers until it finds a correct directory. As
            # users can save projects under different names this should function
            # correctly
            dir_found = False
            if not path.exists(DATA_DIR + f"/{DEFAULT_PROJECT_NAME}"):
                dir_found = True
                self.file_name = DEFAULT_PROJECT_NAME
            else:
                number_addition = 1
                while not dir_found:
                    if not path.exists(DATA_DIR + f"/{DEFAULT_PROJECT_NAME}{number_addition}"):
                        dir_found = True
                        self.file_name = DEFAULT_PROJECT_NAME
                    else:
                        number_addition += 1

        self.path = DATA_DIR + "/" + self.file_name

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def get_data(self):
        """
        This function makes GET request to the api provided by openaltimetry
        and saves the results in a csv format
        """
        for i in range((self.end_date - self.start_date).days + 1):
            day = (self.start_date + i*self.day_delta)

            parameters = {'date': day.strftime('%Y-%m-%d'),
                            'minx': self.min_x,
                            'miny': self.min_y,
                            'maxx' : self.max_x,
                            'maxy': self.max_y,
                            'trackId': '705',
                            'client': 'jupyter',
                            'outputFormat': 'csv'}

            url = "https://openaltimetry.org/data/api/icesat2/atl06"

            r = requests.get(url, params=parameters)
            write_file = self.path + "/" + self.file_name + day.strftime('%Y-%m-%d') + ".csv"


            #print (r.text)
            if r.text != DEFAULT_REQUEST:
                with open(write_file, "w") as f:
                    f.write(r.text)


        write_file = self.path + "/" + self.file_name + "object_info"

        """
        This chunk of code will save needed object info in plain text
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
    def get_height_diff(self):

        start_file = pd.read_csv(self.path + "/" + self.file_name + ''
        + self.start_date.strftime('%Y-%m-%d')+".csv", header=0, index_col='segment_id')

        end_file = pd.read_csv(self.path + "/" + self.file_name + ''
                               + self.end_date.strftime('%Y-%m-%d') + ".csv", header=0, index_col='segment_id')
        decimal_points_lat = 3
        decimal_points_long = 3

        start_file_rounded = start_file.round({'longtitude': decimal_points_long, 'latitidue': decimal_points_lat})
        end_file_rounded = end_file.round({'longtitude': decimal_points_long, 'latitidue': decimal_points_lat})

        start_file_grouped = start_file_rounded.groupby['latitude', 'beam'].agg({'longitude': 'mean', 'h_li': 'mean'})
        end_file_grouped = end_file_rounded.groupby['latitude', 'beam'].agg(
            {'longitude': 'mean', 'h_li': 'mean'})


        #print(start_file)
        diff = pd.DataFrame({'start': start_file_grouped['h_li'],
                             'end': end_file_grouped['h_li']})

        #print(diff)

        df = pd.DataFrame({ 'segment_id'            : start_file['segment_id'],
                            'longitude'             : start_file['longitude'],
                            'h_li'                  : diff['start'] - diff['end'],
                            'atl06_quality_summary' : start_file['atl06_quality_summary'],
                            'track_id'              : start_file['track_id'],
                            'beam'                  : start_file['beam'],
                            'file_name'             : start_file['file_name']})

        #print(df)

        df.to_csv(self.path + "/" + 'change_in_height.csv')


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

        with open(write_file, 'r') as f:
            members = f.readline.split(',')
            self.start_date = members[0]
            self.end_date = members[1]

            self.min_x = members[2]
            self.min_y = members[3]
            self.max_x = members[4]
            self.max_y = members[5]


def create_data(start_date, end_date, min_x,
                min_y, max_x, max_y):

    data = Data(start_date=start_date, end_date=end_date, min_x=min_x,
                min_y=min_y, max_x = max_x, max_y=max_y)
    data.get_data()

    data.get_height_diff()

def fetchData(file_name):
    data = Data(None, None, file_name)
    data.restore_members()

    return data

if __name__ == "__main__":
    x = Data(date(2018, 11, 13), date(2019, 2, 12),
             '105.25', '49.48', '106.06', '50.43', "test")
    x.get_data()
    x.get_height_diff()

