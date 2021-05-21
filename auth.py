from flask_login import login_required, current_user, LoginManager, logout_user
from flask import render_template, redirect, url_for
from models import User


def init_auth(app):

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User()

    @app.route('/login', methods=['POST','GET'])
    def login():
        if current_user.is_authenticated:
            return render_template('index.html')
        else:
            return render_template('login.html')
        
    @app.route('/logout', methods=['POST', 'GET'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))