"""
Descr: module to parse .xlsx file and populate db
@author: vitkai
Created: Wed Feb 19 2019 18:10 MSK
"""
import __main__
import codecs
import logging
import pandas as pd
import yaml as yml
from os import path
from shutil import copy2

# own function to handle an uploaded file
from .my_logger import logging_setup


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


def get_transactions_by_cat(cat, date_col, cat_val_col, cat_comm_col, ccy, df_inp):
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
    
    # print(filtered_df)
    
    return filtered_df
    
    

def process_ssheet_tab(cfg, df_inp):
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
            trans_res = get_transactions_by_cat(cat, date_col, cfg[2020]['spent'][cat]['val'], cfg[2020]['spent'][cat]['comment'], cfg[2020]['CCY'], df_inp)
            # merge transactions vertically
            trans_df = pd.concat([trans_df, trans_res], axis=0).reset_index(drop=True)

    msg = 'Transformed dataframe: \n{}'.format(trans_df)
    # print(msg)
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
    

def general_init():
    global logger, full_path
    logger = logging_setup()

    # get script path
    full_path, filename = path.split(path.realpath(__file__))
    logger.debug("Full path: {0} | filename: {1}".format(full_path, filename))
    

def parse(file_to_proc):
    general_init()
    
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
    
    result = process_ssheet_tab(conf, df_table[df_tabs[1]])
 
    logger.debug("That's all folks")
    print("\nThat's all folks")
    
    return result

# main starts here
if __name__ == "__main__":
    print("Please call 'parse(path_to_file_to_process)' to parse xlsx file getting DF as output")

    
# TODO: 
