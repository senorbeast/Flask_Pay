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
records = [(501, 3000), (502, 4000), (503, 0)]

# insert multiple records in a single query
cur.executemany("INSERT INTO balancet VALUES(?,?);", records)
print("We have inserted", cur.rowcount, "records to the table.")
# commit the changes to db
conn.commit()


## txa records or rows in a list
records = [
    (543, 0, 10, "2022-02-12 19:19:51"),
    (546, 0, 11, "2022-02-12 19:29:51"),
    (547, 0, 12, "2022-02-12 19:39:51"),
]
# insert multiple records in a single query
cur.executemany("INSERT INTO transactionst VALUES(?,?,?,?);", records)
print("We have inserted", cur.rowcount, "records to the table.")
# commit the changes to db
conn.commit()


# close the connection
conn.close()
