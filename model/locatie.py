from database_context import DatabaseContext

class Locatie:
    def __init__(self, naam, maxDrones, id=None):
        self.naam = naam
        self.maxDrones = maxDrones

    def create(self):
        sql = '''insert into startplaats (naam, maxDrones) 
                         values (?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.naam, self.maxDrones))
        conn.commit()

    @staticmethod
    def all():
        sql = '''select * from startplaats'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows