import sqlite3

def initialize_database():
    conn = sqlite3.connect('../database.db')  # Zorg dat dit pad klopt
    cursor = conn.cursor()

    cursor.executescript("""
    PRAGMA foreign_keys = ON;

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
        FOREIGN KEY(locatieId) REFERENCES Startplaats(ID)
    );

    CREATE TABLE IF NOT EXISTS Reserveringen (
        ID INTEGER PRIMARY KEY,
        startplaats_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        drones_id INTEGER NOT NULL,
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
        FOREIGN KEY (user_id) REFERENCES Users(ID),
        FOREIGN KEY (reservering_id) REFERENCES Reserveringen(ID)
    );
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
