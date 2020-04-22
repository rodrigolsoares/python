import mySqlConn
import file
import pandas as pd

pathFile = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/output/'

print('Create void dataFrame Pandas')
values = list()

print('Read csv files')
csvFiles = file.searchFiles(pathFile)
for csvFilePath in csvFiles:

    if(csvFilePath.__contains__('2019_OrcamentoDespesa.zip.csv')):
        break

    df=pd.read_csv(csvFilePath,delimiter=';' ,encoding='Windows-1252')
    df = df[df['Código Órgão Superior'] >= 0]     
    
    df = df[['Código Programa Orçamentário', 'Nome Programa Orçamentário', 'Código Ação', 'Nome Ação']]

    df = df.drop_duplicates()
    
    values.append(list(df.itertuples(index=False,name=None)))
    

	

dfFilter = pd.DataFrame(values) 
dfFilter = dfFilter.drop_duplicates()
listaFiltrada = list(dfFilter.itertuples(index=False,name=None))

out = []

for tupleRecord in listaFiltrada:
    for record in tupleRecord:
        if(record != None ):
            out.append(record)

cnx = mySqlConn.getConnection()
cursor = cnx.cursor()


query = '''INSERT INTO TBL_DIMENSAO_PROGRAMA (PK_PROGRAMA, CD_PROGRAMA_ORCAMENTARIO, NM_PROGRAMA_ORCAMENTARIO, CD_ACAO, NM_ACAO) 
                                      VALUES (0, %s, %s, %s, %s) '''

cursor.executemany(query, out)
cnx.commit() 

print(cursor.rowcount, "linha(s) inserida(s)")



