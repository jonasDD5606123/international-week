from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from database import (
    get_beschikbare_drones,
    get_beschikbare_locaties,
    create_reservering,
    create_verslag,
    get_reserveringen_voor_gebruiker,
    get_available_drones_per_location
)
from datetime import datetime

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
@login_required
def index():
    # Verkrijg de actieve reservatie van de gebruiker (indien aanwezig)
    user_reserveringen = get_reserveringen_voor_gebruiker(current_user.id)
    actieve_reservatie = next((r for r in user_reserveringen if r['verslag_id'] is None), None)
    actieve_drone = None

    if actieve_reservatie:
        # Vind de actieve drone op basis van de reservering
        actieve_drone = next((d for d in get_beschikbare_drones() + [dr for dr in drones if not dr['isbeschikbaar']]
                              if d['id'] == actieve_reservatie['drones_id']), None)

    return render_template('index.html',
                           locations=get_available_drones_per_location(),
                           actieve_drone=actieve_drone)


@routes_bp.route('/reserveer', methods=['GET', 'POST'])
@login_required
def reserveer():
    # Controleer of de gebruiker al een actieve reservatie heeft
    user_reserveringen = get_reserveringen_voor_gebruiker(current_user.id)
    actieve_reservatie = next((r for r in user_reserveringen if r['verslag_id'] is None), None)

    if request.method == 'POST':
        if actieve_reservatie:
            # Laat weten dat je maar één actieve reservatie kunt hebben
            return "Je hebt al een actieve reservatie. Dien eerst een verslag in."

        drone_id = int(request.form['drone_id'])
        startplaats_id = int(request.form['startplaats_id'])

        # Maak een nieuwe reservatie aan
        create_reservering(current_user.id, drone_id, startplaats_id)
        return redirect(url_for('routes.index'))

    return render_template('reserveer.html',
                           drones=get_beschikbare_drones(),
                           startplaatsen=get_beschikbare_locaties(),
                           actieve_reservatie=actieve_reservatie)


@routes_bp.route('/verslag', methods=['GET', 'POST'])
@login_required
def verslag():
    if request.method == 'POST':
        reservering_id = int(request.form['reservering_id'])
        status = request.form['status']
        locatie = request.form['locatie']
        beeldmateriaal = request.form.get('beeldmateriaal', '')

        # Voeg het verslag toe met huidige tijd
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        create_verslag(status, locatie, current_user.id, reservering_id, beeldmateriaal, timestamp)
        return redirect(url_for('routes.index'))

    # Verkrijg reserveringen voor de ingelogde gebruiker
    user_reserveringen = get_reserveringen_voor_gebruiker(current_user.id)
    return render_template('verslag.html', reserveringen=user_reserveringen)


