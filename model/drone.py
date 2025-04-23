#project/model/drone.py
from database_context import DatabaseContext

class Drone:
    def __init__(self, beschikbaarheid, batterijLevel, locatieId, id = None):
        self.id = id
        self.beschikbaarheid = beschikbaarheid
        self.batterijLevel = batterijLevel
        self.locatieId = locatieId

    def create(self):
        # Use parameterized query to avoid SQL injection
        sql = '''insert into drones (batterijlevel, isbeschikbaar, locatieId) 
                 values (?, ?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.batterijLevel, self.beschikbaarheid, self.locatieId))
        conn.commit()

    def updateBatterij(self, batterijLevel):
        sql = '''update drones set batterijLevel = ? where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (batterijLevel, self.id))
        conn.commit()

    @staticmethod
    def all():
        sql = 'SELECT * FROM drones'
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows