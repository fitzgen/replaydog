import sqlite3
import uuid
import settings
import sc2reader
import os

def connect():
    """
    Retrieve a connection to the database.
    """
    return sqlite3.connect(settings.DB_LOCATION)

def create_tables(conn):
    """
    Create the tables for the database if they do not exist already.
    """
    conn.execute("""
    CREATE TABLE IF NOT EXISTS person(
      id   INTEGER NOT NULL UNIQUE,
      name TEXT,
      url  TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS game(
      id          TEXT PRIMARY KEY,
      map         TEXT,
      type        TEXT,
      date        DATETIME,
      region      TEXT,
      release     TEXT,
      length      INTEGER
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS team(
      id      INTEGER PRIMARY KEY,
      won     BOOLEAN,
      game_id TEXT,

      FOREIGN KEY(game_id) REFERENCES game(id)
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS team_member(
      id          INTEGER PRIMARY KEY,
      race_picked TEXT,
      race_played TEXT,
      color       TEXT,
      person_id   INTEGER,
      team_id     INTEGER,

      FOREIGN KEY(person_id) REFERENCES person(id),
      FOREIGN KEY(team_id)   REFERENCES team(id)
    )
    """)

    return conn.commit()

def save_replay(conn, replay_file):
    """
    Create the various entities associated with a replay (persons, team_members,
    teams, and a game), then save the replay file to the file system. Returns
    False when the file is not valid, otherwise returns the generated replay id.
    """
    # If it isn't a *.SC2Replay file, it isn't valid.
    if replay_file.filename.rsplit(".", 1)[1] != "SC2Replay":
        return False

    # Save the file, then make sure it really is a SC2Replay.
    replay_id = uuid.uuid4().hex[:8]
    replay_path = os.path.join(settings.UPLOAD_DIRECTORY,
                               "%s.SC2Replay" % replay_id)
    fh = open(replay_path, "wb")
    replay_file.save(fh)
    fh.close()
    try:
        replay = sc2reader.read_file(replay_path)
    except sc2reader.exceptions.SC2ReaderError:
        os.remove(replay_path)
        return False

    # TODO: get or create persons, create team members, teams, and game
    return replay_id

def get_replay_details(conn, replay_id):
    # TODO
    return {
        "foo": "bar"
    }

def file_for_replay(conn, replay_id):
    # TODO: verify that the replay exists
    return "%s.SC2Replay"
