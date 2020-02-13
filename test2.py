from kivy.garden.mapview import MapView, MapSource
from kivy.garden.mapview.mapview import mbtsource
from kivy.app import App
from kivy.config import Config


class MapViewApp(App):
    def build(self):
        source = mbtsource.MBTilesMapSource("resources\\tiles\\2017-07-03_alaska_juneau.mbtiles")
        mapview = MapView(zoom=5, lat=50.6394, lon=3.057, source = source)
        return mapview

Config.set('input', 'mouse', 'mouse,disable_multitouch')
MapViewApp().run()
