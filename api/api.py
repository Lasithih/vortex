import re
from flask.wrappers import Response
from werkzeug.wrappers import ResponseStream
from db_access import Job
from re import A
from flask import request, jsonify
from flask_login import login_user, login_required
from models import User
import db_access
import youtube
import config

def create_endpoints(app):
    create_endpoint_login(app)
    create_endpoint_job_save(app)
    create_endpoint_job_list(app)
    create_endpoint_get_yt_video_info(app)

def create_endpoint_login(app):
    @app.route('/api/v1/auth/login', methods=['POST'])
    def api_login():
        info = request.form
        username = info.get('username', 'guest')
        password = info.get('password', '')

        if username == 'admin' and password == config.config_get_dashboard_password():
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
            response = {
                'success': True,
                'data': jobs
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
            info = request.args
            url = info.get('url', '')
            start_at_midnight = info.get('start_at_midnight', '')
            job_type = info.get('job_type', '')
            format = info.get('format', '')
            start_time = info.get('start_time', '')
            end_time = info.get('end_time', '')

            # TODO - Validate data

            job = db_access.Job(
                url = url,
                start_at_midnight = start_at_midnight,
                job_type = job_type,
                format = format,
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


def create_endpoint_get_yt_video_info(app):
    @app.route('/api/v1/yt/info', methods=['GET'])
    @login_required
    def get_yt_info():
        try:
            info = request.args
            url = info.get('url', '')
            if(url == ''):
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
