import json

from rewlis.entity import *


class Book:

    def __init__(self, model, path, language):
        self.model = model
        self.path = path
        self.language = language

        self.length = None
        self.annot = None
        self.txt = None
        self.sync = None

        self.init()

    def init(self):
        self.model.log.debug(
            "Enter to function 'Book.init()', " + self.language + " book")
        if self.language == EN:
            current = self.model.conf.BOOK_ENG_SCHEME
        else:
            current = self.model.conf.BOOK_RUS_SCHEME
        try:
            with open(self.path + current[ANNOT],
                      mode="r", encoding="UTF-8") as f:
                self.annot = f.read() + "\n\n"
            with open(self.path + current[TXT],
                      mode="r", encoding="UTF-8") as txt:
                self.txt = txt.read()
            with open(self.path + current[SYNC],
                      mode="r", encoding="UTF-8") as f:
                self.sync = json.load(f)
        except Exception as e:
            self.model.log.debug(
                "BookInit: " + type(e).__name__ + ": " + e.__str__())
        if self.model.current_select in self.model.opt[POSITIONS]:
            self.model.chunk_current = \
                self.model.opt[POSITIONS][self.model.current_select][CHUNK]
        else:
            self.model.chunk_current = 0
