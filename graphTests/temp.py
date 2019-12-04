from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
import csv 

with open('foo.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter= ',')
    csvInput = []
    for row in csv_reader:
        for element in row:
            csvInput.append(int(element))
        
        
print(csvInput)      

plt.plot(csvInput)
plt.title('IGLOO TESTS')
plt.ylabel('Y Axis')
plt.xlabel('X Axis')

class MyApp(App):

    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box

MyApp().run()