# File include configuration parameters for algorithm generation orders
countOrders = 1001
stateOrder = {'new': 0, 'fill': 1, 'partial_fill': 2, 'reject': 8}
stateOrderForTest = ('fill', 'partial_fill', 'reject')
stateRange = {'1': 0.6, '2': 0.1, '8': 0.3}
listInstrument = ('EUR/USD', 'AUD/CAD', 'CHF/GBP', 'CHF/USD')
listInstrumentPrice = {'EUR/USD': 1.05942, 'AUD/CAD': 0.99862, 'CHF/GBP': 0.79363, 'CHF/USD': 0.99427}
deltaPxOrder = 0.05
deltaVolumeForPartialFill = 0.5
volumeOrders = (1000, 100000)
direct = ('buy', 'sell')
fromYear = 2017
fromMonth = 02
fromDate = 24
toYear = 2017
toMonth = 02
toDate = 26
templateForSqlQueryStart = 'INSERT INTO orders (Id,State,Instrument,Date,Px,Volume,PxF,VolumeF,Direct) VALUES ('
templateForSqlQueryEnd = ');\n'
templateForMongoQueryStart = 'db.orders.insert({'
templateForMongoQueryEnd = '})\n'
nameFileForSqlQuery = 'orders.sql'
nameFileForMongoQuery = 'orders.json'
stateOrderForCurl = {'new': '%7B%22stateOrder%22:0%7D',
                     'fill': '%7B%22stateOrder%22:1%7D',
                     'partial_fill': '%7B%22stateOrder%22:2%7D',
                     'reject': '%7B%22stateOrder%22:8%7D'}
listField = ('idOrder', 'stateOrder', 'instrument', 'dateOrder', 'pxOrder', 'volumeOrder', 'pxfOrder', 'volumefOrder', 'directOrder')
fileNameTest1 = 'result_test1.txt'
fileNameTest2 = 'result_test2.txt'