from flask import Flask, request, jsonify
import json
import sqlite3
import datetime

## Transfering money across two bank Accounts.

# NO ORM
# [✔] 1. Creats, request, jsonify Database + View the Transactions and Balances Table
# Operate on Database : Foreign Key - link

# * Transfer API : X amount of money from A to B with post request
# *   payloads for request and response are specified.

# [✔] 2. Validity and consistent data : ACID (BEGIN, COMMIT, ROLLBACK)
# ? Prevent 1 customer tapping twice : UI & _____
# Add more APIs for create a/c, money deposit etc

# [✔] 3. Manage the logic at the database level ( Managed by serialization and ACID methodology)
# What happens if your db becomes unavailable in the middle of logic? :
#   a. Before txa
#   b. During txa
# What happens under high concurrency? :
# SERIALIZATION
# BEGIN EXCLUSIVE lock - COMMIT, 1 Txa (ATOMICITY) + await till unlock
# Flask has inbuilt concurrency through its WSGI/ASGI production server. but need to wait for locked database

# [ ] A,B transfer money to C at same time :
# ? SERIALIZATION locking and unlocking db for read/write for  operation and async await flask ?
# BEGIN - COMMIT 1 Txa, Flask as a WSGI app, uses one worker to handle one request/response cycle.
# [ ] exclusive lock to remove read access...
# https://www.sqlite.org/lockingv3.html
#
# Old Rollback Journall Way (Maintains a Rollback Journal, with data till last commit):
#   Directly writes change to the db
#   COMMIT or ROLLBACK: Delete Rollback journal
#
# WAL Mode : (Origial Content is preserved in the db)
#   Writes changes to wal file
#   Multiple transactions can be COMMITTED to WAL file
#   Chekpointing - Wal file to db
#   Readers can read content before the initial commit

#  PySQLite does'nt autocommit

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
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


# * Transaction Table : Adding new transactions
@app.route("/transfer", methods=["POST"])
def transfer():
    """
    Transfer API, Method = POST,

    request body: {
        "from": "account_no",
        "to": "account_no",
        "amount": "money"
        }
    Balances Table
        Debit amount from "From A/C"
        Credit amount to "TO A/C"

    Transacton Table
        "From A/C" -amount date_created
        "To A/C"   +amount date_created

    commit changes to db only if no errors occur and db is online else rollback changes

    :return: json object
            {
            "id": "transaction_id",
            "from":{
                "id": "account_no",
                "balance": "current_balance"
            },
            "to":{
                "id": "account_no",
                "balance": "current_balance"
            },
            "transfered": "transfer_amount"
            "created_datetime": "transaction created time"
            }
    """
    from_account_no = request.form["from_account_no"]
    to_account_no = request.form["to_account_no"]
    amount = request.form["amount"]
    conn = db_connection()
    cursor = conn.cursor()
    # After connection with db
    if conn:
        # if DB is available after request and before commit
        try:
            #! some how all these in 1 string dont work ?!!
            ex_lock1 = """ PRAGMA locking_mode = EXCLUSIVE"""
            ex_lock2 = """BEGIN EXCLUSIVE"""

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
            # We are not using these cursor objects, we would name them same.
            cursorel = conn.execute(ex_lock1)
            cursorel2 = conn.execute(ex_lock2)
            cursord = conn.execute(debit)
            cursorc = conn.execute(credit)
            cursor_from_txa = conn.execute(update_from_txa)
            cursor_to_txa = conn.execute(update_to_txa)
            txa_rows = conn.execute(
                "SELECT * FROM transactionst ORDER BY id DESC LIMIT 2;"
            )
            # ? Can other instances of the API can read uncommited queries? -- YES
            balance_row_from = conn.execute(
                "SELECT * FROM balancet WHERE account_no={fa} ".format(
                    fa=from_account_no
                )
            )
            balance_row_to = conn.execute(
                "SELECT * FROM balancet WHERE account_no={ta} ".format(ta=to_account_no)
            )
            txas = ldict_txa(txa_rows)[::-1]  # from_txa, to_txa
            bals_from = ldict_bal(balance_row_from)  # from_bal, to_bal
            bals_to = ldict_bal(balance_row_to)

        except Exception as e:
            ## if DB fails before commit (no rollback reqd)
            if str(e) == "CHECK constraint failed: balance >=0":
                return jsonify(
                    {"Error1": "Insufficient funds", "Status": "Transaction Failed!"}
                )
            else:
                return jsonify({"Error2": str(e), "Status": "Transaction Failed!"})
        # COMMITED TO DB
        conn.commit()
        try:
            # Need to commit to read from database,
            # could return payload w/o reading too ?
            payload = {
                "id": txas[0]["id"],  # From txa id
                "from": {
                    "id": bals_from[0]["account_no"],
                    "balance": bals_from[0]["balance"],
                },
                "to": {
                    "id": bals_to[0]["account_no"],
                    "balance": bals_to[0]["balance"],
                },
                "transfered": txas[1]["amount"],  # to_txa amount
                "created_datetime": txas[1]["created_datetime"],
            }
            conn.close()
            return jsonify(payload)
        except Exception as e:
            # if DB fails after commit
            conn.rollback()
            return jsonify({"Error3": str(e), "Status": "Transaction Failed"})
    else:
        return jsonify({"Error4": "Server is down", "Status": "Transaction Failed!"})


# Transaction Table : Display
@app.route("/txa", methods=["GET"])
def transactions():
    conn = db_connection()
    cursor = conn.cursor()
    cursor = conn.execute("SELECT * FROM transactionst ")
    txa = ldict_txa(cursor)
    conn.close()
    if txa is not None:
        return jsonify(txa)


# Balance Table : Display and Add A/C
@app.route("/bal", methods=["GET", "POST"])
def balance():
    if request.method == "GET":
        conn = db_connection()
        cursor = conn.cursor()
        cursor = conn.execute("SELECT * FROM balancet ")
        bal = ldict_bal(cursor)
        conn.close()
        if bal is not None:
            return jsonify(bal)

    if request.method == "POST":
        conn = db_connection()
        cursor = conn.cursor()
        # account_no = request.form["account_no"]
        balance = request.form["balance"]
        sql = """INSERT INTO balancet (balance)
            VALUES( {bal} )""".format(
            bal=balance
        )
        cursor.execute(sql)
        conn.commit()
        sql = """ SELECT * FROM balancet ORDER by account_no DESC LIMIT 1"""
        cursor.execute(sql)
        bal = ldict_bal(cursor)
        conn.close()
        if bal is not None:
            return jsonify(bal)


if __name__ == "__main__":
    app.run(debug=True)
