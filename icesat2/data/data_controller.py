import os
import datetime
import re
from os import listdir
from os.path import isfile, join
from datetime import date

#csv format:
#   segment_id, longitude, latitude, height, quality, track_id, beam, file_name

path = "resources\\csv_data_collection"
class Data:
    day_delta = datetime.timedelta(days=1)
    file_name = "Untitled"

    def __init__(self, start_date=None, end_date=None, file_name=None, day_delta=None):
        self.start_date = start_date
        self.end_date = end_date

        self.avg_height = 0
        self.stdv = 0

        #this counts the number of csv files in the directory
        self.file_count = 0

        if(day_delta != None):
            self.day_delta = day_delta

        if(file_name != None):
            self.file_name = file_name

        self.path = "resources/csv_data_collection/" + self.file_name + "/"

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def get_data(self, minx, miny, maxx, maxy):
        #offset = 7
        for i in range((self.end_date - self.start_date).days + 1):
            day = (self.start_date + i*self.day_delta)
            current = '"https://openaltimetry.org/data/api/icesat2/atl06?date='+ day.strftime('%Y-%m-%d') +'&minx='+ minx +'&miny='+ miny +'&maxx='+ maxx +'&maxy='+ maxy +'&trackId=705&client=jupyter&outputFormat=csv"'
            command = 'curl -X GET ' + current + ' -H' + " accept: */*"

            os.system(command + " >> " + self.path + self.file_name + day.strftime('%Y-%m-%d'))

    """
    get_height, will subtract height at lat x at time b from height at lat x from time a
    where a and b are start and end
    """
    def get_height_diff(self, start_date, end_date):
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]


        start_file = self.path + '/' + self.file_name + start_date.strftime('%Y-%m-%d')
        end_file = self.path + '/' + self.file_name + end_date.strftime('%Y-%m-%d')

        #csv format:
        #   segment_id, longitude, latitude, height, quality, track_id, beam, file_name

        height_diff = {}

        with open(start_file) as sf:
            line = sf.readline()
            split = line.split(',')
            while line:
                height_diff[split[0]] =  split[1:7]
                line = sf.readline()
                split = line.split(',')

        with open(end_file) as ef:
            line = ef.readline()
            line = ef.readline()
            split = line.split(',')

            while line:
                if(split[0] in height_diff):
                    height_diff[split[0]][2] = float(height_diff[split[0]][2]) - float(split[3])
                else:
                    del(height_diff[split[0]])

                line = ef.readline()
                split = line.split(',')

        print(height_diff)
        return

    def get_differential(self):
        """This function will return a csv file the height differentials,
        the differential will be calculate useing all the dates
        This will be a bit harder to implement
        """
        return

def createData(start_date, end_date, file_name, day_delta=None):
    data = Data(start_date, end_date, file_name, day_delta=None)

    return data

