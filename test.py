from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connecting to the db
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("bank.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


# List of Dict from cursor
def ldict_txa(cursor):
    list = [
        dict(id=row[0], amount=row[1], account_no=row[2], created_datetime=row[3])
        for row in cursor.fetchall()
    ]
    return list


def ldict_bal(cursor):
    list = [dict(account_no=row[0], balance=row[1]) for row in cursor.fetchall()]
    return list


conn = db_connection()
from_account_no = 104
to_account_no = 105
amount = 75.00

#! some how all these in 1 string dont work ?!!
debit = """UPDATE balancet 
    SET balance = balance - {amt} 
    WHERE account_no = {fa}
    """.format(
    amt=amount, fa=from_account_no
)
credit = """UPDATE balancet 
    SET balance = balance + {amt} 
    
    WHERE account_no = {ta}
    """.format(
    amt=amount, ta=to_account_no
)

# FROM and TO TXA
update_from_txa = """
    INSERT INTO transactionst(amount, account_no, created_datetime)
    VALUES( -{amt}, {fa}, datetime('now'))
""".format(
    amt=amount, fa=from_account_no
)
update_to_txa = """
    INSERT INTO transactionst(amount, account_no, created_datetime)
    VALUES( {amt}, {ta}, datetime('now'))
""".format(
    amt=amount, ta=to_account_no
)

cursord = conn.execute(debit)
cursorc = conn.execute(credit)
cursor_from_txa = conn.execute(update_from_txa)
cursor_to_txa = conn.execute(update_to_txa)

# COMMIT
conn.commit()

# Need to commit to read from database,
# could return payload w/o reading too ?
# Will give to_txa, from_txa (since desc order)
txa_rows = conn.execute("SELECT * FROM transactionst ORDER BY id DESC LIMIT 2;")

balance_rows = conn.execute(
    "SELECT * FROM balancet WHERE account_no={fa} OR account_no={ta}".format(
        fa=from_account_no, ta=to_account_no
    )
)
txas = ldict_txa(txa_rows)[::-1]  # from_txa, to_txa
bals = ldict_bal(balance_rows)  # from_bal, to_bal

payload = {
    "id": txas[0]["id"],
    "from": {
        "id": bals[0]["account_no"],
        "balance": bals[0]["balance"],
    },
    "to": {
        "id": bals[1]["account_no"],
        "balance": bals[1]["balance"],
    },
    "transfered": txas[1]["amount"],  # to_txa
    "created_datetime": txas[1]["created_datetime"],
}
print(payload)

# # @app.route("/Balance", methods = ["GET", "POST"])
# # def balance():
