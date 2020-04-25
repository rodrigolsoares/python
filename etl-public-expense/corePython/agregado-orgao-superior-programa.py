import utils.mySqlConn as mySqlConn
import pandas as pd
import matplotlib.pyplot as plt

query = '''select O.NM_ORGAO_SUPERIOR AS 'Orgão Superior', 
                P.NM_PROGRAMA_ORCAMENTARIO AS 'Programa Orçamentário', 
                sum(F.VLR_LIQUIDADO) AS 'Valor Liquidado'
                from TBL_FATO F, 
                    TBL_DIMENSAO_ORGAO O,
                    TBL_DIMENSAO_PROGRAMA P
            where O.PK_ORGAO = F.FK_ORGAO 
            AND P.PK_PROGRAMA = F.FK_PROGRAMA
            And VLR_LIQUIDADO > 0
            group by O.NM_ORGAO_SUPERIOR, P.NM_PROGRAMA_ORCAMENTARIO 
            order by sum(F.VLR_LIQUIDADO) DESC'''

dataFrame = pd.read_sql(query, con=mySqlConn.getConnection()) 
                                                
dataFrame.loc[(dataFrame['Valor Liquidado'] <= 700000000000.00), 'Orgão Superior'] = 'Outros'
dataFrame.loc[(dataFrame['Valor Liquidado'] <= 700000000000.00), 'Programa Orçamentário'] = 'Outros'
dataFrame = dataFrame.groupby(['Orgão Superior', 'Programa Orçamentário']).agg({'Valor Liquidado' : sum})


dataFrame.plot(kind='pie', y='Valor Liquidado', 
          shadow=False, label='', legend=True, autopct='%1.1f%%', startangle=149, 
          title='Execução da despesa por Órgão Superior e Programa Orçamentário', figsize=(15, 10))

print(dataFrame)

plt.show()

