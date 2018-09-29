import logging
import sys

loglevel = sys.argv[1].split('=')[1]
print(loglevel)

numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)

logging.basicConfig(
    filename='example.log',
    filemode='w',
    level=numeric_level,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

logging.error('error {}'.format('logging'))


# -----

import logg

# -------

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
