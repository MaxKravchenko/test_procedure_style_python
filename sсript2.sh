#!/bin/bash
HOST="http://localhost:27080"
TEST1=test1.py
TEST2=test2.py
REPORTTEST1=result_test1.txt
REPORTTEST2=result_test2.txt
GENFILE=gen01.py
FILERESULTGEN=orders.json

countLines()
{
	[[ -r $1 ]] && REPLY=$(echo $(wc -l < $1))
	echo "In file $1 found $REPLY rows."
}

checkFile()
{
	if  [ -f $1 ]; then  
		echo "The File '$1' Exist."
		ls -l $1 | awk '{ print "Time created "$8 "   size: " $5 }'	
	else
		echo "The File '$1' Does Not Exist. Program stopped."
		exit 0 
	fi
}

testConnectToMongoose()
{
	echo "Test connect to mongoose"
	if ! curl -s -X GET "$HOST/_hello" > /dev/null 2>&1; then
		echo "Test connect failed. Program stopped."
		exit 0 
	else
		echo "Test connect to mongoose sucssesful"
	fi
}

testBaseIsEmpty()
{
	echo ""
	echo "Test base"
	if curl -s -X GET "$HOST/test/orders/_find?batch_size=1" | grep -c "pxOrder" > /dev/null 2>&1; then
		echo "Base is not empty!!!"
		curl  -s -X POST --data 'criteria={}' "$HOST/test/orders/_remove"
		echo ""
		echo "Base cleaned sucssesful"
	else
		echo "Base is empty."
	fi
	echo ""
}

genData()
{
	echo "Generating data..."
	python $GENFILE
	checkFile $FILERESULTGEN
	countLines $FILERESULTGEN
	echo "Generating data sucssesful"
	echo ""
}

loadData()
{
	echo "Loading data..."
	curl -s -X POST -d @$FILERESULTGEN "$HOST/test/orders/_insert" > /dev/null 2>&1
	if curl -s -X GET "$HOST/test/orders/_find?batch_size=1" | grep -c "pxOrder" > /dev/null 2>&1; then
		echo "Loading data sucssesful!"
	else
		echo "Base is empty."
		echo "Load data failed. Program stopped."
		exit 0 
	fi
}

test1()
{
	echo ""
	echo "Test1. Calculating count orders state"
	python $TEST1
	echo ""
	checkFile $REPORTTEST1
	countLines $REPORTTEST1
	echo "Report generated sucssesful"
}

test2()
{
	echo ""
	echo "Test2. Calculating average price and generate report"
	python $TEST2
	echo ""
	checkFile $REPORTTEST2
	countLines $REPORTTEST2
	echo "Report generated sucssesful"
}
date
testConnectToMongoose
testBaseIsEmpty
genData
loadData
test1
test2
exit 0 