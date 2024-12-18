"""
This file parses PDF election results that are contained in multiple files.
"""
import os
from pypdf import PdfReader
from Candidate import Candidate
from ElectoralRace import ElectoralRace
from TemplateRecord import TemplateRecord
from FileUrlEntry import FileUrlEntry
from urllib.parse import urlparse, unquote
from ElectionGlobals import Globals

# election constants
RESULT_STATUS = "OFFICIAL RESULTS"
DATETIME_RETRIEVED = "11/05/2024 11:30 PM"

"""
County-specific constants
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
END_OF_OFFICE_MARKER = 'Cast Votes'

# Indices of fields starting from candidate name
COLUMN_COUNT = 10
# Number of fields from office to first candidate name.
HEADER_FIELD_COUNT = 7
INDEX_DATE = 16
INDEX_TIME = 15

INDEX_PRECINCT_NAME = 0
INDEX_FIRST_CANDIDATE = 24
INDEX_PARTY = 1
INDEX_VOTES_MAIL = 2
INDEX_VOTES_ED = 4
INDEX_VOTES_PROV = 6
INDEX_VOTES_TOTAL = 8

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
	""" Here, precinct name in all caps is first string in page."""
	return txt[0]

def extractDateTime(txt):
	d = txt[INDEX_DATE]
	t = txt[INDEX_TIME]
	return f"{d} {t}"

def determineIfPresidential(rank):
	if rank == 'PRESIDENTIAL ELECTORS':
		return True
	return False

def votesToInt(strVotes):
	""" Convert string to integer. """
	str2 = strVotes.replace(',', '') # Remove any commas
	return int(str2)

def readLinksFile(resultsDir):
	"""
	The URL Links file is developer-created.  It must be in the county directory with a fixed name.
	"""
	filePath = os.path.join(resultsDir, Globals.URL_LIST_FILENAME)
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

# Parse the choices for a section representing a single race.
def parseRace(raceDef):
	"""
	Parse a single race (section) of the vote results.
	"""
	txt = raceDef.pageText
	candidateOffset = raceDef.candidateStartIndex
	office = raceDef.officeName
	candidateColumnCount = COLUMN_COUNT
	isPresidentialOffset = 0
	# If presidential race, one extra line for VP.
	if raceDef.isPresidential == True:
		candidateColumnCount += 1
		isPresidentialOffset = 1
	# Go through all lines in a section (race)
	for line in range(0, 100):
		dataStart = candidateOffset + isPresidentialOffset
		if dataStart >= raceDef.endOfDataIndex:
			# We are done with this section.
			return
		# Start parsing: 
		candidateName = extractCandidateName(txt[candidateOffset])
		party = txt[INDEX_PARTY + dataStart]
		votes_mail = txt[INDEX_VOTES_MAIL + dataStart]
		votes_ed = txt[INDEX_VOTES_ED + dataStart]
		votes_prov = txt[INDEX_VOTES_PROV + dataStart]
		votes_total = txt[INDEX_VOTES_TOTAL + dataStart]
		c = Candidate(office)
		c.name = candidateName
		c.party = party
		c.votes_ed = votesToInt(votes_ed)
		c.votes_mail = votesToInt(votes_mail)
		c.votes_prov = votesToInt(votes_prov)
		c.votes_total = votesToInt(votes_total)
		raceDef.candidates.append(c)
		candidateOffset += candidateColumnCount

def parseFile(usState, usStateAbbrev, county, status, filePath, fileUrlList):
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
		# Take precinct name from the first page.
		if pageNo == 0:
			precinct = extractPrecinctName(pageTxt)
			dateTime = extractDateTime(pageTxt)
		i = 0
		for line in pageTxt:
			# Find the offices
			for rank in OFFICE_RANKING:
				if line.startswith(rank):
					currentRace = ElectoralRace(url, filename, usState, usStateAbbrev, county, precinct, status, i, dateTime)
					currentRace.pageText = pageTxt
					currentRace.startIndex = i
					currentRace.page = pageNo
					currentRace.officeName = rank  # We take the whole line in the singleDoc version
					currentRace.isPresidential = determineIfPresidential(rank)
					currentRace.candidateStartIndex = i + HEADER_FIELD_COUNT
			# Find end of section
			if line.startswith(END_OF_OFFICE_MARKER):
				currentRace.endOfDataIndex = i
				races.append(currentRace)

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
	for race in races:
		for c in race.candidates:
			rows.append(TemplateRecord.createRecord(race, c, c.votes_ed, Globals.MODE_ELECTION_DAY, 0))
			rows.append(TemplateRecord.createRecord(race, c, c.votes_prov, Globals.MODE_PROVISIONAL, 0))
			rows.append(TemplateRecord.createRecord(race, c, c.votes_mail, Globals.MODE_MAIL_IN, 0))
			rows.append(TemplateRecord.createRecord(race, c, c.votes_total, Globals.MODE_TOTAL, 0))

	print(rows[0].header())
	for row in rows:
		print(row)

###########################
#		MAIN
###########################

def readCountyResults(usState, usStateAbbrev, county):
	inputPath = os.path.join(usStateAbbrev, county, Globals.RESULTS_DIR)
	inputFilePaths = getFiles(inputPath)
	urlLinks = readLinksFile(inputPath)
	fileUrlList = createFileUrlDict(inputFilePaths, urlLinks)

	allRaces = []
	for filePath in inputFilePaths:
		races = parseFile(usState, usStateAbbrev, county, RESULT_STATUS, filePath, fileUrlList)

		for race in races:
			parseRace(race)
			allRaces.append(race)

	printAll(allRaces)

# DONE
