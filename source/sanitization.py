import pandas as pd
import regex as re
import os
from utils import *
def sanitize(df):
    # Remove rejected applications
    df.drop(df[df['Application_status'] == 'Rejected'].index, inplace=True)
    #remove null loan purpose
    df.drop(df[df['Var2'].isnull()].index, inplace=True)
    # Parse dates
    df['application_date'] = pd.to_datetime(df['application_date'], format='%d%b%Y %H:%M:%S')
    df['Var13'] = pd.to_datetime(df['Var13'], format='%d%b%Y', errors='coerce')
    # Change Var13 to value representing time of employment in days
    df['Var13'] = df['application_date'] - df['Var13']

    return df


if __name__ == '__main__':
    descriptions = get_descriptions('../data/descriptions.txt')
    dev = pd.read_csv('../data/development_sample.csv')
    test = pd.read_csv('../data/testing_sample.csv')
    dev = sanitize(dev)
    print(dev.head())