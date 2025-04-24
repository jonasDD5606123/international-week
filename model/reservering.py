from database_context import DatabaseContext

class Reservering:
    def __init__(self,user_id, drone_id, startplaats_id, id=None):
        self.id = id
        self.user_id = user_id
        self.drone_id = drone_id
        self.startplaats_id = startplaats_id

    def create(self):
        conn = DatabaseContext().getDbConn()
        cursor = conn.cursor()
        sql = "INSERT INTO reserveringen (user_id, drones_id, startplaats_id) VALUES (?, ?, ?)"
        cursor.execute(
            sql ,
            (self.user_id, self.drone_id, self.startplaats_id)
        )
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = DatabaseContext().getDbConn()
        cursor = conn.execute("select user_id, drones_id, startplaats_id, id from reserveringen where user_id = ?", (user_id,))
        rows = cursor.fetchall()
        reserveringen = []
        for row in rows:
            reservering = Reservering(user_id=row[0], drone_id=row[1], startplaats_id=row[2], id=row[3])
            reserveringen.append(reservering)

        return reserveringen

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "drone_id": self.drone_id,
            "startplaats_id": self.startplaats_id,
            "verslag_id": self.verslag_id
        }