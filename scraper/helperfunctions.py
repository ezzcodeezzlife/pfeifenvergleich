import re

def priceStringToFloat(priceString):
    floatt = re.findall("\d+\,\d+", priceString)
    if(floatt == []):
        floatt = re.findall("\d+\.\d+", priceString)
        floatt[0].replace('.',',')
    #print(floatt)
    return floatt[0]
