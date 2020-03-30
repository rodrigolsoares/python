import json
import datetime

from pymongo import MongoClient

dataBaseName = 'catalogo'
collectionNamePricing = 'precificacao'

urlcurrentSynchronization = 'url mongo connect'
urlnewSynchronization = 'url mongo connect'


filterCurrentSynchronization = {"_id.filial": 11, "estadoProduto.PADRAO": {"$exists": True} , "estadoProduto.PADRAO.comercializacao.codigo" : {"$ne": 99999999} }
filterNewSynchronization = {"_id.filial": 11}

def toCompareJson(oldJson, newJson):
  return compareElementJson(oldJson, newJson, '_id') and compareElementJson(oldJson, newJson, 'estadoProduto') and compareElementJson(oldJson, newJson, 'precoCusto') and compareElementJson(oldJson, newJson, 'precoSugestao')

    
def compareElementJson(oldJson, newJson, element):
    if(oldJson.__contains__(element)):
        if(newJson.__contains__(element)):
            if oldJson[element] == newJson[element]:
                return True
    return False    


def dateConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def getConnectionMongo (url):
    return MongoClient(url)

def getDataBAse (client, database):
    return client[database]

def getCollection (database, collection):
    return database[collection]

def getPrecing(url, syncVersion, filter):
   
    print('[' + syncVersion + '] doing connection.')
    client = getConnectionMongo(url)
    dataBase = getDataBAse(client, dataBaseName)
    pricing = getCollection(dataBase, collectionNamePricing)
    print('[' + syncVersion + '] search result. Price Quantity: ' + str(pricing.count(filter)) )

    dictionary = {}
    print('[' + syncVersion + '] building price json dictionary')
    for record in pricing.find(filter): 
        id = json.dumps(record['_id'])
        dictionary[id] = record

    client.close

    print('[' + syncVersion + '] Quantity of objects in the dictionary: ' + str(len(dictionary)))

    return dictionary


oldSyncRecords = getPrecing(urlcurrentSynchronization, 'Old Synchronization', filterCurrentSynchronization)
newSyncRecords = getPrecing(urlnewSynchronization, 'New Synchronization', filterNewSynchronization)

totalRecordsFound = 0
totalRecordsNotFound = 0

divergent = 0
correct = 0

divergenceFile = open("./compare-result/divergenceFile.txt", "w")
notFoundFile = open("./compare-result/notFoundFile.txt", "w")
csvLoadFile = open("./compare-result/carga.csv", "w")

csvLoadFile.write('codigo-comercializacao;sku;tipoProduto;\n')

for key, jsonOld in oldSyncRecords.items():
    
    id = jsonOld['_id']
    estadoProduto = jsonOld['estadoProduto']
    padrao = estadoProduto['PADRAO']
    comercializacao = padrao['comercializacao']
    
    sku = id['sku']
    typeSku = id['tipoProduto']
    com = comercializacao['codigo']

    if(newSyncRecords.__contains__(key)):
        
        jsonNew = newSyncRecords[key]
        totalRecordsFound += 1

        if(toCompareJson(jsonOld, jsonNew)):
            correct +=1
        else:
            divergenceFile.write('New: ' + str(json.dumps(jsonNew, default = dateConverter)) + '\n')
            divergenceFile.write('Old: ' + str(json.dumps(jsonOld, default = dateConverter)) + '\n\n')
            csvLoadFile.write(str(com) + ';' + str(sku) + ';' + str(typeSku) + ';\n')
            divergent +=1

        
    else:
       totalRecordsNotFound += 1 
       notFoundFile.write(str(json.dumps(jsonOld, default = dateConverter)) + '\n')
       csvLoadFile.write(str(com) + ';' + str(sku) + ';' + str(typeSku) + ';\n')
       
divergenceFile.close() 
notFoundFile.close()  
csvLoadFile.close() 

print('----------------------------------------------------------------------------------------')
print('- Total records found between the two databases (Match): ' + str(totalRecordsFound))
print('- Number of correct records between the two databases : ' + str(correct))
print('- Number of divergent records between the two databases: ' + str(divergent))
print('----------------------------------------------------------------------------------------')
print('- Total records not found in new Sync (No Match): ' + str(totalRecordsNotFound))
print('----------------------------------------------------------------------------------------')
