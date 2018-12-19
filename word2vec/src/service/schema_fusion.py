from .persistency import pandas_persistency_service as pps
from .persistency import persistence_service as ps
import math
import string
import pandas as pd
import re
from py_stringmatching import SmithWaterman

ID = 'id'
LONG = 'long'
LAT = 'lat'
STREET_NAME = 'street_name'
STREET_NUMBER = 'street_number'
NAME = 'name'
OPENING_HOURS = 'opening_hours'
WEIGHTED_WORD2VEC = 'weighted_word2vec'
SOURCE = 'source'
ZIP_CODE = 'zip_code'
POI_COLUMNS = [ID, NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT, OPENING_HOURS, WEIGHTED_WORD2VEC, SOURCE]

def import_into_poi_table():
    # Truncate current POIs, get empty dataframe
    ps.truncate_points_of_interests()
    poi_df = pps.get_all_points_of_interests_as_df()

    # ODB Import
    odb_pois = pps.get_all_odb_pois_as_df()
    odb_pois = prepare_odb_pois(odb_pois)
    poi_df = import_odb_pois(poi_df, odb_pois)

    # OSM Import
    osm_df = pps.get_all_osm_pois_as_df()
    osm_df = prepare_osm_pois(osm_df)
    poi_df = import_osm_pois(poi_df, osm_df)

    # Commit Data
    pps.insert_df_into_points_of_interests(poi_df)

# ODB

def prepare_odb_pois(odb_pois):
    # add missing columns
    odb_pois['opening_hours'] = None
    odb_pois['weighted_word2vec'] = None
    odb_pois['source'] = 'odb'

    return odb_pois

def import_odb_pois(poi_df, odb_df):
    # first import, definitely duplicate free
    poi_df = poi_df.append(odb_df, ignore_index=True)
    return poi_df

# OSM

def prepare_osm_pois(osm_df):
    # remove places without name
    before = len(osm_df)
    osm_df = osm_df[osm_df['name'].notnull()]
    after = len(osm_df)
    print('removed',before-after,'POIs from OSM Data where the name in null.')
    return osm_df
    
def import_osm_pois(poi_df, osm_df):
    sw = SmithWaterman()

    for idx, osm_row in osm_df.iterrows():
        lat = float(osm_row['lat'])
        lng = float(osm_row['long'])
        close_pois = select_close_pois(poi_df, lat, lng)

        merged = False

        if len(close_pois) != 0:
            name = clean_name(str(osm_row['name']))
            
            for idx, maybe_duplicate in close_pois.iterrows():
                dup_name = clean_name(str(maybe_duplicate['name']))

                score = sw.get_raw_score(name, dup_name) / max(len(name), len(dup_name))

                if osm_row['name_de'] != None:
                    name_de = clean_name(str(osm_row['name_de']))

                    score_de = sw.get_raw_score(name_de, dup_name) / max(len(name_de), len(dup_name))
                    score = max(score, score_de)
                
                if score >= 0.6:
                    consolidated_row = merge_osm_conflict(osm_row, maybe_duplicate)
                    poi_df.loc[idx] = consolidated_row
                    merged = True

        if not merged:
            row = convert_osm_to_poi(osm_row)
            poi_df = poi_df.append(row, ignore_index=True)
    
    return poi_df

def convert_osm_to_poi(osm_row):
    poi_row = pd.Series([None] * len(POI_COLUMNS), POI_COLUMNS)
    poi_row['name'] = osm_row['name']
    poi_row['street_name'] = osm_row['addr_street']
    poi_row['street_number'] = osm_row['addr_housenumber']
    poi_row['zip_code'] = osm_row['addr_postcode']
    poi_row['long'] = osm_row['long']
    poi_row['lat'] = osm_row['lat']
    poi_row['opening_hours'] = osm_row['opening_hours']
    poi_row['weighted_word2vec'] = None
    poi_row['source'] = osm_row['source'] + '(' + osm_row['osm_id'] + ')'

    return poi_row

# Merging Helpers

def merge_osm_conflict(osm_row, poi_row):
    print('merging', poi_row['name'], 'and', osm_row['name'])

    osm_poi_row = convert_osm_to_poi(osm_row)

    return consolidate_rows(poi_row, osm_poi_row)

def consolidate_rows(row_1, row_2):
    """
    Returns the combination of row_1 and row_2, preferring row_1's data
    """
    consolidated_row = pd.Series()
    consolidated_row['name'] = row_1['name'] or row_2['name']
    consolidated_row['street_name'] = row_1['street_name'] or row_2['street_name']
    consolidated_row['street_number'] = row_1['street_number'] or row_2['street_number']
    consolidated_row['zip_code'] = row_1['zip_code'] or row_2['zip_code']
    consolidated_row['long'] = row_1['long'] or row_2['long']
    consolidated_row['lat'] = row_1['lat'] or row_2['lat']
    consolidated_row['opening_hours'] = row_1['opening_hours'] or row_2['opening_hours']
    consolidated_row['weighted_word2vec'] = row_1['weighted_word2vec'] or row_2['weighted_word2vec']
    consolidated_row['source'] = row_1['source'] + ';' + row_2['source']

    return consolidated_row

def select_close_pois(poi_df, lat, lng):
    d = 0.005
    return poi_df.loc[lambda x: (x['lat'] < lat + d) & (x['lat'] > lat - d) & (x['long'] < lng + d) & (x['long'] > lng - d)]

# Miscellaneous

def clean_name(query):
    exclude = set(string.punctuation)
    no_punctuation = ''.join((str.lower(ch) if ch not in exclude else ' ') for ch in query)
    no_punctuation = re.sub(r'\s+', ' ', no_punctuation)
    return no_punctuation