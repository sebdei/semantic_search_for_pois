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

# POI columns

POI_COLUMNS = [ID, NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT, OPENING_HOURS, IS_BUILDING, FEATURE_VECTOR, SOURCE]

# ODB columns

ODB_COLUMNS = [ID, NAME, STREET_NAME, STREET_NUMBER, ZIP_CODE, LONG, LAT]

# OSM columns

OSM_COLUMNS = [ID, ADDR_CITY, ADDR_COUNTRY, ADDR_HOUSENUMBER, ADDR_POSTCODE, ADDR_STREET,
OPENING_HOURS, AMENITY, URL, NAME, NAME_DE, LEISURE, LONG, LAT, BUILDING, WIKIPEDIA, SOURCE, OSM_ID]
