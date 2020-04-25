import sys
sys.path.append('utils')

import utils.mySqlConn as mySqlConn
import pandas as pd
import matplotlib.pyplot as plt

query = '''select A.NM_FUNCAO AS 'Nome Função', 
                sum(F.VLR_LIQUIDADO) AS 'Valor Liquidado'
            from TBL_FATO F, TBL_DIMENSAO_AREA_ATUACAO A
            where A.PK_AREA_ATUACAO = F.FK_AREA_ATUACAO
            group by A.NM_FUNCAO
            order by sum(F.VLR_LIQUIDADO) DESC'''

dataFrame = pd.read_sql(query, con=mySqlConn.getConnection())  
dataFrame.loc[(dataFrame['Valor Liquidado'] <= 400000000000.00), 'Nome Função'] = 'Outros'
dataFrame = dataFrame.groupby('Nome Função').agg({'Valor Liquidado' : sum})


dataFrame.plot(kind='pie', y='Valor Liquidado', 
          shadow=False, label='', legend=True, autopct='%1.1f%%', startangle=280, 
          title='Execução da despesa por função', figsize=(9, 7))

print(dataFrame)

plt.show()

