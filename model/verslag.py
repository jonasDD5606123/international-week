import sqlite3
from database_context import DatabaseContext

class Verslag:
    def __init__(self, id, status, locatie, user_id, reservering_id, beeldmateriaal, timestamp):
        self.id = id
        self.status = status
        self.locatie = locatie
        self.user_id = user_id
        self.reservering_id = reservering_id
        self.beeldmateriaal = beeldmateriaal
        self.timestamp = timestamp

    @staticmethod
    def create(status, locatie, user_id, reservering_id, beeldmateriaal, timestamp):
        conn = DatabaseContext().getDbConn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO verslagen (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp)
        )
        conn.commit()
        id = cursor.lastrowid
        return Verslag(id, status, locatie, user_id, reservering_id, beeldmateriaal, timestamp)
