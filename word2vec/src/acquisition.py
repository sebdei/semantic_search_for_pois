from urllib.request import urlretrieve
import os
import pandas as pd
import re

from src.service.persistency import persistence_service
from src.service.persistency import pandas_persistency_service

DATA_BASE_PATH = 'data/'
CSV_NAME = 'open_data_berlin_cultural_institutes.xlsx'
CSV_URL = 'http://www.berlin.de/sen/kultur/_assets/statistiken/kultureinrichtungen_alle.xlsx'

LONG = 'long'
LAT = 'lat'
STREET_NAME = 'street_name'
STREET_NUMBER = 'street_number'
NAME = 'name'
ZIP_CODE = 'zip_code'

columns = [ NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT ]

def init_acqusition():
    assure_csv_file()

    source_data_frame = pd.read_excel(os.path.join(DATA_BASE_PATH, CSV_NAME))
    init_data_frame = process_init_data_frame(source_data_frame)

    load_init_data_frame_into_postgres(init_data_frame)

def assure_csv_file():
    if not os.path.exists('data'):
        os.makedirs('data')

        if not os.path.exists(DATA_BASE_PATH + CSV_NAME):
            print('downloading CSV file...')
            response = urlretrieve(CSV_URL, DATA_BASE_PATH + CSV_NAME)

def load_init_data_frame_into_postgres(df):
    persistence_service.create_initial_schema()

    pandas_persistency_service.insert_data_frame_into_odb_pois(df)

    # will be removed soon:
    for index, row in df.iterrows():
        persistence_service.insert_into_points_of_interests(row[NAME], row[STREET_NAME], row[STREET_NUMBER], row[ZIP_CODE], row[LONG], row[LAT], None, None)

def process_init_data_frame(source_data_frame):
    init_data_frame = pd.DataFrame(columns = columns)

    for index, row in source_data_frame.iterrows():
        street_name, street_number, zip_code = split_address(row['Adresse'])
        new_panda_row = pd.Series([ row['Institution'], street_name, street_number, zip_code, row['Lon'], row['Lat'] ], columns)

        init_data_frame =  init_data_frame.append([new_panda_row], ignore_index = True)

    return init_data_frame

def split_address(address):
    address_with_number, zip_code = (address.split(',', 1) + [None])[:2]
    street_name = re.sub(r'[\s0-9]{2,}.*|\d.*','', address_with_number)
    street_number = re.search(r'(\d+.?\d*.?)', address_with_number)

    if street_number is not None:
        street_number = street_number.group(0).strip()

    if zip_code is not None:
        zip_code = re.sub('[^0-9]', '', zip_code)
        zip_code = zip_code.strip()

    if street_name is not None:
        street_name = street_name.strip()

    return street_name, street_number, zip_code
