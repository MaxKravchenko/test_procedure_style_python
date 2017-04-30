#!/bin/bash
source "my_function.sh"
FILE="orders.json"

echo "Test connect to mongoose"
if ! curl -X GET 'http://localhost:27080/_hello' > /dev/null 2>&1; then
	echo "Test connect failed. Program stopped."
	exit 0 
else
	echo "Test connect to mongoose sucssesful"
fi

echo ""
echo "Test base"
if curl -X GET 'http://localhost:27080/test/orders/_find?batch_size=1' | grep -c "pxOrder" > /dev/null 2>&1; then
	echo "Base is not empty!!!"
	curl  -X POST --data 'criteria={}' 'http://localhost:27080/test/orders/_remove'
	echo "Base cleaned sucssesful"
else
	echo "Base is empty."
fi

echo ""
echo "Prepare for generating data..."
checkFile "gen01.py"
echo "Generating data..."
python gen01.py
checkFile "orders.json"
echo "Generating data sucssesful"

echo ""
echo "Loading data..."
curl -X POST -d @$FILE http://localhost:27080/test/orders/_insert > /dev/null 2>&1
if curl -X GET 'http://localhost:27080/test/orders/_find?batch_size=1' | grep -c "pxOrder" > /dev/null 2>&1; then
	echo "Loading data sucssesful!"
else
	echo "Base is empty."
	echo "Load data failed. Program stopped."
	exit 0 
fi

echo ""
echo "Calculating count orders state and generate report"
checkFile "validate_order_status.py"
echo ""
python validate_order_status.py
echo ""
checkFile "result_test.txt"
echo "Report generated sucssesful"

exit 0 