"""
Descr: module to setup logging
@author: vitkai
Created: Sat Mar 14 2020 21:55 MSK
"""
import __main__
import logging

from os import path
"""
from shutil import copy2
"""

def logging_setup():
    logger = logging.getLogger(__name__)
    filename = path.splitext(__main__.__file__)[0] + '.log'
    handler = logging.FileHandler(filename, encoding = "UTF-8")

    logger.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(module)s.%(funcName)s %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    logger.debug("\n{0}Starting program\n{0} Logging was setup".format('-' * 10 + '=' * 10 + '-' * 10 + "\n"))

    return logger



if __name__ == "__main__":
    print("Please call 'logging_setup' to get 'logger' instance")
