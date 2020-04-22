import pandas as pd
import numpy as np

import xlwt

titles = ['Codigo Comercialização','SKU', 'Tipo Comercializacao', 'Status']
styleY = xlwt.easyxf('pattern: pattern solid, fore_colour light_yellow;')
styleG = xlwt.easyxf('pattern: pattern solid, fore_colour gray25;')
styleW = xlwt.easyxf('pattern: pattern solid, fore_colour white;')

branch = 1000

df=pd.read_csv('./compare-result/load_'  + str(branch) + '.csv',delimiter=';')
df.sort_values("codigo-comercializacao", inplace = True)
df = df.applymap(str)

listaComercializacao = df['codigo-comercializacao'].unique()

wb = xlwt.Workbook()

ws = wb.add_sheet('Resumo')
ws.write(1, 1, titles[0], styleY)
ws.write(1, 2, titles[2], styleY)
ws.write(1, 3, titles[3], styleY)

contCapa = 2
registryIn = ''
for codigo in listaComercializacao:
    
    style = styleG

    if(contCapa % 2 == 0):
        style = styleW
    
    ws.write(contCapa, 1, codigo, style)
    ws.write(contCapa, 2, '', style)
    ws.write(contCapa, 3, '', style)
    contCapa += 1

    registryIn += codigo + ',' 

ws.write(3, 5, registryIn )


for codigo in listaComercializacao:
    ws = wb.add_sheet(codigo)
    ws.write(1, 1, titles[0], styleY)
    ws.write(1, 2, titles[1], styleY)

    resultDf = df[df['codigo-comercializacao'] == codigo] 

    cont = 2
    for index, row in resultDf.iterrows():

        style = styleG

        if(cont % 2 == 0):
            style = styleW

        ws.write(cont, 1, codigo, style)
        ws.write(cont, 2, str(row['sku']), style)
        cont += 1

wb.save('./compare-result/notFoundCsv_' + str(branch) + '.xls')

