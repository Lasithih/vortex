import logging
from re import A
from flask import request, jsonify
from flask_login import login_user, login_required
from models import User
import db_access
import youtube
import config
from enums import JobType
import json

def create_endpoints(app):
    create_endpoint_login(app)
    create_endpoint_job_save(app)
    create_endpoint_job_delete(app)
    create_endpoint_job_list(app)
    create_endpoint_get_yt_video_info(app)

def create_endpoint_login(app):
    @app.route('/api/v1/auth/login', methods=['POST'])
    def api_login():
        info = request.form
        username = info.get('username', 'guest')
        password = info.get('password', '')

        if username == config.config_get_dashboard_username() and password == config.config_get_dashboard_password():
            login_user(User())
            response = {
                'success': True,
                'data': None
            }
            return jsonify(response)
        else:
            response = {
                'success': False,
                'data': "Username or Password Error"
            }
            return jsonify(response)

def create_endpoint_job_list(app):
    @app.route('/api/v1/jobs/list', methods=['GET'])
    @login_required
    def api_list_jobs():
        try:
            jobs = db_access.get_all_jobs()
            
            jobsJson = []
            for job in jobs:
                jobJson = json.loads(json.dumps(job, cls=db_access.AlchemyEncoder))
                jobsJson.append(jobJson)
            response = {
                'success': True,
                'data': jobsJson
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'success': False,
                'data': str(e)
            }
            return jsonify(response)


def create_endpoint_job_save(app):
    @app.route('/api/v1/jobs/save', methods=['POST'])
    @login_required
    def api_new_job():
        try:
            info = request.get_json()
            url = info.get('url', '')
            title = info.get('title', '')
            start_at_midnight = info.get('isOffPeak', True)
            job_type = int(info.get('jobType', 2))
            format = info.get('format', '')
            preset = info.get('preset', 'auto')
            start_time = info.get('start_time', None)
            end_time = info.get('end_time', None)

            # TODO - Validate data
            if job_type != JobType.Direct.value and job_type != JobType.Youtube.value:
                logging.error("Invalid job type")
                raise Exception("Invalid job type")

            if len(title) > 390:
                title = title[0:390]

            job = db_access.Job(
                url = url,
                title = title,
                start_at_midnight = start_at_midnight,
                job_type = job_type,
                format = format,
                preset = preset,
                start_time = start_time,
                end_time = end_time
            )

            issuccess = db_access.insert_job(job)

            response = {
                'success': issuccess
            }

            return jsonify(response)
        except Exception as e:
            response = {
                'success': False,
                'data': str(e)
            }
            return jsonify(response)


def create_endpoint_job_delete(app):
    @app.route('/api/v1/jobs/delete', methods=['POST'])
    @login_required
    def api_delete_job():
        try:
            info = request.get_json()
            id = info.get('id', '')

            db_access.delete_job(id)

            response = {
                'success': True
            }

            return jsonify(response)

        except Exception as e:
            response = {
                'success': False
            }
            return jsonify(response)



def create_endpoint_get_yt_video_info(app):
    @app.route('/api/v1/yt/info', methods=['GET'])
    @login_required
    def get_yt_info():
        try:
            info = request.args
            url = info.get('url', '')
            if(url == ''):
                logging.error("Invalid URL")
                raise Exception("Invalid URL")
            
            result = youtube.extract_info(url)
            response = {
                'success': True,
                'data': result
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'success': False,
                'data': str(e)
            }
            return jsonify(response)
