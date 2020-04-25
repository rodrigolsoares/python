import os
import zipfile

inputFile = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho-etl-pandas/zip/'
outputFile = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho-etl-pandas/csvFile/'

pathFileDespesa = outputFile
pathAndFileOrcamento = f'{outputFile}2019_OrcamentoDespesa.zip.csv'


def searchFiles(*directories):
   listFiles = list();
   for item in directories:
        for p, _, files in os.walk(os.path.abspath(item)):
            for file in files:
                listFiles.append(os.path.join(p, file))
   return listFiles

def unzipFile(fileZip, outputFile):
    fantasy_zip = zipfile.ZipFile(fileZip)
    fantasy_zip.extractall(outputFile)
    fantasy_zip.close()










