import sqlite3
from model.user import User

DB_PATH = 'database.db'



def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_id(user_id):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Users WHERE ID = ?", (user_id,))
        row = cur.fetchone()
        return User(row['ID'], row['Naam'], row['Rol']) if row else None

def get_user_by_name(naam):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Users WHERE Naam = ?", (naam,))
        row = cur.fetchone()
        return User(row['ID'], row['Naam'], row['Rol']) if row else None

def get_all_drones():
    with get_connection() as conn:
        cur = conn.execute("SELECT D.*, S.naam as locatie_naam FROM Drones D JOIN Startplaats S ON D.locatieId = S.ID")
        return [dict(row) for row in cur.fetchall()]

def get_available_drones_per_location():
    with get_connection() as conn:
        result = []
        locaties = conn.execute("SELECT * FROM Startplaats").fetchall()

        for loc in locaties:
            all_drones = conn.execute("SELECT * FROM Drones WHERE locatieId = ?", (loc['ID'],)).fetchall()
            available = [d for d in all_drones if d['Isbeschikbaar'] == 1]
            result.append({
                "id": loc['ID'],
                "naam": loc['naam'],
                "drones": [dict(d) for d in all_drones],
                "beschikbare_drones": [dict(d) for d in available],
                "max_drones": loc['maxDrones']
            })
        return result

def get_beschikbare_drones():
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Drones WHERE Isbeschikbaar = 1")
        return [dict(row) for row in cur.fetchall()]

def get_beschikbare_locaties():
    locaties = get_available_drones_per_location()
    return [loc for loc in locaties if loc['beschikbare_drones']]

def create_reservering(user_id, drone_id, startplaats_id):
    with get_connection() as conn:
        conn.execute("INSERT INTO Reserveringen (startplaats_id, user_id, drones_id) VALUES (?, ?, ?)",
                     (startplaats_id, user_id, drone_id))
        conn.execute("UPDATE Drones SET Isbeschikbaar = 2 WHERE ID = ?", (drone_id,))
        conn.commit()

def create_verslag(status, locatie, user_id, reservering_id, beeldmateriaal, timestamp):
    with get_connection() as conn:
        conn.execute("INSERT INTO Verslagen (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                     (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp))
        drone_id = conn.execute("SELECT drones_id FROM Reserveringen WHERE ID = ?", (reservering_id,)).fetchone()['drones_id']
        conn.execute("UPDATE Drones SET Isbeschikbaar = 1 WHERE ID = ?", (drone_id,))
        conn.commit()

def get_reserveringen_voor_gebruiker(user_id):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Reserveringen WHERE user_id = ?", (user_id,))
        return [dict(row) for row in cur.fetchall()]
def update_drone_status(drone_id, new_status):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Drones SET Isbeschikbaar = ? WHERE ID = ?', (new_status, drone_id))
    conn.commit()
    conn.close()
