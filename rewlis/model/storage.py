import io
import os
import requests
import zipfile

from rewlis.entity import *
from rewlis.model.sync import Sync
from rewlis.model.cimg import decode_image


class Storage:

    def __init__(self, model):
        self.model = model
        self.controller = self.model.controller
        self.app = self.model.app

        self.data = "data"
        self.storage_books = {}
        self.timeout = 3
        self.verify = True
        self.headers = {
            "User-Agent":
                r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) " +
                "Gecko/20100101 Firefox/96.0",
            "Content-type": "application/x-www-form-urlencoded"
        }
        if self.model.target == TARGET_WINDOWS:
            from rewlis.model.img import Img
            if not os.path.exists("res"):
                os.mkdir("res")
            decode_image(folder="res/img/", img=Img())

    def list(self):
        if self.controller is None:
            return
        if self.controller.app == APP_CREATOR:
            return
        self.storage_list()
        for i in os.listdir(self.data):
            if os.path.isfile(f"{self.data}/" + i) and (i[-4:] == ".jpg"):
                cover = f"{self.data}/{i}"
                self.storage_books[cover] = f"{self.data}/{i[:-4]}/"
                self.model.log.debug(
                    f"self.storage_books[cover]={self.storage_books[cover]}"
                )
                self.model.syncs[self.storage_books[cover]] = \
                    Sync(model=self.model,
                         current_path=self.storage_books[cover])

    def storage_list(self):
        self.model.log.debug("Enter to function storage_list()")
        try:
            direct_link = self.model.conf.LIST_URL
            self.model.log.debug(f"Update {direct_link}")
            resp = requests.get(direct_link,
                                timeout=self.timeout,
                                verify=self.verify,
                                headers=self.headers)
            if resp.status_code == 200:
                self.model.log.debug(f"Unzip list.zip")
                z = zipfile.ZipFile(io.BytesIO(resp.content))
                z.extractall(self.data)
                z.close()
            else:
                raise Exception(f"resp.StatusCode={resp.status_code}")
        except Exception as e:
            self.model.log.warn("ERROR: " + e.__str__())

    def storage_book(self, book):
        self.model.log.debug(f"Enter to function storage_book(book='{book}')")
        try:
            direct_link = self.model.conf.UPDATE_URL + book
            resp = requests.get(direct_link,
                                timeout=self.timeout,
                                verify=self.verify,
                                headers=self.headers)
            if resp.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(resp.content))
                output_dir = self.data + "/" + book[:-4]
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)
                z.extractall(output_dir)
                z.close()
            else:
                raise Exception(f"resp.StatusCode={resp.status_code}")
        except Exception as e:
            self.model.log.warn("ERROR: " + e.__str__())
