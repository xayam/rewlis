import json
import os
import wave
from multiprocessing.dummy import Pool
from vosk import Model, KaldiRecognizer


class RecognizerClass:
    def __init__(self, cprint, model_path, output, language, config):
        self.cprint = cprint
        self.language = language
        if self.language == "rus":
            self.MAPJSON = f"{output}/{config.RUS_MAP}"
            self.WAV = f"{output}/{config.RUS_WAV}"
        else:
            self.MAPJSON = f"{output}/{config.ENG_MAP}"
            self.WAV = f"{output}/{config.ENG_WAV}"
        self.MODEL_PATH = model_path
        # self.create_map()

    def create_map(self):
        if os.path.exists(self.MAPJSON):
            self.cprint(f"Find file '{self.MAPJSON}'")
            return True
        n = 4
        p = Pool(n)
        wf = wave.open(self.WAV, "rb")
        tasks = [wf.getnframes() // n] * (n - 1) + [wf.getnframes() % n]
        results = p.map(self.recognize, tasks)


        model = Model(self.MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        ss = '{\n"fragments": [\n'
        while True:
            dat = wf.readframes(4000)
            if len(dat) == 0:
                break
            if rec.AcceptWaveform(dat):
                sss = rec.Result()
                ss += sss + ",\n"
                self.cprint(sss)
        ss += rec.FinalResult() + "]}"
        with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
            ff.write(ss)
        self.cprint(f"Create file '{self.MAPJSON}'")
        return True

    def recognize(self, line):
        uid, fn = line.split()
        wf = wave.open(fn, "rb")
        model = Model(self.MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())

        text = ""
        while True:
            data = wf.readframes(1000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                jres = json.loads(rec.Result())
                text = text + " " + jres["text"]
        jres = json.loads(rec.FinalResult())
        text = text + " " + jres["text"]
        return uid + text
