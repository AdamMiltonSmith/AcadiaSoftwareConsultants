import glob
import os
import re
from math import sin
from os import listdir
from os.path import isfile, join

import kivy
import kivy.properties as prop
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.garden.mapview import MapView
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.splitter import Splitter
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.graphics import Color
import shutil
import ctypes

import icesat2.graph.graph_png_export as graph_png_export

"""
This stopped some TIFF unknown field with tag warnings. I don't know how it
works. Got it here:
https://stackoverflow.com/questions/58279121/python-tiffreaddirectory-warning-unknown-field-with-tag
"""
libbytiff = ctypes.CDLL("libtiff-5.dll")
libbytiff.TIFFSetWarningHandler.argtypes = [ctypes.c_void_p]
libbytiff.TIFFSetWarningHandler.restype = ctypes.c_void_p
libbytiff.TIFFSetWarningHandler(None)


currentDataSet = "No data set selected"
#Josh - if when I implement clock scheduled refreshing of the data list I will use two variables
currDataSetPath = "No path"

selected_graph = None

def getCurrDataSet():
    #print(">> The current data set is: " + str(currentDataSet))
    print(currentDataSet)
    return currentDataSet

def setCurrentDataSet(dataSet):
    currentDataSet = dataSet

def pre_init_screen():
    import tkinter as tk

    screen = tk.Tk()

    # screenx, screeny = screen.winfo_screenwidth(), screen.winfo_screenheight()

class MainApp(App):
    def build(self):
        self.title = "IGLOO"
        b = Builder.load_file("icesat2\\gui\\kv\\gui.kv")

        #Clock.schedule_interval(self.update, 1)
        return b

    # def update(self, *args):
    #     print("test")

    # def assign(self, booten):
    #     if assigned == False:
    #         print("<Assigning Shit")
    #         carrot = booten
    #         assigned = True
    #         carrot.doTheThing()




class TopButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.9, 0.9, 0.9, 1.0])
    #back_normal = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    text_color = prop.ColorProperty([0.0, 0.0, 0.0, 1.0])
    btn_height = prop.NumericProperty(35)
    btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)


class TopButtonDropDown(DropDown):
    font_size = prop.NumericProperty(14)

class FileDropDown(DropDown):
    font_size = prop.NumericProperty(14)


class EditDropDown(DropDown):
    font_size = prop.NumericProperty(14)


class WindowDropDown(DropDown):
    font_size = prop.NumericProperty(14)


class MapDropDown(DropDown):
    font_size = prop.NumericProperty(14)


class HelpDropDown(DropDown):
    font_size = prop.NumericProperty(14)


class TopButtonDropDownButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ListProperty([0.9, 0.9, 0.9, 1.0])
    back_normal = prop.ListProperty([0.0, 0.0, 0.0, 1.0])
    btn_height = prop.NumericProperty(35)
    btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)


class DefaultButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    text_color = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    btn_height = prop.NumericProperty(20)
    #btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)

class ListButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    text_color = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    btn_height = prop.NumericProperty(20)
    #btn_width = prop.NumericProperty(70)000
    side_width_buffer = prop.NumericProperty(20)

    def on_release(self):
        """Jacob- Calls the plot_graph function on the sample data foo.csv
        which is located in the csv_data_collection folder, graph_png_export
        then creates a png of the graph which is stored in graph_images to be
        displayed later."""

        #g = Graph_Widget()
        set_name = self.text
        #g.set_image(set_name)
        # for child in [child for child in self.parent.parent.parent.parent.parent.parent.children[0].children[0].children[1].children]:
        #     print(child)
        graph_widget = self.parent.parent.parent.parent.parent.parent.children[0].children[1].children[1].children[1]

        graph_widget.set_image(set_name)


class Graph_Widget(Image):

    def __init__(self, **kwargs):
        super(Graph_Widget,self).__init__(**kwargs)
        global selected_graph
        self.source = "resources/graph_images/no_dataset.png"
        self.reload()
        if selected_graph == None:
            selected_graph = "resources/graph_images/no_dataset.png"

        #self.add_widget(Label(text = "Graph"))
        #self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic, 2)

    def set_image(self, set_name):
        data_path = "resources/csv_data_collection/" + set_name
        image_name = set_name[:-4]
        image_path = "resources/graph_images/" + image_name +  ".png"
        graph_data = graph_png_export.read_data(data_path)
        graph_png_export.plot_graph(graph_data, image_name)

        self.source = image_path
        self.reload()
        global selected_graph

        selected_graph = image_path
        #self.add_widget(self.image)

    def update_pic(self, dt):
        if self.source != selected_graph:
            self.source = selected_graph
            self.reload()


class CoordinateTextInput(TextInput):
    default_text = "Format xx.xx"
    default_shade = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        """Disallows users from entering anything other than numbers into the
        boxes"""
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(CoordinateTextInput, self).insert_text(s, from_undo=from_undo)

    def on_enter(self):
        """Function that validates the data that the user just pressed enter
        with"""
        print('User pressed enter in', self, self.coord_dir)


    def check_text(self):
        """Function that will clear the text in the box and change the color
        of the text, more of a quality of life check and not necessary as of
        now"""
        #got focus
        if self.focus:
            pass
        #lost focus
        else:
            pass


class DateChooseButton(Button):
    time_def = prop.StringProperty("")
    font_size = prop.NumericProperty(12)
    back_color = prop.ColorProperty([0.9, 0.9, 0.9, 1.0])
    #back_normal = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    text_color = prop.ColorProperty([0.0, 0.0, 0.0, 1.0])
    side_width_buffer = prop.NumericProperty(20)


class DayDD(DropDown):
    font_size = prop.NumericProperty(12)

    def __init__(self, **kwargs):

        super(DayDD, self).__init__(**kwargs)

        self.month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def set_and_dismiss(self, value):
        self.parent_widget.text = value
        self.dismiss()

    def create_buttons(self, _month, _year):
        self.clear_widgets()

        month = int(_month)
        year = int(_year)

        if month == 2 and year % 4 == 0:
            max_day = 29
        else:
            max_day = self.month_day[month-1]

        for index in range(1, max_day + 1):
            btn = DateChooseDropDownButton(text=f"{index}", size_hint_y=None,
                                           width=40, height=25,
                                           background_color=[
                                               1.0, 1.0, 1.0, 1.0],
                                           color=[0.0, 0.0, 0.0, 1.0], background_normal='')

            btn.bind(on_release=lambda btn: self.set_and_dismiss(btn.text))

            self.add_widget(btn)


class ErrorDateLabel(Label):
    t = prop.StringProperty("")

    def set_text(self, text):
        print(self.t)
        self.t = text
        print(self.t)

class MonthDD(DropDown):
    font_size = prop.NumericProperty(12)

    def __init__(self, **kwargs):

        super(MonthDD, self).__init__(**kwargs)

        for index in range(1, 13):
            btn = DateChooseDropDownButton(text=f"{index}", size_hint_y=None,
                                           width=40, height=25,
                                           background_color=[
                                               1.0, 1.0, 1.0, 1.0],
                                           color=[0.0, 0.0, 0.0, 1.0], background_normal='')

            btn.bind(on_release=lambda btn: self.set_and_dismiss(btn.text))

            self.add_widget(btn)

    def set_and_dismiss(self, value):
        self.parent_widget.text = value
        self.dismiss()


class YearDD(DropDown):
    font_size = prop.NumericProperty(12)

    def __init__(self, **kwargs):

        super(YearDD, self).__init__(**kwargs)

        for index in range(2018, 2023):
            btn = DateChooseDropDownButton(text=f"{index}", size_hint_y=None,
                         width=40, height=25,
                         background_color = [1.0, 1.0,1.0, 1.0],
                         color = [0.0, 0.0, 0.0, 1.0], background_normal = '')

            btn.bind(on_release=lambda btn: self.set_and_dismiss(btn.text))

            self.add_widget(btn)

    def set_and_dismiss(self, value):
        self.parent_widget.text = value
        self.dismiss()


class DateChooseDropDownButton(Button):
    font_size = prop.NumericProperty(14)
    side_width_buffer = prop.NumericProperty(20)
    #back_color = prop.ColorProperty([0.9, 0.9, 0.9, 1.0])
    #back_normal = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    #text_color = prop.ColorProperty([0.0, 0.0, 0.0, 1.0])

class CoordinatePopup(Popup):

    def check_input(self):
        coord_input = []
        start_date_input = []
        end_date_input = []
        error_label = None
        for child in self.ids.popup_layout.children:
            if isinstance(child, CoordinateTextInput):
                coord_input.append(child)
            elif isinstance(child, DateChooseButton):
                if "start" in child.time_def:
                    start_date_input.append(child)
                else:
                    end_date_input.append(child)
            elif isinstance(child, ErrorDateLabel):
                error_label = child

        for widget in coord_input:
            if not is_float(widget.text):
                error_label.t = "Incorrect coordinate entry"
                return

        min_x = float(coord_input[3].text)
        max_x = float(coord_input[2].text)
        min_y = float(coord_input[1].text)
        max_y = float(coord_input[0].text)

        end_year = int(end_date_input[0].text)
        end_month = int(end_date_input[1].text)
        end_day = int(end_date_input[2].text)
        start_year = int(start_date_input[0].text)
        start_month = int(start_date_input[1].text)
        start_day = int(start_date_input[2].text)

        if max_y < min_y:
            error_label.t = "Incorrect coordinate entry"
            return
        elif max_x < min_x:
            error_label.t = "Incorrect coordinate entry"
            return
        elif max_y == min_y or max_x == min_x:
            error_label.t = "No effective area chosen"
            return
        elif max_y > 90 or max_y < -90:
            error_label.t = "Coordinate not within bounds"
            return
        elif min_y > 90 or min_y < -90:
            error_label.t = "Coordinate not within bounds"
            return
        elif max_x > 180 or max_x < -180:
            error_label.t = "Coordinate not within bounds"
            return
        elif min_x > 180 or min_x < -180:
            error_label.t = "Coordinate not within bounds"
            return

        if end_year > start_year:
            pass
        elif end_year == start_year:
            if end_month > start_month:
                pass
            elif end_month == start_month:
                if end_day >= start_day:
                    pass
                elif end_day < start_day:
                    error_label.t = "Incorrect day entered"
                    return
            elif end_month < start_month:
                error_label.t = "Incorrect month entered"
        elif end_year == start_year:
            error_label.t = "Incorrect year entered"

        error_label.t = ""

        # for widget in coord_input:
        #     print(widget.coord_dir)

        coord = [min_x, max_x, min_y, max_y]

        start_date = [start_day, start_month, start_year]
        end_date = [end_day, end_month, end_year]

        self.process_input(coord, start_date, end_date)

    def process_input(self, coord, start_date, end_date):
        from icesat2.data.data_controller import Data

        d = Data(start_date = start_date, end_date=end_date, min_x = coord[0],
                 min_y = coord[2], max_x = coord[1], max_y = coord[3])
        #pass data to eli here
        self.dismiss()


class SavePopup(Popup):
    def doASomething(self):
        print(">> A Something being done.")

    #needs to be converted for dynamic naming system of images
    def save(self, path, filename):
        print (">> Copying")
        newName = path + "\\" + filename + ".png"
        shutil.copy('resources\\graph_images\\foo.png', newName)

class DeletePopup(Popup):
    def delete(self):
        print(">> Deleting")
        dataSets = os.listdir('resources\\csv_data_collection')
        if getCurrDataSet() == "No data set select":
           print(">>> Nothing to delete")
        elif len(dataSets) == 1:
            temp = getCurrDataSet()
            setCurrentDataSet("No data set selected")
            os.remove(temp)
            #currentDataSet
            print('No more datasets')
        else:
            newPath = os.listdir('resources\\csv_data_collection')[0]
            print(newPath)
            temp = getCurrDataSet()
            setCurrentDataSet(newPath)
            os.remove(temp)
            #setCurrentDataSet()
            print('Folder is Not Empty')

#Converts to float without crashing on error
def is_float(input):
    try:
        float(input)
        return True
    except:
        return False

class DataSetRefreshButton(Button):
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    text_color = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    btn_height = prop.NumericProperty(20)
    #btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)

    container = prop.ObjectProperty(None) #container the buttons are added to
    def add_buttons(self):
        datasetPath = "resources\\csv_data_collection"
        files = listdir(datasetPath)
        #files = next(os.walk(datasetPath))[1]
        print(files)
        for f in files:
            tempButton = ListButton()
            tempButton.text = str(f)
            self.container.add_widget(tempButton)
    #remove buttons
    def remove_buttons(self):
        for child in [child for child in self.container.children]:
                self.container.remove_widget(child)


class Main_Window(Screen):
    def __init__(self, **kw):
        super(Main_Window, self).__init__(**kw)
    def openManual(self):
        print(">> Opening Manual")
        os.startfile("resources\\manuals\\user_manual.pdf")
    def deleteCurrent(self):
        os.remove("resources\\csv")


class Graph_Window(Screen):
    def __init__(self, **kw):
        super(Graph_Window, self).__init__(**kw)

# Josh - I know I need to format this to match the formatting standards
class Map_Window(Screen):
    def __init__(self, **kwargs):
        super(Map_Window, self).__init__(**kwargs)
        self.selectBox = True
        
        self.orientation = 'vertical'
        
        self.mainBox = BoxLayout(orientation = 'horizontal')
        self.add_widget(self.mainBox)
        


        self.picture = Image(allow_stretch=True, source='resources\\map_images\\ice_field_map3.TIF')
        self.mainBox.add_widget(self.picture)
        # xmin,xmax,ymin,xmax of the provided image
        self.xminMap = 134.601389
        self.xmaxMap = 134.956389
        self.yminMap = 58.363611
        self.ymaxMap = 58.989167
        
        self.xdiff = self.xmaxMap - self.xminMap
        self.ydiff = self.ymaxMap - self.yminMap
        
  
        #draw a rectangle
        with self.canvas:
            Color(1,0,0,.5,mode='rgba')
            absImageX = self.picture.center_x - self.picture.norm_image_size[0] / 2.0
            absImageY = self.picture.center_y + self.picture.norm_image_size[1] / 2.0


            self.rect = Rectangle(pos=(300, 400), size=(50,50))
        
        
        self.buttonBox = BoxLayout(orientation = 'vertical', spacing = 5)
        self.mainBox.add_widget(self.buttonBox)
        btnCurrentBox = Button(text = 'Box to Current Data Set')
        btnPullData = Button(text = 'Pull Box Data')
        btnReturnToMain = Button(text = 'Return to Main Window')
        self.buttonBox.add_widget(btnCurrentBox)
        self.buttonBox.add_widget(btnPullData)
        self.buttonBox.add_widget(btnReturnToMain)
        
        

    def getImageAbsX(self):
        return self.picture.center_x - self.picture.norm_image_size[0] / 2.0   

    def getImageAbsY(self):
        return self.picture.center_y + self.picture.norm_image_size[1] / 2.0

    def on_touch_down(self, touch):
        if self.selectBox == True:
            #check if selection is being done outside of the actual image not just the image widget
            out_of_bounds = False
            if (touch.x < self.picture.center_x - self.picture.norm_image_size[0] / 2) or (touch.x > self.picture.center_x - self.picture.norm_image_size[0] / 2.0 + self.picture.norm_image_size[0]):
                out_of_bounds = True
            if (touch.y < self.picture.center_y - self.picture.norm_image_size[1] / 2) or (touch.y > self.picture.center_y - self.picture.norm_image_size[1] / 2.0 + self.picture.norm_image_size[1]):
                out_of_bounds = True
            if out_of_bounds:
                pass
            else:
                self.rect.pos = touch.pos
                self.rect.size = (0, 0)

    def on_touch_move(self, touch):
        if self.selectBox == True:
            #check if selection is being done outside of the actual image not just the image widget
            out_of_bounds = False
            if (touch.x < self.picture.center_x - self.picture.norm_image_size[0] / 2) or (touch.x > self.picture.center_x - self.picture.norm_image_size[0] / 2.0 + self.picture.norm_image_size[0]):
                out_of_bounds = True
            if (touch.y < self.picture.center_y - self.picture.norm_image_size[1] / 2) or (touch.y > self.picture.center_y - self.picture.norm_image_size[1] / 2.0 + self.picture.norm_image_size[1]):
                out_of_bounds = True
            if out_of_bounds:
                pass
            else:
                self.rect.size = (touch.x - touch.ox, touch.y - touch.oy)
    
    #set the box position and size based on xmin, xmax, ymin, ymax
    def set_box_pos(self,xmin,xmax,ymin,ymax):
        bottomX = 0
        bottomY = 0
        xsize = 0
        ysize = 0

        #Check if coords are within range of image
        inBounds = True
        if (xmin >= self.xminMap) and (xmax < self.xmaxMap) and (ymin >= self.yminMap) and (ymax < self.ymaxMap):
            inBounds =  True
        else:
            inBounds = False
        
        if inBounds == True:
            #convert actual coords of bottom left of box to relative pixels on map image
            totalPixelsX = (self.picture.center_x - self.picture.norm_image_size[0] / 2.0 + self.picture.norm_image_size[0])
            totalPixelsY = (self.picture.center_y - self.picture.norm_image_size[1] / 2.0 + self.picture.norm_image_size[1]) - (self.picture.center_y - self.picture.norm_image_size[1] / 2)
            distanceRatioX = (self.xmaxMap - xmin) / (self.xmaxMap - self.xminMap)
            distanceRatioY = (self.ymaxMap - ymin) / (self.ymaxMap - self.yminMap)
            bottomX = totalPixelsX * distanceRatioX
            bottomY = totalPixelsY * distanceRatioY

            #convert xmax and ymax for size 
            distanceRatioX = (self.xmaxMap - xmax) / (self.xmaxMap - self.xminMap)
            distanceRatioY = (self.ymaxMap - ymax) / (self.ymaxMap - self.yminMap)
            xsize = (totalPixelsX * distanceRatioX) - bottomX
            ysize = (totalPixelsY * distanceRatioY) - bottomY

        self.rect.pos = (bottomX,bottomY)
        self.rect.size = (xsize, ysize)


    def pullData(self):
        print("Pulling data from selected region on map")


    def process_input(self, coord, start_date, end_date):
        from icesat2.data.data_controller import Data
        coord = [min_x, max_x, min_y, max_y]
        d = Data(start_date = start_date, end_date=end_date, min_x = coord[0],
                 min_y = coord[2], max_x = coord[1], max_y = coord[3])



class Map(MapView):
    pass

class ScreenManagement(ScreenManager):
    pass

class WindowSplitter(Splitter):
    border_size = prop.NumericProperty(5)

class SetGraph(Widget):
    testGraph = prop.ObjectProperty(None)



# sm = ScreenManager()

# screens = [Main_Window(name='main')]

# for screen in screens:
#     sm.add_widget(screen)

# sm.current = 'main'

def main():
    MainApp().run()
