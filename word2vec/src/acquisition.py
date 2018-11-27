from urllib.request import urlretrieve

import os
import pandas

DATA_BASE_PATH = 'data/'
CSV_NAME = 'open_data_berlin_cultural_institutes.xlsx'
CSV_URL = 'http://www.berlin.de/sen/kultur/_assets/statistiken/kultureinrichtungen_alle.xlsx'

def assure_csv_file():
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists(DATA_BASE_PATH + CSV_NAME):
        print('downloading CSV file...')
        response = urlretrieve(CSV_URL, DATA_BASE_PATH + CSV_NAME)

def perform_acqusition():
    assure_csv_file()

    data_frame = pandas.read_excel(os.path.join(DATA_BASE_PATH, CSV_NAME))

    for index, row in data_frame.iterrows():
        row['Institution']
        row['Adresse']
        row['Lat']
        row['Lon']
