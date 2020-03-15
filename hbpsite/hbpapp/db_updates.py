"""
Descr: module to update db from input DF 
@author: vitkai
Created: Sat Mar 14 2020 22:02 MSK
"""
import __main__
import pandas as pd

from os import path
from .models import Category, CCY, Transactions #, Document

# own function to setup logger
from .my_logger import logging_setup

    
def general_init():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    

def check_categories(df):
    """
    receives parameters: 
        df - DataFrame to work with
    returns check status string
    """
    # get a list of unique values form 'Category' column
    catl = set(df['Category'].tolist())
    
    msg = f"Categories list:\n{catl}"
    logger.debug(msg)
    
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
        res_status = 'No Category updates'
    
    return res_status


def check_currencies(df):
    """
    receives parameters: 
        df - DataFrame to work with
    returns check status string
    """
    # get a list of unique values form 'CCY' column
    catl = set(df['CCY'].tolist())
    
    msg = f"Categories list:\n{catl}"
    logger.debug(msg)
    
    res_status = ''
    
    for cat in catl:
        if CCY.objects.filter(name=cat).exists():
            msg = f"Currency: {cat} already exists in db"
            logger.debug(msg)
            res_status = res_status + f'| {msg}'
        else:
            new_cat = CCY.objects.create(name=cat)
            msg = f"Adding CCY: {new_cat}"
            logger.debug(msg)
            res_status = res_status + f'| {msg}'
            new_cat.save()
    
    if res_status == '':
        res_status = 'No Currency updates'
    
    return res_status


def update_transactions(df):
    """
    receives parameters: 
        df - DataFrame to work with
    returns check status string
    """
    
    res_status = ''
    
    tr_ignored_cnt = 0
    tr_updated_cnt = 0
    tr_added_cnt = 0
    
    # iterate through DataFrame rows
    for row in df.itertuples():

        # get currency
        curr = df['CCY']
        curr = CCY.objects.get(name=curr)

        # get Category
        cat = df['Category']
        cat = Category.objects.get(name=cat)

        date = df['Date']
        sum = df['Sum']

        # check if a Transaction exists in db
        if Transaction.objects.filter(tr_date=date, Sum=sum, CCY=curr, Category=cat).exists():
            msg = f"Transaction already exists in db:\n{row}"
            logger.debug(msg)
            tr_ignored_cnt = tr_ignored_cnt + 1
        else:
            msg = f"Adding Transaction: \n{row}"
            logger.debug(msg)
            
            comm = df['Comments']
            comm = Category.objects.get(name=comm)

            new_tran = Transaction.objects.filter(tr_date=date, Sum=sum, CCY=curr, Category=cat, Content=comm)
            new_tran.save()
            
            tr_added_cnt = tr_added_cnt + 1
            
   
    if tr_ignored_cnt + tr_updated_cnt + tr_added_cnt == 0:
        res_status = 'No Transaction updates'
    else:
        msg = f"Transactions counts: \nIgnored: {tr_ignored_cnt} \nUpdated: {tr_updated_cnt} \nAdded: {tr_added_cnt}"
        logger.debug(msg)
        res_status = res_status + '|' + msg
    
    return res_status



def proc_db_import(df_to_proc):
    general_init()
    
    logger.debug("That's all folks")
    print("\nThat's all folks")

    result = 'proc_db_import says hello'
    result = result + ' | ' + check_categories(df_to_proc)
    result = result + ' | ' + check_currencies(df_to_proc)
    result = result + ' | ' + update_transactions(df_to_proc)

    return result


# main starts here
if __name__ == "__main__":
    print("Please call 'proc_db_import(DF)' update db with DF data")

    
# TODO: 
