from database_context import DatabaseContext

class Reservatie:
    def __init__(self, startplaatsId, userId, dronesId, verslagId):
        self.id = id
        self.startplaatsId = startplaatsId
        self.userId = userId
        self.dronesId = dronesId
        self.verslagId = verslagId

    def create(self):
        sql = '''insert into reserveringen (startplaats_id, user_id, drones_id, verslag_id) values (?, ?, ?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.startplaatsId, self.userId, self.dronesId, self.verslagId))
        conn.commit()