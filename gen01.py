import conf
import random
import datetime
import math
import proj_function

# generation ID
def genID(lastIterable):
    nextID = lastIterable * 21 + math.sin(lastIterable) * 20
    return int(nextID)

# generation Direct
def genDirect():
    return random.choice(conf.direct)

# generation volume
def genVolume():
    lowVolume = conf.volumeOrders[0] / 1000
    highVolume = conf.volumeOrders[1] / 1000
    return random.randint(lowVolume,  highVolume) * 1000

# generation random instrument from a tuple
def genInstrument():
    return random.choice(conf.listInstrument)

# generation px
def genPx(instrument):
    etalonPx = conf.listInstrumentPrice[instrument]
    isPlus = random.randint(0, 1)
    offset = (etalonPx * (random.random() * conf.deltaPxOrder))

    if isPlus:
        px = etalonPx + offset
    else:
        px = etalonPx - offset
    return round(px, 5)

# generation date
def genDate():
    # split date
    buildFromD = datetime.date(conf.fromYear, conf.fromMonth, conf.fromDate)
    buildToD = datetime.date(conf.toYear, conf.toMonth, conf.toDate)

    # generation date
    if buildToD > buildFromD:
        d1 = buildFromD.day
        d2 = buildToD.day
        daysInPeriod = d2 - d1
        randOfssetDay = random.randint(0, daysInPeriod - 1)
        randOfssetMinutes = random.randint(0, 59)
        randOfssetHour = random.randint(0, 23)
        goalDate = datetime.datetime(conf.fromYear,
                                     conf.fromMonth,
                                     conf.fromDate + randOfssetDay,
                                     randOfssetHour,
                                     randOfssetMinutes)
        return goalDate
    # wrong input date
    else:
        print 'Start date {0} > End date {1}'.format(buildToD, buildFromD)
        return 1

# generation date
def modifyDate(dateNewOrder):
    newDate = dateNewOrder.replace(second=random.randint(0, 59))
    return newDate

# generation state
def genState():
    countFill = conf.stateRange['1']
    countPartialFill = conf.stateRange['1'] + conf.stateRange['2']
    randNum = random.random()
    if randNum < countFill:
        goalState = conf.stateOrder['fill']
    elif randNum >= countFill and randNum <= countPartialFill:
        goalState = conf.stateOrder['partial_fill']
    elif randNum > countPartialFill:
        goalState = conf.stateOrder['reject']
    return goalState

# generation PxF
def genPxF(stateOrder, pxOrder, directOrder):
    if directOrder == 'buy' and stateOrder != conf.stateOrder['reject']:
        goalPxF = pxOrder + conf.deltaPxOrder
    elif directOrder == 'sell' and stateOrder != conf.stateOrder['reject']:
        goalPxF = pxOrder - conf.deltaPxOrder
    elif stateOrder == conf.stateOrder['reject']:
        goalPxF = 0
    return round(goalPxF, 5)

# generation volumeF
def genVolumeF(stateOrder, volumeOrder):

    if stateOrder == conf.stateOrder['reject']:
        VolumeF = 0
    elif stateOrder == conf.stateOrder['fill']:
        VolumeF = volumeOrder
    elif stateOrder == conf.stateOrder['partial_fill']:
        VolumeF = volumeOrder * conf.deltaVolumeForPartialFill
    return round(VolumeF)

#build sql query
def buildSqlQuery(dictOrders, isProcressedOrder):

    if isProcressedOrder:
        stateOrder = dictOrders['stateProcessedOrder']
        dateOrder = dictOrders['dateProcessedOrder']
    else:
        stateOrder = dictOrders['stateNewOrder']
        dateOrder = dictOrders['dateNewOrder']

    strSqlQuery = conf.templateForSqlQueryStart + \
                     str(dictOrders['idOrder']) + ', ' + \
                     str(stateOrder) + ', ' + \
                     dictOrders['instrument'] + ', ' + \
                     str(dateOrder) + ', ' + \
                     str(dictOrders['pxOrder']) + ', ' + \
                     str(dictOrders['volumeOrder']) + ', ' + \
                     str(dictOrders['pxfOrder']) + ', ' + \
                     str(dictOrders['volumefOrder']) + ', ' + \
                     str(dictOrders['directOrder']) + \
                     conf.templateForSqlQueryEnd
    return strSqlQuery


#build mongo query
def buildMongoQuery(dictOrders, isProcressedOrder):

    if isProcressedOrder:
        stateOrder = dictOrders['stateProcessedOrder']
        dateOrder = dictOrders['dateProcessedOrder']
    else:
        stateOrder = dictOrders['stateNewOrder']
        dateOrder = dictOrders['dateNewOrder']

    strMongoQuery = conf.templateForMongoQueryStart + \
                     'idOrder: ' + str(dictOrders['idOrder']) + ', ' + \
                     'stateOrder: ' + str(stateOrder) + ', ' + \
                     'instrument: ' + "'" + dictOrders['instrument'] + "'" + ', ' + \
                     'dateOrder: ' + "'" + str(dateOrder) + "'" + ', ' + \
                     'pxOrder: ' + str(dictOrders['pxOrder']) + ', ' + \
                     'volumeOrder: ' + str(dictOrders['volumeOrder']) + ', ' + \
                     'pxfOrder: ' + str(dictOrders['pxfOrder']) + ', ' + \
                     'volumefOrder: ' + str(dictOrders['volumefOrder']) + ', ' + \
                     'directOrder: ' + "'" + str(dictOrders['directOrder']) + "'" + \
                     conf.templateForMongoQueryEnd
    return strMongoQuery

#build mongo query
def buildMongoQueryJSON(dictOrders, isProcressedOrder):

    if isProcressedOrder:
        stateOrder = dictOrders['stateProcessedOrder']
        dateOrder = dictOrders['dateProcessedOrder']
    else:
        stateOrder = dictOrders['stateNewOrder']
        dateOrder = dictOrders['dateNewOrder']

    strMongoQuery = '{' + \
                    'idOrder: ' + str(dictOrders['idOrder']) + ', ' + \
                    'stateOrder: ' + str(stateOrder) + ', ' + \
                    'instrument: ' + "'" + dictOrders['instrument'] + "'" + ', ' + \
                    'dateOrder: ' + "'" + str(dateOrder) + "'" + ', ' + \
                    'pxOrder: ' + str(dictOrders['pxOrder']) + ', ' + \
                    'volumeOrder: ' + str(dictOrders['volumeOrder']) + ', ' + \
                    'pxfOrder: ' + str(dictOrders['pxfOrder']) + ', ' + \
                    'volumefOrder: ' + str(dictOrders['volumefOrder']) + ', ' + \
                    'directOrder: ' + "'" + str(dictOrders['directOrder']) + "'" + \
                    '}\n'
    return strMongoQuery

#build mongo query
def buildMongoQueryJSONforREST(dictOrders, isProcressedOrder):

    if isProcressedOrder:
        stateOrder = dictOrders['stateProcessedOrder']
        dateOrder = dictOrders['dateProcessedOrder']
    else:
        stateOrder = dictOrders['stateNewOrder']
        dateOrder = dictOrders['dateNewOrder']

    strMongoQuery = '{' + \
                    '"' + 'idOrder' + '"' + ': ' + str(dictOrders['idOrder']) + ', ' + \
                    '"' + 'stateOrder' + '"' + ': ' + str(stateOrder) + ', ' + \
                    '"' + 'instrument' + '"' + ': ' + '"' + dictOrders['instrument'] + '"' + ', ' + \
                    '"' + 'dateOrder' + '"' + ': ' + '"' + str(dateOrder) + '"' + ', ' + \
                    '"' + 'pxOrder' + '"' + ': ' + str(dictOrders['pxOrder']) + ', ' + \
                    '"' + 'volumeOrder' + '"' + ': ' + str(dictOrders['volumeOrder']) + ', ' + \
                    '"' + 'pxfOrder' + '"' + ': ' + str(dictOrders['pxfOrder']) + ', ' + \
                    '"' + 'volumefOrder' + '"' + ': ' + str(dictOrders['volumefOrder']) + ', ' + \
                    '"' + 'directOrder' + '"' + ': ' + '"' + str(dictOrders['directOrder']) + '"' + \
                    '},\n'
    return strMongoQuery

# generation order
def genOrders(lastIterable):
    # gen data for new orders
    idOrder = genID(lastIterable + 1)
    stateNewOrder = conf.stateOrder['new']
    instrument = genInstrument()
    dateNewOrder = genDate()
    pxOrder = genPx(instrument)
    volumeOrder = genVolume()
    directOrder = genDirect()
    # gen data for processed orders
    stateProcessedOrder = genState()
    pxfOrder = genPxF(stateProcessedOrder, pxOrder, directOrder)
    volumefOrder = genVolumeF(stateProcessedOrder, volumeOrder)
    dateProcessedOrder = modifyDate(dateNewOrder)

    dictOrders = {'idOrder': idOrder,
                  'stateNewOrder': stateNewOrder,
                  'instrument': instrument,
                  'dateNewOrder': dateNewOrder,
                  'pxOrder': pxOrder,
                  'volumeOrder': volumeOrder,
                  'directOrder': directOrder,
                  'stateProcessedOrder': stateProcessedOrder,
                  'pxfOrder': pxfOrder,
                  'volumefOrder':  volumefOrder,
                  'dateProcessedOrder': dateProcessedOrder}

    return dictOrders

# generation order
def genOrdersForSql():
    # list is container for orders
    listOrders = []
    for i in range(1, conf.countOrders):
        dictOrders = genOrders(i)
        newOrderString = buildSqlQuery(dictOrders, False)
        processedOrderString = buildSqlQuery(dictOrders, True)
        listOrders.append(newOrderString)
        listOrders.append(processedOrderString)
    return listOrders


def genOrdersForMongo(typeStr):
    # list is container for orders
    listOrders = []
    for i in range(1, conf.countOrders):
        dictOrders = genOrders(i)
        if typeStr == 'json':
            newOrderString = buildMongoQueryJSON(dictOrders, False)
            processedOrderString = buildMongoQueryJSON(dictOrders, True)
        elif typeStr == 'insertQuery':
            newOrderString = buildMongoQuery(dictOrders, False)
            processedOrderString = buildMongoQuery(dictOrders, True)
        elif typeStr == 'jsonRest':
            newOrderString = buildMongoQueryJSONforREST(dictOrders, False)
            processedOrderString = buildMongoQueryJSONforREST(dictOrders, True)

        if i == 1 and typeStr == 'jsonRest':
           newOrderString = 'docs=[' + newOrderString
        if i == conf.countOrders-1 and typeStr == 'jsonRest':
           processedOrderString = processedOrderString[:-2] + ']'

        listOrders.append(newOrderString)
        listOrders.append(processedOrderString)
    return listOrders

#dataOrders = genOrdersForSql()
#proj_function.writeFile(dataOrders, conf.nameFileForSqlQuery)

dataOrders = genOrdersForMongo('jsonRest')
proj_function.writeFile(dataOrders, conf.nameFileForMongoQuery)


