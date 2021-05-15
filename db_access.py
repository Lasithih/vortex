import re
from flask import app
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_utils as dbUtils
import datetime

db=SQLAlchemy()

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

def init_db(application):
    global app
    global db
    app = application
    db.init_app(application)
    db.app = application
    create_db(application, db)

def create_db(app, db):
    if dbUtils.database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        pass
    else:
        db.create_all()

def create_sample():
    global db
    new_task = Job(url='sdhjfb',
    job_type=1,
    format='format',
    status=1)

    try:
        db.session.add(new_task)
        db.session.commit()
    except:
        print("Insert failed")

    get_sample_data()

def get_sample_data():
    jobs = Job.query.all()
    print("Found {count} jobs".format(count=len(jobs)))

    




