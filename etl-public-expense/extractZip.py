import csv
import file

inputFile = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/input/'
outputFile = '/home/rodrigo/Documents/university/data-manage-and-information/trabalho etl pandas/output/'

print('Start proccess')

print('Read files of type zip')
zipFiles = file.searchFiles(inputFile)

print('to extract file')
for zipFile in zipFiles:
    print(zipFile)
    file.unzipFile(zipFile, outputFile)
