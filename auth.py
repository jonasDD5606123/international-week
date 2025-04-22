from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from database import get_user_by_name

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        naam = request.form['naam']
        user = get_user_by_name(naam)
        if user:
            login_user(user)
            return redirect(url_for('routes.index'))
        return "Gebruiker niet gevonden", 403
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))