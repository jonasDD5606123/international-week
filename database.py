# Hardcoded data voor nu
users = [
    {"id": 1, "naam": "Piloot 1", "rol": "piloot"},
    {"id": 2, "naam": "Piloot 2", "rol": "piloot"},
    {"id": 3, "naam": "Admin", "rol": "admin"}
]

# Nieuwe structuur voor locaties
locations = [
    {"id": 1, "naam": "Locatie A", "max_drones": 3},
    {"id": 2, "naam": "Locatie B", "max_drones": 3}
]

# Drones gelinkt aan locaties
drones = [
    {"id": 1, "batterijlevel": 100, "isbeschikbaar": True, "location_id": 1},
    {"id": 2, "batterijlevel": 85, "isbeschikbaar": True, "location_id": 2},
    {"id": 3, "batterijlevel": 10, "isbeschikbaar": False, "location_id": 1},
    {"id": 4, "batterijlevel": 60, "isbeschikbaar": True, "location_id": 1},
    {"id": 5, "batterijlevel": 60, "isbeschikbaar": True, "location_id": 2},
]

reserveringen = []
verslagen = []


# Database functies
def get_user_by_id(user_id):
    for user in users:
        if user['id'] == int(user_id):
            return User(user['id'], user['naam'], user['rol'])
    return None

# database.py
def get_all_drones():
    # Voorbeeld van hoe je de drones kunt ophalen
    # Hier kun je bijvoorbeeld een databasequery doen om alle drones op te halen
    drones = [
        # Lijst van drones (vervang dit met echte data uit je database)
        {"id": 1, "locatie": "Locatie A", "isbeschikbaar": True, "batterijlevel": 50},
        {"id": 2, "locatie": "Locatie B", "isbeschikbaar": False, "batterijlevel": 20},
        # Voeg meer drones toe
    ]
    return drones


def get_user_by_name(naam):
    for user in users:
        if user['naam'] == naam:
            return User(user['id'], user['naam'], user['rol'])
    return None


# Nieuwe versie op basis van locatie en beschikbaarheid
def get_available_drones_per_location():
    result = []
    for location in locations:
        loc_drones = [d for d in drones if d.get('location_id') == location['id'] or not d.get('location_id')]
        available_drones = [d for d in loc_drones if d['isbeschikbaar']]

        result.append({
            "id": location["id"],
            "naam": location["naam"],
            "drones": loc_drones,
            "beschikbare_drones": available_drones,  # Voeg alleen de beschikbare drones toe
            "max_drones": location["max_drones"]
        })
    return result



# Extra functie om platte lijst van beschikbare drones op te halen (optioneel)
def get_beschikbare_drones():
    return [d for d in drones if d['isbeschikbaar']]


def get_beschikbare_locaties():
    # Alleen locaties met minstens één beschikbare drone
    return [loc for loc in get_available_drones_per_location() if loc["beschikbare_drones"]]


def create_reservering(user_id, drone_id, startplaats_id):
    reservering = {
        "id": len(reserveringen) + 1,
        "user_id": user_id,
        "drones_id": drone_id,
        "startplaats_id": startplaats_id,
        "verslag_id": None
    }
    reserveringen.append(reservering)

    # Update beschikbaarheid
    for drone in drones:
        if drone['id'] == drone_id:
            drone['isbeschikbaar'] = False

    return reservering


def create_verslag(status, locatie, user_id, reservering_id, beeldmateriaal, timestamp):
    verslag = {
        "id": len(verslagen) + 1,
        "status": status,
        "locatie": locatie,
        "user_id": user_id,
        "reservering_id": reservering_id,
        "timestamp": timestamp,  # Gebruik van de timestamp
        "beeldmateriaal": beeldmateriaal
    }
    verslagen.append(verslag)

    # Update reservering met verslag_id
    for res in reserveringen:
        if res['id'] == reservering_id:
            res['verslag_id'] = verslag['id']

            # Maak drone weer beschikbaar
            for drone in drones:
                if drone['id'] == res['drones_id']:
                    drone['isbeschikbaar'] = True

    return verslag

def get_reserveringen_voor_gebruiker(user_id):
    return [r for r in reserveringen if r['user_id'] == user_id]


# User klasse voor Flask-Login
class User:
    def __init__(self, id, naam, rol):
        self.id = id
        self.naam = naam
        self.rol = rol

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
