import mySqlConn
import listUtil
import file
import pandas as pd

pathFile = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/csvFile/'

print('Create void dataFrame Pandas')
values = list()

print('Read csv files')
csvFiles = file.searchFiles(pathFile)
for csvFilePath in csvFiles:

    if(csvFilePath.__contains__('2019_OrcamentoDespesa.zip.csv')):
        continue

    df=pd.read_csv(csvFilePath,delimiter=';' ,encoding='Windows-1252')    
    df = df[['Código Função', 'Nome Função', 'Código Subfução', 'Nome Subfunção']]
    df = df.drop_duplicates()
    values.append(list(df.itertuples(index=False,name=None)))
    
    
out = listUtil.geraListaSemDuplicidade(values)

cnx = mySqlConn.getConnection()
cursor = cnx.cursor()

query = 'INSERT INTO  TBL_DIMENSAO_AREA_ATUACAO (PK_AREA_ATUACAO, CD_FUNCAO, NM_FUNCAO, CD_SUBFUNCAO, NM_SUBFUNCAO) VALUES (0, %s, %s, %s, %s)'

cursor.executemany(query, out)
cnx.commit() 

print(cursor.rowcount, "linha(s) inserida(s)")



