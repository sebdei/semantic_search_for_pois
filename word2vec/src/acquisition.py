from urllib.request import urlretrieve
from src.service import persistence_service
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
  #  return data_frame

def split_address_format(df):
        df['address_with_number'], df['zipcode']=df['Adresse'].str.split(',',1).str
        df['zipcode'].replace({'[^0-9]': ''},inplace=True, regex=True)
        df['street_number'] = df['address_with_number'].str.extract('(\\d+.?\\d*)')
        df['street_name']=df['address_with_number']
        df['street_name'].replace({'[\\s0-9]{2,}.*|\\d.*':''}, inplace=True, regex=True)

def remove_cols(df):
        df.drop(['Adresse', 'address_with_number'],axis=1,inplace=True)
        df1 = df[['Institution', 'zipcode', 'street_name', 'street_number', 'Lat', 'Lon']]
 
def reorder_cols(df):
    df1=df[['Institution', 'zipcode', 'street_name', 'street_number', 'Lat', 'Lon']]
    df1.rename(index=str, columns={"Institution": "institution", "zipcode":"zipcode",'street_number':'street_number', 'street_name':'street_name',"Lat": "lat", "Lon":"lon"},inplace=True)
    return df1
 
def process_data_frame():
        df=perform_acqusition()
        df.usecols(0,1,2,3)
        return df


