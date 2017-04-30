import pycurl
import json
import conf
from StringIO import StringIO

def executeCurl(orderState):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://localhost:27080/test/orders/_find?criteria=' + conf.stateOrderForCurl[orderState] + ';batch_size=1000')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    return json.loads(buffer.getvalue())

def checkStructureData():
    for state in conf.stateOrderForTest:
        dataFromCurl = executeCurl(state)
        for i in range(0, len(dataFromCurl['results'])):
            for fieldData in conf.listField:
                try:
                    temp = dataFromCurl['results'][i][fieldData]
                except KeyError:
                    return 'Exception "KeyError" in field "{0}"'.format(fieldData)
    return 0

def calcOrderVolume(dataOrders):
    orderParameters = {'volume': 0,'countRow': 0,'state': 0}

    orderParameters['state'] = dataOrders['results'][0]['stateOrder']
    orderParameters['countRow'] = len(dataOrders['results'])
    for i in range(0, orderParameters['countRow']):
        orderParameters['volume'] += dataOrders['results'][i]['volumeOrder']

    return orderParameters

def calcMidPriceOrder(dataOrders):
    orderParameters = {'state': dataOrders['results'][0]['stateOrder']}
    countRepeat = {}

    for instrument in conf.listInstrument:
        countRepeat['count' + str(instrument)] = 0
        orderParameters['midPr' + str(instrument)] = 0

    for i in range(0, len(dataOrders['results'])):
        for instrument in conf.listInstrument:
            if dataOrders['results'][i]['instrument'] == instrument:
                countRepeat['count' + str(instrument)] += 1
                orderParameters['midPr' + str(instrument)] += dataOrders['results'][i]['pxOrder']

    for instrument in conf.listInstrument:
        if countRepeat['count' + str(instrument)] != 0:
            orderParameters['midPr' + str(instrument)] = round(orderParameters['midPr' + str(instrument)] / countRepeat['count' + str(instrument)], 3)
        else:
            orderParameters['midPr' + str(instrument)] = 0

    return orderParameters
