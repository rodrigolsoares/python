import utils.mySqlConn as mySqlConn

arrayData = list()
year = 2019


for valueRange in range(1,13):
    row = (valueRange, year)
    arrayData.append(row)

cnx = mySqlConn.getConnection()
cursor = cnx.cursor()


query = '''INSERT INTO TBL_DIMENSAO_TEMPORAL (PK_TEMPORAL, MES, ANO) VALUES (0, %s, %s)'''

cursor.executemany(query, arrayData)
cnx.commit() 

print(f'Etl dimensão temporal:  {cursor.rowcount} linha(s) inserida(s)')




