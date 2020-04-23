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
