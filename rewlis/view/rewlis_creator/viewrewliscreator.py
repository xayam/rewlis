from rewlis.view.rewlis_creator.mykivycreator import MyKivyCreator


class ViewRewlisCreator(MyKivyCreator):

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        super().__init__(model=self.model)
