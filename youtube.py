from enums import JobType
import youtube_dl
import requests
import subprocess
import os
import logging

import config
import db_access


ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

def get_version():
    return subprocess.check_output('youtube-dl --version',shell=True).decode("utf-8").rstrip()

def get_ytdl_latest_version():
    target_url = 'http://rg3.github.io/youtube-dl/update/LATEST_VERSION'
    for line in requests.get(target_url):
        return line.decode("utf-8")


def check_updates():
    ytdl_version = get_version()
    ytdl_latest_version = get_ytdl_latest_version()
    if ytdl_latest_version == ytdl_version:
        logging.info("Youtube-dl up to date")
    else:
        logging.info("New Version Available")
        logging.info("Installed version: {}".format(ytdl_version))
        logging.info("Available version: {}".format(ytdl_latest_version))

        job = db_access.Job(url='dummy',job_type = JobType.YtdlUpdate, format='dummy', preset='dummy')
        db_access.insert_job(job)

        # os.system('sudo wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl')
        # os.system('sudo sudo chmod a+rx /usr/local/bin/youtube-dl')


def extract_info(url):
    try:
        result = ydl.extract_info(
            url,
            download=False # We just want to extract the info
        )
        return result
    except:
        raise Exception("Could not extract data from URL")

