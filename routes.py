from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from model.drone import Drone
from model.user import User
from model.locatie import Locatie
from model.reservering import Reservering
from model.verslag import Verslag

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
@login_required
def index():
    # Laad alle locaties met beschikbare drones
    available_locations = Locatie.get_available_drones_per_location()

    # Voor admin: toon ALLE gereserveerde drones
    if current_user.rol == 'admin':
        reserved_drones = Drone.all_reserved()
    else:
        reserved_drones = Drone.by_user(current_user.id)

    return render_template('index.html', locations=available_locations, drones=reserved_drones)

@routes_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.rol != 'admin':
        return redirect(url_for('routes.index'))

    # Haal de locaties op via Locatie.all() methode
    locaties = Locatie.all()
    return render_template('admin_dashboard.html', locaties=locaties)

@routes_bp.route('/reserveer', methods=['GET', 'POST'])
@login_required
def reserveer():
    if request.method == 'POST':
        location_id = int(request.form['location_id'])
        drone_id = int(request.form['drone_id'])
        startplaats_id = location_id
        reservering = Reservering(user_id=current_user.id, drone_id=drone_id, startplaats_id=startplaats_id)
        reservering.create()

        Drone.update_user_id(user_id=current_user.id, drone_id=drone_id)
        Drone.update_set_onbeschikbaar(drone_id)

        return redirect(url_for('routes.index'))

    location_id = request.args.get('location_id', type=int)
    drone_id = request.args.get('drone_id', type=int)

    available_locations = Locatie.get_available_drones_per_location()

    # Zoek de specifieke locatie en drone
    selected_location = None
    selected_drone = None

    if location_id is not None:
        selected_location = Locatie.by_id(location_id)
    if drone_id is not None:
        selected_drone = Drone.by_id(drone_id)

    return render_template('reserveer.html', locations=available_locations, selected_location=selected_location, selected_drone=selected_drone)

# Verslag indienen
@routes_bp.route('/verslag', methods=['GET', 'POST'])
@login_required
def verslag():
    #post
    if request.method == 'POST':
        reservering_id = int(request.form['reservering_id'])
        status = request.form['status']
        locatie = request.form['locatie']
        beeldmateriaal = request.form['beeldmateriaal']
        bescrijving = request.form['beschrijving']
        #fix timestamp

        # Maak verslag aan
        verslag = Verslag(status, locatie, current_user.id, reservering_id, beeldmateriaal, "2023-01-01 12:00:00", bescrijving)
        # verslag = Verslag(status=status, locatie=locatie, user_id=current_user.id, reservering_id=reservering_id, beeldmateriaal=beeldmateriaal, timestamp="2023-01-01 12:00:00", beschrijving=bescrijving)
        verslag.create()

        reservering = Reservering.by_id(reservering_id)
        Drone.update_user_id(reservering.drone_id, None)
        Reservering.update_status(1, res_id=reservering.id)
        Drone.update_set_beschikbaar(reservering.drone_id)

        return redirect(url_for('routes.index'))

    # get
    reserveringen = Reservering.get_by_user(current_user.id)
    return render_template('verslag.html', reserveringen=reserveringen)


@routes_bp.route("/drone", methods=['POST', 'GET'])
def drone():
    #post
    if request.method == 'POST' :
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

        drone = Drone(beschikbaarheid=beschikbaarheid, batterijLevel=batterijLevel, locatieId=locatieId)
        drone.create()

        return jsonify({'msg': 'drone created.', 'status': 201}), 201

    #get
    drones = Drone.all()
    return jsonify({"data": [d.to_dict() for d in drones]})

# piloot = 1 verslaggever = 2
@routes_bp.route('/user', methods=['POST'])
def user():
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

@routes_bp.route('/locatie', methods=['POST'])
def locatie():
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