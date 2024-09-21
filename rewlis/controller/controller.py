import os

from rewlis.entity import *
from rewlis.model.model import Model


class Controller:

    def __init__(self, app):

        self.app = app
        
        self.model = Model(controller=self, target=self.app[TARGET])
        os.environ["TARGET_PLATFORM"] = self.model.target
        if self.app[APP_NAME] == APP_CREATOR:
            from rewlis.view.rewlis_creator.viewrewliscreator import ViewRewlisCreator
            self.view = ViewRewlisCreator(model=self.model)
        elif self.app[APP_NAME] == APP_CLIENT:
            from rewlis.view.rewlis_client.viewrewlis import ViewRewlisClient
            self.view = ViewRewlisClient(model=self.model)
        elif self.app[APP_NAME] == APP_SERVER:
            from rewlis.controller.cli import CLIRewlisServer
            self.view = CLIRewlisServer(model=self.model)
        else:
            self.model.log.error(f"APP_NAME некорректен | {self.app[APP_NAME]}")
