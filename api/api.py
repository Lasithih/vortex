from re import A
from flask import request, jsonify
from flask_login import login_user
from models import User

def create_endpoints(app):
    create_endpoint_login(app)

def create_endpoint_login(app):
    @app.route('/api/v1/auth/login', methods=['POST'])
    def api_login():
        # print(request.form)
        info = request.form
        username = info.get('username', 'guest')
        password = info.get('password', '')

        if username == 'admin' and password == 'public':
            login_user(User())
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "status": 401,
                            "reason": "Username or Password Error"})