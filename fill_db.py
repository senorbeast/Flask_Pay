from flask import Flask
import sqlite3

app = Flask(__name__)

# INSERT INTO balancet (account_no, balance)
# VALUES (100, 10000);
# INSERT INTO balancet (account_no, balance)
# VALUES (101, 7000);
# INSERT INTO balancet (account_no, balance)
# VALUES (102, 5000);
# INSERT INTO balancet (account_no, balance)
# VALUES (103, 2000);
# INSERT INTO balancet (account_no, balance)
# VALUES (104, 12000);
# INSERT INTO balancet (account_no, balance)
# VALUES (105, 8000);
# INSERT INTO balancet (account_no, balance)
# VALUES (107, 0);
# INSERT INTO balancet (account_no, balance)
# VALUES (108, 9999999);

# INSERT INTO transactionst
# VALUES (2, -50, 102, "2021-2-12 12:20");

conn = sqlite3.connect("bank.sqlite")
cur = conn.cursor()

## balance records or rows in a list
records = [(500, 3000), (501, 4000), (502, 0)]

# insert multiple records in a single query
cur.executemany("INSERT INTO balancet VALUES(?,?);", records)
print("We have inserted", cur.rowcount, "records to the table.")
# commit the changes to db
conn.commit()


## txa records or rows in a list
records = [
    (100, 500, 50, "2022-02-12 19:19:51"),
    (101, 501, -50, "2022-02-12 19:19:51"),
    (102, 502, 1337, "2022-02-12 19:19:51"),
]
# insert multiple records in a single query
cur.executemany("INSERT INTO transactionst VALUES(?,?,?,?);", records)
print("We have inserted", cur.rowcount, "records to the table.")
# commit the changes to db
conn.commit()


# close the connection
conn.close()
