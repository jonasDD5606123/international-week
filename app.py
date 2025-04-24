from flask import Flask
from flask_login import LoginManager
from auth import auth_bp
from routes import routes_bp
from model.user import User

app = Flask(__name__)
app.secret_key = 'geheimesleutel'

# Flask-Login initialiseren
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Blueprints registreren
app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

# User loader voor Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user = User.by_id(user_id)
    return user

if __name__ == '__main__':
    app.run(debug=True)
