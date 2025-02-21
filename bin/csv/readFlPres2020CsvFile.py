from readCsvFile import processCsvFile, printContest
import os

""" Read data for FL 2020 Presidential race. """

FILE = 'all.csv'
presContestName = 'President of the United States'
path = os.path.join('FL', '2020-Pres', FILE)

contests = processCsvFile(path)
printContest(presContestName, contests)