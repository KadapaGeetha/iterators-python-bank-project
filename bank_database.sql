create database Bank_management;

use Bank_management;

CREATE TABLE accounts (
    account_number INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    balance DECIMAL(10,2) NOT NULL
);


