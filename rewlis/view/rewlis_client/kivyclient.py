from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App as KivyApp
from kivy.uix.tabbedpanel import TabbedPanel

from rewlis.model.mysound import MySound

from rewlis import *
from .catalog import Catalog
from .table import Table
from .options import Options


class KivyClient(KivyApp):

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        Config.set('kivy', 'window_icon', self.model.conf.ICON_PNG)
        self.controller.container = TabbedPanel()
        self.controller.table = Table(model=self.model)
        self.controller.catalog = Catalog(model=self.model)
        self.controller.options = Options(model=self.model)
        Window.bind(size=self.controller.catalog.on_resize)

    def build(self):
        self.icon = self.model.conf.ICON_ICO
        self.title = f"{self.model.conf.NAME}"
        self.controller.container.size_hint = (1, 1)
        self.controller.container.do_default_tab = False
        self.controller.container.add_widget(self.controller.catalog)
        self.controller.container.add_widget(self.controller.table)
        self.controller.container.add_widget(self.controller.options)
        self.controller.container.default_tab = self.controller.table
        return self.controller.container

    def on_start(self):
        self.controller.container.tab_width = 3 * self.controller.container.tab_height
        self.controller.catalog.on_resize()
