import ctypes
import glob
import os
import shutil
from os import listdir
from os.path import isfile, join
from os import path

import kivy
import kivy.properties as prop
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.garden.mapview import MapView
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.splitter import Splitter
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from icesat2.graph.graph_png_export import create_graph

"""
This stopped some TIFF unknown field with tag warnings. I don't know how it
works. Got it here:
https://stackoverflow.com/questions/58279121/python-tiffreaddirectory-warning-unknown-field-with-tag
"""
libbytiff = ctypes.CDLL("libtiff-5.dll")
libbytiff.TIFFSetWarningHandler.argtypes = [ctypes.c_void_p]
libbytiff.TIFFSetWarningHandler.restype = ctypes.c_void_p
libbytiff.TIFFSetWarningHandler(None)

#just dataset name - i.e. "Untitled"
current_dataset = ""

#full path - i.e. "resources/graph_images/no_dataset.png"
selected_graph = ""

MONTH_DAY = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

DATA_DIRECTORY = "resources/csv_data_collection"

DEFAULT_GRAPH = "resources/graph_images/no_dataset.png"
ERROR_GRAPH = "resources/graph_images/items_missing.png"


def getCurrDataSet():
    return current_dataset


def setCurrentDataSet(dataSet):
    global current_data_set
    current_data_set = dataSet


def pre_init_screen():
    pass


class MainApp(App):
    def build(self):
        self.title = "IGLOO"
        b = Builder.load_file("icesat2/gui/kv/gui.kv")

        #Clock.schedule_interval(self.update, 1)
        return b


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

    def project_save_check(self):
        if current_dataset == "":
            n = NoProjectChosenPopup().open()
            return
        p = ProjectSavePopup().open()



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


class IncorrectDatasetPopup(Popup):
    pass


class ListButton(Button):
    """
    Author: adamg, jacobb, joshs
    """
    font_size = prop.NumericProperty(14)
    back_color = prop.ColorProperty([0.9, 0.9, 0.9, 1.0])

    text_color = prop.ColorProperty([1.0, 1.0, 1.0, 1.0])
    btn_height = prop.NumericProperty(20)
    btn_width = prop.NumericProperty(25)
    side_width_buffer = prop.NumericProperty(20)

    def __init__(self, **kwargs):
        super(ListButton, self).__init__(**kwargs)
        self.background_color = (0.5, 0.5, 0.5, 1.0)
        self.background_normal = ''
        #self.background_down: (1, 1, 1, 1)
        #self.height = 35
        # self.size_hint_x = None
        # self.width = 40
        # self.pos_hint = {'center_x': .5}

    def on_release(self):
        """
        Author: adamg, jacobb
        Passes data to Graph_Widget class for instantiation of the object.
        """
        for child in self.parent.children:
            child.background_color = (0.5, 0.5, 0.5, 1.0)

        self.background_color = (0.1, .5, 0.1, 1.0)
        project_name = self.text

        global current_dataset
        current_dataset = project_name

        # adamg - god this is awful but it works
        graph_widget = self.parent.parent.parent.parent.parent.parent.children[0].children[1].children[1].children[1]

        # check the data set that it has everything completed for a drawing
        if (not path.exists(f"{DATA_DIRECTORY}/" + project_name + "/change_in_height.csv") or not path.exists("{DATA_DIRECTORY}/" + project_name + "/object_info.csv")):
            i = IncorrectDatasetPopup()
            i.open()

            graph_widget.set_image("error")

            return


        #graph_widget = self.parent.parent.parent.parent.parent.parent.children[0].children[1].children[1].children[1]

        graph_widget.set_image(project_name)


class Graph_Widget(Image):
    """
    Author: adamg and jacobb
    """

    def __init__(self, **kwargs):
        """
        Author: adamg
        """
        super(Graph_Widget, self).__init__(**kwargs)
        #self.allow_stretch = True

        global selected_graph
        self.source = DEFAULT_GRAPH
        self.reload()

        if selected_graph == "":
            selected_graph = DEFAULT_GRAPH

        Clock.schedule_interval(self.update_pic, 2)

    def set_image(self, set_name):
        """
        Author: adamg and jacobb
        """
        from icesat2.data.data_controller import get_metadata

        global selected_graph

        if set_name == "error":

            selected_graph = "resources/graph_images/items_missing.png"

            self.source = selected_graph
            self.reload()

            return

        if path.exists(selected_graph) and (selected_graph != DEFAULT_GRAPH or selected_graph != ERROR_GRAPH):
            os.remove(selected_graph)

        data_path = f"{DATA_DIRECTORY}/" + set_name + "/change_in_height.csv"

        image_path = "resources/graph_images/" + set_name + ".png"

        metadata = get_metadata(set_name)

        create_graph(data_path, set_name,
                     metadata['start_date'], metadata['end_date'])

        self.source = image_path
        self.reload()

        selected_graph = image_path

    def update_pic(self, dt):
        """
        Author: adamg and jacobb
        """
        #print(selected_graph)
        if self.source != selected_graph:
            self.source = selected_graph
            #despite it being a huge edge case, we do not want it to crash here
            if path.exists(selected_graph):
                self.reload()


class CoordinateTextInput(TextInput):
    """
    Author: adamg
    """
    default_text = "Format xx.xx"
    default_shade = prop.ColorProperty([0.5, 0.5, 0.5, 1.0])

    def insert_text(self, substring, from_undo=False):
        """
        Disallows users from entering anything other than numbers into the
        boxes
        """
        import re as regex

        pat = regex.compile('[^0-9]')

        if '.' in self.text:
            s = regex.sub(pat, '', substring)
        else:
            s = '.'.join([regex.sub(pat, '', s)
                          for s in substring.split('.', 1)])
        return super(CoordinateTextInput, self).insert_text(s, from_undo=from_undo)

    def on_enter(self):
        """
        Function that validates the data that the user just pressed enter
        with
        """
        print('User pressed enter in', self, self.coord_dir)

    def check_text(self):
        """
        Function that will clear the text in the box and change the color
        of the text, more of a quality of life check and not necessary as of
        now
        """
        # got focus
        if self.focus:
            pass
        # lost focus
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

        self.max_day = 31

    def calc_max_day(self, month, year):
        if month == 2 and year % 4 == 0:
            self.max_day = 29
        else:
            self.max_day = MONTH_DAY[month-1]
        return self.max_day

    def set_and_dismiss(self, value):
        self.parent_widget.text = value
        self.dismiss()

    def create_buttons(self, _month, _year):
        self.clear_widgets()

        self.calc_max_day(int(_month), int(_year))

        for index in range(1, self.max_day + 1):
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
    #day_button - self.day_button

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

        for index in range(2018, 2022):
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

        if start_day not in range(1, MONTH_DAY[start_month-1] + 1):
            error_label.t = "Incorrect day for start month"
            return
        elif end_day not in range(1, MONTH_DAY[end_month-1] + 1):
            error_label.t = "Incorrect day for end month"
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

        coord = [min_x, max_x, min_y, max_y]

        start_year = str(start_year).zfill(4)
        start_month = str(start_month).zfill(2)
        start_day = str(start_day).zfill(2)

        end_year = str(end_year).zfill(4)
        end_month = str(end_month).zfill(2)
        end_day = str(end_day).zfill(2)

        start_date = f"{start_year}/{start_month}/{start_day}"
        end_date = f"{end_year}/{end_month}/{end_day}"

        self.process_input(coord, start_date, end_date)

    def process_input(self, coord, start_date, end_date):
        from icesat2.data.data_controller import create_data

        create_data(start_date=start_date, end_date=end_date, min_x=float(coord[0]),
                    min_y=float(coord[2]), max_x=float(coord[1]), max_y=float(coord[3]))
        # pass data to eli here
        self.dismiss()


class NoProjectChosenPopup(Popup):
    pass

class ProjectSavePopup(Popup):
    def save(self, new_name):
        #os.rename(src, dst)
        global current_dataset, selected_graph

        #rename image
        os.rename(f"resources/graph_images/{current_dataset}.png",
                  f"resources/graph_images/{new_name}.png")

        selected_graph = f"resources/graph_images/{new_name}.png"

        #rename project
        os.rename(f"{DATA_DIRECTORY}/{current_dataset}",
                  f"{DATA_DIRECTORY}/{new_name}")

        current_dataset = new_name

class ImageSavePopup(Popup):
    # needs to be converted for dynamic naming system of images
    def save(self, path, filename):
        print(">> Copying")
        newName = path + "/" + filename + ".png"
        shutil.copy('resources/graph_images/foo.png', newName)


class DeletePopup(Popup):
    def get_dataset(self):
        return current_dataset

    def set_dataset(self, new_dataset: str):
        global current_dataset
        current_dataset = new_dataset

    def delete(self):
        #print(">> Deleting")
        data_sets = os.listdir(DATA_DIRECTORY)
        if self.get_dataset() == "":
            print(">>> Nothing to delete")
        elif len(data_sets) == 0:
            print(">>> Nothing to delete")
        else:
            temp = self.get_dataset()
            self.set_dataset("")
            shutil.rmtree(path.join(DATA_DIRECTORY, temp))

# Converts to float without crashing on error
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
    btn_height = prop.NumericProperty(25)
    #btn_width = prop.NumericProperty(70)
    side_width_buffer = prop.NumericProperty(20)

    container = prop.ObjectProperty(None)  # container the buttons are added to

    def add_buttons(self):
        datasetPath = "resources/csv_data_collection"
        #folders_only = listdir(datasetPath)
        files = next(os.walk(datasetPath))[1]
        print(files)

        global current_dataset, selected_graph
        selected_graph = DEFAULT_GRAPH
        current_dataset = ""
        for f in files:
            tempButton = ListButton()
            tempButton.text = str(f)
            self.container.add_widget(tempButton)
    # remove buttons

    def remove_buttons(self):
        for child in [child for child in self.container.children]:
            self.container.remove_widget(child)


class Main_Window(Screen):
    def __init__(self, **kw):
        super(Main_Window, self).__init__(**kw)

    def openManual(self):
        print(">> Opening Manual")
        os.startfile("resources/manuals/user_manual.pdf")

    def deleteCurrent(self):
        os.remove("resources/csv")


class Graph_Window(Screen):
    def __init__(self, **kw):
        super(Graph_Window, self).__init__(**kw)

# Josh - I know I need to format this to match the formatting standards


class Map_Window(Screen):
    def __init__(self, **kwargs):
        super(Map_Window, self).__init__(**kwargs)
        self.selectBox = True

        self.orientation = 'vertical'

        self.mainBox = BoxLayout(orientation='horizontal')
        self.add_widget(self.mainBox)

        self.picture = Image(allow_stretch=True,
                             source='resources/map_images/ice_field_map3.TIF')
        self.mainBox.add_widget(self.picture)
        # xmin,xmax,ymin,xmax of the provided image
        self.xminMap = 134.601389
        self.xmaxMap = 134.956389
        self.yminMap = 58.363611
        self.ymaxMap = 58.989167

        self.xdiff = self.xmaxMap - self.xminMap
        self.ydiff = self.ymaxMap - self.yminMap
        # draw a rectangle
        with self.canvas:
            Color(1, 0, 0, .5, mode='rgba')
            absImageX = self.picture.center_x - \
                self.picture.norm_image_size[0] / 2.0
            absImageY = self.picture.center_y + \
                self.picture.norm_image_size[1] / 2.0

            self.rect = Rectangle(pos=(300, 400), size=(50, 50))

        self.buttonBox = BoxLayout(orientation='vertical', spacing=5)
        self.mainBox.add_widget(self.buttonBox)
        btnCurrentBox = Button(text='Box to Current Data Set')
        btnPullData = Button(text='Pull Box Data')
        btnReturnToMain = Button(text='Return to Main Window')
        self.buttonBox.add_widget(btnCurrentBox)
        self.buttonBox.add_widget(btnPullData)
        self.buttonBox.add_widget(btnReturnToMain)

    def getImageAbsX(self):
        return self.picture.center_x - self.picture.norm_image_size[0] / 2.0

    def getImageAbsY(self):
        return self.picture.center_y + self.picture.norm_image_size[1] / 2.0

    def on_touch_down(self, touch):
        if self.selectBox == True:
            # check if selection is being done outside of the actual image not just the image widget
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
            # check if selection is being done outside of the actual image not just the image widget
            out_of_bounds = False
            if (touch.x < self.picture.center_x - self.picture.norm_image_size[0] / 2) or (touch.x > self.picture.center_x - self.picture.norm_image_size[0] / 2.0 + self.picture.norm_image_size[0]):
                out_of_bounds = True
            if (touch.y < self.picture.center_y - self.picture.norm_image_size[1] / 2) or (touch.y > self.picture.center_y - self.picture.norm_image_size[1] / 2.0 + self.picture.norm_image_size[1]):
                out_of_bounds = True
            if out_of_bounds:
                pass
            else:
                self.rect.size = (touch.x - touch.ox, touch.y - touch.oy)

    # set the box position and size based on xmin, xmax, ymin, ymax
    def set_box_pos(self, xmin, xmax, ymin, ymax):
        bottomX = 0
        bottomY = 0
        xsize = 0
        ysize = 0

        # Check if coords are within range of image
        inBounds = True
        if (xmin >= self.xminMap) and (xmax < self.xmaxMap) and (ymin >= self.yminMap) and (ymax < self.ymaxMap):
            inBounds = True
        else:
            inBounds = False

        if inBounds == True:
            # convert actual coords of bottom left of box to relative pixels on map image
            totalPixelsX = (
                self.picture.center_x - self.picture.norm_image_size[0] / 2.0 + self.picture.norm_image_size[0])
            totalPixelsY = (self.picture.center_y - self.picture.norm_image_size[1] / 2.0 + self.picture.norm_image_size[1]) - (
                self.picture.center_y - self.picture.norm_image_size[1] / 2)
            distanceRatioX = (self.xmaxMap - xmin) / \
                (self.xmaxMap - self.xminMap)
            distanceRatioY = (self.ymaxMap - ymin) / \
                (self.ymaxMap - self.yminMap)
            bottomX = totalPixelsX * distanceRatioX
            bottomY = totalPixelsY * distanceRatioY

            # convert xmax and ymax for size
            distanceRatioX = (self.xmaxMap - xmax) / \
                (self.xmaxMap - self.xminMap)
            distanceRatioY = (self.ymaxMap - ymax) / \
                (self.ymaxMap - self.yminMap)
            xsize = (totalPixelsX * distanceRatioX) - bottomX
            ysize = (totalPixelsY * distanceRatioY) - bottomY

        self.rect.pos = (bottomX, bottomY)
        self.rect.size = (xsize, ysize)

    def pullData(self):
        print("Pulling data from selected region on map")

    def process_input(self, coord, start_date, end_date):
        from icesat2.data.data_controller import create_data

        create_data(start_date=start_date, end_date=end_date, min_x=coord[0],
                    min_y=coord[2], max_x=coord[1], max_y=coord[3])


class Map(MapView):
    pass


class ScreenManagement(ScreenManager):
    pass


class WindowSplitter(Splitter):
    border_size = prop.NumericProperty(5)


class SetGraph(Widget):
    testGraph = prop.ObjectProperty(None)


def main():
    MainApp().run()
