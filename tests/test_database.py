from database import reserveringen, verslagen, create_reservering, create_verslag

def setup_function():
    reserveringen.clear()
    verslagen.clear()

def test_reservatie_wordt_opgeslagen():
    res = create_reservering(user_id=1, drone_id=2, startplaats_id=1)

    assert len(reserveringen) == 1
    assert res.user_id == 1
    assert res.drones_id == 2
    assert res.startplaats_id == 1

def test_verslag_wordt_opgeslagen():
    reservering = create_reservering(1, 2, 1)
    verslag = create_verslag("ok", "Locatie A", 1, reservering.reservering_id, "beeld.jpg", "2024-01-01T12:00")

    assert len(verslagen) == 1
    assert verslag.status == "ok"
    assert verslag.user_id == 1
    assert verslag.reservering_id == reservering.reservering_id
