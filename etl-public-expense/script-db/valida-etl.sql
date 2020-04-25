--hAbilitando truncate
--SET SQL_SAFE_UPDATES = 0;

--Verificando se não subiu nenhum registro duplicado na tabela dimensão TBL_DIMENSAO_ORGAO
select CD_ORGAO_SUPERIOR, CD_ORGAO_SUBORDINADO, CD_UNIDADE_ORCAMENTARIA, count(*) from TBL_DIMENSAO_ORGAO 
group by CD_ORGAO_SUPERIOR, CD_ORGAO_SUBORDINADO, CD_UNIDADE_ORCAMENTARIA
having count(*) > 1

--Verificando se não subiu nenhum registro duplicado na tabela dimensão TBL_DIMENSAO_PROGRAMA
select CD_PROGRAMA_ORCAMENTARIO, CD_ACAO, count(*) from TBL_DIMENSAO_PROGRAMA 
group by CD_PROGRAMA_ORCAMENTARIO, CD_ACAO
having count(*) > 1

--Na tabela TBL_DIMENSAO_PROGRAMA existe dados duplicados, pois existem registros de digitação, como o exemplo abaixo
--
--
select * from TBL_DIMENSAO_PROGRAMA 
where CD_PROGRAMA_ORCAMENTARIO = 120
  and CD_ACAO = '6553'

--Total de registros nas tabelas dimensões
select count(*) from TBL_DIMENSAO_ORGAO 
select count(*) from TBL_DIMENSAO_PROGRAMA 

--Exemplo query agregação
select O.NM_ORGAO_SUPERIOR, 
format(sum(F.VLR_ORCADO), 2, 'de_DE') ORCADO, format(sum(F.VLR_LIQUIDADO), 2, 'de_DE')   LIQUIDADO
from TBL_FATO F, TBL_DIMENSAO_ORGAO O
where O.PK_ORGAO = F.FK_ORGAO
  AND O.NM_ORGAO_SUPERIOR = 'Ministério da Previdência Social'
group by O.NM_ORGAO_SUPERIOR

--Orgao Superior
SELECT DISTINCT NM_ORGAO_SUPERIOR FROM TBL_DIMENSAO_ORGAO 
ORDER BY NM_ORGAO_SUPERIOR

--Verificando o espaço em disco utilizando pelo banco de dados MB
select table_schema, sum((data_length+index_length)/1024/1024) AS MB 
from information_schema.tables 
where table_schema = 'etl_despesa_publica'
group by 1;

--Verificando o espaço em disco utilizando pelo banco de dados GB
select table_schema, sum((data_length+index_length)/1024/1024/1024) AS GB
from information_schema.tables 
where table_schema = 'etl_despesa_publica'
group by 1;


/**
* Query referente aos graficos de agregação
*
**/

--Query agregado função
select A.NM_FUNCAO AS 'Nome Função', 
	format(sum(F.VLR_LIQUIDADO), 2, 'de_DE') AS 'Valor Liquidado'
from TBL_FATO F, TBL_DIMENSAO_AREA_ATUACAO A
where A.PK_AREA_ATUACAO = F.FK_AREA_ATUACAO
group by A.NM_FUNCAO
order by sum(F.VLR_LIQUIDADO) DESC


--Query agregado orgão subordinado
select O.NM_ORGAO_SUBORDINADO AS 'Orgão Subordinado', 
    format(sum(F.VLR_LIQUIDADO), 2, 'de_DE')  AS 'Valor Liquidado'
    from TBL_FATO F, TBL_DIMENSAO_ORGAO O 
where O.PK_ORGAO = F.FK_ORGAO 
group by O.NM_ORGAO_SUBORDINADO 
order by sum(F.VLR_LIQUIDADO) DESC

--Query agregado orgão superior e programa orçamentário
select O.NM_ORGAO_SUPERIOR AS 'Orgão Superior', 
    P.NM_PROGRAMA_ORCAMENTARIO AS 'Programa Orçamentário', 
    format(sum(F.VLR_LIQUIDADO), 2, 'de_DE') AS 'Valor Liquidado'
    from TBL_FATO F, 
        TBL_DIMENSAO_ORGAO O,
        TBL_DIMENSAO_PROGRAMA P
where O.PK_ORGAO = F.FK_ORGAO 
AND P.PK_PROGRAMA = F.FK_PROGRAMA
And VLR_LIQUIDADO > 0
group by O.NM_ORGAO_SUPERIOR, P.NM_PROGRAMA_ORCAMENTARIO 
order by sum(F.VLR_LIQUIDADO) DESC

--Query agregado orgão superior
select O.NM_ORGAO_SUPERIOR AS 'Orgão Superior', 
    format(sum(F.VLR_LIQUIDADO), 2, 'de_DE') AS 'Valor Liquidado'
    from TBL_FATO F, TBL_DIMENSAO_ORGAO O 
where O.PK_ORGAO = F.FK_ORGAO 
group by O.NM_ORGAO_SUPERIOR 
order by sum(F.VLR_LIQUIDADO) DESC

--orgão agregado programa orçamentário
select P.NM_PROGRAMA_ORCAMENTARIO AS 'Nome Programa', 
    format(sum(F.VLR_LIQUIDADO), 2, 'de_DE')  AS 'Valor Liquidado'
from TBL_FATO F, TBL_DIMENSAO_PROGRAMA P
where P.PK_PROGRAMA = F.FK_PROGRAMA
group by P.NM_PROGRAMA_ORCAMENTARIO
order by sum(F.VLR_LIQUIDADO) DESC