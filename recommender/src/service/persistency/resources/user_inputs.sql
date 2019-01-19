-- CREATE script for user_inputs table
-- 

CREATE TABLE IF NOT EXISTS user_inputs (
    u_id integer PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    input_text character varying,
    twitter_name character varying
);