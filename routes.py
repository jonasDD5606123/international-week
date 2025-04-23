from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from model.drone import Drone
from model.user import User
from model.reservatie import Reservatie

from database import (
    get_available_drones_per_location,
    create_reservering,
    create_verslag,
    get_reserveringen_voor_gebruiker,
    update_drone_status
)

routes_bp = Blueprint('routes', __name__)

# Homepagina die de beschikbare drones toont
@routes_bp.route('/')
@login_required
def index():
    # Verkrijg de locaties en drones die beschikbaar zijn per locatie
    available_locations = get_available_drones_per_location(current_user.id)
    return render_template('index.html', locations=available_locations)

@routes_bp.route('/reserveer', methods=['GET', 'POST'])
@login_required
def reserveer():
    if request.method == 'POST':
        if not request.form.get('location_id') or not request.form.get('drone_id'):
            return redirect(url_for('routes.index'))

        try:
            location_id = int(request.form['location_id'])
            drone_id = int(request.form['drone_id'])
            startplaats_id = location_id

            # Controleer of de drone bestaat en beschikbaar is
            available_locations = get_available_drones_per_location()
            drone_exists = False

            for loc in available_locations:
                # Controleer zowel beschikbare als gereserveerde drones
                for drone in loc['drones']:
                    if int(drone['ID']) == drone_id:
                        drone_exists = True
                        break
                if drone_exists:
                    break

            if not drone_exists:
                return redirect(url_for('routes.index'))

            create_reservering(current_user.id, drone_id, startplaats_id)
            update_drone_status(drone_id, current_user.id)
            return redirect(url_for('routes.index'))
        except ValueError:
            return redirect(url_for('routes.index'))

    location_id = request.args.get('location_id', type=int)
    drone_id = request.args.get('drone_id', type=int)

    available_locations = get_available_drones_per_location()

    # Zoek de geselecteerde locatie en drone
    selected_location = None
    selected_drone = None

    if location_id and drone_id:
        for loc in available_locations:
            if loc['id'] == location_id:
                selected_location = loc
                # Zoek in alle drones, niet alleen beschikbare
                for drone in loc['drones']:
                    if int(drone['ID']) == drone_id:
                        selected_drone = drone
                        break
                break

    return render_template('reserveer.html',
                           locations=available_locations,
                           selected_location=selected_location,
                           selected_drone=selected_drone)


# drone
@routes_bp.route("/drone", methods=['POST'])
def postDrone():
    data = request.get_json()
    beschikbaarheid = data["beschikbaarheid"]
    batterijLevel = data["batterijLevel"]
    locatieId = data["locatieId"]

    if beschikbaarheid is None:
        return jsonify({'error': 'beschikbaarheid parameter is missing'}), 400
    elif batterijLevel is None:
        return jsonify({'error': 'batterijLevel parameter is missing'}), 400
    elif locatieId is None:
        return jsonify({'error': 'locatieId parameter is missing', 'status': 400}), 400

    from database_context import DatabaseContext
    #Try catch
    drone = Drone(beschikbaarheid=beschikbaarheid, batterijLevel=batterijLevel, locatieId=locatieId)
    drone.create()
    return jsonify({'msg': 'drone created.', 'status': 201}), 201

# piloot = 1 verslaggever = 2
@routes_bp.route('/user', methods=['POST'])
def postUser():
    data = request.get_json()
    naam = data['naam']
    rol = data['rol']
    if naam is None:
        return 'failed naam missing'
    elif rol is None:
        return 'failed rol is missing'
    user = User(naam=naam, rol=rol)
    user.create()
    return jsonify({'msg': 'user created', 'status': 201}), 201

# localisatie
from model.locatie import Locatie
@routes_bp.route('/locatie', methods=['POST'])
def postLocaties():
    data = request.get_json()
    naam = data["naam"]
    maxDrones = data["maxDrones"]

    if naam is None:
        return 'failed naam is missing'
    elif maxDrones is None:
        return 'failed maxDrones is missing'

    locatie = Locatie(naam=naam, maxDrones=maxDrones)
    locatie.create()

    return jsonify({'msg': 'location created', 'status': 201}), 201

# reservatie
@routes_bp.route('/reservatie', methods=['POST'])
def postReservatie():
    data = request.get_json()

    startplaatsId = data.get("startplaatsId")
    userId = data.get("userId")
    dronesId = data.get("dronesId")
    verslagId = data.get("verslagId")

    # Validate input
    if startplaatsId is None:
        return jsonify({'msg': 'failed, startplaatsId is missing'}), 400
    if userId is None:
        return jsonify({'msg': 'failed, userId is missing'}), 400
    if dronesId is None:
        return jsonify({'msg': 'failed, dronesId is missing'}), 400
    if verslagId is None:
        return jsonify({'msg': 'failed, verslagId is missing'}), 400

    # Create and store the reservatie
    reservatie = Reservatie(startplaatsId=startplaatsId, userId=userId, dronesId=dronesId, verslagId=verslagId)
    reservatie.create()

    return jsonify({'msg': 'reservatie created', 'status': 201}), 201


# ici
from model.verslag import Verslag
@routes_bp.route('/verslag', methods=['POST'])
def postVerslag():
    data = request.get_json()

    # Extract the data from the incoming request
    status = data.get("status")
    locatie = data.get("locatie")
    userId = data.get("userId")
    reserveringId = data.get("reserveringId")
    timestamp = data.get("timestamp")
    beeldmateriaal = data.get("beeldmateriaal")

    # Validate required fields
    if status is None:
        return jsonify({'msg': 'failed, status is missing'}), 400
    if locatie is None:
        return jsonify({'msg': 'failed, locatie is missing'}), 400
    if userId is None:
        return jsonify({'msg': 'failed, userId is missing'}), 400
    if reserveringId is None:
        return jsonify({'msg': 'failed, reserveringId is missing'}), 400
    if timestamp is None:
        return jsonify({'msg': 'failed, timestamp is missing'}), 400
    if beeldmateriaal is None:
        return jsonify({'msg': 'failed, beeldmateriaal is missing'}), 400

    # Create and store the verslag
    verslag = Verslag(status=status, locatie=locatie, userId=userId, reserveringId=reserveringId, timestamp=timestamp,
                      beeldmateriaal=beeldmateriaal)
    verslag.create()

    return jsonify({'msg': 'verslag created', 'status': 201}), 201

@routes_bp.route('/verslaginvul', methods=['GET', 'POST'])
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