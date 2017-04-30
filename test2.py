import json
import conf
import calc_order_params
import proj_function

testValidData = calc_order_params.checkStructureData()
if testValidData != 0:
    proj_function.writeFile(testValidData, conf.fileNameTest2)
    print testValidData
else:
    f = open(conf.fileNameTest2, 'w')
    for state in conf.stateOrderForTest:
        dataFromCurl = calc_order_params.executeCurl(state)
        calcParameters = calc_order_params.calcMidPriceOrder(dataFromCurl)
        print calcParameters
        f.writelines(json.dumps(calcParameters))
        f.writelines('\n')
    f.close()


