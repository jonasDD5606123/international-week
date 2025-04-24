from database_context import DatabaseContext

class Verslag:
    def __init__(self, status, locatie, user_id, reservering_id, beeldmateriaal, timestamp, beschrijving, user_naam=None, id=None):
        self.id = id
        self.status = status
        self.locatie = locatie
        self.user_id = user_id
        self.reservering_id = reservering_id
        self.beeldmateriaal = beeldmateriaal
        self.timestamp = timestamp
        self.beschrijving = beschrijving
        self.user_naam = user_naam  # Naam van de gebruiker

    def create(self):
        conn = DatabaseContext().getDbConn()
        cursor = conn.cursor()
        sql = '''insert into verslagen (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp, beschrijving) values (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(
            sql, (self.status, self.locatie, self.user_id, self.reservering_id, self.beeldmateriaal, self.timestamp, self.beschrijving)
        )
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @staticmethod
    def all():
        # Haal alle verslagen op, inclusief de naam van de gebruiker via een JOIN met de users tabel
        sql = '''
            SELECT v.id, v.status, v.locatie, v.user_id, v.reservering_id, v.beeldmateriaal, v.timestamp, v.beschrijving, u.naam
            FROM verslagen v
            JOIN users u ON v.user_id = u.id
        '''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        verslagen = []
        for row in rows:
            verslag = Verslag(
                status=row[1],
                locatie=row[2],
                user_id=row[3],
                reservering_id=row[4],
                beeldmateriaal=row[5],
                timestamp=row[6],
                beschrijving=row[7],
                user_naam=row[8],  # De naam van de gebruiker
                id=row[0]
            )
            verslagen.append(verslag)

        return verslagen