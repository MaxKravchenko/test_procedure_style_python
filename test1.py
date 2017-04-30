import json
import conf
import calc_order_params
import proj_function

testValidData = calc_order_params.checkStructureData()
if testValidData != 0:
    proj_function.writeFile(testValidData, conf.fileNameTest1)
    print testValidData
else:
    totalVolumeAllOrders = 0
    f = open(conf.fileNameTest1, 'w')
    for state in conf.stateOrderForTest:
        dataFromCurl = calc_order_params.executeCurl(state)
        calcParameters = calc_order_params.calcOrderVolume(dataFromCurl)
        print calcParameters
        totalVolumeAllOrders += calcParameters['volume']
        f.writelines(json.dumps(calcParameters))
        f.writelines('\n')

    print 'Total volume of all type orders = {0}'.format(totalVolumeAllOrders)
    f.writelines('Total volume of all type orders = ' + str(totalVolumeAllOrders))
    f.close()