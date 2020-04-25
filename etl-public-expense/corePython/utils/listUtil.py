import pandas as pd

def geraListaSemDuplicidade(values):
    dfFilter = pd.DataFrame(values) 
    dfFilter = dfFilter.drop_duplicates()
    listaFiltrada = list(dfFilter.itertuples(index=False,name=None))

    out = []

    for tupleRecord in listaFiltrada:
        for record in tupleRecord:
            if(record != None ):
                out.append(record)


    dfFilter = pd.DataFrame(out) 
    dfFilter = dfFilter.drop_duplicates()
    listaFiltrada = list(dfFilter.itertuples(index=False,name=None))

    out = []

    for tupleRecord in listaFiltrada:
        out.append(tupleRecord)

    return out


def geraLista(values):
    dfFilter = pd.DataFrame(values) 
    listaFiltrada = list(dfFilter.itertuples(index=False,name=None))

    out = []

    for tupleRecord in listaFiltrada:
        for record in tupleRecord:
            if(record != None ):
                out.append(record)

    return out
    