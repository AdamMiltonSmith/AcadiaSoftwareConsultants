import ctypes
import glob
import os
import shutil
from os import listdir, path
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
try:
    libbytiff = ctypes.CDLL("libtiff-5.dll")
    libbytiff.TIFFSetWarningHandler.argtypes = [ctypes.c_void_p]
    libbytiff.TIFFSetWarningHandler.restype = ctypes.c_void_p
    libbytiff.TIFFSetWarningHandler(None)
except:
    pass


"""Removes red dots when right clicking."""
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# just dataset name - i.e. "Untitled"
current_dataset = ""

# full path - i.e. "resources/graph_images/no_dataset.png"
selected_graph = ""

MONTH_DAY = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

DATA_DIRECTORY = "resources/csv_data_collection"
LOG_DIRECTORY = "logs"

DEFAULT_GRAPH = "resources/graph_images/no_dataset.png"
ERROR_GRAPH = "resources/graph_images/items_missing.png"

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
            n = ErrorPopup(error_message="There is no project to save.").open()
            return
        p = ProjectSavePopup().open()

    def project_delete_check(self):
        data_sets = os.listdir(DATA_DIRECTORY)
        if len(data_sets) == 0:
            e = ErrorPopup(
                error_message="No datasets to delete.").open()
        elif current_dataset == "":
            e = ErrorPopup(
                error_message="No dataset selected to delete."
                "\nRefresh the data list to select a new one.").open()
        else:
            p = DeletePopup().open()

class EditDropDown(DropDown):
    font_size = prop.NumericProperty(14)

    def show_preferences(self):
        # TODO
        e = ErrorPopup(
            error_message="To do:\nThis requires implementation at a later time"). open()

        # show preferences popup that pulls from config file


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

        graph_widget = App.get_running_app(
        ).root.children[0].ids.main_window_graph_widget

        # check the data set that it has everything completed for a drawing
        if not path.exists(f"{DATA_DIRECTORY}/{project_name}/change_in_height.csv") or not path.exists(f"{DATA_DIRECTORY}/{project_name}/object_info.txt"):
            e = ErrorPopup(error_message="The dataset is missing necessary "
                           "files.\nThis is probably due to not completing "
                           "the data acquisition.").open()

            graph_widget.set_image("error")

            return

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

        if path.exists(selected_graph) and (selected_graph != DEFAULT_GRAPH and selected_graph != ERROR_GRAPH):
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
        # print(selected_graph)
        if self.source != selected_graph:
            self.source = selected_graph
            # despite it being a huge edge case, we do not want it to crash here
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


class ErrorPopup(Popup):
    error_message = prop.StringProperty()

    def __init__(self, *, error_message, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        self.error_message = error_message


class NotificationPopup(Popup):
    message = prop.StringProperty()

    def __init__(self, *, message, **kwargs):
        super(NotificationPopup, self).__init__(**kwargs)
        self.message = message

class ProjectSavePopup(Popup):
    def save(self, new_name):
        #os.rename(src, dst)
        global current_dataset, selected_graph

        # rename image
        os.rename(f"resources/graph_images/{current_dataset}.png",
                  f"resources/graph_images/{new_name}.png")

        selected_graph = f"resources/graph_images/{new_name}.png"

        # rename project
        os.rename(f"{DATA_DIRECTORY}/{current_dataset}",
                  f"{DATA_DIRECTORY}/{new_name}")

        current_dataset = new_name


class ImageSavePopup(Popup):
    # needs to be converted for dynamic naming system of images
    def save(self, file_path, file_name):
        new_name = file_path + "/" + file_name + ".png"
        if path.exists(new_name):
            e = ErrorPopup(error_message = "File already exists.")
            return

        if selected_graph == DEFAULT_GRAPH or selected_graph == ERROR_GRAPH:
            e = ErrorPopup(error_message="No project to save.")
            return
        else:
            shutil.copy(selected_graph, new_name)


class DeletePopup(Popup):
    def get_dataset(self):
        return current_dataset

    def set_dataset(self, new_dataset: str):
        global current_dataset
        current_dataset = new_dataset

    def delete(self):
        #print(">> Deleting")

        temp = self.get_dataset()
        self.set_dataset("")
        global selected_graph
        selected_graph = DEFAULT_GRAPH
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


class Map_Widget(Image):
    rect_pos = prop.ListProperty([0, 0])
    rect_size = prop.ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(Map_Widget, self).__init__(**kwargs)
        self.selectBox = True

        # xmin,xmax,ymin,xmax of the provided image
        self.map_xmin = -134.95
        self.map_xmax = -133.601389
        self.map_ymin = 58.363611
        self.map_ymax = 58.989167

        self.x_diff = self.map_xmax - self.map_xmin
        self.y_diff = self.map_ymax - self.map_ymin

    def get_image_size_x(self):
        return self.center_x + self.norm_image_size[0] / 2.0

    def get_image_size_y(self):
        return self.center_y + self.norm_image_size[1] / 2.0

    def on_touch_down(self, touch):
        if self.selectBox == True:
            # check if selection is being done outside of the actual image not just the image widget
            out_of_bounds = False
            if (touch.x < self.center_x - self.norm_image_size[0] / 2) or (touch.x > self.center_x - self.norm_image_size[0] / 2.0 + self.norm_image_size[0]):
                out_of_bounds = True
            if (touch.y < self.center_y - self.norm_image_size[1] / 2) or (touch.y > self.center_y - self.norm_image_size[1] / 2.0 + self.norm_image_size[1]):
                out_of_bounds = True
            if out_of_bounds:
                pass
            else:
                self.rect_pos = touch.pos
                self.rect_size = [0, 0]

    def on_touch_move(self, touch):
        #print(self.rect_size)
        if self.selectBox == True:
            # check if selection is being done outside of the actual image not just the image widget
            out_of_bounds = False
            if (touch.x < self.center_x - self.norm_image_size[0] / 2) or (touch.x > self.center_x - self.norm_image_size[0] / 2.0 + self.norm_image_size[0]):
                out_of_bounds = True
            if (touch.y < self.center_y - self.norm_image_size[1] / 2) or (touch.y > self.center_y - self.norm_image_size[1] / 2.0 + self.norm_image_size[1]):
                out_of_bounds = True
            if out_of_bounds:
                pass
            else:
                self.rect_size = [touch.x - touch.ox, touch.y - touch.oy]



    # set the box position and size based on xmin, xmax, ymin, ymax
    def set_box_pos(self, xmin, xmax, ymin, ymax):

        bottomX = 0
        bottomY = 0
        xsize = 0
        ysize = 0

        # Check if coords are within range of image
        inBounds = True
        if (xmin >= self.map_xmin) and (xmax < self.map_xmax) and (ymin >= self.map_ymin) and (ymax < self.map_ymax):
            inBounds = True
        else:
            inBounds = False

        if inBounds == True:
            # convert actual coords of bottom left of box to relative pixels on map image
            totalPixelsX = (
                self.center_x - self.norm_image_size[0] / 2.0 + self.norm_image_size[0])
            totalPixelsY = (self.center_y - self.norm_image_size[1] / 2.0 + self.norm_image_size[1]) - (
                self.center_y - self.norm_image_size[1] / 2)
            distanceRatioX = (self.map_xmax - xmin) / \
                (self.map_xmax - self.map_xmin)
            distanceRatioY = (self.map_ymax - ymin) / \
                (self.map_ymax - self.map_ymin)
            bottomX = totalPixelsX * distanceRatioX
            bottomY = totalPixelsY * distanceRatioY

            # convert xmax and ymax for size
            distanceRatioX = (self.map_xmax - xmax) / \
                (self.map_xmax - self.map_xmin)
            distanceRatioY = (self.map_ymax - ymax) / \
                (self.map_ymax - self.map_ymin)
            xsize = (totalPixelsX * distanceRatioX) - bottomX
            ysize = (totalPixelsY * distanceRatioY) - bottomY

        self.rect_pos = (bottomX, bottomY)
        self.rect_size = (xsize, ysize)

    def pull_data(self):
        image_size = self.norm_image_size

        image_bottom_left = (
            self.center_x - self.norm_image_size[0] / 2.0, self.center_y - self.norm_image_size[1] / 2.0)

        map_coordinate_diff = (self.x_diff, self.y_diff)

        map_bottom_left_coords = (self.map_xmin, self.map_ymin)

        bottom_left_image_pos = None
        top_right_image_pos = None

        # no selection on the map
        if self.rect_size[0] == 0 and self.rect_size[1] == 0:
            e = ErrorPopup(error_message = "No map selection").open()
            return None

        # one of the dimensions is 0, thus the selection has no area
        elif self.rect_size[0] == 0 or self.rect_size[1] == 0:
            e = ErrorPopup(error_message = "Selection has no area").open()
            return None

        #selection is left and down
        elif self.rect_size[0] < 0 and self.rect_size[1] < 0:
            bottom_left_image_pos = (
                self.rect_pos[0] + self.rect_size[0],
                self.rect_pos[1] + self.rect_size[1])

            top_right_image_pos = (self.rect_pos[0], self.rect_pos[1])

        # selection is right and down
        elif self.rect_size[0] > 0 and self.rect_size[1] < 0:
            bottom_left_image_pos = (
                self.rect_pos[0], self.rect_pos[1] + self.rect_size[1])

            top_right_image_pos = (
                self.rect_pos[0] + self.rect_size[0], self.rect_pos[1])

        # selection is left and up
        elif self.rect_size[0] < 0 and self.rect_size[1] > 0:
            bottom_left_image_pos = (
                self.rect_pos[0] + self.rect_size[0], self.rect_pos[1])

            top_right_image_pos = (
                self.rect_pos[0], self.rect_pos[1] + self.rect_size[1])

        # selection is right and up
        elif self.rect_size[0] > 0 and self.rect_size[1] > 0:
            bottom_left_image_pos = (
                self.rect_pos[0], self.rect_pos[1])

            top_right_image_pos = (
                self.rect_pos[0] + self.rect_size[0],
                self.rect_pos[1] + self.rect_size[1])

        # scale the images to the box they are in

        bottom_left_image_pos_scaled = tuple(
            ele1 - ele2 for ele1, ele2 in zip(bottom_left_image_pos, image_bottom_left))

        top_right_image_pos_scaled = tuple(
            ele1 - ele2 for ele1, ele2 in zip(top_right_image_pos, image_bottom_left))
        # get percent of image they are in

        bottom_left_image_percent = tuple(
            ele1 / ele2 for ele1, ele2 in zip(bottom_left_image_pos_scaled, image_size))

        top_right_image_percent = tuple(
            ele1 / ele2 for ele1, ele2 in zip(top_right_image_pos_scaled, image_size))

        # get coordinate offset of map for pos

        bottom_left_map_coordinate_diff = tuple(
            ele1 * ele2 for ele1, ele2 in zip(bottom_left_image_percent, map_coordinate_diff))

        top_right_map_coordinate_diff = tuple(
            ele1 * ele2 for ele1, ele2 in zip(top_right_image_percent, map_coordinate_diff))

        # add coordinate offset to map to get coordinate value

        bottom_left_scaled_coordinate = tuple(
            ele1 + ele2 for ele1, ele2 in zip(bottom_left_map_coordinate_diff, map_bottom_left_coords))

        top_right_scaled_coordinate = tuple(
            ele1 + ele2 for ele1, ele2 in zip(top_right_map_coordinate_diff, map_bottom_left_coords))

        _coords = (bottom_left_scaled_coordinate, top_right_scaled_coordinate)
        coords = [element for tupl in _coords for element in tupl]
        return coords


class Main_Window(Screen):
    def __init__(self, **kw):
        super(Main_Window, self).__init__(**kw)

    #Launches the manual in default pdf viewer 
    def openManual(self):
        os.startfile(os.path.normpath("resources/manuals/user_manual.pdf"))

    def deleteCurrent(self):
        os.remove("resources/csv")

    def map_selection_to_popup(self):
        coords = self.ids.map_widget.pull_data()

        if coords == None:
            return

        c = CoordinatePopup()
        c.open()

        c.ids.topleft.text = str(round(coords[0], 5))
        c.ids.bottomleft.text = str(round(coords[1], 5))
        c.ids.topright.text = str(round(coords[2], 5))
        c.ids.bottomright.text = str(round(coords[3], 5))


class Graph_Window(Screen):
    def __init__(self, **kw):
        super(Graph_Window, self).__init__(**kw)

    #Launches the manual in default pdf viewer 
    def openManual(self):
        os.startfile(os.path.normpath("resources/manuals/user_manual.pdf"))

# Josh - I know I need to format this to match the formatting standards


class Map_Window(Screen):
    def map_selection_to_popup(self):
        coords = self.ids.map_widget.pull_data()

        if coords == None:
            return

        c = CoordinatePopup()
        c.open()

        c.ids.topleft.text = str(round(coords[0], 5))
        c.ids.bottomleft.text = str(round(coords[1], 5))
        c.ids.topright.text = str(round(coords[2], 5))
        c.ids.bottomright.text = str(round(coords[3], 5))

    # updates the coordinates displayed on the bottom of the window to the box
    def updateCoords(self):
        coords = self.ids.map_widget.pull_data()

        if coords == None:
            return
        self.ids.min_x_label.text = "Minimum X: " + str(round(coords[0], 5))
        self.ids.min_y_label.text = "Minimum Y: " + str(round(coords[1], 5))
        self.ids.max_x_label.text = "Maximum X: " + str(round(coords[2], 5))
        self.ids.max_y_label.text = "Maximum Y: " + str(round(coords[3], 5))

    #Launches the manual in default pdf viewer 
    def openManual(self):
        os.startfile(os.path.normpath("resources/manuals/user_manual.pdf"))
class Map(MapView):
    pass


class ScreenManagement(ScreenManager):
    pass


class WindowSplitter(Splitter):
    border_size = prop.NumericProperty(5)


class SetGraph(Widget):
    testGraph = prop.ObjectProperty(None)


def main():
    if not path.exists(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)
    if not path.exists(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)

    MainApp().run()
