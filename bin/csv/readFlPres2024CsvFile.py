from readCsvFile import processCsvFile, printContest
import os

""" Read data for FL 2024 Presidential race. """

FILE = 'all.csv'
presContestName = 'President and Vice President'
path = os.path.join('FL', '2024-Pres', FILE)

contests = processCsvFile(path)
printContest(presContestName, contests)