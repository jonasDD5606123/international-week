from database_context import DatabaseContext

class Drone:
    def __init__(self, beschikbaarheid=None, batterijLevel=None, locatieId=None, id=None):
        self.id = id
        self.beschikbaarheid = beschikbaarheid
        self.batterijLevel = batterijLevel
        self.locatieId = locatieId

    def create(self):
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        sql = '''insert into drones (batterijlevel, isbeschikbaar, locatieId) values (?, ?, ?)'''
        cursor.execute(sql, (self.batterijLevel, self.beschikbaarheid, self.locatieId))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def update_batterij(self, batterijLevel):
        sql = '''update drones set batterijLevel = ? where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        conn.execute(sql, (batterijLevel, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def by_id(drone_id):
        sql = '''select isbeschikbaar, batterijlevel, locatieId, id from drones where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.execute(sql, (drone_id,))
        row = cursor.fetchone()
        return Drone(beschikbaarheid=row[0], batterijLevel=row[1], locatieId=row[2], id=row[3])

    @staticmethod
    def update_set_beschikbaar(drone_id):
        sql = '''update drones set isbeschikbaar = 1 where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (drone_id,  ))
        conn.commit()

    @staticmethod
    def update_set_onbeschikbaar(drone_id):
        sql = '''update drones set isbeschikbaar = 0 where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (drone_id,))
        conn.commit()

    @staticmethod
    def all():
        sql = 'select id, batterijlevel, isbeschikbaar, locatieId from drones'
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.execute(sql)
        rows = cursor.fetchall()

        drones = []
        for row in rows:
            drone = Drone(
                beschikbaarheid=row[2],
                batterijLevel=row[1],
                locatieId=row[3],
                id=row[0]
            )

            drones.append(drone)

        return drones

    def to_dict(self):
        return {
            "id": self.id,
            "beschikbaarheid": self.beschikbaarheid,
            "batterijlevel": self.batterijLevel,
            "locatieId": self.locatieId
        }