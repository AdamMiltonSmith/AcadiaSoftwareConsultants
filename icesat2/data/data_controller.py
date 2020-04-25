import os
import datetime
import re
import pandas as pd
import requests
import json
import shutil

from os import listdir
from os.path import isfile, join
from datetime import datetime as dt

from os import path

from icesat2.gui.gui import ErrorPopup, NotificationPopup

# csv format:
#   segment_id, longitude, latitude, height, quality, track_id, beam, file_name

DATA_DIR = "resources/csv_data_collection"
DEFAULT_PROJECT_NAME = "Untitled"

DEFAULT_REQUEST = "segment_id,longitude,latitude,h_li,atl06_quality_summary,\
track_id,beam,file_name\n"

DATE_JSON = "resources/data_tracks.json"


class Data:
    def __init__(self, start_date, end_date, min_x, min_y,
                 max_x, max_y, project_name=None, day_delta=None, *, trackId):

        if isinstance(start_date, datetime.date):
            # list is already in datetime.date format, leave it as it is
            self.start_date = start_date
        elif isinstance(start_date, str):
            # convert from list to datetime.date
            self.start_date = dt.strptime(start_date, "%Y/%m/%d")
            self.start_date = self.start_date.date()
        else:
            self.start_date = None

        if isinstance(end_date, datetime.date):
            self.end_date = end_date
        elif isinstance(end_date, str):
            # convert from list to datetime.date
            self.end_date = dt.strptime(end_date, "%Y/%m/%d")
            self.end_date = self.end_date.date()
        else:
            self.end_date = None

        # self.avg_height = 0
        # self.stdv = 0

        self.min_x = str(min_x)
        self.min_y = str(min_y)

        self.max_x = str(max_x)
        self.max_y = str(max_y)

        # this counts the number of csv files in the directory
        self.file_count = 0

        self.day_delta = day_delta or datetime.timedelta(days=1)

        self.project_name = project_name or DEFAULT_PROJECT_NAME

        self.trackId = trackId

        self.path = DATA_DIR + "/" + self.project_name + "/" + self.trackId

        if not path.exists(self.path):
            os.makedirs(self.path)

    def get_data(self):
        """
        This function makes GET request to the api provided by openaltimetry
        and saves the results in a csv format
        """
        first_file, last_file = None, None

        with open('resources/data_tracks.json') as f:
            data = json.load(f)

        for date in data[self.trackId]:
            if self.start_date <= dt.strptime(
                    date, "%Y-%m-%d").date() <= self.end_date:
                parameters = {'date': date,
                              'minx': float(self.min_x),
                              'miny': float(self.min_y),
                              'maxx': float(self.max_x),
                              'maxy': float(self.max_y),
                              'trackId': int(self.trackId),
                              'client': 'jupyter',
                              'outputFormat': 'csv'}

                url = "https://openaltimetry.org/data/api/icesat2/atl06"

                r = requests.get(url, params=parameters)
                write_file = self.path + "/" + date + ".csv"
                print(f"Trying {date}")
                if r.text != DEFAULT_REQUEST:
                    print("Successful data retrieval")
                    with open(write_file, "w") as f:
                        if self.file_count == 0:
                            first_file = date
                        last_file = date
                        f.write(r.text)
                        self.file_count += 1
                else:
                    print("Unsuccessful data retrieval")
        # create metadata file

        if self.file_count is not 0:
            self.valid_start_date = dt.strptime(first_file, '%Y-%m-%d')
            self.valid_end_date = dt.strptime(last_file, '%Y-%m-%d')
        else:
            self.valid_start_date = dt.strptime('1970-01-01', '%Y-%m-%d')
            self.valid_end_date = dt.strptime('1970-01-01', '%Y-%m-%d')

        write_file = self.path + "/" + "object_info.txt"

        """
        This chunk of code will save needed object info in plain text
        This will help with allowing front-end interfaces fetch data objects
        Hopefully serialize in the future
        """
        with open(write_file, "w") as f:
            f.write(self.valid_start_date.strftime('%Y-%m-%d') + ",")
            f.write(self.valid_end_date.strftime('%Y-%m-%d') + ",")
            f.write(str(self.file_count))

    def get_height_diff(self):
        """
        get_height, will subtract height at lat x at time b from height at
        lat x from time a where a and b are start and end
        """
        if self.file_count == 0 or self.file_count == 1:
            shutil.rmtree(self.path)
            return False
        start_file = pd.read_csv(self.path + "/"
                                 + self.valid_start_date.strftime('%Y-%m-%d')
                                 + ".csv", header=0, index_col='segment_id')

        end_file = pd.read_csv(self.path + "/"
                               + self.valid_end_date.strftime('%Y-%m-%d')
                               + ".csv", header=0, index_col='segment_id')

        decimal_points_lat = 3

        start_file_rounded = start_file.round(
            {'latitude': decimal_points_lat})
        end_file_rounded = end_file.round(
            {'latitude': decimal_points_lat})

        start_file_grouped = start_file_rounded.groupby(
            ['latitude', 'beam']).agg({'h_li': 'mean'}).reset_index()
        end_file_grouped = end_file_rounded.groupby(
            ['latitude', 'beam']).agg({'h_li': 'mean'}).reset_index()

        diff = pd.DataFrame({'start': start_file_grouped['h_li'],
                             'end': end_file_grouped['h_li']})

        df = pd.DataFrame({'latitude': end_file_grouped['latitude'],
                           'h_li_start': start_file_grouped['h_li'],
                           'h_li_end': end_file_grouped['h_li'],
                           'h_li_diff': diff['start'] - diff['end'],
                           'beam': end_file_grouped['beam']})

        df.to_csv(self.path + "/" + 'change_in_height.csv')

        return True


def get_metadata(project_name):
    with open(DATA_DIR + "/" + project_name + "/object_info.txt") as f:
        line = f.read()
        line_split = line.split(",")

        metadata = {}

        metadata['start_date'] = line_split[0]
        metadata['end_date'] = line_split[1]
        #metadata['file_count'] = line_split[2]

        return metadata


def create_project_dir(project_n, start_date, end_date):
    project_name = project_n or DEFAULT_PROJECT_NAME

    # looks for the first directory under DEFAULT_PROJECT_NAME (currently
    # Untitled) and adds numbers until it finds a correct directory. As
    # users can save projects under different names this should function
    # correctly
    dir_found = False
    if not path.exists(DATA_DIR + f"/{project_name}"):
        pass
    else:
        num = 1
        while not dir_found:
            if not path.exists(DATA_DIR + f"/{project_name}{num}"):
                dir_found = True
                project_name = f"{project_name}{num}"
                break
            else:
                num += 1

    p = DATA_DIR + "/" + project_name

    if not path.exists(p):
        os.makedirs(p)

    write_file = p + "/" + "object_info.txt"

    """
    This chunk of code will save needed object info in plain text
    This will help with allowing front-end interfaces fetch data objects
    Hopefully serialize in the future
    """
    with open(write_file, "w") as f:
        f.write(f"{start_date},")
        f.write(f"{end_date},")

    return project_name


def compile_diff_data(data_objs, project_name):
    # write function to compile changes in height by latitude
    dataframes = []
    for i in data_objs:
        dataframes.append(pd.read_csv(i.path + "/change_in_height.csv", header=0))

    result = pd.concat(dataframes)

    result.to_csv(DATA_DIR + "/" + project_name + "/" + 'change_in_height.csv')

def create_data(start_date, end_date, min_x, min_y, max_x, max_y, project_name=None):
    with open('resources/data_tracks.json') as f:
        d = json.load(f)

    new_project_name = create_project_dir(project_name, start_date, end_date)

    data_vars = []

    for key in d:
        data = Data(start_date=start_date, end_date=end_date, min_x=min_x,
                    min_y=min_y, max_x=max_x, max_y=max_y, project_name=new_project_name, trackId=key)
        # data_vars.append(data)

        data.get_data()

        if data.get_height_diff():
            data_vars.append(data)
    pass

    if len(data_vars) == 0:
        e = ErrorPopup(error_message=f"No files generated for data comparison on project"
                       f" {data.project_name}.\nProject deletion recommended").open()
    else:
        compile_diff_data(data_vars, new_project_name)
        n = NotificationPopup(
            message=f"Project successfully created with name {new_project_name}").open()


if __name__ == "__main__":
    create_data(datetime.date(2018, 11, 13), datetime.date(2019, 3, 12),
                '105.25', '49.48', '106.06', '50.43', "test")
