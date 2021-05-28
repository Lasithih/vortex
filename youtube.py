from __future__ import unicode_literals
import re
import youtube_dl
import requests
import subprocess
import logging

import db_access
from enums import JobType
import ffmpeg_dl


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
        logging.info("Youtube-dl up to date {}".format(ytdl_latest_version))
    else:
        logging.info("New Version Available")
        logging.info("Installed version: {}".format(ytdl_version))
        logging.info("Available version: {}".format(ytdl_latest_version))

        job = db_access.Job(url='dummy',start_at_midnight=False,job_type = JobType.YtdlUpdate.value, format='dummy', preset='dummy')
        db_access.insert_job(job)

        


def extract_info(url):
    logging.info('Extracting info for url: {}'.format(url))
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
    except Exception as e:
        logging.error("extract_info(url): Could not extract data from URL. Exception: {}".format(str(e)))
        raise e

def preset_is_audio_only(preset, details):
    for format in details['formats']:
        if format['format_id'] == preset:
            if format['width'] == None and format['vcodec'] == 'none':
                print("AUDIO only")
                return True
    return False

def download(job):
    ydl_opts = {
        'format': 'best',
        'noplaylist':True,
        'geo_bypass':True,
        'outtmpl': 'downloads/%(format_id)s-%(title)s.%(ext)s'
    }
    logging.info('Starting a youtube download job format:{format} and preset:{preset}'.format(format=job.format, preset=job.preset))

    if job.start_time is not None or job.end_time is not None:
        logging.info('Download has trimming enabled')
        start = job.start_time if job.start_time is not None else 0
        end = job.end_time if job.end_time is not None else 0
        default_audio_preset = None
        input_video_url = None
        input_audio_url = None
        ext = None

        details = extract_info(job.url)

        is_audio_only = preset_is_audio_only(job.preset, details) or job.format == 'mp3'

        if job.preset == 'auto' and not is_audio_only:
            logging.error('Trimming is not supported for \'Auto\' preset')
            raise Exception('Trimming is not supported for \'Auto\' preset')

        default_formats = details['format_id'].split('+')

        if len(default_formats) == 2:
            default_audio_preset = default_formats[1]
        else:
            logging.error('Default audio stream not found')
            raise Exception('Default audio stream not found')


        if job.format == 'mp3':
            ext = 'mp3'
        
        for format in details['formats']:
            if format['format_id'] == job.preset:
                if is_audio_only:
                    input_audio_url = format['url']
                else:
                    input_video_url = format['url']
                ext = format['ext']
            if format['format_id'] == default_audio_preset:
                input_audio_url = format['url']

        output_file = 'downloads/'+details['title']+'.'+ext

        try:
            if is_audio_only:
                ffmpeg_dl.audio_trim(start_time=int(start),
                                end_time=int(end),
                                input=input_audio_url, 
                                output=output_file)
            else:
                ffmpeg_dl.video_trim(start_time=int(start),
                                end_time=int(end),
                                video_input=input_video_url, 
                                audio_input=input_audio_url, 
                                output=output_file)
            return 0
        except Exception as e:
            logging.error('Error while trimming. Exception: {}'.format(str(e)))
            raise e

    else:
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
            ydl_opts['format'] = '{}+bestaudio'.format(job.preset)


        try:
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            ret_code = ydl.download([job.url])
            return ret_code
        except Exception as e:
            logging.error("Failed to download youtube video - {}".format(str(e)))
            raise e
