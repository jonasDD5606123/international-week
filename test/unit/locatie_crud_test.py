import pytest
from model.locatie import Locatie
from model.drone import Drone
from database_context import DatabaseContext

@pytest.fixture
def db_connection():
    conn = DatabaseContext().getDbConn()
    assert conn is not None
    yield conn
    conn.close()

def test_create_locatie(db_connection):
    locatie = Locatie(naam="TestLocatie", maxDrones=5)
    locatie.create()

    cursor = db_connection.execute("SELECT naam, maxDrones FROM startplaats WHERE id = ?", (locatie.id,))
    row = cursor.fetchone()

    assert row is not None
    assert row[0] == "TestLocatie"
    assert row[1] == 5

def test_locatie_by_id_returns_correct_locatie(db_connection):
    locatie = Locatie(naam="LocatieById", maxDrones=20)
    locatie.create()
    print(f"Locatie ID: {locatie.id}")

    fetched = Locatie.by_id(locatie.id)
    assert fetched.naam == "LocatieById"
    assert fetched.maxDrones == 20
    assert fetched.id == locatie.id

def test_get_drone_count_returns_correct_number(db_connection):
    locatie = Locatie(naam="DroneCountLocatie", maxDrones=10)
    count1 = locatie.get_drone_count()
    locatie.create()

    # Insert mock drones manually tied to this locatie
    db_connection.execute("INSERT INTO drones (locatieId, isbeschikbaar, batterijLevel) VALUES (?, 1, 50)", (locatie.id,))
    db_connection.execute("INSERT INTO drones (locatieId, isbeschikbaar, batterijLevel) VALUES (?, 0, 100)", (locatie.id,))
    db_connection.commit()

    count2 = locatie.get_drone_count()
    assert count1 == count2 - 2

def test_get_available_drones_per_location_returns_correct_info(db_connection):
    locatie = Locatie(naam="AvailableTest", maxDrones=3)
    locatie.create()

    # Insert two drones: one available, one reserved
    drone = Drone(beschikbaarheid=1, batterijLevel=100, locatieId=locatie.id)
    drone.create()
    drone1 = Drone(beschikbaarheid=0, batterijLevel=100, locatieId=locatie.id)
    drone1.create()
    db_connection.commit()

    result = Locatie.get_available_drones_per_location()

    print("Return value of get_available_drones_per_location: ", result[1])

    for loc in result:
        if loc["id"] == locatie.id:
            assert len(loc["drones"]) == 2
            assert len(loc["beschikbare_drones"]) == 1
            assert len(loc["gereserveerde_drones"]) == 1
            assert loc["naam"] == "AvailableTest"
            assert loc["max_drones"] == 3
