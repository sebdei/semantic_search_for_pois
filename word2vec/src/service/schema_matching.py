from .persistency import pandas_persistency_service

def import_into_poi_table():
    odb_pois = pandas_persistency_service.get_all_odb_pois_as_df()
    osm_pois = pandas_persistency_service.get_all_osm_pois_as_df()

    odb_pois['opening_hours'] = None
    odb_pois['weighted_word2vec'] = None

    # for testing and restoring previous behaviour
    pandas_persistency_service.insert_df_into_points_of_interests(odb_pois)