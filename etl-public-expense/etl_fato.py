import mySqlConn
import file
import pandas as pd

ano = 2019
pathFileDespesa = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/csvFile/'
pathAndFileOrcamento = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/csvFile/2019_OrcamentoDespesa.zip.csv'

def getDimensaoOrgao():
    cnx = mySqlConn.getConnection()
    cursor = cnx.cursor()
    query = 'select PK_ORGAO, CD_ORGAO_SUPERIOR, CD_ORGAO_SUBORDINADO, CD_UNIDADE_ORCAMENTARIA from TBL_DIMENSAO_ORGAO'
    cursor.execute(query)
    return  cursor.fetchall()

def getDimensaoPrograma():
    cnx = mySqlConn.getConnection()
    cursor = cnx.cursor()
    query = 'select PK_PROGRAMA, CD_PROGRAMA_ORCAMENTARIO, CD_ACAO from TBL_DIMENSAO_PROGRAMA'
    cursor.execute(query)
    return  cursor.fetchall()

def getDimensaoTemporal(param):
    mes = 0
    cnx = mySqlConn.getConnection()
    cursor = cnx.cursor()
    query = '''select PK_TEMPORAL from TBL_DIMENSAO_TEMPORAL
                where mes = %s and ano = %s '''
    cursor.execute(query, (param, ano))
    results = cursor.fetchall()
    for result in results:
       mes = result[0]
    return  mes

def getMes(pathFile):
    initialPosition = pathFile.index('2019') + 4
    finalPosition = pathFile.index('_')
    return int(pathFile[initialPosition:finalPosition])

print('Inicializando processo')

print('Montando Lista de TBL_DIMENSAO_ORGAO')
listDimensaoOrgao = []
for result in getDimensaoOrgao():
     listDimensaoOrgao.append({'ChaveDimensaoOrgao': result[0], 'Código Órgão Superior': result[1], 'Código Órgão Subordinado': result[2],
                               'Código Unidade Orçamentária': result[3]} )

print('Convert Lista de TBL_DIMENSAO_ORGAO em DataFrame')
dfDimensaoOrgao = pd.DataFrame(listDimensaoOrgao) 


print('Montando Lista de TBL_DIMENSAO_PROGRAMA')
listDimensaoPrograma = []
for result in getDimensaoPrograma():
     listDimensaoPrograma.append({'ChaveDimensaoPrograma': result[0], 'Código Programa Orçamentário': result[1], 'Código Ação': result[2]})

print('Convert Lista de TBL_DIMENSAO_PROGRAMA em DataFrame')
dfDimensaoPrograma = pd.DataFrame(listDimensaoPrograma) 
dfDimensaoPrograma = dfDimensaoPrograma.drop_duplicates()


print('Read csv files')
csvFiles = file.searchFiles(pathFileDespesa)
for csvFilePath in csvFiles:

    if(csvFilePath.__contains__('2019_OrcamentoDespesa.zip.csv')):
        continue
    
    dfDespesa=pd.read_csv(csvFilePath,delimiter=';' ,encoding='Windows-1252')

    mes = getMes(csvFilePath)
    keyTemp = getDimensaoTemporal(mes)
    dfDespesa['ChaveDimensaoTemporal'] = keyTemp
 
    dfDespesa = pd.merge(dfDespesa, dfDimensaoPrograma, how='inner')
    #dfDespesa = pd.merge(dfDespesa, dfDimensaoOrgao, how='inner')

    print(dfDespesa)

    dfOrcamento=pd.read_csv(pathAndFileOrcamento,delimiter=';' ,encoding='Windows-1252')
    dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
    dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
    dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
    dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
    dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
    dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
    dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
    

    print(dfOrcamento)

    resultDF = pd.merge(dfOrcamento, dfDespesa, how='inner')

    print(resultDF)

    break



'''dfFilter = pd.DataFrame(values) 
dfFilter = dfFilter.drop_duplicates()
listaFiltrada = list(dfFilter.itertuples(index=False,name=None))

out = []

for tupleRecord in listaFiltrada:
    for record in tupleRecord:
        if(record != None ):
            out.append(record)

cnx = mySqlConn.getConnection()
cursor = cnx.cursor()'''


#query = '''INSERT INTO TBL_FATO (FK_ORGAO, FK_PROGRAMA, FK_TEMPORAL, VLR_ORCADO, VLR_LIQUIDADO) 
#                         VALUES (%s, %s, %s, %s, %s)'''

#cursor.executemany(query, out)
#cnx.commit() 

#print(cursor.rowcount, "linha(s) inserida(s)")




