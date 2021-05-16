from __future__ import unicode_literals
from locale import resetlocale
import youtube_dl


ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

def extract_info(url):
    try:
        result = ydl.extract_info(
            url,
            download=False # We just want to extract the info
        )
        return result
    except:
        raise Exception("Could not extract data from URL")