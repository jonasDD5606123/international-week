#project/model/drone.py
from database_context import DatabaseContext

class Drone:
    def __init__(self, beschikbaarheid, batterijLevel, id = None):
            self.id = id
            self.beschikbaarheid = beschikbaarheid
            self.batterijLevel = batterijLevel

    def create(self):
        # Use parameterized query to avoid SQL injection
        sql = '''insert into drones (batterijlevel, isbeschikbaar) 
                 values (?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.batterijLevel, self.beschikbaarheid))
        conn.commit()

    def update(self):
        sql = '''update drones where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql (self.id))
        conn.commit()

    @staticmethod
    def all(self):
        sql = 'select * from drones'
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
