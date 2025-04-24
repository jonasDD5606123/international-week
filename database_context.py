#project/model/database-context.py

import sqlite3

class DatabaseContext:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')

    def getDbConn(self):
        return self._conn
