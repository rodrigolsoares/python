import mySqlConn
import pandas as pd
import matplotlib.pyplot as plt

query = 'select * from TBL_FATO F, TBL_DIMENSAO_ORGAO O where O.PK_ORGAO = F.FK_ORGAO'
dataFrame = pd.read_sql(query, con=mySqlConn.getConnection())  

data = dataFrame.groupby('NM_ORGAO_SUPERIOR').agg({'VLR_LIQUIDADO' : sum, 'VLR_ORCADO' : sum})

ax = plt.gca()

data.plot(kind='pie', y='VLR_LIQUIDADO', 
          shadow=False, label='', legend=True, 
          title='Execução da despesa por Órgão Superior', figsize=(8, 8), ax=ax)

#data.plot.area()
plt.show(block=True)

