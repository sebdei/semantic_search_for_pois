from .persistence_service import get_all_points_of_interests
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

def get_all_points_of_interests_as_dataframe():
    columns = [ID, NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT, OPENING_HOURS, WEIGHTED_WORD2VEC]
    return pd.DataFrame(get_all_points_of_interests(), columns = columns).set_index(ID)
