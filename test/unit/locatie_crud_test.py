import pytest
from model.locatie import Locatie
from model.drone import Drone
from database_context import DatabaseContext

@pytest.fixture()
def db_connection():
    conn = DatabaseContext(path='test/test.db').getDbConn()
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def cleanup(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM drones")  # Cleanup drones
    cursor.execute("DELETE FROM startplaats")  # Cleanup locaties
    db_connection.commit()

def test_create_locatie(db_connection):
    locatie = Locatie(naam="TestLocatie", maxDrones=5)
    locatie.create()

    cursor = db_connection.cursor()
    cursor.execute("SELECT naam, maxDrones FROM startplaats WHERE id = ?", (locatie.id,))
    row = cursor.fetchone()

    assert row is not None
    assert row[0] == "TestLocatie"
    assert row[1] == 5

def test_locatie_by_id_returns_correct_locatie(db_connection):
    locatie = Locatie(naam="LocatieById", maxDrones=20)
    locatie.create()

    fetched = Locatie.by_id(locatie.id)
    assert fetched is not None
    assert fetched.naam == "LocatieById"
    assert fetched.maxDrones == 20
    assert fetched.id == locatie.id

def test_get_drone_count_returns_correct_number(db_connection):
    locatie = Locatie(naam="DroneCountLocatie", maxDrones=10)
    locatie.create()

    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO drones (locatieId, isbeschikbaar, batterijLevel) VALUES (?, 1, 50)", (locatie.id,))
    cursor.execute("INSERT INTO drones (locatieId, isbeschikbaar, batterijLevel) VALUES (?, 0, 100)", (locatie.id,))
    db_connection.commit()

    count = locatie.get_drone_count()
    assert count == 2

def test_get_available_drones_per_location_returns_correct_info(db_connection):
    locatie = Locatie(naam="AvailableTest", maxDrones=3)
    locatie.create()

    drone = Drone(beschikbaarheid=1, batterijLevel=100, locatieId=locatie.id)
    drone.create()
    drone1 = Drone(beschikbaarheid=0, batterijLevel=100, locatieId=locatie.id)
    drone1.create()
    db_connection.commit()

    result = Locatie.get_available_drones_per_location()

    match = next((loc for loc in result if loc["id"] == locatie.id), None)
    assert match is not None
    assert len(match["drones"]) == 2
    assert len(match["beschikbare_drones"]) == 1
    assert len(match["gereserveerde_drones"]) == 1
    assert match["naam"] == "AvailableTest"
    assert match["max_drones"] == 3
