import csv
import file

inputFile = '[path directory input]'
outputFile = '[path directory out put zip]'

print('Start proccess')

print('Read files of type zip')
zipFiles = file.searchFiles(inputFile)

print('to extract file')
for zipFile in zipFiles:
    print(zipFile)
    file.unzipFile(zipFile, outputFile)


rows = list()

print('Read csv files')
csvFiles = file.searchFiles(outputFile)

for csvFilePath in csvFiles:
    with open(csvFilePath, 'r', encoding='Windows-1252') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            rows.append(row)


for row in rows:
    print(row)