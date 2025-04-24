from database_context import DatabaseContext

class Drone:
    def __init__(self, beschikbaarheid=None, batterijLevel=None, locatieId=None,user_id=None, id=None):
        self.id = id
        self.beschikbaarheid = beschikbaarheid
        self.batterijLevel = batterijLevel
        self.locatieId = locatieId
        self.user_id = user_id

    def create(self):
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        sql = '''insert into drones (batterijlevel, isbeschikbaar, locatieId, user_id) values (?, ?, ?, ?)'''
        cursor.execute(sql, (self.batterijLevel, self.beschikbaarheid, self.locatieId, self.user_id))
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
    def update_user_id(drone_id, user_id):
        sql = '''update drones set user_id = ? where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        conn.execute(sql, (user_id, drone_id))
        conn.commit()
        conn.close()

    @staticmethod
    def by_user(user_id):
        sql = '''select isbeschikbaar, batterijlevel, locatieId, user_id, id from drones where user_id = ? and isbeschikbaar == 0'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.execute(sql, (user_id,))
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        drones = []

        for row in rows:
            drone = Drone(
                beschikbaarheid=row[0],
                batterijLevel=row[1],
                locatieId=row[2],
                user_id=row[3],
                id=row[4]
            )

            drones.append(drone)

        return drones

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