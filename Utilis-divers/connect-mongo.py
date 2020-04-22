import json
import datetime

from pymongo import MongoClient

#Change the parameters branch and commercialization
branch = 1000
commercialization = 'PADRAO'
queryCompare = 'estadoProduto.' + str(commercialization)


#Do not change code below
dataBaseName = 'catalogo'
collectionNamePricing = 'precificacao'

urlcurrentSynchronization = 'mongodb://usr_dev:XtjclH2L5Tep9bcHO8lb5s0x@mdbp-via-1.dc.nova:27017,mdbp-via-2.dc.nova:27017,mdbp-via-3.dc.nova:27017,mdbp-via-4.dc.nova:27017,mdbp-via-5.dc.nova:27017,mdbp-viamais1.dc.nova:27017,mdbp-viamais2.dc.nova:27017,mdbp-viamais3.dc.nova:27017,mdbp-viamais4.dc.nova:27017,mdbp-viamais5.dc.nova:27017/catalogo?replicaset=rsMULT&readPreference=secondaryPreferred&authSource=admin'
urlnewSynchronization = 'mongodb://svc_sync:ZI7YPHc!Awg6@mdbp-sync-1.dc.nova:27017,mdbp-sync-2.dc.nova:27017,mdbp-sync-3.dc.nova:27017/catalogo?replicaset=rsSYNC&readPreference=secondaryPreferred&authSource=admin'

filterCurrentSynchronization = {"_id.filial": branch, queryCompare : {"$exists": True} , queryCompare + ".comercializacao.codigo" : {"$ne": 99999999} }
filterNewSynchronization = {"_id.filial": branch}


def toCompareJson(oldJson, newJson):
  #return compareElementJson(oldJson, newJson, '_id') and compareElementJson(oldJson, newJson, 'estadoProduto') and compareElementJson(oldJson, newJson, 'precoCusto') and compareElementJson(oldJson, newJson, 'precoSugestao')
  
    if(oldJson.__contains__('estadoProduto')):
        if(newJson.__contains__('estadoProduto')):
            jsonCustomOld = oldJson['estadoProduto']
            jsonCustomNew = newJson['estadoProduto']
            return compareElementJson(jsonCustomOld, jsonCustomNew, commercialization) 
        else:
            return False

    return True


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

divergenceFile = open("./compare-result/divergenceFile_" + str(commercialization) + '_' + str(branch) + ".txt", "w")
notFoundFile = open("./compare-result/notFoundFile_"  + str(commercialization) + '_'  + str(branch) + ".txt", "w")
csvLoadFile = open("./compare-result/load_" + str(commercialization) + '_'  + str(branch) + ".csv", "w")

csvLoadFile.write('codigo-comercializacao;sku;tipoProduto;\n')

for key, jsonOld in oldSyncRecords.items():
    
    id = jsonOld['_id']
    estadoProduto = jsonOld['estadoProduto']
    padrao = estadoProduto[commercialization]
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
print('- Branch: ' + str(branch) + ' Type: ' + commercialization)
print('- Total records found between the two databases (Match): ' + str(totalRecordsFound))
print('- Number of correct records between the two databases : ' + str(correct))
print('- Number of divergent records between the two databases: ' + str(divergent))
print('----------------------------------------------------------------------------------------')
print('- Total records not found in new Sync (No Match): ' + str(totalRecordsNotFound))
print('----------------------------------------------------------------------------------------')

