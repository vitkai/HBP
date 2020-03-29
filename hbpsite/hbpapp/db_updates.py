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
    
    msg = f"Currencies list:\n{catl}"
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
    
    """
    # iterating over one column - `f` is some function that processes your data
    result = [f(x) for x in df['col']]
    # iterating over two columns, use `zip`
    result = [f(x, y) for x, y in zip(df['col1'], df['col2'])]
    # iterating over multiple columns
    result = [f(row[0], ..., row[n]) for row in df[['col1', ...,'coln']].values]
    """
    
    # iterate through DataFrame rows
    #for row in df.itertuples():
    #for curr, cat, date, sum_val, comm in zip(df['CCY'], df['Category'], df['Date'], df['Sum'], df['Comments']):
    for row in df[['Date', 'Sum', 'CCY', 'Category', 'Comments']].values:

        # get currency
        #curr = df['CCY']
        curr = row[2]
        curr = CCY.objects.get(name=curr)

        # get Category
        #cat = df['Category']
        cat = row[3]
        cat = Category.objects.get(name=cat)

        #date = df['Date']
        date = row[0]
        # sum_val = df['Sum']
        sum_val = round(float(row[1]), 2)
        
        #comm = df['Comments']
        comm = row[4]
        
        # check if a Transaction exists in db
        # ToDo: add correct Category checks (ManyToMany field)
        if Transactions.objects.filter(tr_date=date, Sum=sum_val, CCY=curr, Content=comm).exists():
            msg = f"Transaction already exists in db:\n{row}"
            logger.debug(msg)
            tr_ignored_cnt = tr_ignored_cnt + 1
        else:
            msg = f"Adding Transaction: \n{row}"
            logger.debug(msg)
            
            new_tran = Transactions.objects.create(tr_date=date, Sum=sum_val, CCY=curr, Content=comm)
            new_tran.Category.add(cat)
            msg = f"new_tran: \n{new_tran}"
            logger.debug(msg)
            #new_tran.save()
            
            tr_added_cnt = tr_added_cnt + 1
   
    if tr_ignored_cnt + tr_updated_cnt + tr_added_cnt == 0:
        res_status = 'No Transaction updates'
    else:
        msg = f"Transactions counts: \nIgnored: {tr_ignored_cnt} \nUpdated: {tr_updated_cnt} \nAdded: {tr_added_cnt}"
        logger.debug(msg)
        res_status = res_status + '|' + msg
    
    return res_status


def db_remove_duples():
    row_del_cnt = 0
    # assuming which duplicate is removed doesn't matter...
    for row in Transactions.objects.all().reverse():
        
        trans_list = Transactions.objects.filter(tr_date=row.tr_date, Sum=row.Sum, Content=row.Content)
        if trans_list.count() > 1:
            msg=f"row:\n{row}"
            logger.debug(msg)

            # get categories related to the row
            row_cats = list(row.Category.all()) # converting to list to be able to compare
            msg = f"Categories in row:\n{row_cats}"
            logger.debug(msg)
            
            # check categories of other rows in query set
            same_cats = False
            for row_n in trans_list:
                rown_cats = list(row_n.Category.all())
                msg = f"Categories in row_n:\n{rown_cats}"
                logger.debug(msg)
                if row_cats == rown_cats:
                    same_cats = True
                    break
                
            if same_cats:
                msg = f"Removing row:\n{row}"
                logger.debug(msg)
                row.delete()
                row_del_cnt = row_del_cnt + 1

    msg = f"Transaction dupes removed count: {row_del_cnt}"
    logger.debug(msg)

    return msg


def proc_db_import(df_to_proc):
    general_init()
    
    logger.debug("That's all folks")
    print("\nThat's all folks")

    result = 'proc_db_import says hello'

    result = result + ' | ' + check_categories(df_to_proc)
    result = result + ' | ' + check_currencies(df_to_proc)
    result = result + ' | ' + update_transactions(df_to_proc)

    # result = result + ' | ' + db_remove_duples()
    
    return result


# main starts here
if __name__ == "__main__":
    print("Please call 'proc_db_import(DF)' update db with DF data")

    
# TODO: 
