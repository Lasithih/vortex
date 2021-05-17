import logging
import db_access
import time
from threading import Lock
import subprocess
import os
import sys

from enums import JobStatus, JobType
from db_access import Job
import youtube
import direct_download


downloader_queue = []


def fill_pending_jobs():
    global downloader_queue
    global thread_lock
    
    jobs = db_access.get_download_jobs()
    thread_lock.acquire()
    downloader_queue.extend(jobs)
    thread_lock.release()

def execute_job(job):
    db_access.update_job_status(job.id, JobStatus.downloading)
    success = JobStatus.failed
    if job.job_type == JobType.Youtube.value:
        success = JobStatus.success if download_youtube(job) else JobStatus.failed
    elif job.job_type == JobType.Direct.value:
        success = JobStatus.success  if download_direct(job) else JobStatus.failed
    elif job.job_type == JobType.YtdlUpdate.value:
        success = JobStatus.success if update_ytdl() else JobStatus.failed
    else:
        logging.error("Unknown job type: {}".format(job.job_type))
    db_access.update_job_status(job.id, success)
    if job.job_type == JobType.YtdlUpdate.value:
        os.execv(sys.executable, ['python'] + sys.argv)

def init_downloader():
    global downloader_queue 
    global thread_lock

    thread_lock = Lock()
    downloader_queue = []

    while True:
        fill_pending_jobs()
        while(len(downloader_queue) > 0):
            thread_lock.acquire()
            job = downloader_queue.pop(0)
            thread_lock.release()
            print("New job found")
            execute_job(job)
        time.sleep(5)


def update_ytdl():
    # os.system('sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl')
    # os.system('sudo sudo chmod a+rx /usr/local/bin/youtube-dl')
    try:
        subprocess.check_output('pip install --upgrade youtube-dl',shell=True)
        youtube.set_module_needs_reloading()
        return True
    except:
        return False
    

def download_youtube(job):
    try:
        ret = youtube.download(job)
        return ret == 0
    except Exception as e:
        return False

def download_direct(job):
    try:
        direct_download.download(job.url)
        return True
    except Exception as e:
        return False