import os

DB_LOCATION = os.path.realpath(os.path.join(os.path.dirname(__file__), "replaydog.db"))

try:
    from settings_local import *
except ImportError:
    pass
