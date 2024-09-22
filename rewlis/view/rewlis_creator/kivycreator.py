import sys

from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from rewlis.controller.creator import Creator
from rewlis.view.rewlis_creator.menu import Menu
from rewlis.view.rewlis_creator.panel import Panel
from rewlis.view.rewlis_creator.project import Project
from rewlis.view.rewlis_creator.terminal import Terminal


class KivyCreator(KivyApp):

    def __init__(self, model):
        super().__init__()
        self.project = None
        self.menu = None
        self.panel = None
        self.layout = None
        self.layout2 = None
        self.model = model
        self.app = self.model.app
        self.controller = self.model.controller
        self.controller.creator = Creator(model=self.model)
        self.controller.creator.init()
        sys.stdout = Terminal(model=self.model)

        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)

    def build(self):
        self.icon = self.model.conf.ICON_ICO
        self.title = "Rewlis Creator"
        self.controller.menu = Menu(controller=self.controller).init()
        self.controller.project = Project(controller=self.controller).init()
        self.controller.panel = Panel(controller=self.controller).init()
        self.layout = BoxLayout()
        self.layout2 = BoxLayout(orientation="vertical",
                                 size_hint=(1, 1))
        self.layout.add_widget(self.controller.panel)
        self.layout.add_widget(self.controller.menu)
        self.layout2.add_widget(self.controller.project)
        self.layout2.add_widget(sys.stdout)
        self.layout.add_widget(self.layout2)
        self.controller.container = self.layout
        return self.controller.container

    def on_start(self):
        pass
