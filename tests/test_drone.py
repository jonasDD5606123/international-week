import unittest
from unittest.mock import MagicMock, patch
from model.drone import Drone

class TestDroneCreate(unittest.TestCase):
    @patch('model.drone.DatabaseContext')
    def test_create_drone(self, mock_db_context):
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db_context.return_value.getDbConn.return_value = mock_conn

        # Maak een drone instantie
        drone = Drone(beschikbaarheid=1, batterijLevel=90, locatieId=2)

        # Act
        drone.create()

        # Assert
        mock_cursor.execute.assert_called_once_with(
            '''insert into drones (batterijlevel, isbeschikbaar, locatieId) 
                 values (?, ?, ?)''',
            (90, 1, 2)
        )
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
