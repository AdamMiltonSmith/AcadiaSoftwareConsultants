import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.stencilview import StencilView
import ctypes


"""
This stopped some TIFF unknown field with tag warnings. I don't know how it
works. Got it here:
https://stackoverflow.com/questions/58279121/python-tiffreaddirectory-warning-unknown-field-with-tag
"""
libbytiff = ctypes.CDLL("libtiff-5.dll")
libbytiff.TIFFSetWarningHandler.argtypes = [ctypes.c_void_p]
libbytiff.TIFFSetWarningHandler.restype = ctypes.c_void_p
libbytiff.TIFFSetWarningHandler(None)


class StencilTestWidget(StencilView):
    '''Drag to define stencil area
    '''

    def doNothing(self):
        print("doin nothin")



class Touch(BoxLayout):
    def __init__(self, **kwargs):
        super(Touch, self).__init__(**kwargs)
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


            self.rect = Rectangle(pos=(absImageX, absImageY), size=(50,50))
        
        
        self.buttonBox = BoxLayout(orientation = 'vertical')
        self.mainBox.add_widget(self.buttonBox)
        btnCurrentBox = Button(text = 'Box to Current Data Set')
        btnPullData = Button(text = 'Pull Box Data')
        self.buttonBox.add_widget(btnCurrentBox)
        self.buttonBox.add_widget(btnPullData)
        
        

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
    


    




class SimpleImage(App):
    def build(self):
        #return ContainerBox()
        return Touch()

if __name__ == '__main__':
    SimpleImage().run()

