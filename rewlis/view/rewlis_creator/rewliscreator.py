from rewlis.view.rewlis_creator.kivycreator import KivyCreator


class RewlisCreator(KivyCreator):

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        super().__init__(model=self.model)
