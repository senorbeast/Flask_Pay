#!/bin/bash

# Edge cases test and cucurrency test.
# All the curl commands will run concurrently
# Accounts 501, 502, 503 and random


# Account A and Account B transfering to Account C at same time
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="503"' \
--form 'amount="2"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="503"' \
--form 'amount="7"'&

# Self Transfer 
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="502"' \
--form 'amount="4"'&

# Insufficient Balance
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="80000"'&
# Invalid Account No:
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="6"' \
--form 'to_account_no="501"' \
--form 'amount="80000"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="4"' \
--form 'amount="80000"'&
# Negative Amount
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="502"' \
--form 'amount="-80000"'&

# Random
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="104"' \
--form 'amount="5"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="9"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="502"' \
--form 'amount="2"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="100"' \
--form 'to_account_no="502"' \
--form 'amount="1"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="502"' \
--form 'amount="7"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="104"' \
--form 'amount="6"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="8"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="8"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="8"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="104224"' \
--form 'amount="5"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="9"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="502"' \
--form 'amount="2"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="100"' \
--form 'to_account_no="502"' \
--form 'amount="1"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="502"' \
--form 'amount="7"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="14344"' \
--form 'amount="6"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="8"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="8"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="8"'&



wait
