import sys
from datetime import datetime
import winsound
from kivy.clock import Clock

from rewlis.entity import *


class Logger:
    model = None
    _active: bool = False
    _is_progress: bool = False

    def __init__(self):
        pass

    def progress(
            self, message: str = "", is_printable: bool = False, is_savelable: bool = True
    ) -> str:
        sys.stdout.write("\r" + f"{LOG[PINFO]} {message}")
        sys.stdout.flush()
        self._is_progress = True
        return self._log(
            LOG[PINFO], message, is_printable=is_printable, is_savelable=is_savelable
        )

    def info(
            self, message: str = "", is_printable: bool = True, is_savelable: bool = True
    ) -> str:
        return self._log(
            LOG[INFO], message, is_printable=is_printable, is_savelable=is_savelable
        )

    def warn(
            self, message: str = "", is_printable: bool = True, is_savelable: bool = True
    ) -> str:
        # winsound.Beep(5000, 500)
        return self._log(
            LOG[WARN], message, is_printable=is_printable, is_savelable=is_savelable
        )

    def error(
            self, message: str = "", is_printable: bool = True, is_savelable: bool = True
    ):
        winsound.Beep(2000, 500)
        raise Exception(
            self._log(
                LOG[ERROR],
                message,
                is_printable=is_printable,
                is_savelable=is_savelable,
            )
        )

    def debug(
            self, message: str = "", is_printable: bool = True, is_savelable: bool = True
    ) -> str:
        return self._log(
            LOG[DEBUG], message, is_printable=is_printable, is_savelable=is_savelable
        )

    def boot(
            self, message: str = "", is_printable: bool = True, is_savelable: bool = True
    ) -> str:
        return self._log(
            LOG[BOOT], message, is_printable=is_printable, is_savelable=is_savelable
        )

    def _log(
            self,
            event: str = LOG[INFO],
            message: str = "",
            is_printable: bool = True,
            is_savelable: bool = True,
    ) -> str:
        preffix = ""
        output_message = message
        message = f"{event} {message}"
        if self._is_progress:
            preffix = "\n"
        if is_printable:
            self._is_progress = False
            print(preffix + message)

        is_savelable = is_savelable and self._active
        if self.model is not None and is_savelable:
            with open(self.model.path_log, mode="a", encoding="utf-8") as log:
                current = datetime.now()
                log.write(
                    f"{event} [{current.year}-"
                    + f"{str(current.month).rjust(2, '0')}-"
                    + f"{str(current.day).rjust(2, '0')} "
                    + f"{str(current.hour).rjust(2, '0')}:"
                    + f"{str(current.minute).rjust(2, '0')}:"
                    + f"{str(current.second).rjust(2, '0')}:"
                    + f"{str(current.microsecond).rjust(6, '0')}]{output_message}\n"
                )
        return str(message)
