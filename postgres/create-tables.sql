CREATE DATABASE testdb;

\c testdb;

CREATE TABLE IF NOT EXISTS test_table (
    id SERIAL PRIMARY KEY,
    value INT NOT NULL
);

INSERT INTO test_table (value) VALUES (10);

CREATE USER testuser WITH PASSWORD 'testpassword';
GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;
