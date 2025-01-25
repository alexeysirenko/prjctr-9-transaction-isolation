CREATE DATABASE testdb;

\c testdb;

CREATE TABLE IF NOT EXISTS test_table (
    id SERIAL PRIMARY KEY,
    value INT NOT NULL
);

INSERT INTO test_table (value) VALUES (10);