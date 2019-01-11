-- CREATE script for table of scraped visitberlin data
-- 

CREATE TABLE IF NOT EXISTS query_data_visitberlin(
	poi_id integer REFERENCES points_of_interests(id) ON DELETE CASCADE,
	visitberlin_url character varying,
	visitberlin_text character varying
)