#project/model/database-context.py

import sqlite3
from config import Config

class DatabaseContext:
    def __init__(self):
        self._conn = sqlite3.connect(Config.DATABASE_PATH)

    def getDbConn(self):
        return self._conn