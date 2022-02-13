from flask import Flask, request, jsonify
import json
import sqlite3

## Transfering money across two bank Accounts.

# NO ORM
# [✔] 1. Creats, request, jsonify Database + View the Transactions and Balances Table
# Operate on Database : Foreign Key? Required?

# * Transfer API : X amount of money from A to B with post request
# *   payloads for request and response are specified.

# [✔] 2. Validity and consistent data : ACID (BEGIN, COMMIT, ROLLBACK)
# ? Prevent 1 customer tapping twice : UI & _____
# Add more APIs for create a/c, money deposit etc

# [✔] 3. Manage the logic at the database level ( Managed by serialization and ACID methodology)
# What happens under high concurrency? : #!SERIALIZATION
# What happens if your db becomes unavailable in the middle of logic? :
#   a. Before txa
#   b. During txa

# [ ] A,B transfer money to C at same time :
# ! SERIALIZATION locking and unlocking db for read/write for 1 operation and async await flask ?
# ! exclusive lock to remove read access...
# Flask has inbuilt concurrency through its WSGI/ASGI production server.


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
            lock = """ PRAGMA locking_mode = EXCLUSIVE;
            BEGIN EXCLUSIVE;"""
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

            cursord = conn.execute(debit)
            cursorc = conn.execute(credit)
            cursor_from_txa = conn.execute(update_from_txa)
            cursor_to_txa = conn.execute(update_to_txa)
        except Exception as e:
            ## if DB fails before commit (no rollback reqd)
            if str(e) == "CHECK constraint failed: balance >=0":
                return jsonify(
                    {"Error": "Insufficient funds", "Status": "Transaction Failed!"}
                )
            else:
                return jsonify({"Error": str(e), "Status": "Transaction Failed!"})
        # COMMITED TO DB
        conn.commit()
        try:
            # Need to commit to read from database,
            # could return payload w/o reading too ?
            # Will give to_txa, from_txa (since desc order)
            txa_rows = conn.execute(
                "SELECT * FROM transactionst ORDER BY id DESC LIMIT 2;"
            )

            balance_rows = conn.execute(
                "SELECT * FROM balancet WHERE account_no={fa} OR account_no={ta}".format(
                    fa=from_account_no, ta=to_account_no
                )
            )

            txas = ldict_txa(txa_rows)[::-1]  # from_txa, to_txa
            bals = ldict_bal(balance_rows)  # from_bal, to_bal
            conn.close()

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
            return jsonify(payload)
        except Exception as e:
            # if DB fails after commit
            conn.rollback()
            return jsonify({"Error": str(e), "Status": "Transaction Failed"})
    else:
        return jsonify({"Error": "Server is down", "Status": "Transaction Failed!"})


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
        account_no = request.form["account_no"]
        balance = request.form["balance"]
        sql = """INSERT INTO balancet
            VALUES( {amt},{bal} )""".format(
            amt=account_no, bal=balance
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
