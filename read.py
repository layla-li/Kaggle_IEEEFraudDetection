# import math
import pandas as pd
from pandas.api.types import is_numeric_dtype
# import numpy as np


def count_missing(data):
    """
    count missing data
    """
    # count missing data in each column
    missing = pd.DataFrame()
    for col, content in data.items():
        idict = {"name": [col],
                 "total": [len(content)],
                 "miss": [content.isnull().sum()],
                 "percent": [100. * content.isnull().sum() / len(content)]}
        ipddf = pd.DataFrame.from_dict(idict, orient='columns')
        missing = pd.concat([missing, ipddf], axis=0, ignore_index=True)

    print("---- Missing Data Report ----")
    print("Following columns has no missing data:")
    print(missing[missing.miss == 0])
    print("\nFollowing columns has missing data:")
    print(missing[missing.miss > 0.].sort_values(by=['miss']).head(5))
    print("--------")
    print(missing[missing.miss > 0.].sort_values(by=['miss']).tail(5))
    print("\n\n")

    return missing


def column_str_to_int(data, name):
    """
    Convert string column to number. Save converted dataframe to csv file.

    Parameters:
    -----------
    data: pd.DataFrame()

    Returns:
    --------
    pd.DataFrame()
        the converted data frame
    """
    print("Convert string columns to int numbers.")
    for col, content in data.items():
        if not is_numeric_dtype(content):
            # create {string:number} dictionary
            col_dict = {y: x for x, y in enumerate(content.unique())}
            # replace string with number
            data[col+"_i"] = \
                data.apply(lambda row: col_dict[row[col]], axis=1)
            # remove the original column with string data
            data.drop([col], axis=1, inplace=True)
    try:
        data.to_csv("data/"+name+".csv")
    except IOError:
        print("Failed to save to data/"+name+".csv")

    return data


def read_raw_data(name="train"):
    """
    read raw data downloaded from competition web.

    Parameters:
    -----------
    name: string
        name of the file to read: train OR test

    Returns:
    --------
    pd.DataFrame()
    """
    try:
        print("Reading raw data from data/ folder")
        data_transaction = pd.read_csv('data/'+name+'_transaction.csv',
                                       index_col='TransactionID')
        data_identity = pd.read_csv('data/'+name+'_identity.csv',
                                    index_col='TransactionID')
    except IOError:
        print("Inputs not found in data/ folder.")

    data = pd.concat([data_transaction, data_identity], axis=1)
    return data


def read_data(name="train", converted=True):
    """
    read data from disk

    Parameters:
    -----------
    name: string
        name of the file to read: train OR test
    converted: bool
        whether the string data columns are converted to int or not
        True or False

    Returns:
    --------
    dp.DataFrame()
    """
    if converted:
        try:
            import os.path
            if os.path.exists('data/'+name+'.csv'):
                # test if the converted csv file exists already
                print('Reading: data/'+name+'.csv')
                data = pd.read_csv('data/'+name+'.csv',
                                   index_col='TransactionID')
            else:
                # read raw data and convert string columns to int
                data = read_raw_data(name)
                data = column_str_to_int(data, name)
        except IOError:
            print('data/'+name+'.csv not found and read raw data failed.')
    else:
        data = read_raw_data(name)

    return data
