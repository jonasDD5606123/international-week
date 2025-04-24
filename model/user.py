from flask_login import UserMixin
from database_context import DatabaseContext

class User(UserMixin):
    def __init__(self, naam, rol, id = None):
        self.id = id
        self.naam = naam
        self.rol = rol

    def create(self):
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
            user = User(id=row[0], naam=row[1], rol=row[2])
            users.append(user)

        return users

    @staticmethod
    def by_id(user_id):
        dc = DatabaseContext()
        conn = dc.getDbConn()
        sql = '''select naam, rol, id from users where id = ?'''
        cursor = conn.execute(sql, (user_id,))
        row = cursor.fetchone()
        if row:
            return User(naam=row[0], rol=row[1], id=row[2])
        return None

    @staticmethod
    def by_name(user_name):
        dc = DatabaseContext()
        conn = dc.getDbConn()
        sql = '''select naam, rol, id from users where naam = ?'''
        cursor = conn.execute(sql, (user_name,))
        row = cursor.fetchone()
        if row:
            return User(naam=row[0], rol=row[1], id=row[2])
        return None