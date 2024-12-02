
APP_NAME = "APP_NAME"
APP_CREATOR = "REWLIS-CREATOR"
APP_CLIENT = "REWLIS-CLIENT"
TARGET = "TARGET"
TARGET_WINDOWS = "WINDOWS"
TARGET_ANDROID = "ANDROID"

INFO: str = "info"
PINFO: str = "pinfo"
WARN: str = "warn"
ERROR: str = "error"
DEBUG: str = "debug"
BOOT: str = "boot"

LOG: dict = {
    INFO: "[INFO ]",
    PINFO: "[PINFO]",
    WARN: "[WARN ]",
    ERROR: "[ERROR]",
    DEBUG: "[DEBUG]",
    BOOT: "[BOOT ]",
}

# Langs
EN = "eng"
RU = "rus"

# Scheme options.json
LOCALE = "locale"
FG = "fg"
BG = "bg"
SEL = "sel"
FONT = "font"
FONTSIZESCALE = "fontsizescale"
SPEED = "speed"
POSITIONS = "positions"
POSI = "posi"
AUDIO = "audio"
CHUNK = "chunk"

# Scheme sync.json
TIME_START = 0
TIME_END = 1
TIME = 2
WORD = 3
POS_START = 4
POS_END = 5
POS = 6

# Scheme micro.json / micro2.json
L_POS = 0
R_POS = 1
L_WORDS = 2
R_WORDS = 3
L_a = 4
L_b = 5

# Scheme BOOK_SCHEME
COVER = 0
METADATA = 1
TXT = 2
FB2 = 3
MP3 = 4
SYNC = 5
BOOK_VALID = 6

# Scheme SYNC_SCHEME
MICRO2 = 0
ENG2RUS = 1
RUS2ENG = 2
SYNC_VALID = 3

barrier = 0.0

AUDIOBOOK_FOLDER = "audiobook"
METADATA_JSON = "metadata.json"
COVER_JPG = "cover.jpg"
BOOK_FB2 = "book.fb2"
BOOK_TXT = "book.txt"
ALL_MP3 = "all.mp3"
ALL_WAV = "all.wav"
ALL_FLAC = "all.flac"
SYNC_JSON = "sync.json"
MAP_JSON = "map.json"
ORIG_HTML = "orig.html"

ALL_HTML = "all.html"

SYNC_PNG = "sync.png"


TWO_PNG = "two.png"
TWO2_PNG = "two2.png"
TWO3_PNG = "two3.png"
ADAPTER_PNG = "adapter.png"
ADAPTER2_PNG = "adapter2.png"

TWO_JSON = "two.json"

MICRO_JSON = "micro.json"
MICRO2_JSON = "micro2.json"
ENG2RUS_JSON = "eng2rus.json"
RUS2ENG_JSON = "rus2eng.json"
RESULT_VALID = "valid"

BOOK_SCHEME = [
    COVER_JPG,
    BOOK_TXT,
    BOOK_FB2,
    ALL_MP3,
    SYNC_JSON,
    RESULT_VALID
]

SYNC_SCHEME = [
    MICRO2_JSON,
    ENG2RUS_JSON,
    RUS2ENG_JSON,
    RESULT_VALID
]

MINI_SCHEME = [
    BOOK_TXT,
    SYNC_JSON,
    MICRO2_JSON,
    ENG2RUS_JSON,
    RUS2ENG_JSON,
    RESULT_VALID
]