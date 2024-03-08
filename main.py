import pandas as pd
from get_descriptions import get_descriptions
descriptions = get_descriptions('descriptions.txt')

dev = pd.read_csv('development_sample.csv')
test = pd.read_csv('testing_sample.csv')
dev.rename(columns=descriptions, inplace=True) # Rename columns using the descriptions dictionary

print(dev.isnull().sum())