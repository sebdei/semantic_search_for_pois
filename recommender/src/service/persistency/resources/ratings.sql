-- CREATE script for ratings table
--

CREATE TABLE IF NOT EXISTS ratings (
    user_id integer REFERENCES users(id) ON DELETE CASCADE,
    poi_id integer REFERENCES points_of_interests(id) ON DELETE CASCADE,
    liked boolean,

    PRIMARY KEY (user_id, poi_id)
);
