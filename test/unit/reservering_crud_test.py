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
    cursor = db_connection.execute("SELECT * FROM reserveringen WHERE id = ?", (reservering.id,))
    row = cursor.fetchone()

    # Assert that the reservering is created and data matches
    assert row is not None
    assert row[1] == reservering.user_id  # user_id
    assert row[2] == reservering.drone_id  # drone_id
    assert row[3] == reservering.startplaats_id  # startplaats_id
    assert row[4] is None  # verslag_id should be None as per the insert statement


def test_get_reserveringen_by_user(db_connection):
    # Prepare test data
    reservering1 = Reservering(user_id=1, drone_id=2, startplaats_id=3)
    reservering2 = Reservering(user_id=1, drone_id=3, startplaats_id=4)
    reservering1.create()
    reservering2.create()

    # Call the method to get the reserveringen for user_id=1
    reserveringen = Reservering.get_by_user(1)

    # Assert that we get exactly two reserveringen back for user_id=1
    assert len(reserveringen) == 2
    assert reserveringen[0].user_id == 1
    assert reserveringen[1].user_id == 1
