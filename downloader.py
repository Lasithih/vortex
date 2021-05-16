from enums import JobStatus
import logging
import threading
import db_access
import time
from threading import Lock
from db_access import Job

downloader_queue = []


def fill_pending_jobs():
    global downloader_queue
    global thread_lock

    print("Before: Queue has {} items".format(len(downloader_queue)))
    jobs = db_access.get_download_jobs()
    thread_lock.acquire()
    downloader_queue.extend(jobs)
    thread_lock.release()
    print("After: Queue has {} items".format(len(downloader_queue)))

def execute_job(job):
    print("executing job {id}: {type}".format(id=job.id, type=job.job_type))
    time.sleep(10)
    print("executed job {id}: {type}".format(id=job.id, type=job.job_type))
    db_access.update_job_status(job.id, JobStatus.success)

def init_downloader():
    global downloader_queue 
    global thread_lock

    thread_lock = Lock()
    downloader_queue = []

    # start db listener thread
    while True:
        fill_pending_jobs()
        while(len(downloader_queue) > 0):
            thread_lock.acquire()
            job = downloader_queue.pop(0)
            thread_lock.release()
            execute_job(job)

        time.sleep(5)


    # start job processor





