# ETL de despesa da governo federal

Este projeto é uma atividade que importa para os arquivos csv adquiridos na portal transparência <br /> 
do governo federal, e importa no banco o mysql Server utilizando python3 com pandas, e utilizando a <br />
biblioteca matplotlib gera gráficos do tipo pizza

## Url para downloads dos arquivos
http://www.portaltransparencia.gov.br/download-de-dados/despesas-execucao <br /> 
http://www.portaltransparencia.gov.br/download-de-dados/orcamento-despesa <br /> 

## Url dicionário de dados
http://www.portaltransparencia.gov.br/pagina-interna/603453-dicionario-de-dados-execucao-da-despesa  <br /> 
http://www.portaltransparencia.gov.br/pagina-interna/603417-dicionario-de-dados-orcamento-da-despesa <br /> 


## Bibliotecas necessárias
> Versão do Python 3 <br />
> sudo pip3 install mysql-connector-python <br />
> sudo pip3 install pandas <br />
> sudo pip3 install matplotlib <br />

## Arquivo file.py
> Altere as seguintes variáveis abaixo, que estão no arquivo file

### caminho do arquivo:
>  corePython/utils/file.py


### Variáveis:

>  inputFile: [Caminho dos arquivos zips] <br />
>  outputFile: [Caminho onde armazenaremos o extract dos arquivos zips] <br />


### Configuração database
>  Para configurar o database alterar os parametros do arquivo mySqlConn.py

