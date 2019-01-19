from .persistence_service import *
import pandas as pd
from .data_model import *

# points of interests

def insert_df_into_points_of_interests(df):
    for _, row in df.iterrows():
        insert_into_points_of_interests(row[ID], row[NAME], row[STREET_NAME], row[STREET_NUMBER], row[ZIP_CODE], row[LONG], row[LAT], row[OPENING_HOURS], row[IS_BUILDING], row[FEATURE_VECTOR], row[SOURCE])

def get_all_points_of_interests_as_df():
    return pd.DataFrame(get_all_points_of_interests(), columns = POI_COLUMNS).set_index(ID)

def get_points_of_interests_by_id_as_df(id):
    return pd.DataFrame([get_points_of_interests_by_id(id)], columns = POI_COLUMNS)

# OSM POIs

def insert_df_into_osm_pois(df):
    for _, row in df.iterrows():
        insert_into_osm_pois(row[ID], row[ADDR_CITY], row[ADDR_COUNTRY], row[ADDR_HOUSENUMBER], row[ADDR_POSTCODE], row[ADDR_STREET],
        row[OPENING_HOURS], row[AMENITY], row[URL], row[NAME], row[NAME_DE], row[LEISURE], row[TOURISM], row[LONG], row[LAT], row[BUILDING], row[WIKIPEDIA], row[SOURCE], row[OSM_ID])

def get_all_osm_pois_as_df():
    return pd.DataFrame(get_all_osm_pois(), columns = OSM_COLUMNS).set_index(ID)

# ODB POIs

def insert_df_into_odb_pois(df):
    for _, row in df.iterrows():
        insert_into_odb_pois(row[ID], row[NAME], row[STREET_NAME], row[STREET_NUMBER], row[ZIP_CODE], row[LONG], row[LAT])

def get_all_odb_pois_as_df():
    return pd.DataFrame(get_all_odb_pois(), columns = ODB_COLUMNS).set_index(ID)

# Wikipedia query data

def get_all_wiki_data_as_df():
    return pd.DataFrame(get_wikipedia_data(), columns = WIKI_COLUMNS).set_index(POI_ID)

def insert_df_into_wiki_data(df):
    for _, row in df.iterrows():
        insert_query_data_wikipedia(row[POI_ID], row[WIKI_TITLE], row[WIKI_URL], row[WIKI_TEXT])

# Visitberlin query data

def get_all_visitberlin_data_as_df():
    return pd.DataFrame(get_visitberlin_data(), columns = VISITBERLIN_COLUMNS).set_index(POI_ID)

def insert_df_into_visitberlin_data(df):
    for _, row in df.iterrows():
        insert_query_data_visitberlin(row[POI_ID], row[VISITBERLIN_TITLE], row[VISITBERLIN_URL], row[VISITBERLIN_TEXT])

# Users data

def insert_df_into_users(df):
    for _, row in df.iterrows():
        insert_user(row[ID], row[EMAIL], row[FEATURE_VECTOR], row[NAME])

# User Inputs data

def insert_df_into_user_inputs(df):
    for _, row in df.iterrows():
        insert_user_input(row[U_ID], row[INPUT_TEXT], row[TWITTER_NAME])

# Ratings data

def get_all_ratings_as_df():
    return pd.DataFrame(get_all_ratings(), columns = RATINGS_COLUMNS)

def insert_df_into_ratings(df):
    for _, row in df.iterrows():
        insert_rating(row[U_ID], row[POI_ID], row[RATING])