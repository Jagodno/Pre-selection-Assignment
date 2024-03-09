import pandas as pd
import regex as re
import os

def get_descriptions(fname):
    descriptions = {}
    with open(fname , 'r') as file:
        for line in file:
            argname, argvalue = line.split(maxsplit=1)
            descriptions[argname] = argvalue.strip()
    return descriptions


def get_dataFrame_withShortCols():
    """
    Returns dataframe wwith short 
    """
    cwd = os.getcwd().replace('jupyter_notebooks', '')
    dataDict = f'{cwd}\\data'

    df = pd.read_csv(f'{dataDict}\\development_sample.csv')
    columnHeaders = pd.read_excel(f'{dataDict}\\variables_description.xlsx', sheet_name= 'List of variables')
    
    VarList = columnHeaders['Column'].values.tolist()
    DescList = columnHeaders['Description'].values.tolist()

    DescList[3] = 'Default indicator'

    for i in range(len(DescList)):
        DescList[i] = DescList[i].replace('Application data: ', '')
        DescList[i] = DescList[i].replace('(Approved/Rejected)', '')
        reg = r' \([\s\S]*\)'
        DescList[i] = re.sub(reg, '', DescList[i])

    newColNames = {}

    for i in range(len(VarList)):
        newColNames[VarList[i]] = DescList[i]

    df.rename(columns = newColNames, inplace = True) 
    
    return df