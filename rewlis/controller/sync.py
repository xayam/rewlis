import json
import os
import sys
import time

import numpy as np
from PIL import Image  # , ImageDraw

from rewlis.utils import *


class Sync:
    def __init__(self, cprint, output, language):
        self.cprint = cprint
        self.output = output
        np.set_printoptions(threshold=sys.maxsize)
        self.MAPJSON = f"{self.output}/{language}.map.json"
        self.SYNCJSON = f"{self.output}/{language}.sync.json"
        self.TWOSYNC = f"{self.output}/two.json"
        mapjson = open(self.MAPJSON, mode="r", encoding="UTF-8")
        self.data = json.load(mapjson)
        mapjson.close()
        self.language = language

    def create_sync(
            self, synchronize, L_start, L_end, L_word, R_start, R_end, R_word):
        img = Image.fromarray(np.uint8(synchronize * 2.55), 'L')
        img.save(f"{self.output}/{self.language}.sync.png")
        sync = []
        L = 0
        R = 0
        L_window = 50
        R_window = int(L_window * (len(R_word) / len(L_word)))
        maxtime = {"max_time": 0, "L": L, "R": R}
        if not os.path.exists(self.SYNCJSON):
            self.cprint("Not find file self.SYNCJSON, creating...")
            while (L < len(L_word)) and (R < len(R_word)):
                # scores = process.cdist(L_chunk, R_chunk, scorer=fuzz.ratio,
                #                        dtype=np.uint8, score_cutoff=100)
                t1 = time.perf_counter()
                p = find_max_path(synchronize[L:L + L_window, R:R + R_window])
                # p = dijkstra_max_path(synchronize[L:L + L_window, R:R + R_window])
                t2 = time.perf_counter()
                # print(t2-t1)
                # break
                if t2 - t1 > maxtime["max_time"]:
                    maxtime = {"max_time": t2 - t1, "L": L, "R": R}
                a = -1
                b = -1
                for i in p:
                    a = i["a"]
                    b = i["b"]
                    sync.append([R_start[R + b],
                                 R_end[R + b],
                                 R + b,
                                 L_word[L + a],
                                 L_start[L + a],
                                 L_end[L + a],
                                 L + a])
                    # self.cprint(L_word[L + a], "|||", R_word[R + b])
                if (a == -1) or (b == -1):
                    break
                L = L + a + 1
                R = R + b + 1
                self.cprint(
                    "|||",
                    f"L={L}, R={R}, POS_START={sync[-1][POS_START]}, " +
                    f"TIME_START={sync[-1][TIME_START]}")
                self.cprint(maxtime)
                # break
            json_string = json.dumps(sync)
            with open(self.SYNCJSON, mode="w") as fsync:
                fsync.write(json_string)

        self.cprint("Find file self.SYNCJSON")
        with open(self.SYNCJSON, mode="r") as fsync:
            sync = json.load(fsync)
        self.cprint(f"len(L_word)={len(L_word)}")
        self.cprint(f"len(R_word)={len(R_word)}")
        self.cprint(f"len(sync)={len(sync)}")
        return sync


    def create_sync_v2(self, synchronize, L_word, R_word, L_end, R_end, L_len,
                       R_len, append=True, L_window=50):
        sync1 = []
        L = 0
        R = 0
        R_window = int(L_window * (len(R_word) / len(L_word)))
        maxtime = {"max_time": 0, "L": L, "R": R}
        while (L < len(L_word)) and (R < len(R_word)):
            t1 = time.perf_counter()
            # p = dijkstra_max_path(synchronize[L:L + L_window, R:R + R_window])
            p = find_max_path(synchronize[L:L + L_window, R:R + R_window])
            # p = find_max_path_v2(synchronize[L:L + L_window, R:R + R_window])
            t2 = time.perf_counter()
            if t2 - t1 > maxtime["max_time"]:
                maxtime = {"max_time": t2 - t1, "L": L, "R": R}
            a = -1
            b = -1
            for i in p:
                a = i["a"]
                b = i["b"]
                sync1.append([L_end[L + a],
                              R_end[R + b],
                              L_word[L + a],
                              R_word[R + b],
                              L + a,
                              R + b])
                # self.cprint(sync1[-1][L_POS], sync1[-1][R_POS])
                # self.cprint(sync1[-1][L_WORDS])
                # self.cprint(sync1[-1][R_WORDS])
            if (a == -1) or (b == -1):
                break
            L = L + a + 1
            R = R + b + 1
            self.cprint("::", f"L={L}, R={R}")
            self.cprint(maxtime)
        if append:
            sync1.append([L_len,
                          R_len,
                          "",
                          "",
                          L - 1,
                          R - 1])
            self.cprint("::", sync1[-1][L_POS], sync1[-1][R_POS])
            self.cprint(sync1[-1][L_WORDS])
            self.cprint(sync1[-1][R_WORDS])
        self.cprint(f"len(L_word)={len(L_word)}")
        self.cprint(f"len(R_word)={len(R_word)}")
        self.cprint(f"len(sync)={len(sync1)}")
        return sync1

    @staticmethod
    def create_sync_v3(synchronize, L_word, R_word, L_end, R_end, L_len, R_len, two):
        sync1 = []
        for i in range(L_len):
            sync1.append([L_end[i],
                          R_end[i],
                          L_word[i],
                          R_word[i],
                          i,
                          i])
        return sync1
