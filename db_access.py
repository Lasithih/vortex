from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import sqlalchemy_utils as dbUtils
from datetime import datetime, time
import logging
from enums import JobStatus, JobType
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

db=SQLAlchemy()


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(400), nullable=True)
    start_at_midnight = db.Column(db.Boolean, default=True)
    job_type = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(10), nullable=True)
    preset = db.Column(db.String(10), nullable=True, default='auto')
    status = db.Column(db.Integer, default=JobStatus.pending.value)
    start_time = db.Column(db.String(20), nullable=True)
    end_time = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return '<Task %r>' % self.id

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_db_version = db.Column(db.String(10), nullable=False)
    
    def __repr__(self) -> str:
        return '<Task %r>' % self.id

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

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
        jobs = Job.query.filter(Job.job_type != JobType.YtdlUpdate.value).order_by(Job.date_created.desc()).limit(100)
        return jobs
    except Exception as e:
        logging.error("get_all_jobs() failed. Exception: {}".format(str(e)))
        raise Exception ("Database operation error!")

def delete_job(job_id):
    global db
    try:
        Job.query.filter(Job.id == job_id).delete()
        db.session.commit()
    except Exception as e:
        logging.error("delete_job() failed. Exception: {}".format(str(e)))
        raise Exception ("Database operation error!")

def get_download_jobs():
    try:
        isOffPeak = is_time_between(time(00,00), time(7,30))
        jobs = []
        if(isOffPeak):
            jobs = Job.query.filter(Job.status==JobStatus.pending.value)
        else:
            jobs = Job.query.filter(sqlalchemy.and_(Job.status == JobStatus.pending.value, Job.start_at_midnight==False))
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


