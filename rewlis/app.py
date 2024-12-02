from rewlis.controller.controller import Controller
from rewlis.entity import TARGET


class App:
    def __init__(self, app):
        self.app = app
        self.controller = Controller(app=self.app)
        self.view = self.controller.view
        self.model = self.controller.model
        self.model.target = self.app[TARGET]

    def run(self):
        self.view.run()
