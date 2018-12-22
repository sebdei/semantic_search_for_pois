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

def create_initial_schema():
    cur.execute(poi_schema)
    cur.execute(osm_schema)
    cur.execute(odb_schema)
    conn.commit()

# CRUD core POI table

def delete_from_points_of_interests(id):
    cur.execute("DELETE FROM points_of_interests WHERE id=%s", [id])
    conn.commit()

def truncate_points_of_interests():
    cur.execute("TRUNCATE TABLE points_of_interests")
    conn.commit()

def get_points_of_interests_by_id(id):
    cur.execute("SELECT * FROM points_of_interests WHERE id= %s", [id])

    return cur.fetchone()

def get_all_points_of_interests():
    cur.execute("SELECT * FROM points_of_interests")

    return cur.fetchall()

def insert_into_points_of_interests(name, street_name, street_number, zip_code, long, lat, opening_hours, feature_vector, source):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('points_of_interests')),
            [name, street_name, street_number, zip_code, long, lat, opening_hours, feature_vector, source]
    )
    conn.commit()

def update_values_of_points_of_interests(id, name, street_name, street_number, zip_code, long, lat, opening_hours, feature_vector, source):
    cur.execute((   "UPDATE points_of_interests SET "
                    "name= %s, street_name=%s, street_number=%s, zip_code=%s, long=%s, lat=%s, opening_hours=%s, feature_vector=%s, source=%s"
                    " WHERE id =%s"
                ), [name, street_name, street_number, zip_code, long, lat, opening_hours, feature_vector,source,id])
    conn.commit()

def update_feature_vector_by_id(id, feature_vector_json):
    cur.execute("UPDATE points_of_interests SET feature_vector = array_to_json(%s) WHERE id= %s", [feature_vector_json, id])
    conn.commit()

# OSM Points of Interest

def insert_into_osm_pois(addr_city, addr_country, addr_housenumber, addr_postcode, addr_street,
        opening_hours, amenity, url, name, name_de, leisure, long, lat, building, wikipedia, source, osm_id):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('osm_points_of_interests')),
            [addr_city, addr_country, addr_housenumber, addr_postcode, addr_street,
            opening_hours, amenity, url, name, name_de, leisure, long, lat, building, wikipedia, source, osm_id]
    )
    conn.commit()

def get_all_osm_pois():
    cur.execute("SELECT * FROM osm_points_of_interests")

    return cur.fetchall()

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