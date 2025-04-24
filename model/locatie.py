from database_context import DatabaseContext
from model.drone import Drone

class Locatie:
    def __init__(self, naam=None, maxDrones=None, id=None):
        self.id = id
        self.naam = naam
        self.maxDrones = maxDrones

    def create(self):
        dc = DatabaseContext()
        conn = dc.getDbConn()
        sql = '''insert into startplaats (naam, maxDrones) values (?, ?)'''
        cursor = conn.execute(sql, (self.naam, self.maxDrones))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    @staticmethod
    def all():
        sql = '''select id, naam, maxDrones from startplaats'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        locaties = []

        for row in rows:
            locatie = Locatie(
                naam=row[1],
                maxDrones=row[2],
                id=row[0]
            )

            locaties.append(locatie)

        return locaties

    @staticmethod
    def by_id(loc_id):
        dc = DatabaseContext()
        conn = dc.getDbConn()
        sql = '''select naam, maxDrones, id from startplaats where id = ?'''
        cursor = conn.execute(sql, (loc_id,))
        row = cursor.fetchone()
        locatie = Locatie(naam=row[0], maxDrones=row[1], id=row[2])
        return locatie

    def get_drone_count(self):
        dc = DatabaseContext()
        conn = dc.getDbConn()
        sql = 'select count(*) from drones where locatieId = ?'
        cursor = conn.execute(sql, (self.id,))
        row = cursor.fetchone()
        return row[0]

    @staticmethod
    def get_available_drones_per_location():
        result = []
        locaties = Locatie.all()
        drones = Drone.all()

        # Group drones by location ID
        drones_by_loc = {}
        for d in drones:
            loc_id = d.locatieId
            if loc_id not in drones_by_loc:
                drones_by_loc[loc_id] = []
            drones_by_loc[loc_id].append(d)

        # Now process each location once
        for loc in locaties:
            all_drones = drones_by_loc.get(loc.id, [])
            available = [d for d in all_drones if d.beschikbaarheid == 1]
            reserved = [d for d in all_drones if d.beschikbaarheid == 0]

            result.append({
                "id": loc.id,
                "naam": loc.naam,
                "drones": [d.to_dict() for d in all_drones],
                "beschikbare_drones": [d.to_dict() for d in available],
                "gereserveerde_drones": [d.to_dict() for d in reserved],
                "max_drones": loc.maxDrones
            })

        return result
