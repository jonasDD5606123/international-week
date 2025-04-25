import pytest
import random
import string
from database_context import DatabaseContext
from model.reservering import Reservering
from model.drone import Drone
from model.locatie import Locatie
from model.user import User  # Assuming you have a `User` model for users

# Fixture to setup the database connection for tests
@pytest.fixture
def test_db():
    """Fixture to setup and teardown the database connection."""
    dc = DatabaseContext('test/test.db')
    conn = dc.getDbConn()
    yield conn  # Yield the connection to the test
    conn.close()  # Ensure connection is closed after tests.

@pytest.fixture
def test_data(test_db):
    """Fixture to create necessary test data for the tests."""
    # Generate a unique user name (e.g., using a random string)
    unique_user_name = f"TestUser_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"

    # Create a user for testing with a unique name
    user = User(naam=unique_user_name, rol="user")
    user.create()  # Insert the user into the database

    # Create a locatie for testing
    locatie = Locatie(naam="Test Locatie", maxDrones=5)
    locatie.create()  # Insert the location into the database

    # Create a drone for testing and associate it with the user and location
    drone = Drone(beschikbaarheid=1, batterijLevel=100, locatieId=locatie.id, user_id=user.id)
    drone.create()  # Insert the drone into the database

    return user, drone, locatie  # Return all created objects for use in the tests

def test_create_reservering(test_db, test_data):
    """Test creating a new reservation."""
    user, drone, locatie = test_data

    # Now create the reservation (Reservering)
    reservering = Reservering(user_id=user.id, drone_id=drone.id, startplaats_id=locatie.id)
    reservering.create()  # Insert the reservation into the database

    assert reservering.id is not None  # Ensure the reservation has been created and ID is assigned

    # Verify the reservation was correctly inserted into the database
    fetched_reservering = Reservering.by_id(reservering.id)
    assert fetched_reservering.id == reservering.id
    assert fetched_reservering.user_id == user.id
    assert fetched_reservering.drone_id == drone.id
    assert fetched_reservering.startplaats_id == locatie.id

def test_reservering_by_id(test_db, test_data):
    """Test retrieving a reservation by its ID."""
    user, drone, locatie = test_data

    # Create and retrieve a reservation
    reservering = Reservering(user_id=user.id, drone_id=drone.id, startplaats_id=locatie.id)
    reservering.create()

    # Fetch the reservation by ID
    fetched_reservering = Reservering.by_id(reservering.id)
    assert fetched_reservering.id == reservering.id  # Ensure the fetched reservation matches the created one
    assert fetched_reservering.user_id == user.id
    assert fetched_reservering.drone_id == drone.id
    assert fetched_reservering.startplaats_id == locatie.id

def test_get_reserveringen_by_user(test_db, test_data):
    """Test retrieving all reservations for a specific user."""
    user, drone, locatie = test_data

    # Create multiple reservations for the user
    reservering1 = Reservering(user_id=user.id, drone_id=drone.id, startplaats_id=locatie.id)
    reservering1.create()

    # Create another reservation with a different drone
    drone2 = Drone(beschikbaarheid=1, batterijLevel=90, locatieId=locatie.id, user_id=user.id)
    drone2.create()
    reservering2 = Reservering(user_id=user.id, drone_id=drone2.id, startplaats_id=locatie.id)
    reservering2.create()

    # Retrieve the reservations by the user
    reserveringen = Reservering.get_by_user(user.id)
    assert len(reserveringen) >= 2  # Ensure at least 2 reservations were created for the user
    assert any(r.id == reservering1.id for r in reserveringen)
    assert any(r.id == reservering2.id for r in reserveringen)

def test_update_reservering_status(test_db, test_data):
    """Test updating the status of a reservation."""
    user, drone, locatie = test_data

    # Create a reservation
    reservering = Reservering(user_id=user.id, drone_id=drone.id, startplaats_id=locatie.id)
    reservering.create()

    # Update the reservation status (assuming '1' means "completed")
    Reservering.update_status(status=1, res_id=reservering.id)

    # Fetch the reservation and check if the status was updated
    updated_reservering = Reservering.by_id(reservering.id)
    assert updated_reservering.id == reservering.id
    assert updated_reservering.is_afgerond == 1  # Assuming 1 means "completed"
