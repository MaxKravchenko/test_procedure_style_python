def writeFile(strQuery, nameFile):
    f = open(nameFile, 'w')
    for i in strQuery:
        f.writelines(i)
    f.close()