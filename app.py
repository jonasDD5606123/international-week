from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'geheimesleutel'

# Flask-Login initialiseren
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Blueprints registreren
from auth import auth_bp
from routes import routes_bp

app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

# User loader voor Flask-Login
from database import get_user_by_id

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(debug=True)