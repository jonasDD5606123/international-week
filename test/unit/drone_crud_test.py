import pytest
from database_context import DatabaseContext
from model.drone import Drone  # adjust import if needed
from model.locatie import Locatie

@pytest.fixture(autouse=True)
def db_connection():
    # Before each test
    conn = DatabaseContext(path='test/test.db').getDbConn()
    conn.commit()
    yield
    conn.close()

def test_drone_creation_and_fetch():
    loc = Locatie('Test-Locatie-1', maxDrones=20)
    loc.create()

    drone = Drone(beschikbaarheid=1, batterijLevel=95, locatieId=101)
    #create drone
    drone.create()

    created_drone = Drone.by_id(drone.id)

    assert created_drone.batterijLevel == 95
    assert created_drone.beschikbaarheid == 1
    assert created_drone.locatieId == 101

def test_drone_update_batterij():
    drone = Drone(beschikbaarheid=1, batterijLevel=60, locatieId=102)
    drone.create()
    original_id = drone.id

    drone.update_batterij(85)
    updated_drones = Drone.all()
    updated_drone = next(d for d in updated_drones if d.id == original_id)

    assert updated_drone.batterijLevel == 85