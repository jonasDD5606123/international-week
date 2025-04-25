from behave import *
from datetime import datetime
from model.user import User
from model.verslag import Verslag
from model.reservering import Reservering
from database import (
    get_reserveringen_voor_gebruiker,
    get_verslagen_voor_gebruiker
)


@given(u'Een nieuwe reservering is aangemaakt')
def step_impl(context):
    # Create a pilot user
    context.pilot = User(naam="test-piloot", rol=1)
    context.pilot.create()

    # Create test reservation data
    context.drone_id = 1  # Assuming drone with ID 1 exists
    context.startplaats_id = 1  # Assuming location with ID 1 exists

    # Create the reservation
    context.reservering = Reservering(
        user_id=context.pilot.id,
        drone_id=context.drone_id,
        startplaats_id=context.startplaats_id
    )
    context.reservering.create()
    assert context.reservering is not None


@when(u'Het systeem slaat de reservering op')
def step_impl(context):
    # Verify the reservation exists in the database
    context.db_reservering = next(
        (r for r in get_reserveringen_voor_gebruiker(context.pilot.id)
         if r['drones_id'] == context.drone_id),
        None
    )
    assert context.db_reservering is not None


@then(u'De database bevat een record met piloot_id, drone_id, startplaats_id, reservatietijdstip, en status')
def step_impl(context):
    # Verify all required fields are present
    assert context.db_reservering['user_id'] == context.pilot.id
    assert context.db_reservering['drones_id'] == context.drone_id
    assert context.db_reservering['startplaats_id'] == context.startplaats_id

@given(u'Een piloot heeft een verslag ingediend')
def step_impl(context):
    # First create a reservation
    context.execute_steps(u'Given Een nieuwe reservering is aangemaakt')

    context.pilot = User(naam="test_pilot_reservatie", rol=1)
    context.pilot.create()

    # Create test report data
    context.verslag_data = {
        'status': 'voltooid',
        'locatie': 'Test locatie',
        'beeldmateriaal': 'test.jpg',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'beschrijving': "Dit is een test"
    }

@when(u'Het systeem slaat het verslag op')
def step_impl(context):
    # Create the report
    context.verslag = Verslag(
        status=context.verslag_data['status'],
        locatie=context.verslag_data['locatie'],
        user_id=context.pilot.id,
        reservering_id=context.reservering.id,
        beeldmateriaal=context.verslag_data['beeldmateriaal'],
        timestamp=context.verslag_data['timestamp'],
        beschrijving=context.verslag_data["beschrijving"]
    )
    context.verslag.create()

    # Verify creation
    assert context.verslag is not None

    verslagen = get_verslagen_voor_gebruiker(context.pilot.id)
    print("Gevonden verslagen:", verslagen)

    # Get from database
    context.db_verslag = next(
        (v for v in get_verslagen_voor_gebruiker(context.pilot.id)
         if v['reservering_id'] == context.reservering.id),
        None
    )


@then(u'De database bevat een record met verslaginhoud, timestamp, reservering_id, piloot_id, en optioneel beeldmateriaal')
def step_impl(context):
    # Verify all required fields
    assert context.db_verslag['user_id'] == context.pilot.id
    assert context.db_verslag['reservering_id'] == context.reservering.id
    assert context.db_verslag['status'] == context.verslag_data['status']
    assert context.db_verslag['locatie'] == context.verslag_data['locatie']
    assert context.db_verslag['timestamp'] is not None

    # Verify optional image
    if 'beeldmateriaal' in context.verslag_data:
        assert context.db_verslag['beeldmateriaal'] == context.verslag_data['beeldmateriaal']
    else:
        assert context.db_verslag['beeldmateriaal'] is None