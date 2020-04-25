import utils.mySqlConn as mySqlConn
import pandas as pd
import matplotlib.pyplot as plt

query = '''select O.NM_ORGAO_SUBORDINADO AS 'Orgão Subordinado', 
                sum(F.VLR_LIQUIDADO) AS 'Valor Liquidado'
                from TBL_FATO F, TBL_DIMENSAO_ORGAO O 
            where O.PK_ORGAO = F.FK_ORGAO 
            group by O.NM_ORGAO_SUBORDINADO 
            order by sum(F.VLR_LIQUIDADO) DESC'''

dataFrame = pd.read_sql(query, con=mySqlConn.getConnection())  
dataFrame.loc[(dataFrame['Valor Liquidado'] <= 200000000000.00), 'Orgão Subordinado'] = 'Outros'
dataFrame = dataFrame.groupby('Orgão Subordinado').agg({'Valor Liquidado' : sum})


dataFrame.plot(kind='pie', y='Valor Liquidado', 
          shadow=False, label='', legend=True, autopct='%1.1f%%', startangle=320, 
          title='Execução da despesa por Orgão Subordinado', figsize=(15, 12))

print(dataFrame)

plt.show()

