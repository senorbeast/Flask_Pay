echo "Account 501 and Account 502 transfering to Account 503 at same time"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="503"' \
--form 'amount="2"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="503"' \
--form 'amount="7"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "Account 501 and Account 502 transfering to Account 503 at same time"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="503"' \
--form 'amount="53"'&
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="503"' \
--form 'amount="5"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "Self Transfer" 
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="502"' \
--form 'amount="4"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "Insufficient Balance"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="502"' \
--form 'to_account_no="501"' \
--form 'amount="80000"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "Invalid from A/C"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="6"' \
--form 'to_account_no="501"' \
--form 'amount="80000"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "Invalid from A/C"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="6"' \
--form 'to_account_no="501"' \
--form 'amount="80"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "Invalid from A/C"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="9"' \
--form 'amount="8"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "Invalid to A/C"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="4"' \
--form 'amount="80"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

echo "-ve Account"
curl --location --request POST 'http://127.0.0.1:5000/transfer' \
--form 'from_account_no="501"' \
--form 'to_account_no="502"' \
--form 'amount="-80000"'&
read -n 1 -r -s -p $'Press enter to continue...\n'

