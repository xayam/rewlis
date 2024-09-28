import json
import os
import wave
import mutagen.mp3

import concurrent.futures
from vosk import Model, KaldiRecognizer


class Recognizer:
    def __init__(self, cprint, model_path, output, language, config):
        self.chunk = None
        self.cprint = cprint
        self.language = language
        if self.language == "rus":
            self.MAPJSON = f"{output}/{config.RUS_MAP}"
        else:
            self.MAPJSON = f"{output}/{config.ENG_MAP}"
        self.WAV = [f"{output}/wav{self.language}/{i}"
                    for i in os.listdir(f"{output}/wav{self.language}")
                    if i.endswith(".wav")]
        self.mp3_list = [f"{output}/chunk{self.language}/{i}"
                         for i in os.listdir(f"{output}/chunk{self.language}")
                         if i.endswith(".mp3")]
        self.cprint(self.WAV)
        self.MODEL_PATH = model_path
        self.create_map()

    def create_map(self):
        if os.path.exists(self.MAPJSON):
            self.cprint(f"Find file '{self.MAPJSON}'")
            return True
        self.cprint(f"Starting recognize {self.language.upper()}...")
        results = []
        futures = {}
        sizes1 = [mutagen.mp3.MP3(m).info.length
                  for m in self.mp3_list]
        shift = 0
        sizes = []
        for s in sizes1:
            sizes.append(shift)
            shift += s
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for i in range(len(self.mp3_list)):
                futures[i] = executor.submit(
                    self.recognize, self.WAV[i], sizes[i], i
                )
            executor.shutdown()
            for i in futures:
                results.append(futures[i].result())
        buffer = ""
        for result in results:
            buffer = buffer + ",\n" + ",\n".join(result)
        result = '{\n"fragments": [\n'
        result += buffer[2:]
        result += "]}"
        with open(self.MAPJSON, mode="w", encoding="UTF-8") as ff:
            ff.write(result)
        self.cprint(f"Creating file '{self.MAPJSON}'...")
        return True

    def recognize(self, wav, size, i):
        wf = wave.open(wav, "rb")
        self.cprint(f"Running recognize model {self.language.upper()}-{i}...")
        model = Model(self.MODEL_PATH)
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        result = []
        self.cprint(f"Running recognize process {self.language.upper()}-{i}...")
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                buffer = self.update_buffer(buffer=rec.Result(), size=size)
                result.append(buffer)
        result.append(
            self.update_buffer(buffer=rec.FinalResult(), size=size)
        )
        self.cprint(f"End recognize process {self.language.upper()}-{i}")
        return result

    @staticmethod
    def update_buffer(buffer, size):
        r = json.loads(buffer)
        try:
            for i in range(len(r["result"])):
                r["result"][i]["end"] += size
                r["result"][i]["start"] += size
        except KeyError:
            return buffer
        buffer = json.dumps(r).encode(errors="ignore").decode('unicode-escape')
        return buffer
