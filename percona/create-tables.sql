CREATE DATABASE IF NOT EXISTS testdb;

USE testdb;

CREATE TABLE IF NOT EXISTS test_table (
    id INT PRIMARY KEY AUTO_INCREMENT,
    value INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO test_table (value) VALUES (10);