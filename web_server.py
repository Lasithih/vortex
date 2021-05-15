from flask import Flask, render_template, request
from flask_login import login_required
import datetime

from api import api
import auth
import db_access

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/downloads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '72cowDH%FeJpqxX7*YXV'

#Database
db_access.init_db(app)

# Authentication
auth.init_auth(app)

#API
api.create_endpoints(app)

@app.route('/', methods=['POST','GET'])
@login_required
def index():
    return render_template('index.html')

# if __name__ == "__main__":
#     app.run(host="0.0.0.0",debug=True)

def init_web_server():
    app.run(host="0.0.0.0",debug=True)