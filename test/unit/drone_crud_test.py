import pytest
from database_context import DatabaseContext
from model.drone import Drone  # adjust import if needed

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Before each test
    conn = DatabaseContext().getDbConn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM drones")  # Clear table before test
    conn.commit()
    yield
    conn.close()

def test_drone_creation_and_fetch():
    drone = Drone(beschikbaarheid=1, batterijLevel=95, locatieId=101)
    drone.create()

    all_drones = Drone.all()
    assert len(all_drones) == 1

    fetched = all_drones[0]
    assert fetched.batterijLevel == 95
    assert fetched.beschikbaarheid == 1
    assert fetched.locatieId == 101

def test_drone_update_batterij():
    drone = Drone(beschikbaarheid=1, batterijLevel=60, locatieId=102)
    drone.create()
    original_id = drone.id

    drone.updateBatterij(85)
    updated_drones = Drone.all()
    updated_drone = next(d for d in updated_drones if d.id == original_id)

    assert updated_drone.batterijLevel == 85