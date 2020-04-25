import utils.mySqlConn as mySqlConn
import pandas as pd
import matplotlib.pyplot as plt

query = '''select O.NM_ORGAO_SUPERIOR AS 'Orgão Superior', 
                sum(F.VLR_LIQUIDADO) AS 'Valor Liquidado'
                from TBL_FATO F, TBL_DIMENSAO_ORGAO O 
            where O.PK_ORGAO = F.FK_ORGAO 
            group by O.NM_ORGAO_SUPERIOR 
            order by sum(F.VLR_LIQUIDADO) DESC'''

dataFrame = pd.read_sql(query, con=mySqlConn.getConnection())  
dataFrame.loc[(dataFrame['Valor Liquidado'] <= 300000000000.00), 'Orgão Superior'] = 'Outros'
dataFrame = dataFrame.groupby('Orgão Superior').agg({'Valor Liquidado' : sum})


dataFrame.plot(kind='pie', y='Valor Liquidado', 
          shadow=False, label='', legend=True, autopct='%1.1f%%', startangle=300, 
          title='Execução da despesa por Órgão Superior', figsize=(9, 7))

print(dataFrame)

plt.show()

