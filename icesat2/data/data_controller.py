import os
import datetime
from datetime import date

#csv format:
#   segment_id, longitude, latitude, height, quality, track_id, beam, file_name
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

        if(day_delta != None):
            self.day_delta = day_delta

        if(file_name != None):
            self.file_name = file_name

    def get_data(self):
        offset = 7
        for i in range((self.end_date - self.start_date).days):
            day = (self.start_date + i*self.day_delta)
            current = '"https://openaltimetry.org/data/api/icesat2/atl06?date='+ day.strftime('%Y-%m-%d') +'&minx='+ self.minx +'&miny='+ self.miny +'&maxx='+ self.maxx +'&maxy='+ self.maxy +'&trackId=705&client=jupyter&outputFormat=csv"'
            command = 'curl -X GET ' + current + ' -H' + " accept: */*"
            os.system(command + " >> " + self.file_name)
            # with open(self.file_name) as f:
            #     f.seek()
        return
    
    #This function will return a csv file of the difference in height from the start date to the end date

    #make dict with key being lat, each key will point to a height and beam number
    #upon finding the same late again,
    #iterate through
    # def get_height_diff(self):
    #     with open(self.file_name) as f:
            
    #     return
    
    def get_differential(self):
        """This function will return a csv file the height differentials, 
        the differential will be calculate useing all the dates
        This will be a bit harder to implement 
        """
        return

#test command input
x = data(date(2018, 11, 13), date(2018, 11, 15), '105.25', '49.48', '106.06', '50.43', "test")
x.get_data()
