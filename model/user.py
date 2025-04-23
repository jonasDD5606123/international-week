from flask_login import UserMixin
from database_context import DatabaseContext

class User(UserMixin):
    def __init__(self, id, naam, rol):
        self.id = id
        self.naam = naam
        self.rol = rol

    def get_id(self):
        return str(self.id)


    def create(self):
        # Parameterized query to avoid SQL injection
        sql = '''INSERT INTO users (naam, rol) 
                 VALUES (?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.naam, self.rol))
        conn.commit()
        self.id = cursor.lastrowid
        return self

    @staticmethod
    def all():
        sql = 'SELECT * FROM users'
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        users = []
        for row in rows:
            user = User(id=row[0], naam=row[1], rol=row[2], email=row[3], wachtwoord=row[4])
            users.append(user)

        return users