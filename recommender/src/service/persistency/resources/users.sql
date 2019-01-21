-- CREATE script for users table
--

CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    email character varying UNIQUE, 
    feature_vector json,
    name character varying
);
