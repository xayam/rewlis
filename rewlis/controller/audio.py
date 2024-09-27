import os

import mutagen.mp3
from mutagen.easyid3 import EasyID3
import psutil
import sox
import concurrent.futures


class AudioClass:
    def __init__(self, cprint, audio_list, output, language):
        self.CHUNK = None
        self.cprint = cprint
        self.audio_list = audio_list
        self.output = output
        self.language = language
        self.max_workers = psutil.cpu_count(logical=False)
        self.MP3 = f"{self.output}/{self.language}.mp3"
        self.WAV = None
        self.FLAC = f"{self.output}/{self.language}.flac"

    def process(self):
        if not self.audio_list:
            self.cprint("Error: mp3 files not found")
            return {
                "raise": True,
                "exception": Exception("Error: mp3 files not found")
            }
        futures = {}
        results = []
        results.append(self.create_mp3())
        results.append(self.create_chunk())
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) \
                as executor:
            futures["create_wav"] = executor.submit(self.create_wav)
            futures["create_flac"] = executor.submit(self.create_flac)
            executor.shutdown()
            for future in futures:
                results.append(futures[future].result())
        for result in results:
            if result["raise"]:
                return {
                    "raise": True,
                    "exception": result["exception"]
                }
        return {
            "raise": False,
            "exception": None
        }

    def create_mp3(self):
        if os.path.exists(self.MP3):
            self.cprint(f"File exists '{self.MP3}'...")
        else:
            cbn = sox.Combiner()
            cbn.convert(samplerate=16000, n_channels=1)
            list_input = [f"{i[2]}" for i in self.audio_list]
            self.cprint(f"Create '{self.MP3}'...")
            cbn.build(list_input, self.MP3, 'concatenate')
        return {
            "raise": False,
            "exception": None
        }

    def create_chunk(self):
        # if os.path.exists(self.MP3):
        #     self.cprint(f"File exists '{self.MP3}'...")
        # else:
        length = mutagen.mp3.MP3(self.MP3).info.length
        chunk_len = length // self.max_workers - 1
        last = length % self.max_workers
        chunk_sizes = [chunk_len] * (self.max_workers - 1) + [last]
        chunks = []
        shift = 0
        for c in chunk_sizes:
            chunks.append(shift)
            shift += c
        chunks.append(length)
        self.CHUNK = [
            f"{self.output}/chunk{self.language}" +
            f"/chunk-{str(i).rjust(3, '0')}.mp3"
            for i in range(len(chunks) - 1)]
        for i in range(len(chunks) - 1):
            if os.path.exists(self.CHUNK[i]):
                self.cprint(f"File exists '{self.CHUNK[i]}'")
                continue
            self.cprint(f"Creating '{self.CHUNK[i]}'...")
            tfm = sox.Transformer()
            tfm.trim(chunks[i], chunks[i + 1])
            tfm.compand()
            tfm.build_file(self.MP3, self.CHUNK[i])
            track = EasyID3(self.CHUNK[i])
            for key in track.keys():
                track[key] = ""
            track.save()
        return {
            "raise": False,
            "exception": None
        }

    def create_wav(self):
        self.cprint("Converting mp3 to wav...")
        cbn = sox.Transformer()
        cbn.convert(samplerate=16000, n_channels=1)
        self.WAV = [
            f"{self.output}/wav{self.language}" +
            f"/{str(i).split('/')[-1][:-4].rjust(3, '0')}.wav"
            for i in self.CHUNK]
        for i in range(len(self.CHUNK)):
            if os.path.exists(self.WAV[i]):
                self.cprint(f"File exists '{self.WAV[i]}'...")
                continue
            self.cprint(f"Creating '{self.WAV[i]}'...")
            cbn.build(self.CHUNK[i], self.WAV[i])
        return {
            "raise": False,
            "exception": None
        }

    def create_flac(self):
        if os.path.exists(self.FLAC):
            self.cprint(f"File exists '{self.FLAC}'...")
        else:
            self.cprint(f"Create '{self.FLAC}'...")
            cbn = sox.Transformer()
            cbn.convert(samplerate=16000, n_channels=1)
            cbn.build(self.MP3, self.FLAC)
        return {
            "raise": False,
            "exception": None
        }
