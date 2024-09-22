from kivy.uix.anchorlayout import AnchorLayout


class Project(AnchorLayout):

    def __init__(self, controller, **kwargs):
        AnchorLayout.__init__(self, **kwargs)
        self.controller = controller
        self.model = self.controller.model


    def init(self):
        return self

    def load_project(self, book):
        print(book)
