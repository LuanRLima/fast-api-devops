CREATE DATABASE employees;
use employees;

CREATE TABLE employees (
first_name varchar(25),
last_name  varchar(25),
department varchar(15),
email  varchar(50)
);

INSERT INTO employees (first_name, last_name, department, email) VALUES ("Meu", "Nome", "Financeiro", "meu@email.com");