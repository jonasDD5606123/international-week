from database_context import DatabaseContext


class User():
    def __init__(self, naam, rol, id=None):
        self.id = id
        self.naam = naam
        self.rol = rol

    @staticmethod
    def login(naam):
        sql = 'SELECT * FROM Users WHERE Naam = ?'
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (naam,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return True
        return False

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
