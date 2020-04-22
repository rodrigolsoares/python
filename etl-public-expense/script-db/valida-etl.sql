--Verificando se não subiu nenhum registro duplicado na tabela dimensão TBL_DIMENSAO_ORGAO
select CD_ORGAO_SUPERIOR, CD_ORGAO_SUBORDINADO, CD_UNIDADE_ORCAMENTARIA, count(*) from TBL_DIMENSAO_ORGAO 
group by CD_ORGAO_SUPERIOR, CD_ORGAO_SUBORDINADO, CD_UNIDADE_ORCAMENTARIA
having count(*) > 1
