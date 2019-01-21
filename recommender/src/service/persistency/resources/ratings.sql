-- CREATE script for ratings table
--

CREATE TABLE IF NOT EXISTS ratings (
    u_id integer REFERENCES users(id) ON DELETE CASCADE,
    poi_id integer REFERENCES points_of_interests(id) ON DELETE CASCADE,
    rating boolean,

    PRIMARY KEY (u_id, poi_id)
);
