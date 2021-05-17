import threading
import time
import signal

import web_server
import logging
import config
from enums import Env
import youtube
import downloader

def signal_handler(sig, frame):
    print('cleaning up!')
    thread_downloader.join()
    thread_ytdl_updater.join()
    print('exiting')

#Thread targets
def run_auto_updater():
    while True:
        youtube.check_updates()
        time.sleep(config.config_get_ytdl_check_update_interval())

def run_downloader():
    downloader.init_downloader()


# signal.signal(signal.SIGINT, signal_handler)

log_level = logging.DEBUG
if config.config_get_env() == Env.Production:
    log_level = logging.WARN


# Initializing logger
logging.basicConfig(filename="logs/downloader.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=log_level)



#start ytdl-auto updater
thread_ytdl_updater = threading.Thread(target=run_auto_updater)
thread_ytdl_updater.start()

# start worker
thread_downloader = threading.Thread(target=run_downloader)
thread_downloader.start()


web_server.init_web_server()




