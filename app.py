from flask import Flask, render_template, url_for, request, jsonify
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
import datetime

from werkzeug.utils import redirect
from api import api
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///downloads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '72cowDH%FeJpqxX7*YXV'
db = SQLAlchemy(app)


# Authentication
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



@app.route('/api/v1/auth/login', methods=['POST'])
def api_login():
    # print(request.form)
    info = request.form
    username = info.get('username', 'guest')
    password = info.get('password', '')
    print(request.form)
    print(username)
    print(password)
    if username == 'admin' and password == 'public':
        login_user(User())
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "status": 401,
                        "reason": "Username or Password Error"})

class User():
    name = 'admin'
    id = 1
    
    def to_json(self):
        return {"name": self.name}
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    start_at_midnight = db.Column(db.Boolean, default=True)
    job_type = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, default=0) #TODO - Check default value
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id


@app.route('/', methods=['POST','GET'])
@login_required
def index():
    if request.method == 'POST':
        print("POST received")
    else:
        pass
    return render_template('index.html')

api.create_endpoints(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)