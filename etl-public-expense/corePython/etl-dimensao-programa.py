import utils.mySqlConn as mySqlConn
import utils.file as file
import utils.listUtil as listUtil
import pandas as pd

pathFile = pathFileDespesa = file.pathFileDespesa

print('Create void dataFrame Pandas')
values = list()

print('Read csv files')
csvFiles = file.searchFiles(pathFile)
for csvFilePath in csvFiles:

    if(csvFilePath.__contains__('2019_OrcamentoDespesa.zip.csv')):
        continue

    df=pd.read_csv(csvFilePath,delimiter=';' ,encoding='Windows-1252')
    df = df[df['Código Programa Orçamentário'] >= 0]     
    df = df[['Código Programa Orçamentário', 'Nome Programa Orçamentário', 'Código Ação', 'Nome Ação']]
    df = df.drop_duplicates()
    values.append(list(df.itertuples(index=False,name=None)))
    
    
out = listUtil.geraListaSemDuplicidade(values)

cnx = mySqlConn.getConnection()
cursor = cnx.cursor()

query = '''INSERT INTO TBL_DIMENSAO_PROGRAMA (PK_PROGRAMA, CD_PROGRAMA_ORCAMENTARIO, NM_PROGRAMA_ORCAMENTARIO, CD_ACAO, NM_ACAO) 
                                      VALUES (0, %s, %s, %s, %s) '''

cursor.executemany(query, out)
cnx.commit() 

print(f'Etl dimensão programa:  {cursor.rowcount} linha(s) inserida(s)')



