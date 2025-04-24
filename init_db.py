import sqlite3

def initialize_database():
    conn = sqlite3.connect('database.db')
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
        Naam TEXT NOT NULL,
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
        timestamp TEXT DEFAULT (datetime('now')),
        beeldmateriaal TEXT,
        beschrijving TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(ID),
        FOREIGN KEY (reservering_id) REFERENCES Reserveringen(ID)
    );
    """)

    # Voeg testdata toe
    cursor.execute("INSERT INTO Users (Naam, Rol) VALUES (?, ?)", ("Admin", "admin"))
    cursor.execute("INSERT INTO Users (Naam, Rol) VALUES (?, ?)", ("Piloot 1", "piloot"))
    cursor.execute("INSERT INTO Startplaats (naam, maxDrones) VALUES (?, ?)", ("Locatie A", 3))
    cursor.execute("INSERT INTO Startplaats (naam, maxDrones) VALUES (?, ?)", ("Locatie B", 3))
    cursor.execute(f'INSERT INTO Drones (batterijlevel, locatieId, Isbeschikbaar) VALUES ({100}, {1}, {1})')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
