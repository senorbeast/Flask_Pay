#!/bin/bash

curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="108"' \
--form 'to_account_no="107"' \
--form 'amount="2"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="100"' \
--form 'to_account_no="107"' \
--form 'amount="7"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="102"' \
--form 'to_account_no="107"' \
--form 'amount="4"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="107"' \
--form 'to_account_no="104"' \
--form 'amount="5"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="107"' \
--form 'to_account_no="108"' \
--form 'amount="9"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="108"' \
--form 'to_account_no="107"' \
--form 'amount="2"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="100"' \
--form 'to_account_no="107"' \
--form 'amount="1"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="102"' \
--form 'to_account_no="107"' \
--form 'amount="7"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="107"' \
--form 'to_account_no="104"' \
--form 'amount="6"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="107"' \
--form 'to_account_no="108"' \
--form 'amount="8"'&
wait
