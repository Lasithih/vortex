from flask import app
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_utils as dbUtils
import datetime
import logging
from enums import JobStatus

db=SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    start_at_midnight = db.Column(db.Boolean, default=True)
    job_type = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(10), nullable=False)
    preset = db.Column(db.String(10), nullable=False, default='auto')
    status = db.Column(db.Integer, default=JobStatus.pending.value)
    start_time = db.Column(db.String(20), nullable=True)
    end_time = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self) -> str:
        return '<Task %r>' % self.id

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_db_version = db.Column(db.String(10), nullable=False)
    
    def __repr__(self) -> str:
        return '<Task %r>' % self.id

def init_db(application):
    global db
    try:
        db.init_app(application)
        db.app = application
        create_db(application, db)
        return True
    except Exception as e:
        logging.error("init_db() failed. Exception: {}".format(str(e)))
        return False


def create_db(app, db):
    if dbUtils.database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        logging.debug("Database already found")
        pass
    else:
        try:
            db.create_all()
        except Exception as e:
            logging.error("db.create_all() failed. Exception: {}".format(str(e)))
            raise e


def insert_job(job):
    global db
    try:
        db.session.add(job)
        db.session.commit()
        return True
    except Exception as e:
        logging.error("insert_job() failed. Exception: {}".format(str(e)))
        raise Exception ("Database operation error!")

def get_all_jobs():
    try:
        jobs = Job.query.all()
        return jobs
    except Exception as e:
        logging.error("get_all_jobs() failed. Exception: {}".format(str(e)))
        raise Exception ("Database operation error!")

def get_download_jobs():
    try:
        jobs = Job.query.filter_by(status=JobStatus.pending.value)
        return jobs
    except Exception as e:
        logging.error("get_download_jobs error: {}".format(str(e)))
        return []

def update_job_status(jobId, status):
    global db
    try:
        job = Job.query.get(jobId)
        job.status = status.value
        db.session.commit()
        return True
    except Exception as e:
        logging.error("update_job_status error: {}".format(str(e)))
        return False