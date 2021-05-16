from __future__ import unicode_literals
import youtube_dl

import youtube_dl
import requests
import subprocess
import logging

import db_access
from db_access import Job
from enums import JobType


ydl = youtube_dl.YoutubeDL({
    'noplaylist':True,
    'geo_bypass':True
})

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

        job = db_access.Job(url='dummy',job_type = JobType.YtdlUpdate.value, format='dummy', preset='dummy')
        db_access.insert_job(job)

        


def extract_info(url):
    try:
        result = ydl.extract_info(
            url,
            download=False # We just want to extract the info
        )
        return result
    except:
        raise Exception("Could not extract data from URL")


def download(job):
    ydl_opts = {
        'format': 'best',
        'noplaylist':True,
        'geo_bypass':True,
        'outtmpl': 'downloads/%(format_id)s-%(title)s.%(ext)s'
    }
    print("Format: {}".format(job.format))
    print("preset: {}".format(job.preset))
    if job.preset == 'auto':
        if job.format == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['format'] = job.format
    else:
        ydl_opts['format'] = job.preset


    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([job.url])
