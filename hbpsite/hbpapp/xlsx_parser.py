"""
Descr: module to parse .xlsx file and populate db
@author: vitkai
Created: Wed Feb 19 2019 18:10 MSK
"""
import __main__
import codecs
# import locale
import logging
import pandas as pd
# import sys
import yaml as yml
from os import path
from shutil import copy2
# import sqlite3
# from sqlite3 import Error
# from time import gmtime, strftime

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


def load_cfg():
    # read configuration
    cfg_file = full_path + '\\' + "xlsx_parser.yaml" 
    msg = 'Loading configuration:\nOpening {}'.format(cfg_file)
    logger.debug(msg)
    print(msg)
    
    with codecs.open(cfg_file, mode='rb', encoding='utf-8') as yml_fl:
        cfg = yml.safe_load(yml_fl)
    
    msg = 'Config loaded successfully'
    logger.debug(msg)
    print(msg)
    
    logger.debug(cfg)
    
    return cfg


def get_transactions(cat, date_col, cat_val_col, cat_comm_col, ccy, df_inp):
    """
    receives parameters:
        cat - category name
        date_col - date column ID
        cat_val_col - category value column ID
        cat_comm_col - category comment column ID
        ccy - currency
        df_inp - dataframe to work on
    returns set of transactions (date, sum, category, comment)
    """
    # need to filter non-empty rows of df_inp for given category
    # and to store in a new df (date, sum, category, comment)
    
    # fields(columns) in a temp dataframe
    fields = ['Date', 'Sum', 'Comments']
    
    # get new df without empty rows
    if cat_comm_col != 'N/A':
        # new_df = pd.DataFrame(df_inp.iloc[data_start_row:,[date_col, cat_val_col, cat_comm_col]], columns=fields)#.loc(mask)
        new_df = df_inp.iloc[data_start_row:data_end_row,[date_col, cat_val_col, cat_comm_col]].copy()
    else:
        new_df = df_inp.iloc[data_start_row:data_end_row,[date_col, cat_val_col]].copy()
        # need to add an empty comments column
        new_df['Comments'] = ""
    
    # rename columns
    for idx, col in enumerate(fields):
        new_df.rename(columns={ new_df.columns[idx]: col }, inplace = True)
    
    # remove all empty val rows
    filtered_df = new_df[~new_df[fields[1]].isna()].reset_index(drop=True)
    
    #currency Column to be added
    cat_list = [ccy] * len(filtered_df)
    filtered_df.insert(2, 'CCY', cat_list)
    
    #category Column to be added with current category
    cat_list = [cat] * len(filtered_df)
    filtered_df.insert(3, 'Category', cat_list)
    
    print(filtered_df)
    
    return filtered_df
    
    

def check_cfg(cfg, df_inp):
    # configuration check
    
    date_col = cfg[2020]['date']
    
    global data_start_row, data_end_row
    data_start_row = cfg[2020]['data_row']
    
    # determine column index by end row token
    data_end_row = df_inp[df_inp.iloc[:,0] == cfg[2020]['data_end_token']].index.tolist()[0]

    trans_df = pd.DataFrame(columns=['Date', 'Sum', 'CCY', 'Category', 'Comments'])
    
    for cat in cfg['categories']:
        if cat in cfg[2020]['spent']:
            # print('{} | {} '.format(cat, cfg[2020]['spent'][cat]['val']))
            trans_res = get_transactions(cat, date_col, cfg[2020]['spent'][cat]['val'], cfg[2020]['spent'][cat]['comment'], cfg[2020]['CCY'], df_inp)
            # merge transactions vertically
            trans_df = pd.concat([trans_df, trans_res], axis=0).reset_index(drop=True)

    msg = 'Transformed dataframe: \n{}'.format(trans_df)
    print(msg)
    logger.debug(msg)
    
    return trans_df
    

def import_xlsx(src_fl):
    
    work_fl = path.join(full_path, 'tmp.csv')
    copy2(src_fl, work_fl)
    
    logger.debug('Importing: {}'.format(src_fl))
    
    pd_imp = pd.read_excel(work_fl, None)
    stored_tabs = list(pd_imp.keys())
    
    logger.debug('Import success')
    
    tmp = pd_imp[stored_tabs[1]].head(5)
    msg = 'xlsx stored tabs head5: \n{}'.format(tmp)
    logger.debug(msg)
    
    return pd_imp, stored_tabs
    

# main starts here
def parse(file_to_proc):
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    
    conf = load_cfg()
    
    if not file_to_proc:
        tmp = 'my_buh.xlsx'
        msg = 'Processing {}'.format(tmp)
        print(msg)
        logger.debug(msg)
        file_to_proc = full_path + '\\' + tmp
    else:
        # construct file path
        file_to_proc = path.join(full_path, '..', file_to_proc)
        
    msg = 'file_to_proc = {}'.format(file_to_proc)
    print(msg)
    logger.debug(msg)
    
    df_table, df_tabs = import_xlsx(file_to_proc)
    
    result = check_cfg(conf, df_table[df_tabs[1]])
 
    logger.debug("That's all folks")
    print("\nThat's all folks")
    
    return result

if __name__ == "__main__":
    parse()
    
# TODO: 
