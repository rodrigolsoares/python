import csv
import utils.file as file



print('Start proccess')

print('Read files of type zip')
zipFiles = file.searchFiles(file.inputFile)

print('to extract file')
for zipFile in zipFiles:
    print(zipFile)
    file.unzipFile(zipFile, file.outputFile)
