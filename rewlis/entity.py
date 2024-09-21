
APP_NAME = "APP_NAME"
APP_CREATOR = "REWLIS-CREATOR"
APP_CLIENT = "REWLIS-CLIENT"
APP_SERVER = "REWLIS-SERVER"
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
EN = "English"
RU = "Русский"

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

# Scheme micro.json
L_POS = 0
R_POS = 1
L_WORDS = 2
R_WORDS = 3
L_a = 4
L_b = 5

# Scheme BOOK_ENG_SCHEME / BOOK_RUS_SCHEME
ANNOT = 0
TXT = 1
FB2 = 2
MP3 = 3
SYNC = 4

# Scheme BOOK_SCHEME
COVER = 0
MICRO = 1
ENG2RUS = 2
RUS2ENG = 3
VALID = 4

barrier = 0.0
