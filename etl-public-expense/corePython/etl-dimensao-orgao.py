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
    
    df = df[df['Código Órgão Superior'] >= 0]

    df = df[['Código Órgão Superior', 'Nome Órgão Superior', 'Código Órgão Subordinado', 
             'Nome Órgão Subordinado', 'Código Unidade Orçamentária', 'Nome Unidade Orçamentária']]

    df = df.drop_duplicates()
    
    values.append(list(df.itertuples(index=False,name=None)))
    

out = listUtil.geraListaSemDuplicidade(values)	

cnx = mySqlConn.getConnection()
cursor = cnx.cursor()


query = '''INSERT INTO TBL_DIMENSAO_ORGAO (PK_ORGAO, CD_ORGAO_SUPERIOR, NM_ORGAO_SUPERIOR, 
                                           CD_ORGAO_SUBORDINADO, NM_ORGAO_SUBORDINADO,CD_UNIDADE_ORCAMENTARIA, 
                                           NM_UNIDADE_ORCAMENTARIA) VALUES (0, %s, %s, %s, %s, %s, %s)'''

cursor.executemany(query, out)
cnx.commit() 

print(f'Etl dimensão orgão:  {cursor.rowcount} linha(s) inserida(s)')




