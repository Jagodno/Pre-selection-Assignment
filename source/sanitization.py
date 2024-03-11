import pandas as pd
import regex as re
import os
from utils import *
def sanitize(df):
    # Remove rejected applications
    df.drop(df[df['Application_status'] == 'Rejected'].index, inplace=True)
    #remove null loan purpose
    df.drop(df[df['Loan purpose'].isnull()].index, inplace=True)  # to w sumie już jest w utils
    # Parse dates
    df['Application date'] = pd.to_datetime(df['Application date'], format='%d%b%Y %H:%M:%S')
    df['employment date'] = pd.to_datetime(df['employment date'], format='%d%b%Y', errors='coerce')
    # Change Var13 to value representing time of employment in days
    df['employment date'] = df['Application date'] - df['employment date']
    df = df.rename(columns={'employment date': 'employment duration'})

    return df


if __name__ == '__main__':
    descriptions = get_descriptions('../data/descriptions.txt')
    dev = pd.read_csv('../data/development_sample.csv')
    test = pd.read_csv('../data/testing_sample.csv')
    dev = sanitize(dev)
    print(dev.head())