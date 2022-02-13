import sqlite3

# https://docs.python.org/3/library/sqlite3.html

# Creating and connecting sqlite3 db
conn = sqlite3.connect("bank.sqlite")

# Cursor Object: used to execute SQL statements
cursor = conn.cursor()

## One Account can have multiple transactions (1 to many relation) using Foreign Key

# Transaction Relation(Table) with attributes(columns):
#   id (unique)
#   amount
#   account_no
#   created_datetime
sql_query = """ CREATE TABLE transactionst (
    id INT PRIMARY KEY,
    amount REAL NOT NULL,
    account_no INT NOT NULL,
    created_datetime TEXT NOT NULL,
    FOREIGN KEY (account_no) REFERENCES balancet(account_no)
)"""
cursor.execute(sql_query)


# Balances Relation with attributes:
#   account_no (unique)
#   balance
sql_query = """ CREATE TABLE balancet (
    account_no INT PRIMARY KEY,
    balance REAL NOT NULL DEFAULT 0,
    CHECK(balance >=0)

)"""
cursor.execute(sql_query)


#############################################################
