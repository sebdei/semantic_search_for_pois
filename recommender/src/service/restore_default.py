import pandas as pd
import os
from .persistency import persistence_service as ps
from .persistency import pandas_persistence_service as pps
from .persistency.data_model import *

default_data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../default_data'))

odb_path = os.path.join(default_data_folder, 'odb_points_of_interests.csv')
osm_path = os.path.join(default_data_folder, 'osm_points_of_interests.csv')
poi_path = os.path.join(default_data_folder, 'points_of_interests.csv')
wiki_path = os.path.join(default_data_folder, 'query_data_wikipedia.csv')
visitberlin_path = os.path.join(default_data_folder, 'query_data_visitberlin.csv')

def restore_default_database():
    """
    Imports all default data into the database.
    """

    ps.drop_all()
    ps.create_schemata()

    # import ODB
    odb_df = pd.read_csv(odb_path, quotechar='"', escapechar="'")
    odb_df = odb_df.where((pd.notnull(odb_df)), None)
    pps.insert_df_into_odb_pois(odb_df)

    # import OSM
    osm_df = pd.read_csv(osm_path, quotechar='"', escapechar="'")
    osm_df = osm_df.where((pd.notnull(osm_df)), None)
    pps.insert_df_into_osm_pois(osm_df)

    # import POIs
    poi_df = pd.read_csv(poi_path, quotechar='"', escapechar="'")
    poi_df = poi_df.where((pd.notnull(poi_df)), None)
    pps.insert_df_into_points_of_interests(poi_df)

    # import Wikipedia query data
    wiki_df = pd.read_csv(wiki_path, quotechar='"', escapechar="'")
    wiki_df = wiki_df.where((pd.notnull(wiki_df)), None)
    pps.insert_df_into_wiki_data(wiki_df)

    # import VisitBerlin query data
    visitberlin_df = pd.read_csv(visitberlin_path, quotechar='"', escapechar="'")
    visitberlin_df = visitberlin_df.where((pd.notnull(visitberlin_df)), None)
    pps.insert_df_into_visitberlin_data(visitberlin_df)

    print('Restored default database state')