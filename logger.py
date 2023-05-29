import logging

from config import config

logging.basicConfig(level=config.logger_level, 
                    format='[ %(asctime)s %(filename)s line:%(lineno)d %(levelname)s ]  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('transfer-agent')