import pytest
from database_context import DatabaseContext
from model.reservering import Reservering

@pytest.fixture
def db_connection():
    conn = DatabaseContext().getDbConn()
    assert conn is not None
    yield conn
    conn.close()


def test_create_reservering(db_connection):
    # Prepare test data
    reservering = Reservering(user_id=1, drone_id=2, startplaats_id=3)

    # Create a new reservering
    reservering.create()

    # Fetch the created reservering directly from the database
    reservering1 = Reservering.by_id(reservering.id)

    # Assert that the reservering is created and data matches
    assert reservering1 is not None
    assert reservering1.user_id == reservering.user_id  # user_id
    assert reservering1.drone_id == reservering.drone_id  # drone_id
    assert reservering1.startplaats_id == reservering.startplaats_id  # startplaats_id
    assert reservering1.id == reservering.id


def test_get_reserveringen_by_user(db_connection):
    # Prepare test data
    reserveringen_before = Reservering.get_by_user(1)
    reservering1 = Reservering(user_id=1, drone_id=2, startplaats_id=3)
    reservering2 = Reservering(user_id=1, drone_id=3, startplaats_id=4)
    reservering1.create()
    reservering2.create()

    # Call the method to get the reserveringen for user_id=1
    reserveringen = Reservering.get_by_user(1)

    # Assert that we get exactly two reserveringen back for user_id=1
    assert len(reserveringen) == (len(reserveringen_before) + 2)
    assert reserveringen[0].user_id == 1
    assert reserveringen[1].user_id == 1