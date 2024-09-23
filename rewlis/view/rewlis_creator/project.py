import os.path

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
        self.size = 1, self.cbs[self.model.conf.MP3RUS].height * len(self.cbs)
        return self

    def load_project(self, book, current):
        self.controller.current_book = book
        for w in self.cbs:
            curr = current + "/" + w
            self.cbs[w].label.text = curr
            self.cbs[w].label.text_size = self.cbs[w].label.size
            if os.path.exists(curr):
                self.cbs[w].checkbox.active = True
                self.cbs[w].label.color = 0., 1., 0., 1.
            else:
                self.cbs[w].checkbox.active = False
                self.cbs[w].label.color = 1., 0., 0., 1.

        print(book)
