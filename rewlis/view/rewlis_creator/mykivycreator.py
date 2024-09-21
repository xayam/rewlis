from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.uix.label import Label

from rewlis import VERSION


class MyKivyCreator(KivyApp):

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)
        self.controller.container = Label(text="In development")

    def build(self):
        self.icon = self.model.conf.ICON_ICO
        self.title = "Rewlis Creator"

        return self.controller.container

    def on_start(self):
        pass
