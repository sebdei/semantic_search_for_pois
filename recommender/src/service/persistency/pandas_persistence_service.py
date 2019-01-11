from .persistence_service import insert_into_points_of_interests, get_all_points_of_interests, get_all_odb_pois, get_all_osm_pois, insert_into_osm_pois, insert_into_odb_pois
import pandas as pd
from .data_model import *

# points of interests

def insert_df_into_points_of_interests(df):
    for _, row in df.iterrows():
        insert_into_points_of_interests(row[NAME], row[STREET_NAME], row[STREET_NUMBER], row[ZIP_CODE], row[LONG], row[LAT], row[OPENING_HOURS], row[IS_BUILDING], row[FEATURE_VECTOR], row[SOURCE])

def get_all_points_of_interests_as_df():
    return pd.DataFrame(get_all_points_of_interests(), columns = POI_COLUMNS).set_index(ID)

# OSM POIs

def insert_df_into_osm_pois(df):
    for _, row in df.iterrows():
        insert_into_osm_pois(row[ADDR_CITY], row[ADDR_COUNTRY], row[ADDR_HOUSENUMBER], row[ADDR_POSTCODE], row[ADDR_STREET],
        row[OPENING_HOURS], row[AMENITY], row[URL], row[NAME], row[NAME_DE], row[LEISURE], row[LONG], row[LAT], row[BUILDING], row[WIKIPEDIA], row[SOURCE], row[OSM_ID])

def get_all_osm_pois_as_df():    
    return pd.DataFrame(get_all_osm_pois(), columns = OSM_COLUMNS).set_index(ID)

# ODB POIs

def insert_df_into_odb_pois(df):
    for _, row in df.iterrows():
        insert_into_odb_pois(row[NAME], row[STREET_NAME], row[STREET_NUMBER], row[ZIP_CODE], row[LONG], row[LAT])

def get_all_odb_pois_as_df():
    return pd.DataFrame(get_all_odb_pois(), columns = ODB_COLUMNS).set_index(ID) 