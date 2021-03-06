import math
import string
import pandas as pd
import re
from py_stringmatching import SmithWaterman

from src.service.persistency import pandas_persistence_service as pps
from src.service.persistency import persistence_service as ps
from src.service.persistency.data_model import *

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
    poi_df[ID] = None
    pps.insert_df_into_points_of_interests(poi_df)

# ODB

def prepare_odb_pois(odb_pois):
    # add missing columns
    odb_pois[OPENING_HOURS] = None
    odb_pois[FEATURE_VECTOR] = None
    odb_pois[SOURCE] = 'odb'
    odb_pois[IS_BUILDING] = True # implicitly true for this dataset

    return odb_pois

def import_odb_pois(poi_df, odb_df):
    # first import, definitely duplicate free
    poi_df = poi_df.append(odb_df, ignore_index=True)
    return poi_df

# OSM

def prepare_osm_pois(osm_df):
    # remove places without name
    before = len(osm_df)
    osm_df = osm_df[osm_df[NAME].notnull()]
    after = len(osm_df)
    print('removed', before-after, 'POIs from OSM Data where the name is null.')
    return osm_df

def import_osm_pois(poi_df, osm_df):
    sw = SmithWaterman()

    for idx, osm_row in osm_df.iterrows():
        lat = float(osm_row[LAT])
        lng = float(osm_row[LONG])
        close_pois = select_close_pois(poi_df, lat, lng)

        merged = False

        if len(close_pois) != 0:
            name = clean_name(str(osm_row[NAME]))

            for idx, maybe_duplicate in close_pois.iterrows():
                dup_name = clean_name(str(maybe_duplicate[NAME]))

                score = sw.get_raw_score(name, dup_name) / max(len(name), len(dup_name))

                if osm_row[NAME_DE] != None:
                    name_de = clean_name(str(osm_row[NAME_DE]))

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
    poi_row[NAME] = osm_row[NAME]
    poi_row[STREET_NAME] = osm_row[ADDR_STREET]
    poi_row[STREET_NUMBER] = osm_row[ADDR_HOUSENUMBER]
    poi_row[ZIP_CODE] = osm_row[ADDR_POSTCODE]
    poi_row[LONG] = osm_row[LONG]
    poi_row[LAT] = osm_row[LAT]
    poi_row[OPENING_HOURS] = osm_row[OPENING_HOURS]
    # IS_BUILDING: either BUILDING is defined or it is a osm node (and not a osm way)
    poi_row[IS_BUILDING] = (osm_row[BUILDING] is not None and len(osm_row[BUILDING]) > 0) or (osm_row[SOURCE] == 'osm:node')
    poi_row[FEATURE_VECTOR] = None
    poi_row[SOURCE] = osm_row[SOURCE] + '(' + osm_row[OSM_ID] + ')'

    return poi_row

# Merging Helpers

def merge_osm_conflict(osm_row, poi_row):
    print('merging', poi_row[NAME], 'and', osm_row[NAME])

    osm_poi_row = convert_osm_to_poi(osm_row)

    return consolidate_rows(poi_row, osm_poi_row)

def consolidate_rows(row_1, row_2):
    """
    Returns the combination of row_1 and row_2, preferring row_1's data
    """
    consolidated_row = pd.Series()
    consolidated_row[NAME] = row_1[NAME] or row_2[NAME]
    consolidated_row[STREET_NAME] = row_1[STREET_NAME] or row_2[STREET_NAME]
    consolidated_row[STREET_NUMBER] = row_1[STREET_NUMBER] or row_2[STREET_NUMBER]
    consolidated_row[ZIP_CODE] = row_1[ZIP_CODE] or row_2[ZIP_CODE]
    consolidated_row[LONG] = row_1[LONG] or row_2[LONG]
    consolidated_row[LAT] = row_1[LAT] or row_2[LAT]
    consolidated_row[OPENING_HOURS] = row_1[OPENING_HOURS] or row_2[OPENING_HOURS]
    consolidated_row[IS_BUILDING] = row_1[IS_BUILDING] or row_2[IS_BUILDING]
    consolidated_row[FEATURE_VECTOR] = row_1[FEATURE_VECTOR] or row_2[FEATURE_VECTOR]
    consolidated_row[SOURCE] = row_1[SOURCE] + ';' + row_2[SOURCE]

    return consolidated_row

def select_close_pois(poi_df, lat, lng):
    d = 0.005
    return poi_df.loc[lambda x: (x[LAT] < lat + d) & (x[LAT] > lat - d) & (x[LONG] < lng + d) & (x[LONG] > lng - d)]

# Miscellaneous

def clean_name(query):
    exclude = set(string.punctuation)
    no_punctuation = ''.join((str.lower(ch) if ch not in exclude else ' ') for ch in query)
    no_punctuation = re.sub(r'\s+', ' ', no_punctuation)
    return no_punctuation
