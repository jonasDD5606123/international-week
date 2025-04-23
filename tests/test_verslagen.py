import unittest
from database import create_verslag, verslagen, reserveringen, create_reservering

class TestVerslagen(unittest.TestCase):
    def test_verslag_opslaan(self):
        reserveringen.clear()
        verslagen.clear()

        res = create_reservering(user_id=1, drone_id=1, startplaats_id=1)

        verslag = create_verslag(
            status="Goed", locatie="TestLocatie", user_id=1,
            reservering_id=res["id"], beeldmateriaal="image.jpg",
            timestamp="2024-04-23 10:00:00"
        )

        self.assertEqual(len(verslagen), 1)
        self.assertEqual(verslag["status"], "Goed")
        self.assertEqual(verslag["locatie"], "TestLocatie")
        self.assertEqual(verslag["reservering_id"], res["id"])
        self.assertEqual(verslag["user_id"], 1)
        self.assertEqual(verslag["beeldmateriaal"], "image.jpg")
