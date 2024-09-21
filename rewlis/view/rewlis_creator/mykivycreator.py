from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.uix.boxlayout import BoxLayout

from rewlis.view.rewlis_creator.menu import Menu
from rewlis.view.rewlis_creator.panel import Panel
from rewlis.view.rewlis_creator.project import Project


class MyKivyCreator(KivyApp):

    def __init__(self, model):
        super().__init__()
        self.project = None
        self.menu = None
        self.panel2 = None
        self.panel1 = None
        self.panel = None
        self.layout = None
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)

    def build(self):
        self.icon = self.model.conf.ICON_ICO
        self.title = "Rewlis Creator"
        self.panel = Panel().init()
        self.menu = Menu().init()
        self.project = Project().init()
        self.layout = BoxLayout()
        self.layout.add_widget(self.panel)
        self.layout.add_widget(self.menu)
        self.layout.add_widget(self.project)
        self.controller.container = self.layout
        return self.controller.container

    def on_start(self):
        pass
