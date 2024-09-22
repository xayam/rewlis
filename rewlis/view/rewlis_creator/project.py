import os.path

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from rewlis.view.rewlis_creator.mycheckbox import MyCheckBox


class Project(BoxLayout):

    def __init__(self, controller, **kwargs):
        BoxLayout.__init__(self,
                           orientation="vertical",
                           size_hint=(1, None),
                           **kwargs)
        self.layout = None
        self.controller = controller
        self.model = self.controller.model
        self.cbs = {
            self.model.conf.MP3RUS: MyCheckBox(),
            self.model.conf.MP3ENG: MyCheckBox(),
            self.model.conf.COVER: MyCheckBox(),
            self.model.conf.RUS_ANNOT: MyCheckBox(),
            self.model.conf.ENG_ANNOT: MyCheckBox(),
            self.model.conf.RUS_FB2: MyCheckBox(),
            self.model.conf.ENG_FB2: MyCheckBox(),
            self.model.conf.RUS_TXT: MyCheckBox(),
            self.model.conf.ENG_TXT: MyCheckBox(),
        }


    def init(self):
        self.layout = BoxLayout(orientation="vertical",
                                size_hint=(1, 1))
        for w in self.cbs:
            self.layout.add_widget(self.cbs[w])
        self.add_widget(self.layout)
        self.size = 1, 30 * len(self.cbs)
        return self

    def load_project(self, book, current):
        for w in self.cbs:
            curr = current + "/" + w
            if os.path.exists(curr):
                self.cbs[w].label.text = curr
                self.cbs[w].checkbox.active = True
        print(book)
