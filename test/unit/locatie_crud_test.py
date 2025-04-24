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
    assert fetched.maxDrones == 3
    assert fetched.id == locatie.id

def test_get_drone_count_returns_correct_number(db_connection):
    locatie = Locatie(naam="DroneCountLocatie", maxDrones=10)
    locatie.create()

    # Insert mock drones manually tied to this locatie
    db_connection.execute("INSERT INTO drones (locatieId, isbeschikbaar) VALUES (?, 1)", (locatie.id,))
    db_connection.execute("INSERT INTO drones (locatieId, isbeschikbaar) VALUES (?, 0)", (locatie.id,))
    db_connection.commit()

    count = locatie.get_drone_count()
    assert count == 2

def test_get_available_drones_per_location_returns_correct_info(db_connection):
    locatie = Locatie(naam="AvailableTest", maxDrones=3)
    locatie.create()

    # Insert two drones: one available, one reserved
    db_connection.execute("INSERT INTO drones (locatieId, beschikbaarheid) VALUES (?, 1)", (locatie.id,))
    db_connection.execute("INSERT INTO drones (locatieId, beschikbaarheid) VALUES (?, 0)", (locatie.id,))
    db_connection.commit()

    result = Locatie.get_available_drones_per_location()
    for loc in result:
        if loc["id"] == locatie.id:
            assert len(loc["drones"]) == 2
            assert len(loc["beschikbare_drones"]) == 1
            assert len(loc["gereserveerde_drones"]) == 1
            assert loc["naam"] == "AvailableTest"
            assert loc["max_drones"] == 3
