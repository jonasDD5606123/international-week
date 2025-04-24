from database_context import DatabaseContext

class Verslag:
    def __init__(self, status, locatie, user_id, reservering_id, beeldmateriaal, timestamp, beschrijving, id = None):
        self.id = id
        self.status = status
        self.locatie = locatie
        self.user_id = user_id
        self.reservering_id = reservering_id
        self.beeldmateriaal = beeldmateriaal
        self.timestamp = timestamp
        self.beschrijving = beschrijving

    def create(self):
        conn = DatabaseContext().getDbConn()
        cursor = conn.cursor()
        sql = '''insert into verslagen (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp, beschrijving) values (?, ?, ?, ?, ?, ?, ?)'''
        print(self.status, self.locatie, self.user_id, self.reservering_id, self.beeldmateriaal, self.timestamp, self.beschrijving)
        cursor.execute(
            sql, (self.status, self.locatie, self.user_id, self.reservering_id, self.beeldmateriaal, self.timestamp, self.beschrijving)
        )
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()
