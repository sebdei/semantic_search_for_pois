-- CREATE script for Open Data Berlin staging table
-- 

CREATE TABLE IF NOT EXISTS odb_points_of_interests (
    id serial PRIMARY KEY, 
    name character varying, 
    street_name character varying, 
    street_number character varying, 
    zip_code character varying, 
    long numeric, 
    lat numeric
);