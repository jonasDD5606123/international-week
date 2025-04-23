import unittest
from database import create_reservering, reserveringen

class TestReserveringen(unittest.TestCase):
    def test_reservering_opslaan(self):
        reserveringen.clear()
        res = create_reservering(user_id=1, drone_id=2, startplaats_id=1)

        self.assertEqual(len(reserveringen), 1)
        self.assertEqual(res["user_id"], 1)
        self.assertEqual(res["drones_id"], 2)
        self.assertEqual(res["startplaats_id"], 1)
        self.assertIn("id", res)
