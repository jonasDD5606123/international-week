import sqlite3
from database_context import DatabaseContext

class Reservering:
    def __init__(self, id, user_id, drones_id, startplaats_id, verslag_id):
        self.reservering_id = id
        self.user_id = user_id
        self.drones_id = drones_id
        self.startplaats_id = startplaats_id
        self.verslag_id = verslag_id

    @staticmethod
    def create(user_id, drone_id, startplaats_id):
        conn = DatabaseContext().getDbConn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reserveringen (user_id, drones_id, startplaats_id, verslag_id) VALUES (?, ?, ?, NULL)",
            (user_id, drone_id, startplaats_id)
        )
        conn.commit()
        id = cursor.lastrowid
        return Reservering(id, user_id, drone_id, startplaats_id, None)

    @staticmethod
    def get_by_user(user_id):
        conn = DatabaseContext().getDbConn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reserveringen WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [Reservering(*row) for row in rows]
