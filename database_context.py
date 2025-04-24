#project/model/database-context.py

import sqlite3

class DatabaseContext:
    def __init__(self, path = 'database.db'):
        self._conn = sqlite3.connect(path)

    def getDbConn(self):
        return self._conn
