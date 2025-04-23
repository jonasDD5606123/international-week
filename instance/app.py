from flask import Flask, render_template, request, jsonify
from config import Config
from model.drone import Drone

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

    if beschikbaarheid is None:
        return jsonify({'error': 'beschikbaarheid parameter is missing'}), 400
    elif batterijLevel is None:
        return jsonify({'error': 'batterijLevel parameter is missing'}), 400

    from database_context import DatabaseContext
    #Try catch
    drone = Drone(beschikbaarheid=beschikbaarheid, batterijLevel=batterijLevel)
    drone.create()
    return jsonify({'msg': 'drone created.', 'status': 201}), 201

if __name__ == "__main__":
    app.run(debug=True)

app.config.from_object(Config)