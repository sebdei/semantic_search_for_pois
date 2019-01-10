import psycopg2
from psycopg2 import sql

def create_connection():
    conn = psycopg2.connect("dbname='admin' user='admin' host='localhost' port=5433 password='admin'")
    cur = conn.cursor()

    return cur, conn

cur, conn = create_connection()

initial_schema = (  "CREATE TABLE points_of_interests ("
                    "id serial PRIMARY KEY, "
                    "name character varying, "
                    "street_name character varying, "
                    "street_number character varying, "
                    "zip_code character varying, "
                    "long numeric, "
                    "lat numeric, "
                    "opening_hours character varying, "
                    "weighted_word2vec json"
                    ");")

<<<<<<< Updated upstream
=======
def create_connection():
    conn = psycopg2.connect("dbname='jensmechelhoff' user='jensmechelhoff' host='localhost'")
    cur = conn.cursor()

    return cur, conn

cur, conn = create_connection()

>>>>>>> Stashed changes
def create_initial_schema():
    cur.execute(initial_schema)
    conn.commit()

def delete_from_points_of_interests(id):
    cur.execute("DELETE FROM points_of_interests WHERE id=%s", [id])
    conn.commit()

def get_points_of_interests_by_id(id):
    cur.execute("SELECT * FROM points_of_interests WHERE id= %s", [id])

    return cur.fetchone()

def get_all_points_of_interests():
    cur.execute("SELECT * FROM points_of_interests")

    return cur.fetchall()

def insert_into_points_of_interests(name, street_name, street_number, zip_code, long, lat, opening_hours, weighted_word2vec):
    cur.execute(
        sql.SQL("INSERT INTO {} VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)")
            .format(sql.Identifier('points_of_interests')),
            [name, street_name, street_number, zip_code, long, lat, opening_hours, weighted_word2vec]
    )
    conn.commit()

def update_values_of_points_of_interests(id, name, street_name, street_number, zip_code, long, lat, opening_hours, weighted_word2vec):
    cur.execute((   "UPDATE points_of_interests SET "
                    "name= %s, street_name=%s, street_number=%s, zip_code=%s, long=%s, lat=%s, opening_hours=%s, weighted_word2vec=%s"
                    " WHERE id =%s"
                ), [name, street_name, street_number, zip_code, long, lat, opening_hours, weighted_word2vec,id])
    conn.commit()

def update_weighted_word2vec_by_id(id, word2vec_json):
    cur.execute("UPDATE points_of_interests SET  weighted_word2vec = array_to_json(%s) WHERE id= %s", [word2vec_json, id])
    conn.commit()
