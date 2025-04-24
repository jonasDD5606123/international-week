from behave import *
import pytest
from unittest.mock import patch
from datetime import datetime
from model.user import User
from model.verslag import Verslag
from model.reservering import Reservering
from database import (
    create_reservering,
    create_verslag,
    get_reserveringen_voor_gebruiker,
    update_drone_status
)


@given(u'Een ingelogde piloot met een actieve reservering')
def step_impl(context):
    # Create test user (pilot)
    context.pilot = User(naam="test_pilot", rol=1)  # rol=1 for pilot
    context.pilot.create()

    # Create a test drone and reservation
    context.drone_id = 1  # Assuming drone with ID 1 exists
    context.startplaats_id = 1  # Assuming location with ID 1 exists

    # Create reservation
    create_reservering(context.pilot.id, context.drone_id, context.startplaats_id)
    context.reserveringen = get_reserveringen_voor_gebruiker(context.pilot.id)

    # Verify we have an active reservation
    assert len(context.reserveringen) > 0
    context.reservering_id = context.reserveringen[0]['ID']


@when(u'De piloot vult het verslagformulier in (met observaties en optionele afbeelding) en dient het in')
def step_impl(context):
    context.verslag_data = {
        "reservering_id": context.reservering_id,
        "status": "voltooid",
        "locatie": "Test locatie",
        "beeldmateriaal": "test_image.jpg",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Submit the report
    create_verslag(
        status=context.verslag_data["status"],
        locatie=context.verslag_data["locatie"],
        user_id=context.pilot.id,
        reservering_id=context.verslag_data["reservering_id"],
        beeldmateriaal=context.verslag_data["beeldmateriaal"],
        timestamp=context.verslag_data["timestamp"]
    )


@then(u'Het systeem koppelt het verslag aan de reservering en zet de drone terug op "beschikbaar"')
def step_impl(context):
    with patch('database.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.execute.return_value.fetchone.return_value = {
            "ID": 1,
            "drones_id": context.drone_id,
            "verslag_id": 1
        }

        reservering_data = get_reserveringen_voor_gebruiker(context.pilot.id)[0]
        assert reservering_data['verslag_id'] is not None

    # Check drone status was updated to available (1)
    with patch('database.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.execute.return_value.fetchone.return_value = {
            "ID": context.drone_id,
            "Isbeschikbaar": 1
        }

        cursor = mock_conn.return_value.cursor.return_value
        cursor.execute.assert_any_call(
            "UPDATE Drones SET Isbeschikbaar = 1 WHERE ID = ?",
            (context.drone_id,)
        )


@when(u'De piloot probeert een verslag in te dienen zonder "incidentinhoud"')
def step_impl(context):
    context.verslag_data = {
        "reservering_id": context.reservering_id,
        "status": "",  # Missing required field
        "locatie": "Test locatie",
        "beeldmateriaal": "test_image.jpg",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Try to submit invalid report
    with pytest.raises(ValueError) as excinfo:
        create_verslag(
            status=context.verslag_data["status"],
            locatie=context.verslag_data["locatie"],
            user_id=context.pilot.id,
            reservering_id=context.verslag_data["reservering_id"],
            beeldmateriaal=context.verslag_data["beeldmateriaal"],
            timestamp=context.verslag_data["timestamp"]
        )

    context.exception = excinfo.value


@then(u'Het systeem weigert het verslag en vraagt om verplichte velden in te vullen')
def step_impl(context):
    # Verify the exception was raised
    assert "status" in str(context.exception)

    # Verify no report was created
    with patch('database.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.execute.return_value.fetchone.return_value = None

        reservering_data = get_reserveringen_voor_gebruiker(context.pilot.id)[0]
        assert reservering_data['verslag_id'] is None

    # Verify drone status wasn't changed
    with patch('database.get_connection') as mock_conn:
        mock_conn.return_value.cursor.return_value.execute.return_value.fetchone.return_value = {
            "ID": context.drone_id,
            "Isbeschikbaar": 2  # Still reserved
        }

        cursor = mock_conn.return_value.cursor.return_value
        cursor.execute.assert_not_called_with(
            "UPDATE Drones SET Isbeschikbaar = 1 WHERE ID = ?",
            (context.drone_id,)
        )