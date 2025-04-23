from database_context import DatabaseContext

class Verslag:
    def __init__(self, status, locatie, userId, reserveringId, timestamp, beeldmateriaal):
        self.id = id
        self.status = status
        self.locatie = locatie
        self.userId = userId
        self.reserveringId = reserveringId
        self.timestamp = timestamp
        self.beeldmateriaal = beeldmateriaal

    def create(self):
        sql = '''insert into verslagen (status, locatie, user_id, reservering_id, timestamp, beeldmateriaal) values (?, ?, ?, ?, ?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.status, self.locatie, self.userId, self.reserveringId, self.timestamp, self.beeldmateriaal))
        conn.commit()