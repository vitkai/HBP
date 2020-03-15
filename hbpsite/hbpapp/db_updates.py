"""
Descr: module to update db from input DF 
@author: vitkai
Created: Sat Mar 14 2020 22:02 MSK
"""
import __main__
import pandas as pd

from os import path
from .models import Category #, Transactions, CCY, Document

# own function to setup logger
from .my_logger import logging_setup

    
def general_init():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    

def check_categories(catl):
    """
    receives parameters:
        catl - categories list
    returns check status string
    """
    res_status = ''
    
    for cat in catl:
        if Category.objects.filter(name=cat).exists():
            msg = f"Category: {cat} already exists in db"
            logger.debug(msg)
            res_status = res_status + f'| {msg}'
        else:
            new_cat = Category.objects.create(name=cat)
            msg = f"Adding Category: {new_cat}"
            logger.debug(msg)
            res_status = res_status + f'| {msg}'
            new_cat.save()
    
    if res_status == '':
        res_status = 'No db updates'
    
    return res_status



def proc_db_import(df_to_proc):
    general_init()
    
    logger.debug("That's all folks")
    print("\nThat's all folks")

    result = 'proc_db_import says hello'
    
    # get a list of unique values form 'Category' column
    # cats = get_uniq_col_values(df_to_proc)
    cats = set(df_to_proc['Category'].tolist())
    
    msg = f"Categories list:\n{cats}"
    logger.debug(msg)
    
    result = result + ' | ' + check_categories(cats)

    return result


# main starts here
if __name__ == "__main__":
    print("Please call 'proc_db_import(DF)' update db with DF data")

    
# TODO: 
