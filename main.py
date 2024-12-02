from rewlis.entity import *
from rewlis.app import App

APP = APP_CLIENT
TARGET_PLATFORM = TARGET_ANDROID
application = App(app={APP_NAME: APP, TARGET: TARGET_PLATFORM})

try:

    application.run()

except Exception as e:

    application.model.log.debug(
        APP + "Error: " +
        type(e).__name__ + ": " +
        e.__str__()
    )
