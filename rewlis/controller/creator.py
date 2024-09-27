import concurrent.futures
import json
import os
import traceback

from PIL import ImageDraw
from kivy.clock import Clock

from rewlis.model.model import Model
from rewlis.controller.eps import *
import rewlis.controller.audio as audio
import rewlis.controller.recognizer as recognizer
import rewlis.controller.sync as sync
import rewlis.controller.cross as cross
from rewlis.utils import *


class Creator:

    def __init__(self, model, cprint):
        self.folder_of_books = None
        self.data = None
        self.model = model
        self.cprint = cprint
        self.controller = self.model.controller
        self.config = self.model.conf

    def init(self):
        self.data = self.model.conf.FOLDER_CREATE
        if not os.path.exists(self.data):
            os.mkdir(self.data)
        self.folder_of_books = os.listdir(self.data)

    def init_process(self):
        self.book = self.controller.current_book
        if self.book is None:
            message = "End create book"
            self.cprint(message)
            raise Exception(message)
        if not os.path.isdir(f"{self.data}/{self.book}"):
            message = "End create book"
            self.cprint(message)
            raise Exception(message)
        return self.valid_process(check=True)

    def check_process(self):
        if os.path.exists(f"{self.data}/{self.book}/{self.config.VALID}"):
            with open(f"{self.data}/{self.book}/{self.config.VALID}",
                      mode="r", encoding="UTF-8") as f:
                valid = f.read()
            if valid == "True":
                self.cprint(f"self.book {self.book} is valid")
                return
        if not os.path.exists(f"{self.data}/{self.book}/{self.config.RUS_TXT}"):
            message = \
                f"File '{self.data}/{self.book}/{self.config.RUS_TXT}' not exists"
            self.cprint(message)
            raise Exception(message)
        with open(f"{self.data}/{self.book}/{self.config.RUS_TXT}",
                  mode="r", encoding="UTF-8") as rus:
            rus_txt = rus.read()
        if not os.path.exists(f"{self.data}/{self.book}/{self.config.ENG_TXT}"):
            message = \
                f"File '{self.data}/{self.book}/{self.config.ENG_TXT}' not exists"
            self.cprint(message)
            raise Exception(message)
        with open(f"{self.data}/{self.book}/{self.config.ENG_TXT}",
                  mode="r", encoding="UTF-8") as eng:
            eng_txt = eng.read()
        return rus_txt, eng_txt

    def audio_process(self):
        mp3rus = [(f"{self.data}/{self.book}", x,
                   f"{self.data}/{self.book}/mp3rus/{x}")
                  for x in os.listdir(f"{self.data}/{self.book}/mp3rus")
                  if x[-4:] == ".mp3"]
        mp3eng = [(f"{self.data}/{self.book}", x,
                   f"{self.data}/{self.book}/mp3eng/{x}")
                  for x in os.listdir(f"{self.data}/{self.book}/mp3eng")
                  if x[-4:] == ".mp3"]
        audio_rus = audio.Audio(self.cprint, mp3rus,
                                os.getcwd() + f"/{self.data}/{self.book}",
                                     "rus")
        audio_eng = audio.Audio(self.cprint, mp3eng,
                                os.getcwd() + f"/{self.data}/{self.book}",
                                     "eng")
        futures = {}
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures["rus"] = executor.submit(audio_rus.process)
            futures["eng"] = executor.submit(audio_eng.process)
            executor.shutdown()
            for lang in futures:
                results.append(futures[lang].result())
        for result in results:
            if result["raise"]:
                raise result["exception"]

    def recognize_process(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(recognizer.Recognizer,
                            self.cprint, f"recognize/rus",
                            f"{self.data}/{self.book}", "rus", self.config
                            )
            executor.submit(recognizer.Recognizer,
                            self.cprint, f"recognize/eng",
                            f"{self.data}/{self.book}", "eng", self.config
                            )
            executor.shutdown()

    def rus_process(self, rus_txt):
        if not os.path.exists(f"{self.data}/{self.book}/{self.config.RUS_SYNC}"):
            with open(f"{self.data}/{self.book}/rus.map.json",
                      mode="r", encoding="UTF-8") as map_json:
                R_start, R_end, R_word = r_map(json.load(map_json))
            rus_html = text2html(text=rus_txt.lower(),
                                 pattern=r'([а-я0-9a-z]+)([^а-я0-9a-z]+)')
            if not os.path.exists(f"{self.data}/{self.book}/rus.html"):
                with open(f"{self.data}/{self.book}/rus.html",
                          mode="w", encoding="UTF-8") as f:
                    f.write(rus_html)
            self.cprint("Get similarity...")
            synchronize, L_word, L_start, L_end = \
                cross.get_sim(rus_html, R_word)
            sync_rus = sync.Sync(cprint=self.cprint,
                                 output=f"{self.data}/{self.book}",
                                 language="rus")
            two_sync = sync_rus.create_sync(
                synchronize, L_start, L_end, L_word, R_start, R_end, R_word)
            for i in range(len(synchronize)):
                for j in range(len(synchronize[i])):
                    synchronize[i][j] = 0
            for i in two_sync:
                synchronize[i[POS]][i[TIME]] = 255
            img = Image.fromarray(np.uint8(synchronize), 'L')
            img.save(f"{self.data}/{self.book}/rus2.sync.png")
            sync2 = two_sync
        else:
            self.cprint(f"Loading file '{self.config.RUS_SYNC}'...")
            with open(f"{self.data}/{self.book}/{self.config.RUS_SYNC}",
                      mode="r") as fsync:
                sync2 = json.load(fsync)

        if not os.path.exists(f"{self.data}/{self.book}/{self.config.RUS_ORIG}"):
            orig_html = text2html(
                text=rus_txt.lower(),
                pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){4})',
                replacepattern=r'<p>\1</p>')
            with open(f"{self.data}/{self.book}/{self.config.RUS_ORIG}",
                      mode="w", encoding="UTF-8") as f:
                f.write(orig_html)
        return sync2

    def eng_process(self, eng_txt):
        if not os.path.exists(f"{self.data}/{self.book}/{self.config.ENG_SYNC}"):
            with open(f"{self.data}/{self.book}/eng.map.json",
                      mode="r", encoding="UTF-8") as map_json:
                R_start, R_end, R_word = r_map(json.load(map_json))
            eng_html = text2html(text=eng_txt.lower(),
                                 pattern=r'([а-я0-9a-z]+)([^а-я0-9a-z]+)')
            if not os.path.exists(f"{self.data}/{self.book}/eng.html"):
                with open(f"{self.data}/{self.book}/eng.html",
                          mode="w", encoding="UTF-8") as f:
                    f.write(eng_html)
            self.cprint("Get similarity...")
            synchronize, L_word, L_start, L_end = \
                cross.get_sim(eng_html, R_word)
            sync_eng = sync.Sync(cprint=self.cprint,
                                 output=f"{self.data}/{self.book}",
                                 language="eng")
            two_sync = sync_eng.create_sync(synchronize, L_start, L_end,
                                            L_word, R_start, R_end, R_word)
            for i in range(len(synchronize)):
                for j in range(len(synchronize[i])):
                    synchronize[i][j] = 0
            for i in two_sync:
                synchronize[i[POS]][i[TIME]] = 255
            img = Image.fromarray(np.uint8(synchronize), 'L')
            img.save(f"{self.data}/{self.book}/eng2.sync.png")
            sync1 = two_sync
        else:
            self.cprint(f"Loading file '{self.config.ENG_SYNC}'...")
            with open(f"{self.data}/{self.book}/{self.config.ENG_SYNC}",
                      mode="r") as fsync:
                sync1 = json.load(fsync)

        if not os.path.exists(f"{self.data}/{self.book}/{self.config.ENG_ORIG}"):
            orig_html2 = text2html(
                text=eng_txt.lower(),
                pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){4})',
                replacepattern=r'<p>\1</p>')
            with open(f"{self.data}/{self.book}/{self.config.ENG_ORIG}",
                      mode="w", encoding="UTF-8") as f:
                f.write(orig_html2)
        return sync1

    def process(self):
        folders = [f"{self.data}/book" for book in self.folder_of_books]
        for book in folders:
            self.controller.current_book = book
            try:
                if self.init_process():
                    continue
                print(f"Selected book '{self.book}'")
                rus_txt, eng_txt = self.check_process()
                self.audio_process()
                self.recognize_process()
                sync2 = self.rus_process(rus_txt=rus_txt)
                sync1 = self.eng_process(eng_txt=eng_txt)
                sync_rus = sync.Sync(
                    cprint=self.cprint,
                    output=f"{self.data}/{self.book}", language="rus")
                two_sync = self.two_process(sync_rus=sync_rus)
                self.micro_process(sync_rus=sync_rus,
                                   two_sync=two_sync, sync1=sync1, sync2=sync2,
                                   rus_txt=rus_txt, eng_txt=eng_txt)
                self.valid_process()
            except Exception as e:
                self.cprint(
                    type(e).__name__ + ": " +
                    e.__str__() + "\n" + traceback.format_exc())
                return

    def two_process(self, sync_rus):
        if not os.path.exists(f"{self.data}/{self.book}/two.json"):
            self.cprint("Not find file two.json, creating...")
            synchronize, L_word, R_word, L_end, R_end = \
                cross.get_sim_v2(self.book, self.data)
            synchronize = find_max_path_v2(synchronize)
            img = Image.fromarray(np.uint8(synchronize * 255), 'L')
            img.save(f"{self.data}/{self.book}/two.png")

            res_min_max = filtered_main_diag(f"{self.data}/{self.book}/two.png")
            synchronize = np.asarray(np.uint8(res_min_max * 100))
            res_min_max = Image.fromarray(np.uint8(res_min_max * 255))
            res_min_max.save(f"{self.data}/{self.book}/two2.png")
            two_sync = sync_rus.create_sync_v2(
                synchronize, L_word, R_word, L_end, R_end,
                len(L_word) - 1, len(R_word) - 1, append=False)
            for i in range(len(synchronize)):
                for j in range(len(synchronize[i])):
                    synchronize[i][j] = 0
            for i in two_sync:
                synchronize[i[L_a]][i[L_b]] = 255
            img = Image.fromarray(np.uint8(synchronize), 'L')
            img.save(f"{self.data}/{self.book}/two3.png")

            img1 = np.zeros_like(synchronize)
            img2 = Image.fromarray(img1)
            img = ImageDraw.Draw(img2)
            a = 0
            b = 0
            for i in range(len(two_sync)):
                img.line([(b, a),
                          (two_sync[i][L_b], two_sync[i][L_a])],
                         fill="white", width=0)
                a = two_sync[i][L_a]
                b = two_sync[i][L_b]
            img2.save(f"{self.data}/{self.book}/adapter.png")
            for i in range(len(synchronize)):
                for j in range(len(synchronize[i])):
                    img1[i][j] = int(img2.getpixel((j, i)) / 2.55)
            synchronize = np.asarray(img1)
            self.cprint("Recreate two_sync...")
            two_sync = sync_rus.create_sync_v2(
                synchronize, L_word, R_word, L_end, R_end,
                len(L_word) - 1, len(R_word) - 1,
                append=False,
                L_window=25)

            for i in range(len(synchronize)):
                for j in range(len(synchronize[i])):
                    synchronize[i][j] = 0
            for i in two_sync:
                synchronize[i[L_a]][i[L_b]] = 255
            img = Image.fromarray(np.uint8(synchronize), 'L')
            img.save(f"{self.data}/{self.book}/adapter2.png")

            with open(f"{self.data}/{self.book}/two.json",
                      mode="w") as fsync:
                json.dump(two_sync, fsync)
        else:
            self.cprint("Loading file 'two.json'...")
            with open(f"{self.data}/{self.book}/two.json",
                      mode="r") as fsync:
                two_sync = json.load(fsync)
        return two_sync

    def micro_process(self, sync_rus,
                      two_sync, sync1, sync2, rus_txt, eng_txt):
        micro = []
        self.cprint(f"Enter to function self.micro_process()...")
        if not os.path.exists(
                f"{self.data}/{self.book}/{self.config.MICRO_JSON}"
        ):
            for i in two_sync:
                phraza_1 = i[2]
                phraza_2 = i[3]
                self.cprint(phraza_1, "<||>", phraza_2)
                if phraza_1.strip() == '' or phraza_2.strip() == '':
                    phraza_1 = 'и '
                    phraza_2 = 'and '
                words1 = re.findall(r"[а-я0-9a-z]+[^а-я0-9a-z]+",
                                    phraza_1)
                words2 = re.findall(r"[а-я0-9a-z]+[^а-я0-9a-z]+",
                                    phraza_2)
                synchronize, L_word, R_word, L_end, R_end = \
                    cross.get_sim_v21(words1, words2)
                assert len(L_word) == len(R_word)
                two = sync_rus.create_sync_v3(
                    synchronize, L_word, R_word, L_end, R_end,
                    len(L_word), len(R_word), i)
                micro.append(two)
            index = -1
            micro2 = micro[:]
            for _ in micro2:
                index += 1
                L_sync = two_sync[index][L_POS]
                R_sync = two_sync[index][R_POS]
                for k in range(len(micro[index]) - 1):
                    L_delta = sum([len(t[L_WORDS])
                                   for t in micro[index][k:]])
                    R_delta = sum([len(t[R_WORDS])
                                   for t in micro[index][k:]])
                    micro[index][k][L_POS] = L_sync - L_delta
                    micro[index][k][R_POS] = R_sync - R_delta
            micro[-1][-1][L_POS] = len(rus_txt) - 1
            micro[-1][-1][R_POS] = len(eng_txt) - 1
            with open(f"{self.data}/{self.book}/{self.config.MICRO_JSON}",
                      mode="w") as f:
                json.dump(micro, f)

        micro2 = []
        self.cprint("Loading file 'micro.json'...")
        with open(f"{self.data}/{self.book}/{self.config.MICRO_JSON}",
                  mode="r") as f:
            m = json.load(f)
        for i in range(len(m)):
            for j in range(len(m[i])):
                micro2.append(m[i][j])
        json_string = json.dumps(micro2)
        self.cprint("Save file 'micro2.json'")
        with open(f"{self.data}/{self.book}/micro2.json", mode="w") as f:
            f.write(json_string)

        if not os.path.exists(f"{self.data}/{self.book}/eng2rus.json"):
            eng2rus = eng_to_rus(micro2, R_POS, L_POS, sync1, sync2)
            json_string = json.dumps(eng2rus)
            self.cprint("Save file 'eng2rus.json'")
            with open(f"{self.data}/{self.book}/eng2rus.json", mode="w") as f:
                f.write(json_string)

        if not os.path.exists(f"{self.data}/{self.book}/rus2eng.json"):
            rus2eng = eng_to_rus(micro2, L_POS, R_POS, sync2, sync1)
            json_string = json.dumps(rus2eng)
            self.cprint("Save file 'rus2eng.json'")
            with open(f"{self.data}/{self.book}/rus2eng.json", mode="w") as f:
                f.write(json_string)

    def valid_process(self, check=False):
        if check:
            valid = "False"
            if os.path.exists(f"{self.data}/{self.book}/{self.config.VALID}"):
                with open(f"{self.data}/{self.book}/{self.config.VALID}",
                          mode="r", encoding="UTF-8") as f:
                    valid = f.read()
            if valid == "True":
                self.cprint(f"Book '{self.book}' created complete")
                return True
            else:
                return False
        else:
            with open(f"{self.data}/{self.book}/{self.config.VALID}",
                      mode="w", encoding="UTF-8") as f:
                f.write("True")
            self.cprint(f"Book '{self.book}' created complete")


if __name__ == "__main__":
    pass
