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
    # Remove rejected applications
    df.drop(df[df['Application_status'] == 'Rejected'].index, inplace=True)
    
    # Remove null loan purpose
    df.drop(df[df['Loan purpose'].isnull()].index, inplace=True)
    
    # Parse dates
    df['Application date'] = pd.to_datetime(df['Application date'], format='%d%b%Y %H:%M:%S')
    df['employment date'] = pd.to_datetime(df['employment date'], format='%d%b%Y', errors='coerce')
    
    # Add work experience column at the time of credit application
    df['work experience'] = (df['Application date'] - df['employment date']).dt.days
    
    # Modify distribution channel column 
    df['Distribution channel'] = df['Distribution channel'].apply(lambda x: 4 if x == 'Direct' else (5 if x == 'Online' else x))
    
    # Drop useless columns
    df.drop(['Application_status', 'ID', 'Customer ID', 'employment date'], axis=1, inplace=True)
    
    # Drop rows with null values in specific columns
    df.dropna(subset=['Default indicator', 'Distribution channel', 'Spendings estimation'], inplace=True)
    
    # Fill null values with 0 for multiple columns
    columns_to_fill = ['Value of the goods', 'income of second applicant', 'profession of second applicant',
                      'Amount on current account', 'Amount on savings account', 'work experience']
    df[columns_to_fill] = df[columns_to_fill].fillna(0)
    
    return df


def preprocess_data(df):
    # One-hot encoding for 'Loan purpose' only
    df_loan_purpose = pd.get_dummies(df['Loan purpose'], prefix='loan_purpose')
    
    # Encoding based on conditions
    df['loan_purpose_1_0'] = ((df_loan_purpose['loan_purpose_1.0'] == 1) & (df['Clasification of the vehicle'] == 0)).astype(int)
    df['loan_purpose_1_1'] = ((df_loan_purpose['loan_purpose_1.0'] == 1) & (df['Clasification of the vehicle'] == 1)).astype(int)
    df['loan_purpose_2_0'] = ((df_loan_purpose['loan_purpose_2.0'] == 1) & (df['Property ownership for property renovation'] == 0)).astype(int)
    df['loan_purpose_2_1'] = ((df_loan_purpose['loan_purpose_2.0'] == 1) & (df['Property ownership for property renovation'] == 1)).astype(int)

    # One-hot encoding for remaining categorical columns
    cols = ['Distribution channel', 'Payment frequency',
            'profession of main applicant', 'profession of second applicant',
            'marital status of main applicant']
    df_remaining = pd.get_dummies(df[cols], columns=cols, prefix=cols)
    
    # Concatenate encoded columns
    df_encoded = pd.concat([df, df_loan_purpose, df_remaining], axis=1)
    
    # Drop unnecessary columns
    df_encoded.drop(columns=['Loan purpose', 'Clasification of the vehicle', 'Property ownership for property renovation', 'Distribution channel', 'Payment frequency',
            'profession of main applicant', 'profession of second applicant',
            'marital status of main applicant'], inplace=True)
    
    return df_encoded
    

