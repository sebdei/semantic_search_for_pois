-- CREATE script for table of scraped wikipedia data
-- 

CREATE TABLE IF NOT EXISTS query_data_wikipedia(
	poi_id integer PRIMARY KEY REFERENCES points_of_interests(id) ON DELETE CASCADE,
    wiki_title character varying,
	wiki_url character varying,
	wiki_text character varying
)