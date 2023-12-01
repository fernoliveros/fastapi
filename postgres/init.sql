CREATE TABLE IF NOT EXISTS students (
    student_id serial PRIMARY KEY,
    first_name VARCHAR ( 50 ) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);