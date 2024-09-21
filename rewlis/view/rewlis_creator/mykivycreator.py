from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.uix.boxlayout import BoxLayout

from rewlis.controller.creator import Creator
from rewlis.view.rewlis_creator.menu import Menu
from rewlis.view.rewlis_creator.panel import Panel
from rewlis.view.rewlis_creator.project import Project


class MyKivyCreator(KivyApp):

    def __init__(self, model):
        super().__init__()
        self.project = None
        self.menu = None
        self.panel = None
        self.layout = None
        self.model = model
        self.app = self.model.app
        self.controller = self.model.controller
        self.controller.creator = Creator(model=self.model)
        self.controller.creator.init()

        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)

    def build(self):
        self.icon = self.model.conf.ICON_ICO
        self.title = "Rewlis Creator"
        self.controller.menu = Menu(controller=self.controller).init()
        self.controller.project = Project(controller=self.controller).init()
        self.controller.panel = Panel(controller=self.controller).init()
        self.layout = BoxLayout()
        self.layout.add_widget(self.controller.panel)
        self.layout.add_widget(self.controller.menu)
        self.layout.add_widget(self.controller.project)
        self.controller.container = self.layout
        return self.controller.container

    def on_start(self):
        pass
