-- CREATE script for OSM staging table
-- 

CREATE TABLE IF NOT EXISTS osm_points_of_interests (
    id serial PRIMARY KEY, 
    addr_city character varying, 
    addr_country character varying, 
    addr_housenumber character varying, 
    addr_postcode character varying, 
    addr_street character varying, 
    opening_hours character varying,
    amenity character varying,
    url character varying,
    name character varying,
    name_de character varying,
    leisure character varying,
    long numeric, 
    lat numeric,
    building character varying,
    wikipedia character varying,
    source character varying,
    osm_id character varying
);