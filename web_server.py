import logging
from flask import Flask, render_template
from flask_login import login_required

import api
import auth
import db_access
import config
import enums

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/vortex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = config.config_get_secret_key()

#Database
db_initialized = False
while ( not db_initialized):
    db_initialized = db_access.init_db(app)

# Authentication
auth.init_auth(app)

#API
api.create_endpoints(app)

@app.route('/', methods=['POST','GET'])
@login_required
def index():
    return render_template('index.html')


def init_web_server():
    flaskLogger = logging.getLogger('werkzeug')
    flaskLogger.setLevel(logging.WARNING)
    app.run(host="0.0.0.0",debug=config.config_get_env() == enums.Env.Development)