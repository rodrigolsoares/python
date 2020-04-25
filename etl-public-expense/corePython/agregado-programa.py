import utils.mySqlConn as mySqlConn
import pandas as pd
import matplotlib.pyplot as plt

query = '''select P.NM_PROGRAMA_ORCAMENTARIO AS 'Nome Programa', 
                sum(F.VLR_LIQUIDADO) AS 'Valor Liquidado'
            from TBL_FATO F, TBL_DIMENSAO_PROGRAMA P
            where P.PK_PROGRAMA = F.FK_PROGRAMA
            group by P.NM_PROGRAMA_ORCAMENTARIO
            order by sum(F.VLR_LIQUIDADO) DESC'''

dataFrame = pd.read_sql(query, con=mySqlConn.getConnection())  
dataFrame.loc[(dataFrame['Valor Liquidado'] <= 800000000000.00), 'Nome Programa'] = 'Outros'
dataFrame = dataFrame.groupby('Nome Programa').agg({'Valor Liquidado' : sum})


dataFrame.plot(kind='pie', y='Valor Liquidado', 
          shadow=False, label='', legend=True, autopct='%1.1f%%', startangle=357, 
          title='Execução da despesa por Programa Orçamentário', figsize=(15, 12))

print(dataFrame)

plt.show()

