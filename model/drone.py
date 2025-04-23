#project/model/drone.py
from database_context import DatabaseContext

class Drone:
    def __init__(self, beschikbaarheid, batterijLevel, id = None):
            self.id = id
            self.beschikbaarheid = beschikbaarheid
            self.batterijLevel = batterijLevel

    def create(self):
        # Use parameterized query to avoid SQL injection
        sql = '''INSERT INTO drones (batterijlevel, isbeschikbaar) 
                 VALUES (?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.batterijLevel, self.beschikbaarheid))
        conn.commit()