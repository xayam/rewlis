import concurrent.futures
import json
import os
import traceback
import shutil

from PIL import ImageDraw
from kivy.clock import Clock

from rewlis import utils
from rewlis.controller.eps import *
import rewlis.controller.audio as audio
import rewlis.controller.recognizer as recognizer
import rewlis.controller.sync as sync
import rewlis.controller.cross as cross
from rewlis.utils import *


class Creator:

    def __init__(self, model, cprint):
        self.folder_rus = None
        self.folder_eng = None
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
        self.folder_rus = [(book, RU) for book in os.listdir(f"{self.data}/{RU}")]
        self.folder_eng = [(book, EN) for book in os.listdir(f"{self.data}/{EN}")]
        self.folder_of_books = self.folder_rus + self.folder_eng

    def check_process(self, book, lang):
        if not os.path.exists(f"{self.data}/{lang}/{book}/{BOOK_TXT}"):
            message = \
                f"File '{self.data}/{lang}/{book}/{BOOK_TXT}' not exists"
            self.cprint(message)
            raise Exception(message)
        with open(f"{self.data}/{lang}/{book}/{BOOK_TXT}",
                  mode="r", encoding="UTF-8") as f:
            file_txt = f.read()
        return file_txt

    def audio_process(self, book, lang):
        audiobooks = [
            (f"{self.data}/{lang}/{book}", x,
             f"{self.data}/{lang}/{book}/audiobook/{x}")
            for x in os.listdir(f"{self.data}/{lang}/{book}/audiobook")
            if x[-4:] == ".mp3"]
        audiobook = audio.Audio(cprint=self.cprint, audio_list=audiobooks,
                                output=f"/{self.data}/{lang}/{book}",
                                language=lang)
        result = audiobook.process()
        if result["raise"]:
            raise result["exception"]

    def recognize_process(self, book, lang):
        recognize = recognizer.Recognizer(
            cprint=self.cprint,
            output=f"{self.data}/{lang}/{book}",
            language=lang, config=self.config
        )
        recognize.create_map()

    def rus_process(self, rus_txt, book, lang):
        if not os.path.exists(f"{self.data}/{lang}/{book}/{SYNC_JSON}"):
            with open(f"{self.data}/{lang}/{book}/{MAP_JSON}",
                      mode="r", encoding="UTF-8") as map_json:
                R_start, R_end, R_word = r_map(json.load(map_json))
            rus_html = text2html(text=rus_txt.lower(),
                                 pattern=r'([а-я0-9a-z]+)([^а-я0-9a-z]+)')
            if not os.path.exists(f"{self.data}/{lang}/{book}/{ALL_HTML}"):
                with open(f"{self.data}/{lang}/{book}/{ALL_HTML}",
                          mode="w", encoding="UTF-8") as f:
                    f.write(rus_html)
            self.cprint(f"Getting similarity text and audio book '{lang}/{book}'...")
            synchronize, L_word, L_start, L_end = \
                cross.get_sim(rus_html, R_word)
            sync_rus = sync.Sync(cprint=self.cprint,
                                 output=f"{self.data}/{lang}/{book}",
                                 language=RU)
            two_sync = sync_rus.create_sync(
                synchronize, L_start, L_end, L_word, R_start, R_end, R_word)
            # for i in range(len(synchronize)):
            #     for j in range(len(synchronize[i])):
            #         synchronize[i][j] = 0
            # for i in two_sync:
            #     synchronize[i[POS]][i[TIME]] = 255
            # img = Image.fromarray(np.uint8(synchronize), 'L')
            # img.save(f"{self.data}/{book}/rus2.sync.png")
            sync2 = two_sync
        else:
            self.cprint(f"Loading file '{SYNC_JSON}'...")
            with open(f"{self.data}/{lang}/{book}/{SYNC_JSON}",
                      mode="r") as fsync:
                sync2 = json.load(fsync)

        if not os.path.exists(f"{self.data}/{lang}/{book}/{ORIG_HTML}"):
            orig_html_rus = text2html(
                text=rus_txt.lower(),
                pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){4})',
                replacepattern=r'<p>\1</p>')
            with open(f"{self.data}/{lang}/{book}/{ORIG_HTML}",
                      mode="w", encoding="UTF-8") as f:
                f.write(orig_html_rus)
        return {"raise": False, "exception": None, "sync": sync2}

    def eng_process(self, eng_txt, book, lang):
        if not os.path.exists(f"{self.data}/{lang}/{book}/{SYNC_JSON}"):
            with open(f"{self.data}/{lang}/{book}/{MAP_JSON}",
                      mode="r", encoding="UTF-8") as map_json:
                R_start, R_end, R_word = r_map(json.load(map_json))
            eng_html = text2html(text=eng_txt.lower(),
                                 pattern=r'([а-я0-9a-z]+)([^а-я0-9a-z]+)')
            if not os.path.exists(f"{self.data}/{lang}/{book}/{ALL_HTML}"):
                with open(f"{self.data}/{lang}/{book}/{ALL_HTML}",
                          mode="w", encoding="UTF-8") as f:
                    f.write(eng_html)
            self.cprint(
                f"Getting similarity text and audio book '{lang}/{book}'...")
            synchronize, L_word, L_start, L_end = \
                cross.get_sim(eng_html, R_word)
            sync_eng = sync.Sync(cprint=self.cprint,
                                 output=f"{self.data}/{lang}/{book}",
                                 language=EN)
            two_sync = sync_eng.create_sync(synchronize, L_start, L_end,
                                            L_word, R_start, R_end, R_word)
            # for i in range(len(synchronize)):
            #     for j in range(len(synchronize[i])):
            #         synchronize[i][j] = 0
            # for i in two_sync:
            #     synchronize[i[POS]][i[TIME]] = 255
            # img = Image.fromarray(np.uint8(synchronize), 'L')
            # img.save(f"{self.data}/{book}/eng2.sync.png")
            sync1 = two_sync
        else:
            self.cprint(f"Loading file '{SYNC_JSON}'...")
            with open(f"{self.data}/{lang}/{book}/{SYNC_JSON}",
                      mode="r") as fsync:
                sync1 = json.load(fsync)

        if not os.path.exists(f"{self.data}/{lang}/{book}/{ORIG_HTML}"):
            orig_html_eng = text2html(
                text=eng_txt.lower(),
                pattern=r'(([а-я0-9a-z]+[^а-я0-9a-z]+){4})',
                replacepattern=r'<p>\1</p>')
            with open(f"{self.data}/{lang}/{book}/{ORIG_HTML}",
                      mode="w", encoding="UTF-8") as f:
                f.write(orig_html_eng)
        return {"raise": False, "exception": None, "sync": sync1}

    def rus_eng_process(self, rus_txt, eng_txt, book):
        results = [self.rus_process(rus_txt, book, RU),
                   self.eng_process(eng_txt, book, EN)]
        for result in results:
            if result["raise"]:
                raise result["exception"]
        return results[0]["sync"], results[1]["sync"]

    def process(self):
        files_txt = {}
        try:
            for book, lang in self.folder_of_books:
                self.cprint(f"Selected book '{lang}/{book}'")
                files_txt[f"{lang}/{book}"] = self.check_process(book, lang)
                if self.valid_process(
                        book, lang,
                        output=f"{self.data}/{lang}/{book}/{RESULT_VALID}",
                        check=True):
                    continue
                self.audio_process(book, lang)
                self.recognize_process(book, lang)
                self.valid_process(
                    book, lang,
                    output=f"{self.data}/{lang}/{book}/{RESULT_VALID}")
                Clock.schedule_once(self.controller.panel.check_valid, 0)
            self.sync_process(files_txt)
            # self.copy_process()
            # self.list_process()
        except Exception as e:
            self.cprint(
                type(e).__name__ + ": " +
                e.__str__() + "\n" + traceback.format_exc())
        self.cprint("Process create sync books is complete")
        Clock.schedule_once(self.controller.menu.unblock, 0)

    def sync_process(self, files_txt):
        do = []
        for book1, lang1 in self.folder_rus:
            for book2, lang2 in self.folder_eng:
                if not files_txt.__contains__(f"{lang1}/{book1}"):
                    continue
                if not files_txt.__contains__(f"{lang2}/{book2}"):
                    continue
                if (book1 != book2) or (book1 in do):
                    continue
                if self.valid_process(
                        book1, "sync",
                        output=f"{self.data}/sync/{book1}/{RESULT_VALID}",
                        check=True):
                    continue
                if not os.path.exists(f"{self.data}/sync/{book1}"):
                    os.mkdir(f"{self.data}/sync/{book1}")
                self.cprint(f"Selected sync book 'sync/{book1}'")
                sync2, sync1 = self.rus_eng_process(
                    rus_txt=files_txt[f"{lang1}/{book1}"],
                    eng_txt=files_txt[f"{lang2}/{book2}"], book=book1
                )
                sync_rus = sync.Sync(
                    cprint=self.cprint,
                    output=f"{self.data}/{lang1}/{book1}", language=RU
                )
                two_sync = self.two_process(sync_rus=sync_rus, book=book1)
                self.micro_process(
                    sync_rus=sync_rus,
                    two_sync=two_sync, sync1=sync1, sync2=sync2,
                    rus_txt=files_txt[f"{lang1}/{book1}"],
                    eng_txt=files_txt[f"{lang2}/{book2}"], book=book1
                )
                do.append(book1)
                self.valid_process(
                    book1, "sync",
                    output=f"{self.data}/sync/{book1}/{RESULT_VALID}")
                Clock.schedule_once(self.controller.panel.check_valid, 0)

    def two_process(self, sync_rus, book):
        if not os.path.exists(f"{self.data}/sync/{book}/{TWO_JSON}"):
            self.cprint(f"Not find file '{TWO_JSON}', creating...")
            synchronize, L_word, R_word, L_end, R_end = \
                cross.get_sim_v2(book, self.data)
            synchronize = find_max_path_v2(synchronize)
            img = Image.fromarray(np.uint8(synchronize * 255), 'L')
            img.save(f"{self.data}/sync/{book}/{TWO_PNG}")

            res_min_max = filtered_main_diag(f"{self.data}/sync/{book}/{TWO_PNG}")
            synchronize = np.asarray(np.uint8(res_min_max * 100))
            res_min_max = Image.fromarray(np.uint8(res_min_max * 255))
            res_min_max.save(f"{self.data}/sync/{book}/{TWO2_PNG}")
            two_sync = sync_rus.create_sync_v2(
                synchronize, L_word, R_word, L_end, R_end,
                len(L_word) - 1, len(R_word) - 1, append=False)
            for i in range(len(synchronize)):
                for j in range(len(synchronize[i])):
                    synchronize[i][j] = 0
            for i in two_sync:
                synchronize[i[L_a]][i[L_b]] = 255
            img = Image.fromarray(np.uint8(synchronize), 'L')
            img.save(f"{self.data}/sync/{book}/{TWO3_PNG}")

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
            img2.save(f"{self.data}/sync/{book}/{ADAPTER_PNG}")
            for i in range(len(synchronize)):
                for j in range(len(synchronize[i])):
                    img1[i][j] = int(img2.getpixel((j, i)) / 2.55)
            synchronize = np.asarray(img1)
            self.cprint(f"Recreating '{TWO_JSON}'...")
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
            img.save(f"{self.data}/sync/{book}/{ADAPTER2_PNG}")

            with open(f"{self.data}/sync/{book}/{TWO_JSON}",
                      mode="w") as fsync:
                json.dump(two_sync, fsync)
        else:
            self.cprint(f"Loading file '{TWO_JSON}'...")
            with open(f"{self.data}/sync/{book}/{TWO_JSON}",
                      mode="r") as fsync:
                two_sync = json.load(fsync)
        return two_sync

    def micro_process(self, sync_rus,
                      two_sync, sync1, sync2, rus_txt, eng_txt, book):
        micro = []
        if not os.path.exists(
                f"{self.data}/sync/{book}/{MICRO_JSON}"
        ):
            for i in two_sync:
                phraza_1 = i[2]
                phraza_2 = i[3]
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
            with open(f"{self.data}/sync/{book}/{MICRO_JSON}",
                      mode="w") as f:
                json.dump(micro, f)

        micro2 = []
        self.cprint(f"Loading file '{MICRO_JSON}'...")
        with open(f"{self.data}/sync/{book}/{MICRO_JSON}",
                  mode="r") as f:
            m = json.load(f)
        for i in range(len(m)):
            for j in range(len(m[i])):
                micro2.append(m[i][j])
        json_string = json.dumps(micro2)
        self.cprint(f"Save file '{MICRO2_JSON}'")
        with open(f"{self.data}/sync/{book}/{MICRO2_JSON}", mode="w") as f:
            f.write(json_string)

        if not os.path.exists(f"{self.data}/sync/{book}/{ENG2RUS_JSON}"):
            eng2rus = eng_to_rus(micro2, R_POS, L_POS, sync1, sync2)
            json_string = json.dumps(eng2rus)
            self.cprint(f"Save file '{ENG2RUS_JSON}'")
            with open(f"{self.data}/sync/{book}/{ENG2RUS_JSON}", mode="w") as f:
                f.write(json_string)

        if not os.path.exists(f"{self.data}/sync/{book}/{RUS2ENG_JSON}"):
            rus2eng = eng_to_rus(micro2, L_POS, R_POS, sync2, sync1)
            json_string = json.dumps(rus2eng)
            self.cprint(f"Save file '{RUS2ENG_JSON}'")
            with open(f"{self.data}/sync/{book}/{RUS2ENG_JSON}", mode="w") as f:
                f.write(json_string)

    def valid_process(self, book, lang, output, check=False):
        if check:
            valid = "False"
            if os.path.exists(output):
                with open(output, mode="r", encoding="UTF-8") as f:
                    valid = f.read()
            if valid == "True":
                self.cprint(f"Book '{lang}/{book}' is valid")
                return True
            else:
                return False
        else:
            with open(output, mode="w", encoding="UTF-8") as f:
                f.write("True")
            self.cprint(f"Book '{lang}/{book}' create complete")

    def copy_process_func(self, book, lang, scheme):
        for filename in scheme:
            src = f"{self.data}/{lang}/{book}/{filename}"
            dst = f"data/{lang}/{book}/"
            if not os.path.exists(dst):
                os.mkdir(dst)
            dst += filename
            if os.path.exists(src):
                shutil.copyfile(src, dst)

    def copy_process(self):
        self.cprint("Copy result in folder 'data'...")
        for book, lang in self.folder_rus + self.folder_eng:
            if self.valid_process(
                    book, lang,
                    output=f"{self.data}/{lang}/{book}/{RESULT_VALID}",
                    check=True):
                self.copy_process_func(book, lang, BOOK_SCHEME)

        for book, _ in self.folder_rus:
            if self.valid_process(
                    book, "sync",
                    output=f"{self.data}/sync/{book}/{RESULT_VALID}",
                    check=True):
                self.copy_process_func(book, "sync", SYNC_SCHEME)

    def list_process(self):
        output = {"key": [], "value": []}
        for lang in [RU, EN, "sync"]:
            for book, _ in self.folder_rus:
                for filename in MINI_SCHEME:
                    key = f"data/{lang}/{book}/{filename}"
                    if not os.path.exists(key):
                        continue
                    output["key"].append(key)
                    output["value"].append(utils.get_size(key))
        with open("data/list.json", mode="w", encoding="utf-8") as fd:
            json.dump(output, fd, ensure_ascii=False, indent=4)

    def share(self):
        pass

        Clock.schedule_once(self.controller.menu.unblock, 0)


if __name__ == "__main__":
    pass
