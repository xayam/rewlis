import json
import os

from rewlis.model.book import Book
from rewlis.entity import *


class Sync:

    def __init__(self, model, current_path):
        self.model = model
        self.current_path = current_path

        self.chunks1 = []
        self.chunks2 = []

        self.cover = self.current_path + self.model.conf.BOOK_SCHEME[COVER]
        self.valid = self.current_path + self.model.conf.BOOK_SCHEME[VALID]
        self.micro = []
        self.book1 = None
        self.book2 = None
        self.eng2rus = {}
        self.rus2eng = {}
        self.loaded = False

    def loads(self):
        self.model.log.debug("Enter to function 'sync.loads()'")
        if not os.path.exists(self.valid):
            path = self.model.conf.UPDATE_URL + self.current_path + ".zip"
            self.model.log.debug(f"Try download '{path}'")
            self.model.stor.storage_book(path)
        if not self.loaded:
            self.model.log.debug(f"False == self.loaded")
            self.book1 = Book(model=self.model, path=self.current_path, language=EN)
            self.book2 = Book(model=self.model, path=self.current_path, language=RU)
            try:
                with open(self.current_path + self.model.conf.BOOK_SCHEME[MICRO],
                          mode="r", encoding="UTF-8") as f:
                    self.micro = json.load(f)
                with open(self.current_path + self.model.conf.BOOK_SCHEME[ENG2RUS],
                          mode="r", encoding="UTF-8") as f:
                    self.eng2rus = json.load(f)
                with open(self.current_path + self.model.conf.BOOK_SCHEME[RUS2ENG],
                          mode="r", encoding="UTF-8") as f:
                    self.rus2eng = json.load(f)
                self.split_book()
                self.model.log.debug(f"Length of self.chunks1={len(self.chunks1)}")
                self.model.log.debug(f"Length of self.chunks2={len(self.chunks2)}")
                self.loaded = True
            except Exception as e:
                self.model.log.debug(type(e).__name__ + ": " + e.__str__())

    def split_book(self):
        self.model.log.debug("Enter function 'split_book()'")
        begin2 = 0
        begin1 = 0
        page = 1
        for i in range(len(self.micro)):
            if self.micro[i][L_POS] > page * self.model.chunk_width:
                text2 = self.book2.txt[begin2:self.micro[i][L_POS]]
                if text2 == "":
                    break
                self.chunks2.append(text2)
                begin2 = self.micro[i][L_POS]
                self.chunks1.append(
                    self.book1.txt[begin1:self.micro[i][R_POS]])
                begin1 = self.micro[i][R_POS]
                page += 1
        self.chunks2.append(
            self.book2.txt[begin2:len(self.book2.txt)])
        self.chunks1.append(
            self.book1.txt[begin1:len(self.book1.txt)])
