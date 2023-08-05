import threading
import time
import signal
import datetime
from logging.handlers import RotatingFileHandler

import web_server
import logging
import config
from enums import Env
import youtube
import downloader

def signal_handler(sig, frame):
    global run_updater
    if signal.SIGINT == sig:
        logging.info('SIGINT received...')
        downloader.run_downloader = False
        run_updater = False
        thread_downloader.join()
        thread_ytdl_updater.join()
        exit(0)

#Thread targets
def run_auto_updater():
    global ytdl_update_last_checked
    ytdl_update_last_checked = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    while run_updater:
        current = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        if ytdl_update_last_checked == None or current - ytdl_update_last_checked > config.config_get_ytdl_check_update_interval():
            youtube.check_updates()
            ytdl_update_last_checked = current
        time.sleep(3600)
    logging.info('Exited thread: Auto updater')

def run_downloader():
    downloader.init_downloader()


signal.signal(signal.SIGINT, signal_handler)

log_level = logging.DEBUG
ytdl_update_last_checked = None
run_updater = True

if config.config_get_env() == Env.Production:
    log_level = logging.INFO


# Initializing logger
logFormatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
rootLogger = logging.getLogger()
rootLogger.setLevel(log_level)

fileHandler = RotatingFileHandler("{0}/{1}.log".format('logs', 'vortex'), maxBytes=50000000, backupCount=10)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

#start ytdl-auto updater
thread_ytdl_updater = threading.Thread(target=run_auto_updater)
thread_ytdl_updater.start()

# start worker
thread_downloader = threading.Thread(target=run_downloader)
thread_downloader.start()


web_server.init_web_server()




