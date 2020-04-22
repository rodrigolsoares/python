import mySqlConn
import file
import pandas as pd

pathFileDespesa = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/output/'
pathAndFileOrcamento = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/output/2019_OrcamentoDespesa.zip.csv'

def getDimensaoOrgao()

print('Read csv files')
csvFiles = file.searchFiles(pathFile)
for csvFilePath in csvFiles:

    if(csvFilePath.__contains__('2019_OrcamentoDespesa.zip.csv')):
        break

    df=pd.read_csv(csvFilePath,delimiter=';' ,encoding='Windows-1252')
    df = df[['Código Órgão Superior', 'Nome Órgão Superior', 'Código Órgão Subordinado', 
             'Nome Órgão Subordinado', 'Código Unidade Orçamentária', 'Nome Unidade Orçamentária']]

    df = df[df['Código Órgão Superior'] >= 0]         

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


query = '''INSERT INTO TBL_FATO (FK_ORGAO, FK_PROGRAMA, FK_TEMPORAL, VLR_ORCADO, VLR_LIQUIDADO) 
                         VALUES (%s, %s, %s, %s, %s)'''

cursor.executemany(query, out)
cnx.commit() 

print(cursor.rowcount, "linha(s) inserida(s)")




