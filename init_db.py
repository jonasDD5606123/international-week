import sqlite3
from database_context import DatabaseContext

def initialize_database(dc):
    conn = dc.getDbConn()
    cursor = conn.cursor()

    # Zet foreign key enforcement aan
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Verwijder bestaande tabellen
    cursor.executescript("""
    DROP TABLE IF EXISTS Verslagen;
    DROP TABLE IF EXISTS Reserveringen;
    DROP TABLE IF EXISTS Drones;
    DROP TABLE IF EXISTS Startplaats;
    DROP TABLE IF EXISTS Users;
    """)

    # Maak tabellen opnieuw aan
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Users (
        ID INTEGER PRIMARY KEY,
        naam TEXT NOT NULL UNIQUE,
        Rol TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Startplaats (
        ID INTEGER PRIMARY KEY,
        naam TEXT NOT NULL,
        maxDrones INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Drones (
        ID INTEGER PRIMARY KEY,
        batterijlevel INTEGER NOT NULL,
        Isbeschikbaar INTEGER NOT NULL DEFAULT 1,
        locatieId INTEGER NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE SET NULL,
        FOREIGN KEY(locatieId) REFERENCES Startplaats(ID)
    );

    CREATE TABLE IF NOT EXISTS Reserveringen (
        ID INTEGER PRIMARY KEY,
        startplaats_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        drones_id INTEGER NOT NULL,
        is_afgerond int default 0,
        FOREIGN KEY (startplaats_id) REFERENCES Startplaats(ID),
        FOREIGN KEY (user_id) REFERENCES Users(ID),
        FOREIGN KEY (drones_id) REFERENCES Drones(ID)
    );

    CREATE TABLE IF NOT EXISTS Verslagen (
        ID INTEGER PRIMARY KEY,
        status TEXT NOT NULL,
        locatie TEXT,
        user_id INTEGER NOT NULL,
        reservering_id INTEGER NOT NULL,
        timestamp timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        beeldmateriaal TEXT,
        beschrijving TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(ID),
        FOREIGN KEY (reservering_id) REFERENCES Reserveringen(ID)
    );
    """)

    # Create trigger to check if max drones are reached before inserting a new drone
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS check_max_drones
    BEFORE INSERT ON Drones
    FOR EACH ROW
    BEGIN
        -- Check if adding the new drone will exceed maxDrones for the location
        SELECT CASE
            WHEN (SELECT COUNT(*) FROM Drones WHERE locatieId = NEW.locatieId) >= (SELECT maxDrones FROM Startplaats WHERE ID = NEW.locatieId)
            THEN RAISE (ABORT, 'Maximum number of drones reached for this location.')
        END;
    END;
    """)
    conn.commit()

# Voeg drones toe aan verschillende locaties
def add_drone(batterijlevel, locatieId, dc):
    conn = dc.getDbConn()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Drones (batterijlevel, locatieId, Isbeschikbaar) VALUES (?, ?, ?)',
                       (batterijlevel, locatieId, 1))
        conn.commit()  # Commit the changes to the database
        print(f"Drone toegevoegd op locatie {locatieId}.")
    except sqlite3.DatabaseError as e:
        print(f"Fout bij toevoegen drone: {e}")


if __name__ == '__main__':
    # First context (e.g., 'database.db')
    dc1 = DatabaseContext(path='database.db')
    conn1 = dc1.getDbConn()
    initialize_database(dc1)
    # Voeg testdata toe
    conn1.execute("INSERT INTO Users (Naam, Rol) VALUES (?, ?)", ("Admin", "admin"))
    conn1.execute("INSERT INTO Users (Naam, Rol) VALUES (?, ?)", ("Piloot 1", "user"))
    conn1.execute("INSERT INTO Users (Naam, Rol) VALUES (?, ?)", ("Piloot 2", "user"))
    conn1.execute("INSERT INTO Users (Naam, Rol) VALUES (?, ?)", ("Manager", "user"))

    conn1.execute("INSERT INTO Startplaats (naam, maxDrones) VALUES (?, ?)", ("Locatie A", 3))
    conn1.execute("INSERT INTO Startplaats (naam, maxDrones) VALUES (?, ?)", ("Locatie B", 3))
    conn1.execute("INSERT INTO Startplaats (naam, maxDrones) VALUES (?, ?)", ("Locatie C", 3))

    add_drone(100, 1, dc1)
    add_drone(100, 1, dc1)
    add_drone(80, 1, dc1)
    add_drone(90, 1, dc1)  # This will exceed the maxDrones for Locatie A
    add_drone(70, 2, dc1)
    add_drone(60, 2, dc1)
    add_drone(50, 3, dc1)

    conn1.commit()
    conn1.close()
    # Second context (e.g., 'test/test.db')
    dc2 = DatabaseContext(path='test/test.db')
    initialize_database(dc2)
    dc2.getDbConn().close()
