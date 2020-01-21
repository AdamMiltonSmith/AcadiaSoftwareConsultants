import os
import datetime
import re
from os import listdir
from os.path import isfile, join
from datetime import date

#csv format:
#   segment_id, longitude, latitude, height, quality, track_id, beam, file_name

path = "resources\\csv_data_collection"
class data:
    day_delta = datetime.timedelta(days=1)
    file_name = "Untitled"

    def __init__(self, start_date, end_date, minx, miny, maxx, maxy, file_name=None, day_delta=None):
        self.start_date = start_date
        self.end_date = end_date

        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

        #this counts the number of csv files in the directory
        self.file_count = 0

        if(day_delta != None):
            self.day_delta = day_delta

        if(file_name != None):
            self.file_name = file_name

        self.path = "resources/csv_data_collection/" + self.file_name + "/"

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def get_data(self):
        #offset = 7
        for i in range((self.end_date - self.start_date).days + 1):
            day = (self.start_date + i*self.day_delta)
            current = '"https://openaltimetry.org/data/api/icesat2/atl06?date='+ day.strftime('%Y-%m-%d') +'&minx='+ self.minx +'&miny='+ self.miny +'&maxx='+ self.maxx +'&maxy='+ self.maxy +'&trackId=705&client=jupyter&outputFormat=csv"'
            command = 'curl -X GET ' + current + ' -H' + " accept: */*"

            os.system(command + " >> " + self.path + self.file_name + day.strftime('%Y-%m-%d'))
    
    """
    get_height, will subtract height at lat x at time b from height at lat x from time a
    where a and b are start and end
    """
    def get_height_diff(self):
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]

        
        start_file = self.path + '/' + self.file_name + self.start_date.strftime('%Y-%m-%d')
        end_file = self.path + '/' + self.file_name + self.end_date.strftime('%Y-%m-%d')

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

        # with open(end_file) as ef:
        #     line = sf.readline()
        #     split = line.split(',')
        #     while line:
        #         if(split[0] in height_diff):

        print(height_diff)
        return
    
    def get_differential(self):
        """This function will return a csv file the height differentials,
        the differential will be calculate useing all the dates
        This will be a bit harder to implement
        """
        return

#test command input
x = data(date(2018, 11, 13), date(2018, 11, 15), '105.25', '49.48', '106.06', '50.43', "test")
#x.get_data()
x.get_height_diff()
