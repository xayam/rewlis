import traceback

from rewlis.entity import *
from rewlis.app import App

APP = APP_SERVER
TARGET_PLATFORM = TARGET_WINDOWS
application = App(app={APP_NAME: APP, TARGET: TARGET_PLATFORM})

try:

    application.run()

except Exception as e:

    application.model.log.debug(
        APP + "Error: " +
        type(e).__name__ + ": " +
        e.__str__() + "\n" + traceback.format_exc()
    )
