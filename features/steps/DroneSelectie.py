from behave import *

from model.drone import Drone
from model.locatie import Locatie
from model.reservering import Reservering
from model.user import User
from database import (
    get_beschikbare_drones,
    get_beschikbare_locaties,
    create_reservering,
    get_reserveringen_voor_gebruiker,
    update_drone_status,
    get_available_drones_per_location
)


@given(u'Een ingelogde piloot')
def step_impl(context):
    # Create and log in a pilot user (rol=1 for pilot)
    context.pilot = User(naam="test_pilot", rol=1)
    context.pilot.create()
    context.user_id = context.pilot.id


@when(u'De piloot vraagt de lijst van beschikbare drones en startplaatsen op')
def step_impl(context):
    # Get available drones and locations
    context.available_drones = get_beschikbare_drones()
    context.available_locations = get_beschikbare_locaties()
    context.drones_per_location = get_available_drones_per_location()


@then(u'Het systeem toont een lijst van drones en startplaatsen met hun beschikbaarheid')
def step_impl(context):
    # Verify the lists are returned and contain expected data
    assert isinstance(context.available_drones, list)
    assert isinstance(context.available_locations, list)
    assert isinstance(context.drones_per_location, list)

    # Verify the structure of returned data
    for location in context.drones_per_location:
        assert 'id' in location
        assert 'naam' in location
        assert 'beschikbare_drones' in location
        assert isinstance(location['beschikbare_drones'], list)


@given(u'Een ingelogde piloot en een beschikbare drone + startplaats')
def step_impl(context):
    context.execute_steps(u'Given Een ingelogde piloot')

    context.locatie = Locatie(naam="Dronelocatie", maxDrones=113)
    context.locatie.create()

    context.drone = Drone(beschikbaarheid=1, batterijLevel=80, locatieId=context.locatie.id)
    context.drone.create()

    context.selected_drone = context.drone
    context.selected_location = context.locatie

    assert hasattr(context, 'selected_drone'), "No available drones found"
    assert hasattr(context, 'selected_location'), "No available locations found"



@when(u'De piloot selecteert een drone en startplaats en bevestigt de reservatie')
def step_impl(context):
    # Create reservation
    reservering = Reservering(
        user_id=context.user_id,
        drone_id=context.selected_drone.id,
        startplaats_id=context.selected_location.id
    )
    reservering.create()
    context.reservation_result = reservering

    # Update drone status
    update_drone_status(
        drone_id=context.selected_drone.id,
        user_id=context.user_id
    )


@then(u'Het systeem controleert beschikbaarheid en maakt een reservering aan')
def step_impl(context):
    # Verify reservation was created successfully
    assert context.reservation_result is not None

    # Check the reservation exists in database
    reservations = get_reserveringen_voor_gebruiker(context.user_id)
    assert len(reservations) > 0

    # Verify the correct drone was reserved
    found_reservation = False
    for reservation in reservations:
        if reservation['drones_id'] == context.selected_drone.id:
            found_reservation = True
            break
    assert found_reservation, "Reservation for selected drone not found"

    # Verify drone status was updated
    available_drones_after = get_beschikbare_drones()
    print(available_drones_after)
    assert not any(drone['ID'] == context.selected_drone.id
                   for drone in available_drones_after), "Drone should no longer be available"
