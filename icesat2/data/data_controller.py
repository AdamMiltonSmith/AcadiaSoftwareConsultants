import os
import datetime

class data:
    day_delta = datetime.timedelta(days=1)
    name = "Untitled"

    def __init__(self, start_date, end_date, minx, miny, maxx, maxy, name=None, day_delta=None):
        self.start_date = start_date
        self.end_date = end_date

        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

        if(day_delta != None):
            self.day_delta = day_delta

        if(name != None):
            self.name = name

    def get_data(self):
        for i in range((self.end_date - self.start_date).days):
            current = "https://openaltimetry.org/data/api/icesat2/atl06?date=" + i + "&minx=" + self.minx + \
                "&miny=" + self.miny + "&maxx=" + self.maxx + "&maxy=" + self.maxy + \
                "&trackId=705&client=jupyter&outputFormat=csv"
            os.system('curl -X GET' + current +
                      '-H' '"accept: */*" >>' + self.name)

    def get_height_diff(self):
        """This function will return a csv file of the difference in height
        from the start date to the end date"""
        return

    def get_differential(self):
        """This function will return a csv file the height differentials, the
        differential will be calculate useing all the dates. This will be a bit
        harder to implement"""
        return
