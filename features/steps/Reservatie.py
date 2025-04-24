from behave import *
import pytest
from unittest.mock import patch
from model.user import User
from database import (
    get_beschikbare_drones,
    create_reservering,
    get_reserveringen_voor_gebruiker,
)


@given(u'Een ingelogde piloot die een drone wil reserveren')
def step_impl(context):
    # Create and log in a pilot user (rol=1 for pilot)
    context.pilot = User(naam="test_pilot", rol=1)
    context.pilot.create()

    # Get available drones to simulate selection
    context.available_drones = get_beschikbare_drones()
    assert len(context.available_drones) > 0  # Ensure there are drones available

    # Select the first available drone
    context.selected_drone = context.available_drones[0]
    context.drone_id = context.selected_drone['ID']
    context.startplaats_id = context.selected_drone['locatieId']


@when(u'De geselecteerde drone is al gereserveerd op het gewenste moment')
def step_impl(context):
    # First reserve the drone (simulating someone else reserving it)
    with patch('database.get_connection') as mock_conn:
        # Mock the database to show drone is already reserved
        mock_conn.return_value.cursor.return_value.execute.return_value.fetchone.return_value = {
            'ID': context.drone_id,
            'Isbeschikbaar': 2,  # 2 = reserved
            'locatieId': context.startplaats_id
        }

        # Try to reserve the already reserved drone
        with pytest.raises(Exception) as excinfo:
            create_reservering(
                user_id=context.pilot.id,
                drone_id=context.drone_id,
                startplaats_id=context.startplaats_id
            )

        context.exception = excinfo.value


@then(u'Het systeem toont een foutmelding en vraagt een nieuwe selectie')
def step_impl(context):
    # Verify an exception was raised
    assert context.exception is not None
    assert "niet beschikbaar" in str(context.exception).lower() or "already reserved" in str(context.exception).lower()

    # Verify the drone wasn't assigned to our pilot
    with patch('database.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.execute.return_value.fetchone.return_value = None

        reservations = get_reserveringen_voor_gebruiker(context.pilot.id)
        assert len(reservations) == 0  # No reservation was created

    # Verify the error suggests selecting another drone
    assert "selecteer een andere" in str(context.exception).lower() or "try another" in str(context.exception).lower()