# from src.service.acquisition.open_street_map import import_osm_points_of_interest
# from src.service.acquisition.open_data_berlin import import_odb_points_of_interest
# from src.service.acquisition.schema_fusion import import_into_poi_table

# from src.service.embedding_preprocess import embedding_preprocess
from src.service.acquisition.restore_default import restore_default_database

from src.web import flask

def run():
    # do a manual import of from source (ODB/OSM/Wikipedia/VisitBerlin)
    # create_schemata()
    # import_odb_points_of_interest()
    # import_osm_points_of_interest()
    # import_into_poi_table()

    # drop all tables and import default data
    restore_default_database()

    flask.bind_routes()

    # (re-) calculate the word embedding feature vector
    # embedding_preprocess.init_word_embeddings_calculation_for_articles()
