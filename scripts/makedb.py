#!/usr/bin/env python
import os
import sys

# XXX: hacky-hack
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                 "..")))

import settings
import data

if os.path.isfile(settings.DB_LOCATION):
    print("Database exists at %s" % settings.DB_LOCATION)
else:
    print("Creating database at %s" % settings.DB_LOCATION)
    conn = data.connect()
    data.create_tables(conn)
