import os

DB_LOCATION = os.path.realpath(os.path.join(os.path.dirname(__file__), "replaydog.db"))

UPLOAD_DIRECTORY = os.path.realpath(os.path.join(os.path.dirname(__file__), "uploads"))

DEBUG = True

try:
    from settings_local import *
except ImportError:
    pass
