import pytest
from database_context import DatabaseContext
from model.locatie import Locatie

# Fixture to setup the database connection for tests
@pytest.fixture
def test_db():
    """Fixture to setup and teardown the database connection."""
    dc = DatabaseContext('test/test.db')
    conn = dc.getDbConn()
    yield conn  # Yield the connection to the test
    conn.close()  # Ensure connection is closed after tests.

def test_create_locatie(test_db):
    """Test creating a new location."""
    locatie = Locatie(naam="Test Locatie", maxDrones=5)
    locatie.create()  # Insert into DB
    assert locatie.id is not None  # Ensure the location was assigned an ID.

def test_all_locaties(test_db):
    """Test retrieving all locations."""
    # First, create a few locations
    loc1 = Locatie(naam="Locatie 1", maxDrones=5)
    loc2 = Locatie(naam="Locatie 2", maxDrones=3)
    loc1.create()
    loc2.create()

    # Test retrieval
    locaties = Locatie.all()
    assert len(locaties) >= 2  # Ensure we got at least 2 locations.
    assert any(loc.naam == "Locatie 1" for loc in locaties)  # Check if the first location is there.
    assert any(loc.naam == "Locatie 2" for loc in locaties)  # Check if the second location is there.

def test_locatie_by_id(test_db):
    """Test retrieving a location by ID."""
    locatie = Locatie(naam="Test Locatie", maxDrones=5)
    locatie.create()  # Insert location
    fetched_locatie = Locatie.by_id(locatie.id)
    assert fetched_locatie is not None
    assert fetched_locatie.id == locatie.id
    assert fetched_locatie.naam == "Test Locatie"

def test_get_drone_count(test_db):
    """Test getting the number of drones for a location."""
    locatie = Locatie(naam="Locatie for Drone Count", maxDrones=10)
    locatie.create()  # Insert location
    # Assume the `create_drone` method is already implemented elsewhere.
    drone_count = locatie.get_drone_count()
    assert drone_count == 0  # Initially, no drones assigned, so count should be 0.
