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
			

def processCsvFile(path):
    """
    Process CSV file
    """
    if not os.path.exists(path):
        print(f"Error: {path} does not exist in the current directory.")
        return {}

    """ Read rows of entire file. """
    allContests = {}
    allrecs = readFile(path)
    for rec in allrecs:
        contest = rec.contest
        if allContests.get(contest) == None:
            allContests[contest] = Contest(contest)
        curContest = allContests.get(contest)
        curContest.addCandidate(rec.candidate, rec.party, rec.county, rec.precinctVotes)
    return allContests


def printContest(contestName, allContests):
    """ Print a specific contest. """
    presContest = allContests.get(contestName)
    candidates = presContest.candidates.keys()
    header = "County"
    firstCandidate = None
    for c in candidates:
        candidateResults = presContest.candidates.get(c)
        header = header + ',' + c
        if firstCandidate == None:
            firstCandidate = c
    print(header)
    """ Get counties from first row. """
    firstResults = presContest.candidates.get(firstCandidate)
    for c in firstResults.counties.keys():
        row = f"{c}"
        for candidate in candidates:
            candidateResults = presContest.candidates.get(candidate)
            votes = candidateResults.counties.get(c)
            row = row + f",{votes}"
        print(row)
	

def printEverything(allContests):
    """ Print all contests. """
    for j in allContests.keys():
        contest = allContests.get(j)
        for i in contest.candidates.keys():
            candidate = contest.candidates.get(i)
            print(f"{i}:")
            for c in candidate.keys():
                countyVotes = candidate.get(c)
                print(f"...{c}: {countyVotes}")
			


