import psycopg2
import os
from psycopg2 import sql

# set-up stuff

def create_connection():
    db_connection = os.getenv('DB_CONNECTION', "dbname='admin' user='admin' host='localhost' port=5433 password='admin'")
    conn = psycopg2.connect(db_connection)
    cur = conn.cursor()

    return cur, conn

cur, conn = create_connection()

poi_schema = open(os.path.join(os.path.dirname(__file__), 'resources/points_of_interests.sql')).read()
osm_schema = open(os.path.join(os.path.dirname(__file__), 'resources/osm_points_of_interests.sql')).read()
odb_schema = open(os.path.join(os.path.dirname(__file__), 'resources/odb_points_of_interests.sql')).read()
query_wiki_schema = open(os.path.join(os.path.dirname(__file__), 'resources/query_data_wikipedia.sql')).read()
query_visitberlin_schema = open(os.path.join(os.path.dirname(__file__), 'resources/query_data_visitberlin.sql')).read()

def create_schemata():
    cur.execute(poi_schema)
    cur.execute(osm_schema)
    cur.execute(odb_schema)
    cur.execute(query_wiki_schema)
    cur.execute(query_visitberlin_schema)
    print('Created required tables in PostgreSQL')
    conn.commit()

# immediately execute after definition
create_schemata()

##### CRUD operations #####

def drop_all():
    tables = [
        "odb_points_of_interests",
        "osm_points_of_interests",
        "points_of_interests",
        "query_data_wikipedia",
        "query_data_visitberlin"
    ]
    for table in tables:
        try:
            cur.execute("DROP TABLE %s CASCADE" % (table))
            print("Dropped table %s" % (table))
        except:
            print("Could not drop table %s" % (table))

# CRUD core POI table

def delete_from_points_of_interests(id):
    cur.execute("DELETE FROM points_of_interests WHERE id=%s", [id])
    conn.commit()

def truncate_points_of_interests():
    cur.execute("TRUNCATE TABLE points_of_interests CASCADE")
    conn.commit()

def get_points_of_interests_by_id(id):
    cur.execute("SELECT * FROM points_of_interests WHERE id= %s", [id])

    return cur.fetchone()

def get_all_points_of_interests():
    cur.execute("SELECT * FROM points_of_interests")

    return cur.fetchall()

def insert_into_points_of_interests(id, name, street_name, street_number, zip_code, long, lat, opening_hours, is_building, feature_vector, source):
    if id == None:
        cur.execute(
            sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                .format(sql.Identifier('points_of_interests')),
                [name, street_name, street_number, zip_code, long, lat, opening_hours, is_building, feature_vector, source]
        )
    else:
        cur.execute(
            sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                .format(sql.Identifier('points_of_interests')),
                [id, name, street_name, street_number, zip_code, long, lat, opening_hours, is_building, feature_vector, source]
        )

    conn.commit()

def update_values_of_points_of_interests(id, name, street_name, street_number, zip_code, long, lat, opening_hours, is_building, feature_vector, source):
    cur.execute((   "UPDATE points_of_interests SET "
                    "name= %s, street_name=%s, street_number=%s, zip_code=%s, long=%s, lat=%s, opening_hours=%s, is_building=%s, feature_vector=%s, source=%s"
                    " WHERE id =%s"
                ), [name, street_name, street_number, zip_code, long, lat, opening_hours, feature_vector,source,id])
    conn.commit()

def update_feature_vector_by_id(id, feature_vector_json):
    cur.execute("UPDATE points_of_interests SET feature_vector = array_to_json(%s) WHERE id= %s", [feature_vector_json, id])
    conn.commit()

# OSM Points of Interest

def insert_into_osm_pois(id, addr_city, addr_country, addr_housenumber, addr_postcode, addr_street,
        opening_hours, amenity, url, name, name_de, leisure, tourism, long, lat, building, wikipedia, source, osm_id):
    if id == None:
        cur.execute(
            sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                .format(sql.Identifier('osm_points_of_interests')),
                [addr_city, addr_country, addr_housenumber, addr_postcode, addr_street,
                opening_hours, amenity, url, name, name_de, leisure, tourism, long, lat, building, wikipedia, source, osm_id]
        )
    else:
        cur.execute(
            sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                .format(sql.Identifier('osm_points_of_interests')),
                [id, addr_city, addr_country, addr_housenumber, addr_postcode, addr_street,
                opening_hours, amenity, url, name, name_de, leisure, tourism, long, lat, building, wikipedia, source, osm_id]
        )
    conn.commit()

def get_all_osm_pois():
    cur.execute("SELECT * FROM osm_points_of_interests")

    return cur.fetchall()

def truncate_osm_pois():
    cur.execute("TRUNCATE TABLE osm_points_of_interests CASCADE")
    conn.commit()

# ODB Points of Interest

def insert_into_odb_pois(id, name, street_name, street_number, zip_code, long, lat):
    if id == None:
        cur.execute(
            sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)")
                .format(sql.Identifier('odb_points_of_interests')),
                [name, street_name, street_number, zip_code, long, lat]
        )
    else:
        cur.execute(
            sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s)")
                .format(sql.Identifier('odb_points_of_interests')),
                [id, name, street_name, street_number, zip_code, long, lat]
        )
    conn.commit()

def get_all_odb_pois():
    cur.execute("SELECT * FROM odb_points_of_interests")

    return cur.fetchall()

def truncate_odb_pois():
    cur.execute("TRUNCATE TABLE odb_points_of_interests CASCADE")
    conn.commit()

# Queried wikipedia data

def get_queried_pois_wikipedia():
    cur.execute("SELECT poi_id FROM query_data_wikipedia")
    return cur.fetchall()

def insert_query_data_wikipedia(poi_id, wiki_title, wiki_url, wiki_text):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s)")
            .format(sql.Identifier('query_data_wikipedia')),
            [poi_id, wiki_title, wiki_url, wiki_text]
    )
    conn.commit()

def get_wikipedia_data():
    cur.execute("SELECT * FROM query_data_wikipedia")

    return cur.fetchall()

# Queried visitberlin data

def get_queried_pois_visitberlin():
    cur.execute("SELECT poi_id FROM query_data_visitberlin")
    
    return cur.fetchall()

def insert_query_data_visitberlin(poi_id, visitberlin_title, visitberlin_url, visitberlin_text):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s)")
            .format(sql.Identifier('query_data_visitberlin')),
            [poi_id, visitberlin_title, visitberlin_url, visitberlin_text]
    )
    conn.commit()

def get_visitberlin_data():
    cur.execute("SELECT * FROM query_data_visitberlin")

    return cur.fetchall()

# Combined visitberlin and wikipedia texts per ID

text_query = """
SELECT visitberlin_text, wiki_text
FROM query_data_visitberlin as vb
JOIN query_data_wikipedia as wiki
ON vb.poi_id = wiki.poi_id
WHERE vb.poi_id = {}
"""

def get_text_for_poi(id):
    """
    Gives the stored Visitberlin and Wikipedia text for a given POI, if they exist
    """

    cur.execute(sql.SQL(text_query.format((id))))

    query_result = cur.fetchall()

    if len(query_result) != 1:
        return None, None
    else:
        visitberlin_text, wiki_text = query_result[0]

        # Remove some of the ugly markup
        wiki_text = ''.join((ch if ch != '=' else '') for ch in wiki_text)

        return visitberlin_text, wiki_text

