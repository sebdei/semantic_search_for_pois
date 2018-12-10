-- CREATE script for core points of interests table
-- 

CREATE TABLE IF NOT EXISTS points_of_interests (
    id serial PRIMARY KEY, 
    name character varying, 
    street_name character varying, 
    street_number character varying, 
    zip_code character varying, 
    long numeric, 
    lat numeric, 
    opening_hours character varying, 
    weighted_word2vec json
);