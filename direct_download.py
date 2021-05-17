import requests
import logging
import time

def get_file_name(url):
    arr = url.split('/')
    return arr[len(arr)-1]

def download(url):
    try:
        r = requests.get(url, allow_redirects=True)

        ret = open('downloads/{}'.format(get_file_name(url)), 'wb').write(r.content)
        
    except Exception as e:
        logging.error('Direct download error: {}'.format(str(e)))
        raise e