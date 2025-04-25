import pytest
from model.drone import Drone
from model.locatie import Locatie  # Assuming you have a Locatie class in the model
from database_context import DatabaseContext

@pytest.fixture(scope='module')
def test_db():
    """Fixture that provides an existing database connection."""
    # Initialize the database context (use an existing test DB)
    dc = DatabaseContext('test/test.db')
    conn = dc.getDbConn()

    # Yield the connection so that it can be used in tests
    yield conn

    # Cleanup: We won't drop tables, since we assume the database already exists.
    conn.close()


@pytest.fixture
def create_locatie(test_db):
    """Fixture to create a new Locatie for the tests."""
    locatie = Locatie(naam='test_locatie', maxDrones=30)
    locatie.create()  # Create locatie dynamically# Save the locatie in the DB
    return locatie  # Return the created Locatie


def test_by_user(test_db, create_locatie):
    """Test retrieving drones by user."""
    user_id = 1
    locatie = Locatie(naam='test_locatie', maxDrones=30);
    locatie.create()# Create locatie dynamically
    drone1 = Drone(beschikbaarheid=0, batterijLevel=75, locatieId=locatie.id)
    drone2 = Drone(beschikbaarheid=0, batterijLevel=85, locatieId=locatie.id)
    drone1.create()
    drone2.create()

    # Fetch drones by user dynamically using the method
    drones = Drone.by_user(user_id)

    # Check if the drones returned match the expected values
    assert all(drone.user_id == user_id for drone in drones)


def test_all(test_db, create_locatie):
    """Test retrieving all drones."""
    locatie = Locatie(naam='test_locatie', maxDrones=30);
    locatie.create()  # Create locatie dynamically
    drone1 = Drone(beschikbaarheid=1, batterijLevel=75, locatieId=locatie.id)
    drone2 = Drone(beschikbaarheid=1, batterijLevel=85, locatieId=locatie.id)
    drone1.create()
    drone2.create()

    # Fetch all drones dynamically
    drones = Drone.all()

    # Check if the drones are retrieved correctly
    assert all(drone.id is not None for drone in drones)


def test_all_reserved(test_db, create_locatie):
    """Test retrieving all reserved drones."""
    locatie = Locatie(naam='test_locatie', maxDrones=30);
    locatie.create()  # Create locatie dynamically
    drone1 = Drone(beschikbaarheid=0, batterijLevel=75, locatieId=locatie.id)
    drone2 = Drone(beschikbaarheid=1, batterijLevel=85, locatieId=locatie.id)
    drone1.create()
    drone2.create()

    # Fetch all reserved drones dynamically
    drones = Drone.all_reserved()

    # Verify that only reserved drones (isbeschikbaar == 0) are returned
    assert all(drone.beschikbaarheid == 0 for drone in drones)

