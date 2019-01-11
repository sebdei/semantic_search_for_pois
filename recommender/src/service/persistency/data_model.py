# all columns

ID = 'id'
LONG = 'long'
LAT = 'lat'
STREET_NAME = 'street_name'
STREET_NUMBER = 'street_number'
NAME = 'name'
OPENING_HOURS = 'opening_hours'
FEATURE_VECTOR = 'feature_vector'
ZIP_CODE = 'zip_code'
ADDR_CITY = 'addr_city'
ADDR_COUNTRY = 'addr_country'
ADDR_HOUSENUMBER = 'addr_housenumber'
ADDR_POSTCODE = 'addr_postcode'
ADDR_STREET = 'addr_street'
AMENITY = 'amenity'
URL = 'url'
NAME_DE = 'name_de'
LEISURE = 'leisure'
BUILDING = 'building'
WIKIPEDIA = 'wikipedia'
SOURCE = 'source'
OSM_ID = 'osm_id'
IS_BUILDING = 'is_building'
POI_ID = 'poi_id'
WIKI_TITLE = 'wiki_title'
WIKI_URL = 'wiki_url'
WIKI_TEXT = 'wiki_text'
VISITBERLIN_TITLE = 'visitberlin_title'
VISITBERLIN_URL = 'visitberlin_url'
VISITBERLIN_TEXT = 'visitberlin_text'

# POI columns

POI_COLUMNS = [ID, NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT, OPENING_HOURS, IS_BUILDING, FEATURE_VECTOR, SOURCE]

# ODB columns

ODB_COLUMNS = [ID, NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT]

# OSM columns

OSM_COLUMNS = [ID, ADDR_CITY, ADDR_COUNTRY, ADDR_HOUSENUMBER, ADDR_POSTCODE, ADDR_STREET,
OPENING_HOURS, AMENITY, URL, NAME, NAME_DE, LEISURE, LONG, LAT, BUILDING, WIKIPEDIA, SOURCE, OSM_ID]

# Wikipedia data columns

WIKI_COLUMNS = [POI_ID, WIKI_TITLE, WIKI_URL, WIKI_TEXT]

# Visitberlin data columns

VISITBERLIN_COLUMNS = [POI_ID, VISITBERLIN_TITLE, VISITBERLIN_URL, VISITBERLIN_TEXT]