import json
import os
import wave
from multiprocessing.dummy import Pool
from vosk import Model, KaldiRecognizer


class RecognizerClass:
    def __init__(self, cprint, model_path, output, language, config):
        self.chunk = None
        self.cprint = cprint
        self.language = language
        if self.language == "rus":
            self.MAPJSON = f"{output}/{config.RUS_MAP}"
            self.WAV = f"{output}/{config.RUS_WAV}"
        else:
            self.MAPJSON = f"{output}/{config.ENG_MAP}"
            self.WAV = f"{output}/{config.ENG_WAV}"
        self.MODEL_PATH = model_path
        self.create_map()

    def create_map(self):
        if os.path.exists(self.MAPJSON):
            self.cprint(f"Find file '{self.MAPJSON}'")
            return True
        n = 4
        p = Pool(n)
        wf = wave.open(self.WAV, "rb")
        self.chunk = wf.getnframes() // n
        tasks = [wf.getnframes() // n] * (n - 1) + [wf.getnframes() % n]
        results = p.map(self.recognize, tasks)
        wf.close()
        self.cprint(results)
        # result = '{\n"fragments": [\n'
        # result += ",\n"
        # result += "]}"
        # with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
        #     ff.write(result)
        # self.cprint(f"Create file '{self.MAPJSON}'")
        return True

    def recognize(self, uid):
        wf = wave.open(self.WAV[uid], "rb")
        model = Model(self.MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        wf.setpos(uid * self.chunk)
        count = self.chunk // 4000
        last = self.chunk % 4000
        result = []
        while True:
            if count == 1:
                data = wf.readframes(last)
            else:
                data = wf.readframes(4000)
            if (len(data) == 0) or (count == 0):
                break
            count -= 1
            if rec.AcceptWaveform(data):
                buffer = rec.Result()
                result.append(buffer)
                self.cprint(buffer)
        result.append(rec.FinalResult())
        return result
