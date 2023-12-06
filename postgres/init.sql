CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY,
    nickname VARCHAR ( 50 ) NOT NULL,
    passhash VARCHAR ( 100 ) NOT NULL,
    email VARCHAR ( 50 ) NOT NULL UNIQUE,
    disabled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS pets (
    pet_id serial PRIMARY KEY,
    user_id integer REFERENCES users,
    first_name VARCHAR ( 50 ) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);
