from flask import Flask, render_template, request, jsonify
from config import Config
from model.drone import Drone
from model.user import User

app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/drone", methods=['POST'])
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
@app.route('/user', methods=['POST'])
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

@app.route('/login', methods=['POST'])
def postLogin():
    data = request.get_json()
    naam = data['naam']
    if naam is None:
        return 'failed login'
    if not User.login(naam):
        return 'failed log in'
    return 'logged in'


if __name__ == "__main__":
    app.run(debug=True)

app.config.from_object(Config)