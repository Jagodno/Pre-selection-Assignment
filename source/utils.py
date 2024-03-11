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


def get_dataFrame_withShortCols(file_name = 'development_sample.csv'):
    """
    Returns dataframe wwith short 
    """
    cwd = os.getcwd().replace('jupyter_notebooks', '')
    dataDict = f'{cwd}\\data'

    df = pd.read_csv(f'{dataDict}\\{file_name}')
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


def data_cleaner(df):
    df['Distribution channel'] = df['Distribution channel'].apply(lambda x: 4 if x == 'Direct' else (5 if x == 'Online' else x))
    df['Application_status'] = df['Application_status'].apply(lambda x: 1 if x == 'Approved' else (0 if x == 'Rejected' else x))
    df['Clasification of the vehicle'] = df['Clasification of the vehicle'].fillna(2)
    # cos jeszcze z property ownership (też osobna klasa jak przy pojazdach?)
    df['Spendings estimation'] = df['Spendings estimation'].fillna(df['Spendings estimation'].median())
    return df.drop(['Application_status', 'ID', 'Customer ID'], axis=1).dropna(subset=['Default indicator',
                                                                                       'Loan purpose',
                                                                                       'Distribution channel',
                                                                                       'Amount on current account',
                                                                                       'Amount on savings account',
                                                                                       'Value of the goods']).fillna(0)


def handle_categorical_columns(df):

    categorical_columns = ['Loan purpose', 'profession of main applicant', 'profession of second applicant',
                           'marital status of main applicant']
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True, dtype=int)

    return df
