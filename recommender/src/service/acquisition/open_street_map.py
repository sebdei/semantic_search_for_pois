import overpy
import time
import pandas as pd
from ..persistency import pandas_persistence_service
from ..persistency import persistence_service
from ..persistency.data_model import *

# https://taginfo.openstreetmap.org/keys/leisure#values

leisures = [
    "water_park",
    "sports_centre",
    "nature_reserve",
    "park",
    "stadium",
    "golf_course",
    "miniature_golf",
    "escape_game",
    "swimming_area"
]

# https://wiki.openstreetmap.org/wiki/Key:amenity

amenities = [
    "theatre",
    "cinema",
    "arts_centre",
    "fountain",
    "planetarium"
]

# https://wiki.openstreetmap.org/wiki/Key:tourism

tourism_activities = [
    "aquarium",
    "artwork",
    "attraction",
    "gallery",
    "museum",
    "theme_park",
    "viewpoint",
    "zoo",
    "yes"
]

tag_schema_assignment = {
    'addr:city': ADDR_CITY,
    'addr:country': ADDR_COUNTRY,
    'addr:housenumber': ADDR_HOUSENUMBER,
    'addr:postcode': ADDR_POSTCODE,
    'addr:street': ADDR_STREET,
    'amenity': AMENITY,
    'contact:website': URL,
    'leisure': LEISURE,
    'tourism': TOURISM,
    'name': NAME,
    'name:en': NAME,
    'name:de': NAME_DE,
    'opening_hours': OPENING_HOURS,
    'url': URL,
    'website': URL,
    'wikipedia': WIKIPEDIA,
    'building': BUILDING,
}

way_query_template = """
area["ISO3166-2"="DE-BE"];
(
    way["leisure"="%s"](area);
);
out center;
"""

node_query_template = """
area["ISO3166-2"="DE-BE"];
(
    node["amenity"="%s"](area);
);
out;
"""

node_tourism_query_template = """
area["ISO3166-2"="DE-BE"];
(
    node["tourism"="%s"](area);
);
out;
"""


api = overpy.Overpass()

# could possibly be extended by https://wiki.openstreetmap.org/wiki/Key:tourism

def import_osm_points_of_interest():

    osm_data_frame = pd.DataFrame(columns = OSM_COLUMNS)

    # query for ways

    for leisure in leisures:
        try:
            r = api.query(str.format(way_query_template % leisure))
        except:
            # try again after a short break
            time.sleep(15)
            print('Trying again in a few seconds ...')
            r = api.query(str.format(way_query_template % leisure))

        print('Found %d ways for leisure %s' % (len(r.get_ways()), leisure))

        for way in r.get_ways():
            row = pd.Series([None] * len(OSM_COLUMNS), OSM_COLUMNS)
            
            for tag in way.tags.keys():
                if tag in tag_schema_assignment.keys():
                    col = tag_schema_assignment.get(tag)
                    value = way.tags.get(tag)
                    row[col] = value
            
            row[LAT] = way.center_lat
            row[LONG] = way.center_lon
            row[OSM_ID] = way.id
            row[SOURCE] = "osm:way"

            osm_data_frame = osm_data_frame.append([row], sort = False)
        
    # query for nodes

    for amenity in amenities:
        try:
            r = api.query(str.format(node_query_template % amenity))
        except:
            print('Something went wrong, trying again in a few seconds ...')
            time.sleep(5)
            r = api.query(str.format(node_query_template % amenity))

        print('Found %d nodes for amenity %s' % (len(r.get_nodes()), amenity))

        for node in r.get_nodes():
            row = pd.Series([None] * len(OSM_COLUMNS), OSM_COLUMNS)
            
            for tag in node.tags.keys():
                if tag in tag_schema_assignment.keys():
                    col = tag_schema_assignment.get(tag)
                    value = node.tags.get(tag)
                    row[col] = value
            
            row[LAT] = node.lat
            row[LONG] = node.lon
            row[OSM_ID] = node.id
            row[SOURCE] = "osm:node"

            osm_data_frame = osm_data_frame.append([row], sort = False)

    # query for toursim nodes

    for activity in tourism_activities:
        try:
            r = api.query(node_tourism_query_template % activity)
        except:
            print('Something went wrong, trying again in a few seconds ...')
            time.sleep(5)
            r = api.query(node_tourism_query_template % activity)

        print('Found %d nodes for tourism-related activity %s' % (len(r.get_nodes()), activity))

        for node in r.get_nodes():
            row = pd.Series([None] * len(OSM_COLUMNS), OSM_COLUMNS)

            for tag in node.tags.keys():
                if tag in tag_schema_assignment.keys():
                    col = tag_schema_assignment.get(tag)
                    value = node.tags.get(tag)
                    row[col] = value
            
            row[LAT] = node.lat
            row[LONG] = node.lon
            row[OSM_ID] = node.id
            row[SOURCE] = "osm:tourism-node"

            osm_data_frame = osm_data_frame.append([row], sort = False)


    persistence_service.truncate_osm_pois()
    pandas_persistence_service.insert_df_into_osm_pois(osm_data_frame)
    print("Loaded", len(osm_data_frame), "POIs from OSM into DB")
