"""
This file parses PDF election results that are collated into a single file.
Typically, the bottom of the page may say 'Report generated with Electionware'.
It may have one or several races per page.
"""
import os
from pypdf import PdfReader
from Candidate import Candidate
from ElectoralRace import ElectoralRace
from TemplateRecord import TemplateRecord
from FileUrlEntry import FileUrlEntry
from FormatSpec import FormatSpec
from ElectionGlobals import Globals
from urllib.parse import urlparse, unquote

"""
County-specific constants
"""

END_OF_OFFICE_MARKER = 'WRITE-IN'
# Indices for each page
PRECINCT_PREFIX = 'Precinct '
# Indices of fields starting from candidate name
COLUMN_COUNT = 10
INDEX_DATE = 6
INDEX_TIME = 7

INDEX_PRECINCT_NAME = 0
INDEX_FIRST_CANDIDATE = 24
INDEX_CANDIDATE_NAME = 1

def extractCandidateName(listedName):
	"""
	Presidential candidates have " - presidential candidate" after their name.
	Return name with this removed, else, name unchanged.
	"""
	if " - " in listedName:
		end = listedName.find(" - ")
		return listedName[:end]
	return listedName

def extractPrecinctName(formatSpec, txt):
	p = txt[formatSpec.precinct_name_index]
	if p.startswith(PRECINCT_PREFIX):
		p = p.replace(PRECINCT_PREFIX, '')
	return p

def extractDateTime(formatSpec, txt):
	""" The date/time is often on a line like: 'Precinct Summary - 11/21/2024 10:39 AM """
	if formatSpec.date_index > 0:
		d = txt[formatSpec.date_index]
		t = txt[formatSpec.time_index]
		return f"{d} {t}"
	for line in txt:
		indx = line.find(formatSpec.datetime_search_string)
		if indx >= 0:
			rtnLine = line[indx + len(formatSpec.datetime_search_string):len(line)]
			pgIndex = rtnLine.find('Page')
			if pgIndex > 0:
				rtnLine = rtnLine[0:pgIndex] #  Remove any page number after the date/time
			return rtnLine
	return 'UNKNOWN'

def extractResultsType(formatSpec, txt):
	return txt[formatSpec.results_type_index]

def determineIfPresidential(rank):
	if rank == 'PRESIDENTIAL ELECTORS':
		return True
	return False

def getHeaderFieldCount(fmtSpec):
	""" Returns Number of fields from office to first candidate name. """
	return fmtSpec.header_field_count

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
	# Special case a single entry
	if len(urls) == 1 and len(filePaths) == 1:
		filename = os.path.basename(filePaths[0])
		entry = FileUrlEntry(filename, urls[0])
		entryList.append(entry)
		return entryList
	# Multiple lists
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
	lineSpec = raceDef.formatSpec.lineSpec

	# Go through all lines in a section (race)
	for line in range(0, 100):
		dataStart = candidateOffset
		if dataStart >= raceDef.raceIndexEnd:
			# We are done with this section.
			return
		# Start parsing:
		candidateLine = txt[candidateOffset]
		fields = candidateLine.replace(',', '').split(' ')
		party = fields[lineSpec.party_index]
		candidateName = fields[INDEX_CANDIDATE_NAME]
		countStartIndex = findFirstNumber(fields)
		candidateName = normalizeCandidateName(countStartIndex, candidateName, fields)
		votes_mail = fields[lineSpec.votes_mail_index + countStartIndex]
		votes_ed = fields[lineSpec.votes_ed_index + countStartIndex]
		votes_prov = fields[lineSpec.votes_prov_index + countStartIndex]
		votes_total = fields[lineSpec.votes_total_index + countStartIndex]
		c = Candidate(office)
		c.name = candidateName
		c.party = party
		c.votes_ed = votesToInt(votes_ed)
		c.votes_mail = votesToInt(votes_mail)
		c.votes_prov = votesToInt(votes_prov)
		c.votes_total = votesToInt(votes_total)
		raceDef.candidates.append(c)
		candidateOffset += 1   # All vote counts for a candidate are in a single line, so just bump by 1.

def parseFile(usState, usStateAbbrev, formatSpec, filePath, fileUrlList):
	""" 
	parse all pages in vote results PDF file. 
	"""
	filename = os.path.basename(filePath)
	url = findUrl(fileUrlList, filePath)
	reader = PdfReader(filePath)
	total = len(reader.pages)
	precinct = 'UNKNOWN'
	dateTime = 'UNKNOWN'
	headerFieldCount = getHeaderFieldCount(formatSpec)

	races = []
	# creating a page object
	for pageNo in range(0, total):
		page = reader.pages[pageNo]
		pageTxt = page.extract_text().splitlines()
		# Take precinct name from each page.
		precinct = extractPrecinctName(formatSpec, pageTxt)
		dateTime = extractDateTime(formatSpec, pageTxt)
		resultStatus = extractResultsType(formatSpec, pageTxt)

		i = 0
		for line in pageTxt:
			# Find the offices
			for rank in Globals.OFFICE_RANKING:
				if line.upper().startswith(rank):
					currentRace = ElectoralRace(url, filename, usState, usStateAbbrev, formatSpec, precinct, resultStatus, i, dateTime)
					currentRace.pageText = pageTxt
					currentRace.page = pageNo
					currentRace.raceStartIndex = i
					currentRace.officeName = line
					currentRace.isPresidential = determineIfPresidential(rank)
					currentRace.candidateStartIndex = i + headerFieldCount
					break
			# Find end of section
			if line.upper().startswith(END_OF_OFFICE_MARKER):
				currentRace.raceIndexEnd = i
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
	if len(races) == 0:
		print("No races found!")
		return
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

def readCountyResults(usState, usStateAbbrev, fmtSpec):
	inputPath = os.path.join(usStateAbbrev, fmtSpec.county, Globals.RESULTS_DIR)
	inputFilePaths = getFiles(inputPath)
	urlLinks = readLinksFile(inputPath)
	fileUrlList = createFileUrlDict(inputFilePaths, urlLinks)

	allRaces = []
	for filePath in inputFilePaths:
		races = parseFile(usState, usStateAbbrev, fmtSpec, filePath, fileUrlList)

		for race in races:
			parseRace(race)
			allRaces.append(race)

	printAll(allRaces)
# DONE
	

