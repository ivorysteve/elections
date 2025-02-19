import csv
import os
from CsvRow import CsvRow
from Contest import Contest


def readFile(path):
	"""
	Read CSV file
	"""
	rows = []
	csvFile = open(path, "r")
	freader = csv.reader(csvFile, delimiter=',', quotechar='|')
	i = 0
	for r in freader:
		if i == 0:
			""" Skip header """
			i = 1
			continue
		rows.append(CsvRow(r))
	return rows
			
FILE = 'all.csv'

path = os.path.join('FL', FILE)
if not os.path.exists(path):
	print(f"Error: {path} does not exist in the current directory.")

""" Read entire file. """
allContests = {}
allrecs = readFile(path)
for rec in allrecs:
	contest = rec.contest
	if allContests.get(contest) == None:
		allContests[contest] = Contest(contest)
	curContest = allContests.get(contest)
	curContest.addCandidate(rec.candidate, rec.party, rec.county, rec.precinctVotes)



presContestName = 'President and Vice President'
presContest = allContests.get(presContestName)
candidates = presContest.candidates.keys()
header = "County"
for c in candidates:
	candidateResults = presContest.candidates.get(c)
	header = header + ',' + c
print(header)
""" Get counties from first row. """
trumpName = 'Trump / Vance'
trumpResults = presContest.candidates.get(trumpName)
for c in trumpResults.counties.keys():
    row = f"{c}"
    for candidate in candidates:
        candidateResults = presContest.candidates.get(candidate)
        votes = candidateResults.counties.get(c)
        row = row + f",{votes}"
    print(row)
	


""" Format output """
presContestName = 'President and Vice President'
presContest = allContests.get(presContestName)
trumpName = 'Trump / Vance'
trumpResults = presContest.candidates.get(trumpName)
harrisName = 'Harris / Walz'
harrisResults = presContest.candidates.get(harrisName)
steinName = 'Stein / Ware'
steinResults =presContest.candidates.get(steinName)
print(f"County,{trumpName},{harrisName}")
for c in trumpResults.counties.keys():
	trumpVotes = trumpResults.counties.get(c)
	harrisVotes = harrisResults.counties.get(c)
	print(f"{c},{trumpVotes},{harrisVotes}")



def printEverything(allContests):
    """ Print all results. """
    for j in allContests.keys():
        contest = allContests.get(j)
        for i in contest.candidates.keys():
            candidate = contest.candidates.get(i)
            print(f"{i}:")
            for c in candidate.keys():
                countyVotes = candidate.get(c)
                print(f"...{c}: {countyVotes}")
			


