# importing required classes
import os
from pypdf import PdfReader
from Candidate import Candidate
from ElectoralRace import ElectoralRace
from TemplateRecord import TemplateRecord
from FileUrlEntry import FileUrlEntry
from urllib.parse import urlparse, unquote

# election constants
ELECTION = '2024 GENERAL'
STATE = 'PENNSYLVANIA'
COUNTY = 'HUNTINGDON COUNTY'
RESULT_STATUS = "OFFICIAL RESULTS"
DATETIME_RETRIEVED = "11/05/2024 11:30 PM"

URL_LIST_FILENAME = "URL_List.txt"

# Modes of vote result
MODE_ELECTION_DAY = 'ELECTION DAY'
MODE_MAIL_IN = 'MAIL-IN'
MODE_PROVISIONAL = 'PROVISIONAL'
MODE_TOTAL = 'TOTAL'


"""
HUNTINGDON County Specific constants
"""
OFFICE_RANKING = [
	'PRESIDENTIAL ELECTORS',
	'UNITED STATES SENATOR',
	'ATTORNEY GENERAL',
	'AUDITOR GENERAL',
	'STATE TREASURER',
	'REPRESENTATIVE IN CONGRESS',
	'REPRESENTATIVE IN THE GENERAL ASSEMBLY'
]
END_OF_OFFICE_MARKER = 'Write-In Totals'
DATETIME_SEARCH_STRING = 'Precinct Summary - '
# Indices for each page
INDEX_PRECINCT = 5
# Indices of fields starting from candidate name
COLUMN_COUNT = 10
# Number of fields from office to first candidate name.
HEADER_FIELD_COUNT = 8
INDEX_DATE = 16
INDEX_TIME = 15

INDEX_PRECINCT_NAME = 0
INDEX_FIRST_CANDIDATE = 24
INDEX_PARTY = 0
INDEX_CANDIDATE_NAME = 1
INDEX_VOTES_MAIL = 2
INDEX_VOTES_ED = 1
INDEX_VOTES_PROV = 3
INDEX_VOTES_TOTAL = 0

def extractCandidateName(listedName):
	"""
	Presidential candidates have " - presidential candidate" after their name.
	Return name with this removed, else, name unchanged.
	"""
	if " - " in listedName:
		end = listedName.find(" - ")
		return listedName[:end]
	return listedName

def extractPrecinctName(txt):
	return txt[INDEX_PRECINCT]

def extractDateTime(txt):
	for line in txt:
		if line.startswith(DATETIME_SEARCH_STRING):
			return line.replace(DATETIME_SEARCH_STRING, '')
	return 'UNKNOWN'

def determineIfPresidential(rank):
	if rank == 'PRESIDENTIAL ELECTORS':
		return True
	return False

def votesToInt(strVotes):
	""" Convert string to integer. """
	str2 = strVotes.replace(',', '') # Remove any commas
	return int(str2)

def findFirstNumber(strArray):
	""" Find first numeric field in an array of strings. """
	i = 0
	for line in strArray:
		if line.isnumeric():
			return i
		i += 1
	return -1

def normalizeCandidateName(indexToCounts, name, fields):
	n = name
	if (indexToCounts > 1):
		for j in range(2, indexToCounts):
			if fields[j] == '/':
				break
			n = n + ' ' + fields[j]
	return n

def readLinksFile(resultsDir):
	"""
	The URL Links file is developer-created.  It must be in the county directory with a fixed name.
	"""
	filePath = os.path.join(resultsDir, URL_LIST_FILENAME)
	urlList = []
	f = open(filePath, "r")
	for line in f:
		urlList.append(line.replace('\n', ''))
	return urlList

def createFileUrlDict(filePaths, urls):
	"""
	Create a list that allows us to get the source URL, given a filename.
	"""
	entryList = []
	for url in urls:
		urlUnquoted = unquote(url).replace('\n', '')
		for f in filePaths:
			filename = os.path.basename(f)
			if urlUnquoted.endswith(filename):
				entry = FileUrlEntry(filename, url)
				entryList.append(entry)
	return entryList

def findUrl(entryList, filename):
	"""
	Seach through list of FileUrlEntry items for one with matching filename.  Return its URL.
	"""
	f = os.path.basename(filename)
	for entry in entryList:
		if entry.filename == f:
			return entry.url
	return 'UNKNOWN_URL'

def createRecord(race, candidate, votes, vote_mode, is_writein):
	"""
	Create record suitable for printing CSV
	"""
	t = TemplateRecord()
	t.election = ELECTION
	t.state = race.state
	t.county = race.county
	t.jurisdiction = race.county
	t.precinct = race.precinct
	t.office = candidate.office
	t.candidate = candidate.name
	t.party = candidate.party
	t.vote_mode = vote_mode
	t.votes = votes
	t.writein = is_writein
	t.result_status = race.resultStatus
	t.source_url = race.source_url
	t.source_filename = race.filename
	t.datetime_retrieved = race.dateTime
	return t


# Parse the choices for a section representing a single race.
def parseRace(raceDef):
	"""
	Parse a single race (section) of the vote results.
	"""
	txt = raceDef.pageText
	candidateOffset = raceDef.candidateStartIndex
	office = raceDef.officeName

	# Go through all lines in a section (race)
	for line in range(0, 100):
		dataStart = candidateOffset
		if dataStart >= raceDef.endOfDataIndex:
			# We are done with this section.
			return
		# Start parsing:
		candidateLine = txt[candidateOffset]
		fields = candidateLine.replace(',', '').split(' ')
		party = fields[INDEX_PARTY]
		candidateName = fields[INDEX_CANDIDATE_NAME]
		countStartIndex = findFirstNumber(fields)
		candidateName = normalizeCandidateName(countStartIndex, candidateName, fields)
		votes_mail = fields[INDEX_VOTES_MAIL + countStartIndex]
		votes_ed = fields[INDEX_VOTES_ED + countStartIndex]
		votes_prov = fields[INDEX_VOTES_PROV + countStartIndex]
		votes_total = fields[INDEX_VOTES_TOTAL + countStartIndex]
		c = Candidate(office)
		c.name = candidateName
		c.party = party
		c.votes_ed = votesToInt(votes_ed)
		c.votes_mail = votesToInt(votes_mail)
		c.votes_prov = votesToInt(votes_prov)
		c.votes_total = votesToInt(votes_total)
		raceDef.candidates.append(c)
		candidateOffset += 1   # All vote counts for a candidate are in a single line, so just bump by 1.

def parseFile(usState, county, status, filePath, fileUrlList):
	""" 
	parse all pages in vote results PDF file. 
	"""
	filename = os.path.basename(filePath)
	url = findUrl(fileUrlList, filePath)
	reader = PdfReader(filePath)
	total = len(reader.pages)
	precinct = 'UNKNOWN'
	dateTime = 'UNKNOWN'

	races = []
	# creating a page object
	for pageNo in range(0, total):
		page = reader.pages[pageNo]
		pageTxt = page.extract_text().splitlines()
		# Take precinct name from each page.
		precinct = extractPrecinctName(pageTxt)
		dateTime = extractDateTime(pageTxt)
		i = 0
		currentRace = ElectoralRace(url, filename, usState, county, precinct, status, i, dateTime)
		for line in pageTxt:
			# Find the offices
			for rank in OFFICE_RANKING:
				if line.startswith(rank):
					currentRace.pageText = pageTxt
					currentRace.startIndex = i
					currentRace.officeName = rank
					currentRace.isPresidential = determineIfPresidential(rank)
					currentRace.candidateStartIndex = i + HEADER_FIELD_COUNT
			# Find end of section
			if line.startswith(END_OF_OFFICE_MARKER):
				currentRace.endOfDataIndex = i
				races.append(currentRace)
				currentRace = ElectoralRace(url, filename, usState, county, precinct, status, i, dateTime)

			# Bump line number
			i += 1

		# End of page
	# End of document
	return races
# End method

def getFiles(resultsDir):
	"""
	Get paths to all PDF files in a given directory.
	Return a list of paths, or an empty list if there was a problem.
	"""
	pdfPaths = []
	if not os.path.exists(resultsDir):
		print(f"Error: {resultsDir} does not exist in the current directory.")
		return []
	if os.path.isfile(resultsDir):
		pdfPaths.append(resultsDir)
		return pdfPaths
	pdfFiles = [f for f in os.listdir(resultsDir) if f.endswith(".pdf")]
	if len(pdfFiles) == 0:
		print(f"Warning: No PDF files exist in {resultsDir}")
		return []
	pdfFiles.sort()
	for f in pdfFiles:
		pdfPaths.append(os.path.join(resultsDir, f))
	return pdfPaths


def printAll(races):
	"""
	Format and output results of all races.
	"""
	rows = []
	if len(races) == 0:
		print("No races found!")
		return
	for race in races:
		for c in race.candidates:
			rows.append(createRecord(race, c, c.votes_ed, MODE_ELECTION_DAY, 0))
			rows.append(createRecord(race, c, c.votes_prov, MODE_PROVISIONAL, 0))
			rows.append(createRecord(race, c, c.votes_mail, MODE_MAIL_IN, 0))
			rows.append(createRecord(race, c, c.votes_total, MODE_TOTAL, 0))

	print(rows[0].header())
	for row in rows:
		print(row)

###########################
#		MAIN
###########################

# inputPath = 'PA/Huntingdon/Final-Count-Precinct-Summary-(11-8-24).pdf'
inputPath = 'PA/Huntingdon/Results_PDF'
inputFilePaths = getFiles(inputPath)
urlLinks = readLinksFile(inputPath)
fileUrlList = createFileUrlDict(inputFilePaths, urlLinks)

allRaces = []
for filePath in inputFilePaths:
	races = parseFile(STATE, COUNTY, RESULT_STATUS, filePath, fileUrlList)

	for race in races:
		parseRace(race)
		allRaces.append(race)

printAll(allRaces)

# DONE
