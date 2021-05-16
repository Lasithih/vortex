import web_server
import logging
import config
from config import Env

log_level = logging.DEBUG
if config.config_get_env() == Env.Production:
    log_level = logging.WARN


# Initializing logger
logging.basicConfig(filename="logs/downloader.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=log_level)

web_server.init_web_server()