from .persistence_service import get_all_points_of_interests, insert_into_osm_pois
import pandas as pd

ID = 'id'
LONG = 'long'
LAT = 'lat'
STREET_NAME = 'street_name'
STREET_NUMBER = 'street_number'
NAME = 'name'
OPENING_HOURS = 'opening_hours'
WEIGHTED_WORD2VEC = 'weighted_word2vec'
ZIP_CODE = 'zip_code'
ADDR_CITY = "addr_city"
ADDR_COUNTRY = "addr_country"
ADDR_HOUSENUMBER = "addr_housenumber"
ADDR_POSTCODE = "addr_postcode"
ADDR_STREET = "addr_street"
AMENITY = "amenity"
URL = "url"
NAME_DE = "name_de"
LEISURE = "leisure"
BUILDING = "building"
WIKIPEDIA = "wikipedia"
SOURCE = "source"
OSM_ID = "osm_id"

def get_all_points_of_interests_as_dataframe():
    columns = [ID, NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT, OPENING_HOURS, WEIGHTED_WORD2VEC]
    return pd.DataFrame(get_all_points_of_interests(), columns = columns).set_index(ID)

def insert_data_frame_into_osm_pois(df):
    for idx, row in df.iterrows():
        insert_into_osm_pois(row[ADDR_CITY], row[ADDR_COUNTRY], row[ADDR_HOUSENUMBER], row[ADDR_POSTCODE], row[ADDR_STREET],
        row[OPENING_HOURS], row[AMENITY], row[URL], row[NAME], row[NAME_DE], row[LEISURE], row[LONG], row[LAT], row[BUILDING], row[WIKIPEDIA], row[SOURCE], row[OSM_ID])
