"""
Descr: module to update db from input DF 
@author: vitkai
Created: Sat Mar 14 2020 22:02 MSK
"""
import __main__
from os import path
import pandas as pd
"""
import codecs
import logging
import yaml as yml
from shutil import copy2
"""

# own function to handle an uploaded file
from .my_logger import logging_setup

    
def general_init():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    

# main starts here
if __name__ == "__main__":
    print("Please call 'proc_db_import' to update db with DF data")

def proc_db_import(df_to_proc):
    general_init()
    
    logger.debug("That's all folks")
    print("\nThat's all folks")

    result = 'proc_db_import says hello'

    return result

# main starts here
if __name__ == "__main__":
    print("Please call 'proc_db_import(DF)' update db with DF data")

    
# TODO: 
