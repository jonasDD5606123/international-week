kan je ervoor zorgen dat de drones correct gereserveerd kunnen worden door op de button te drukken angezien ik er nu een probleem mee heb
reservatie.html
{% extends "base.html" %}

{% block content %}
    <h1>Drone reserveren</h1>
    <form method="POST">
        <h2>Selecteer een locatie:</h2>
        <select name="location_id" id="location-select" required>
            <option value="" disabled {% if not selected_location %}selected{% endif %}>Kies een locatie</option>
            {% for location in locations %}
                <option value="{{ location.id }}" {% if location.id == selected_location.id %}selected{% endif %}>{{ location.naam }}</option>
            {% endfor %}
        </select>

        <div id="drone-selection">
            <h3>Beschikbare drone:</h3>
            {% if selected_drone %}
                <p>Drone #{{ selected_drone.id }} (Batterij: {{ selected_drone.batterijlevel }}%)</p>
                <input type="hidden" name="drone_id" value="{{ selected_drone.id }}">
            {% else %}
                <!-- Dynamisch de drones tonen op basis van de geselecteerde locatie -->
                <p>Selecteer een locatie om drones weer te geven.</p>
            {% endif %}
        </div>

        <buton type="submit">Reserveer</buton>
    </form>
<script>
    document.getElementById('location-select').addEventListener('change', function() {
        var locationId = this.value;
        var dronesContainer = document.getElementById('drone-selection');
        dronesContainer.innerHTML = '<h3>Beschikbare drone:</h3>';

        var locations = {{ locations|tojson|safe }};
        var selectedLocation = locations.find(loc => loc.id == locationId);

        if (selectedLocation && selectedLocation.beschikbare_drones.length > 0) {
            selectedLocation.beschikbare_drones.forEach(function(drone) {
                var droneElement = document.createElement('div');
                droneElement.innerHTML = `
                    <input type="radio" name="drone_id" value="${drone.ID}" required>
                    <label>Drone #${drone.ID} (Batterij: ${drone.batterijlevel}%)</label><br>
                `;
                dronesContainer.appendChild(droneElement);
            });
        } else {
            dronesContainer.innerHTML += '<p>Geen drones beschikbaar voor deze locatie.</p>';
        }
    });
</script>
{% endblock %}


routes.py:
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from model.drone import Drone
from model.user import User

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

        # Update de status van de drone naar gereserveerd
        update_drone_status(drone_id, current_user.id)

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

drone.py:
from database_context import DatabaseContext

class Drone:
    def init(self, beschikbaarheid, batterijLevel, locatieId, id = None):
        self.id = id
        self.beschikbaarheid = beschikbaarheid
        self.batterijLevel = batterijLevel
        self.locatieId = locatieId

    def create(self):
        # Use parameterized query to avoid SQL injection
        sql = '''insert into drones (batterijlevel, isbeschikbaar, locatieId) 
                 values (?, ?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.batterijLevel, self.beschikbaarheid, self.locatieId))
        conn.commit()

    def updateBatterij(self, batterijLevel):
        sql = '''update drones set batterijLevel = ? where id = ?'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (batterijLevel, self.id))
        conn.commit()

    @staticmethod
    def all():
        sql = 'SELECT * FROM drones'
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

model/localisatie.py:
from database_context import DatabaseContext

class Locatie:
    def init(self, naam, maxDrones, id=None):
        self.naam = naam
        self.maxDrones = maxDrones

    def create(self):
        sql = '''insert into startplaats (naam, maxDrones) 
                         values (?, ?)'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.naam, self.maxDrones))
        conn.commit()

    @staticmethod
    def all():
        sql = '''select * from startplaats'''
        dc = DatabaseContext()
        conn = dc.getDbConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

database.py:
import sqlite3
from model.user import User

DB_PATH = 'database.db'



def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_id(user_id):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Users WHERE ID = ?", (user_id,))
        row = cur.fetchone()
        return User(row['ID'], row['Naam'], row['Rol']) if row else None

def get_user_by_name(naam):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Users WHERE Naam = ?", (naam,))
        row = cur.fetchone()
        return User(row['ID'], row['Naam'], row['Rol']) if row else None

def get_all_drones():
    with get_connection() as conn:
        cur = conn.execute("SELECT D.*, S.naam as locatie_naam FROM Drones D JOIN Startplaats S ON D.locatieId = S.ID")
        return [dict(row) for row in cur.fetchall()]

def get_available_drones_per_location():
    with get_connection() as conn:
        result = []
        locaties = conn.execute("SELECT * FROM Startplaats").fetchall()

        for loc in locaties:
            all_drones = conn.execute("SELECT * FROM Drones WHERE locatieId = ?", (loc['ID'],)).fetchall()
            available = [d for d in all_drones if d['Isbeschikbaar'] == 1]
            result.append({
                "id": loc['ID'],
                "naam": loc['naam'],
                "drones": [dict(d) for d in all_drones],
                "beschikbare_drones": [dict(d) for d in available],
                "max_drones": loc['maxDrones']
            })
        return result

def get_beschikbare_drones():
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Drones WHERE Isbeschikbaar = 1")
        return [dict(row) for row in cur.fetchall()]

def get_beschikbare_locaties():
    locaties = get_available_drones_per_location()
    return [loc for loc in locaties if loc['beschikbare_drones']]

def create_reservering(user_id, drone_id, startplaats_id):
    with get_connection() as conn:
        conn.execute("INSERT INTO Reserveringen (startplaats_id, user_id, drones_id) VALUES (?, ?, ?)",
                     (startplaats_id, user_id, drone_id))
        conn.execute("UPDATE Drones SET Isbeschikbaar = 2 WHERE ID = ?", (drone_id,))
        conn.commit()

def create_verslag(status, locatie, user_id, reservering_id, beeldmateriaal, timestamp):
    with get_connection() as conn:
        conn.execute("INSERT INTO Verslagen (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                     (status, locatie, user_id, reservering_id, beeldmateriaal, timestamp))
        drone_id = conn.execute("SELECT drones_id FROM Reserveringen WHERE ID = ?", (reservering_id,)).fetchone()['drones_id']
        conn.execute("UPDATE Drones SET Isbeschikbaar = 1 WHERE ID = ?", (drone_id,))
        conn.commit()

def get_reserveringen_voor_gebruiker(user_id):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Reserveringen WHERE user_id = ?", (user_id,))
        return [dict(row) for row in cur.fetchall()]

def update_drone_status(drone_id, new_status):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Drones SET Isbeschikbaar = ? WHERE ID = ?', (new_status, drone_id))
    conn.commit()
    conn.close()


import sqlite3

def add_user(naam, rol):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (Naam, Rol) VALUES (?, ?)", (naam, rol))
    conn.commit()
    conn.close()

def add_startplaats(naam, max_drones):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Startplaats (naam, maxDrones) VALUES (?, ?)", (naam, max_drones))
    conn.commit()
    conn.close()