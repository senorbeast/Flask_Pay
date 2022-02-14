# Transfer API

## To run the project:

### Setup:

With virtualenv

```
virtualenv pay-env
source pay-env/bin/activate
cd Flask_Pay
pip install -r requirements.txt
```

OR
Just install Flask by:

```
pip install Flask
```

#### Setup db and fill it with some values:

```
python db.py
python fill_db.py
```

#### To run (dev):

For virtualenv

```
source pay-env/bin/activate
cd Flask_Pay
python main.py
```

OR Just

```
python main.py
```

## Request and Endpoints

1. GET : [/bal](http://127.0.0.1:5000/bal) - To get all accounts and their balance
2. GET : [/txa](http://127.0.0.1:5000/txa) - To get transactions
3. POST : /bal - To add new accounts and balance

    Request

    ```
    curl --location --request POST 'http://127.0.0.1:5000/bal' \
    --form 'balance="1338"'
    ```

    Respose Payload

    ```
    {
        "account_no": "account_no_inserted",
        "balance": "amount_inserted",
    }
    ```

4. POST : /transfer - To do a transaction

    Request example:

    ```
    curl --location --request POST 'http://127.0.0.1:5000/transfer' \
    --form 'from_account_no="108"' \
    --form 'to_account_no="107"' \
    --form 'amount="0.01"'
    ```

    Response Payload

    ```bash
    {
    "id": "transaction_id",                                 # From transaction id
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
    ```

### Edge Cases Test and Concurrency Test

```bash
chmod u+x test.sh
./test.sh
```

## DB

### Balance table

| account_no |  balance  |
| :--------: | :-------: |
|    501     |   15000   |
|    502     | 100000000 |
|    503     |    250    |

### Transaction table

| id  | account_no | amount |  created_datetime   |
| :-: | :--------: | :----: | :-----------------: |
|  1  |    501     |  -500  | 2022-02-12 19:15:51 |
|  2  |    502     |  +500  | 2022-02-12 19:25:51 |
|  3  |    502     | -1337  | 2022-02-12 19:35:51 |

> **Positive amount** indicates **Credit** from the respective account_no

> While **Negative amount** indicates **Debit** from the respective account_no
