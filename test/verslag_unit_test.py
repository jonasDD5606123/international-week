import pytest
import random
import string
from database_context import DatabaseContext
from model.verslag import Verslag
from model.reservering import Reservering
from model.drone import Drone
from model.locatie import Locatie
from model.user import User  # Assuming a User model exists

# Fixture to setup the database connection for tests
@pytest.fixture
def test_db():
    """Fixture to setup and teardown the database connection."""
    dc = DatabaseContext('test/test.db')
    conn = dc.getDbConn()
    yield conn  # Yield the connection to the test
    conn.close()  # Ensure connection is closed after tests.

# Fixture to create necessary test data with a unique user name for each test
@pytest.fixture
def test_data(test_db):
    """Fixture to create necessary test data with a unique user name for testing."""
    # Generate a unique user name for each test run
    unique_user_name = f"TestUser_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"
    user = User(naam=unique_user_name, rol="user")
    user.create()  # Insert the user into the database

    # Create a locatie (location) for testing
    locatie = Locatie(naam="Test Locatie", maxDrones=5)
    locatie.create()  # Insert the location into the database

    # Create a drone for testing and associate it with the user and location
    drone = Drone(beschikbaarheid=1, batterijLevel=100, locatieId=locatie.id, user_id=user.id)
    drone.create()  # Insert the drone into the database

    # Create a reservering (reservation) for testing
    reservering = Reservering(user_id=user.id, drone_id=drone.id, startplaats_id=locatie.id)
    reservering.create()  # Insert the reservation into the database

    return user, drone, locatie, reservering  # Return all created objects for use in the tests

def test_create_verslag(test_db, test_data):
    """Test creating a new verslag (report)."""
    user, drone, locatie, reservering = test_data

    # Create a verslag (report) linked to the reservering, user, and locatie
    verslag = Verslag(status="completed", locatie=locatie.naam, user_id=user.id, reservering_id=reservering.id,
                      beeldmateriaal="path/to/image.jpg", beschrijving="Test verslag")
    verslag.create()  # Insert the verslag into the database

    assert verslag.id is not None  # Ensure the verslag has been created and ID is assigned

    # Verify the verslag was correctly inserted into the database
    fetched_verslag = Verslag.by_id(verslag.id)
    assert fetched_verslag.id == verslag.id
    assert fetched_verslag.status == verslag.status
    assert fetched_verslag.locatie == verslag.locatie
    assert fetched_verslag.user_id == user.id
    assert fetched_verslag.reservering_id == reservering.id
    assert fetched_verslag.beeldmateriaal == verslag.beeldmateriaal
    assert fetched_verslag.beschrijving == verslag.beschrijving

def test_verslagen_all(test_db, test_data):
    """Test retrieving all verslagen (reports)."""
    user, drone, locatie, reservering = test_data

    # Create multiple verslagen (reports)
    verslag1 = Verslag(status="completed", locatie=locatie.naam, user_id=user.id, reservering_id=reservering.id,
                       beeldmateriaal="path/to/image1.jpg", beschrijving="Test verslag 1")
    verslag1.create()

    verslag2 = Verslag(status="pending", locatie=locatie.naam, user_id=user.id, reservering_id=reservering.id,
                       beeldmateriaal="path/to/image2.jpg", beschrijving="Test verslag 2")
    verslag2.create()

    # Retrieve all verslagen (reports)
    verslagen = Verslag.all()
    assert len(verslagen) >= 2  # Ensure at least 2 verslagen were created
    assert any(v.id == verslag1.id for v in verslagen)
    assert any(v.id == verslag2.id for v in verslagen)

def test_verslag_by_id(test_db, test_data):
    """Test retrieving a verslag by its ID."""
    user, drone, locatie, reservering = test_data

    # Create a verslag
    verslag = Verslag(status="completed", locatie=locatie.naam, user_id=user.id, reservering_id=reservering.id,
                      beeldmateriaal="path/to/image.jpg", beschrijving="Test verslag")
    verslag.create()

    # Fetch the verslag by ID
    fetched_verslag = Verslag.by_id(verslag.id)
    assert fetched_verslag.id == verslag.id  # Ensure the fetched verslag matches the created one
    assert fetched_verslag.status == verslag.status
    assert fetched_verslag.locatie == verslag.locatie
    assert fetched_verslag.user_id == user.id
    assert fetched_verslag.reservering_id == reservering.id
    assert fetched_verslag.beeldmateriaal == verslag.beeldmateriaal
    assert fetched_verslag.beschrijving == verslag.beschrijving

def test_verslag_with_user_name(test_db, test_data):
    """Test retrieving verslagen with the user name."""
    user, drone, locatie, reservering = test_data

    # Create a verslag
    verslag = Verslag(status="completed", locatie=locatie.naam, user_id=user.id, reservering_id=reservering.id,
                      beeldmateriaal="path/to/image.jpg", beschrijving="Test verslag")
    verslag.create()

    # Retrieve the verslag with user name
    fetched_verslag = Verslag.by_id(verslag.id)
    assert fetched_verslag.user_naam == user.naam  # Ensure the user's name is included in the verslag
