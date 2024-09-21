from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from rewlis.view.rewlis_creator.panel import Panel
from rewlis.view.rewlis_creator.project import Project


class MyKivyCreator(KivyApp):

    def __init__(self, model):
        super().__init__()
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
        self.panel1 = Panel(anchor_x="left", anchor_y="center").init()
        self.panel2 = Project().init()
        self.layout = BoxLayout()
        self.layout.add_widget(self.panel1)
        self.layout.add_widget(self.panel2)
        self.controller.container = self.layout
        return self.controller.container

    def on_start(self):
        pass
