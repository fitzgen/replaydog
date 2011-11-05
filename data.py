import sqlite3

import settings

def connect():
    return sqlite3.connect(settings.DB_LOCATION)

def create_tables(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS person(
      id   INTEGER NOT NULL UNIQUE,
      name TEXT,
      url  TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS game(
      id      INTEGER PRIMARY KEY,
      map     TEXT,
      type    TEXT,
      date    DATETIME,
      region  TEXT,
      release TEXT,
      length  INTEGER
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS team(
      id  INTEGER PRIMARY KEY,
      won BOOLEAN,
      game_id INTEGER,

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
