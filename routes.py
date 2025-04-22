from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from database import (
    get_available_drones_per_location,
    create_reservering,
    create_verslag,
    get_reserveringen_voor_gebruiker
)

routes_bp = Blueprint('routes', __name__)

# Homepagina die de beschikbare drones toont
@routes_bp.route('/')
@login_required
def index():
    # Verkrijg de locaties en drones die beschikbaar zijn per locatie
    available_locations = get_available_drones_per_location()
    return render_template('index.html', locations=available_locations)


# Reserveren van een drone
@routes_bp.route('/reserveer', methods=['GET', 'POST'])
@login_required
def reserveer():
    if request.method == 'POST':
        location_id = int(request.form['location_id'])  # De locatie die geselecteerd is
        drone_id = int(request.form['drone_id'])  # De drone die geselecteerd is
        startplaats_id = location_id  # De locatie wordt ook de startplaats

        # Maak de reservering
        create_reservering(current_user.id, drone_id, startplaats_id)

        # Redirect naar de homepagina
        return redirect(url_for('routes.index'))

    # Verkrijg de locatie en drone op basis van de URL-parameters
    location_id = request.args.get('location_id', type=int)
    drone_id = request.args.get('drone_id', type=int)

    available_locations = get_available_drones_per_location()

    # Zoek de specifieke locatie en drone
    selected_location = next((loc for loc in available_locations if loc['id'] == location_id), None)
    selected_drone = next((drone for loc in available_locations for drone in loc['drones'] if drone['id'] == drone_id), None)

    return render_template('reserveer.html', locations=available_locations, selected_location=selected_location, selected_drone=selected_drone)


# Verslag indienen
@routes_bp.route('/verslag', methods=['GET', 'POST'])
@login_required
def verslag():
    if request.method == 'POST':
        reservering_id = int(request.form['reservering_id'])
        status = request.form['status']
        locatie = request.form['locatie']
        beeldmateriaal = request.form.get('beeldmateriaal', '')

        # Maak verslag aan
        create_verslag(status, locatie, current_user.id, reservering_id, beeldmateriaal, "2023-01-01 12:00:00")
        return redirect(url_for('routes.index'))

    # Haal reserveringen op voor de huidige gebruiker
    user_reserveringen = get_reserveringen_voor_gebruiker(current_user.id)
    return render_template('verslag.html', reserveringen=user_reserveringen)
