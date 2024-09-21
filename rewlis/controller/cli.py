

class CLIRewlisServer:

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app
        
        # super().__init__(model=self.model)
