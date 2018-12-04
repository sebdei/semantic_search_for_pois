from urllib.request import urlretrieve
from src.service import persistence_service
import os
import pandas
import re

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
    data_frame2= process_data_frame(data_frame)
    load_data_frame_into_postgres(data_frame2)

def split_address(address):
        address_with_number, zip_code = (address.split(',',1)+[None])[:2]
        street_name=re.sub('[\s0-9]{2,}.*|\d.*','',address_with_number)
        street_number=re.search(r'(\d+.?\d*.?)',address_with_number)
        if street_number is None:
                street_number=None
        else:
                street_number=street_number.group(0).strip()
        if zip_code is None:
                zip_code=None
        else:
                zip_code=re.sub('[^0-9]', '',zip_code)
                zip_code=zip_code.strip()
        street_name=street_name.strip()
        return street_name, street_number, zip_code

def process_data_frame(df):
        columns=['name', 'street_name', 'street_number', 'zip_code', 'long','lat']
        data_frame2=pandas.DataFrame(columns=columns)
        for index, row in df.iterrows():
                street_name,street_number,zip_code=split_address(row['Adresse'])
                new_row=[row['Institution'],street_name,street_number,zip_code,row['Lon'],row['Lat']]
                data_frame3=pandas.DataFrame([new_row], columns=columns)
                data_frame2=data_frame2.append(data_frame3, ignore_index=True)
        return data_frame2

def load_data_frame_into_postgres(df):
        for index, row in df.iterrows():
                persistence_service.insert_into_points_of_interests(row['name'], row['street_name'], row['street_number'], row['zip_code'], row['long'], row['lat'], None, None)



                
