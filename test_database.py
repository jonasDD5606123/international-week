import unittest
import sqlite3
from database import add_user, add_startplaats

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        # Setup: maak verbinding en reset de tabellen (alleen nodig voor testisolatie)
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.cursor.executescript("""
            DELETE FROM Users;
            DELETE FROM Startplaats;
        """)
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_add_user(self):
        # Act
        add_user("TestGebruiker", "piloot")

        # Assert
        self.cursor.execute("SELECT * FROM Users WHERE Naam = ?", ("TestGebruiker",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "TestGebruiker")
        self.assertEqual(result[2], "piloot")

    def test_add_startplaats(self):
        # Act
        add_startplaats("TestLocatie", 5)

        # Assert
        self.cursor.execute("SELECT * FROM Startplaats WHERE naam = ?", ("TestLocatie",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "TestLocatie")
        self.assertEqual(result[2], 5)

if __name__ == '__main__':
    unittest.main()
