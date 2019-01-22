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

all_schemata = [
    "odb_points_of_interests",
    "osm_points_of_interests",
    "points_of_interests",
    "query_data_wikipedia",
    "query_data_visitberlin",
    "users",
    "user_inputs",
    "ratings",
]

def create_schemata():
    for schema in all_schemata:
        create_query = open(os.path.join(os.path.dirname(__file__), 'resources/%s.sql' % (schema))).read()
        print("Created table %s" % (schema))

        cur.execute(create_query)

    print('Created all schemata in PostgreSQL')
    conn.commit()

##### CRUD operations #####

def drop_all():
    for schema in all_schemata:
        try:
            cur.execute("DROP TABLE %s CASCADE" % (schema))
            print("Dropped table %s" % (schema))
        except:
            print("Could not drop table %s" % (schema))
    print('Dropped all schemata in PostgreSQL')

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

def insert_into_points_of_interests(name, street_name, street_number, zip_code, long, lat, opening_hours, is_building, feature_vector, source):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('points_of_interests')),
            [name, street_name, street_number, zip_code, long, lat, opening_hours, is_building, feature_vector, source]
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

def insert_into_osm_pois(addr_city, addr_country, addr_housenumber, addr_postcode, addr_street,
    opening_hours, amenity, url, name, name_de, leisure, tourism, long, lat, building, wikipedia, source, osm_id):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('osm_points_of_interests')),
            [addr_city, addr_country, addr_housenumber, addr_postcode, addr_street,
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

def insert_into_odb_pois(name, street_name, street_number, zip_code, long, lat):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('odb_points_of_interests')),
            [name, street_name, street_number, zip_code, long, lat]
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

# Ratings

def get_all_ratings():
    cur.execute("SELECT * FROM ratings")

    return cur.fetchall()

def get_poi_rating_for_user(poi_id, user_id):
    cur.execute(
        sql.SQL("SELECT * FROM {} WHERE poi_id = %s AND user_id = %s")
            .format(sql.Identifier('ratings')),
            [poi_id, user_id]
    )
    poi_user_rating = cur.fetchone()

    if poi_user_rating:
        return poi_user_rating[2]

def count_recommendations_by_user(user_id):
    cur.execute("SELECT count(*) FROM ratings WHERE user_id = %s", [user_id])
    return cur.fetchone()[0]

def upsert_rating(user_id, poi_id, liked):
    cur.execute(
        sql.SQL("INSERT INTO {} (user_id, poi_id, liked) VALUES (%s, %s, %s) " +
        "ON CONFLICT (user_id, poi_id) " +
        "DO UPDATE SET (user_id, poi_id, liked) = (EXCLUDED.user_id, EXCLUDED.poi_id, EXCLUDED.liked)")
            .format(sql.Identifier('ratings')),
            [user_id, poi_id, liked]
    )
    conn.commit()

# Users

def get_user_by_id(id):
    cur.execute("SELECT * FROM users WHERE id = %s", [id])

    return cur.fetchone()

def create_user():
    cur.execute(
        sql.SQL("INSERT INTO {} (id) VALUES (DEFAULT) RETURNING id")
            .format(sql.Identifier('users')),
    )

    user_id = cur.fetchone()[0]

    return user_id

def insert_user(email, name):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s)")
            .format(sql.Identifier('users')),
            [email, name]
    )
    conn.commit()

# User input

def get_user_input_for_id(id):
    cur.execute("SELECT * FROM user_inputs WHERE user_id = %s", [id])

    return cur.fetchone()

def insert_user_input(user_id, input_text, twitter_name):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (%s, %s, %s)")
            .format(sql.Identifier('user_inputs')),
            [user_id, input_text, twitter_name]
    )
    conn.commit()

# Get texts per ID

def get_wiki_text_for_id(id):
    query = 'SELECT wiki_url, wiki_text FROM query_data_wikipedia WHERE poi_id = {}'
    cur.execute(sql.SQL(query.format(id)))

    result = cur.fetchone()

    return result[0], result[1]

def get_visit_berlin_text_for_id(id):
    query = 'SELECT visitberlin_url, visitberlin_text FROM query_data_visitberlin WHERE poi_id = {}'
    cur.execute(sql.SQL(query.format(id)))

    result = cur.fetchone()

    return result[0], result[1]

def get_text_for_poi(id):
    wiki_url, wiki_text = get_wiki_text_for_id(id)

    result = {}

    if wiki_url and wiki_text :
        result['url'] = wiki_url
        result['text'] = wiki_text
    else:
        visitberlin_url, visit_berlin_text = get_visit_berlin_text_for_id(id)

        if visitberlin_url and visit_berlin_text:
            result['url'] = visitberlin_url
            result['text'] = visit_berlin_text

    return result
