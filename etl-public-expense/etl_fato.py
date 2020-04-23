import mySqlConn
import file
import listUtil
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

dfOrcamento=pd.read_csv(pathAndFileOrcamento, delimiter=';', decimal= ',' ,encoding='Windows-1252')
dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUPERIOR': 'Código Órgão Superior'}, inplace=True)
dfOrcamento.rename(columns={'CÓDIGO ÓRGÃO SUBORDINADO': 'Código Órgão Subordinado'}, inplace=True)
dfOrcamento.rename(columns={'CÓDIGO UNIDADE ORÇAMENTÁRIA': 'Código Unidade Orçamentária'}, inplace=True)
dfOrcamento.rename(columns={'CÓDIGO PROGRAMA ORÇAMENTÁRIO': 'Código Programa Orçamentário'}, inplace=True)
dfOrcamento.rename(columns={'CÓDIGO AÇÃO': 'Código Ação'}, inplace=True)
dfOrcamento.rename(columns={'ORÇAMENTO REALIZADO (R$)': 'Orçamento Realizado (R$)'}, inplace=True)
    
dfOrcamento = dfOrcamento[['Código Órgão Superior', 'Código Órgão Subordinado','Código Unidade Orçamentária', 
                           'Código Programa Orçamentário', 'Código Ação', 'Orçamento Realizado (R$)']]

print('Create void dataFrame Pandas')
values = list()

print('Read csv files')
csvFiles = file.searchFiles(pathFileDespesa)
for csvFilePath in csvFiles:

    if(csvFilePath.__contains__('2019_OrcamentoDespesa.zip.csv')):
        continue
    
    mes = getMes(csvFilePath)
    keyTemp = getDimensaoTemporal(mes)

    dfDespesa=pd.read_csv(csvFilePath,delimiter=';', decimal=',' ,encoding='Windows-1252')
    
    dfDespesa = dfDespesa[(dfDespesa['Código Programa Orçamentário'] >= 0) & (dfDespesa['Código Órgão Superior'] >= 0)]     

    dfDespesa = dfDespesa[['Código Órgão Superior', 'Código Órgão Subordinado','Código Unidade Orçamentária', 
                           'Código Programa Orçamentário', 'Código Ação', 'Valor Liquidado (R$)']]

    dfDespesa['ChaveDimensaoTemporal'] = keyTemp
 
    dfDespesa = pd.merge(dfDespesa, dfDimensaoPrograma, how='inner')
    dfDespesa = pd.merge(dfDespesa, dfDimensaoOrgao, how='inner')


    resultMergeDF = pd.merge(dfOrcamento, dfDespesa, how='inner')
    grouped_keys = resultMergeDF.groupby([resultMergeDF['ChaveDimensaoTemporal'], resultMergeDF['ChaveDimensaoPrograma'], resultMergeDF['ChaveDimensaoOrgao']])
    resultDF  = grouped_keys.agg({'Orçamento Realizado (R$)' : sum, 'Valor Liquidado (R$)': sum}).reset_index()
    
    resultDF['Orçamento Realizado (R$)'] = resultDF['Orçamento Realizado (R$)'].apply(lambda x: x / 12)
    resultDF['Orçamento Realizado (R$)'] = resultDF['Orçamento Realizado (R$)'].apply(lambda x: round(x, 2))
    resultDF['Valor Liquidado (R$)'] = resultDF['Valor Liquidado (R$)'].apply(lambda x: round(x, 2))

    values.append(list(resultDF.itertuples(index=False,name=None)))


out = listUtil.geraLista(values)

cnx = mySqlConn.getConnection()
cursor = cnx.cursor()


query = '''INSERT INTO TBL_FATO (FK_TEMPORAL, FK_PROGRAMA, FK_ORGAO, VLR_ORCADO, VLR_LIQUIDADO) 
                         VALUES (%s, %s, %s, %s, %s)'''

cursor.executemany(query, out)
cnx.commit() 

print(cursor.rowcount, "linha(s) inserida(s)")




