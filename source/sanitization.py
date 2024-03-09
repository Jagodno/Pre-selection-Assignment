import pandas as pd
import regex as re
import os
from utils import *


if __name__ == '__main__':
    descriptions = get_descriptions('../data/descriptions.txt')
    dev = pd.read_csv('../data/development_sample.csv')
    test = pd.read_csv('../data/testing_sample.csv')
    print(dev.head())
    dev.rename(columns=descriptions, inplace=True)  # Rename columns using the descriptions dictionary
    print(dev.isnull().sum())
    print(dev.dtypes)
    dev_str = dev.select_dtypes(include='object')
    print(dev_str.head())

def sanitize(df):
    df.drop(df[df['Application status'] == 'Rejected'].index, inplace=True) # Remove rejected applications
