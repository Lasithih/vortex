from __future__ import unicode_literals
import re
import youtube_dl
import requests
import subprocess
import logging

import db_access
from enums import JobType


def get_version():
    # return subprocess.check_output('youtube-dl --version',shell=True).decode("utf-8").rstrip()
    # return db_access.get_module_version(PyModule.Ytdl)
    output = subprocess.check_output('pip list | grep youtube-dl',shell=True).decode("utf-8")
    version_search = re.search('youtube-dl[\s\t]+(.*)', output, re.IGNORECASE)
    version = None
    if version_search:
        version = version_search.group(1)
    return version
        


def get_ytdl_latest_version():
    target_url = 'http://rg3.github.io/youtube-dl/update/LATEST_VERSION'
    for line in requests.get(target_url):
        return line.decode("utf-8")


def check_updates():
    ytdl_version = get_version()
    ytdl_latest_version = get_ytdl_latest_version()

    latest_array = ytdl_latest_version.split('.')
    current_array = ytdl_version.split('.')

    if len(latest_array) != len(current_array):
        return
    
    is_equal = True
    try:
        for i in range(len(latest_array)):
            if int(latest_array[i]) != int(current_array[i]):
                is_equal = False
                break
    except:
        return

    if is_equal:
        logging.info("Youtube-dl up to date")
    else:
        logging.info("New Version Available")
        logging.info("Installed version: {}".format(ytdl_version))
        logging.info("Available version: {}".format(ytdl_latest_version))

        job = db_access.Job(url='dummy',start_at_midnight=False,job_type = JobType.YtdlUpdate.value, format='dummy', preset='dummy')
        db_access.insert_job(job)

        


def extract_info(url):
    try:
        ydl = youtube_dl.YoutubeDL({
            'noplaylist':True,
            'geo_bypass':True
        })
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


    try:
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        ret_code = ydl.download([job.url])
        return ret_code
    except Exception as e:
        logging.error("Failed to download youtube video - {}".format(str(e)))
        raise e
