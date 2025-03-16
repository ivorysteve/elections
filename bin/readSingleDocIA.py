"""
This file parses PDF election results for Iowa.
"""
import os
from pypdf import PdfReader
from Elections.Candidate import Candidate
from Elections.ElectoralRace import ElectoralRace
from Elections.ElectionGlobals import Globals
from Elections.ElectionUtils import extractDateTime, extractResultsType
from Elections.ElectionUtils import readLinksFile, getPdfFiles, getHeaderFieldCount, findUrl, createFileUrlDict, findFirstNumber, votesToInt
from urllib.parse import unquote

"""
County-specific constants
"""

SEP = ','
LINES_PER_COUNTY = 3
OFFICE_NAME = 'President and Vice President'
END_OF_HEADER = 'Votes Total'
### There are 3 lines per county: Absentee, Election Day, and Total
FIRST_LINE_KEY = 'DAY '
MIDDLE_LINE_KEY = 'ABSENTEE '
LAST_LINE_KEY = 'TOTAL '

def printRows(races, candidateList):
	""" Print vote totals across a single county. """
	i = 0
	for race in races:
		if i == 0:
			header = 'County' + SEP
			for c in race.candidates:
				header = f"{header}{c.name}{SEP}"
			print(f"{header}")
			i += 1
		totalLine = race.county + SEP
		for c in race.candidates:
			totalLine = f"{totalLine}{c.votes_total}{SEP}"
		print(f"{totalLine}")

def extractCountyName(formatSpec, txt):
	""" County ends with 'Election'. """
	COUNTY_SUFFIX = ' Election'
	p = txt
	if p.find(COUNTY_SUFFIX) > 0:
		p = p.replace(COUNTY_SUFFIX, '')
	return p.strip()

def buildCandidateList(candidateNameList):
	candidateList = []
	for i in range(0, len(candidateNameList)):
		cd = Candidate(OFFICE_NAME)
		cd.name = candidateNameList[i]
		candidateList.append(cd)
	return candidateList

def recordVotes(candidateList, txt, offset):
	line = txt[offset].strip()
	fields = line.replace(',', '').split(' ')
	if len(line.strip()) == 0:
		# Weird issue where there are spaces between last candidate and Write-In.  Ignore these.
		candidateOffset += 1
		return
	for i in range(0, len(candidateList)):
		candidate = candidateList[i]
		voteType = fields[0]
		if voteType == 'Day':
			candidate.votes_ed = fields[i+1]
		elif voteType == 'Absentee':
			candidate.votes_absentee = fields[i+1]
		elif voteType == 'Total':
			candidate.votes_total = fields[i+1]
		

def parseRace(raceDef, candidateNameList):
	"""
	Parse a single race (section) of the vote results.
	"""
	txt = raceDef.pageText
	candidateOffset = raceDef.raceStartIndex
	if raceDef.hasOnlyWriteIns == True:
		# Nothing to do here
		return

	candidateList = buildCandidateList(candidateNameList)
	for candidate in candidateList:
		raceDef.candidates.append(candidate)

	#  IA shows 3 results.  Record each.
	recordVotes(candidateList, raceDef.pageText, raceDef.raceStartIndex)
	recordVotes(candidateList, raceDef.middlePageText, raceDef.middlePageIndex)
	recordVotes(candidateList, raceDef.endPageText, raceDef.endPageIndex)
		

def parseFile(usState, usStateAbbrev, formatSpec, filePath, fileUrlList):
	""" 
	parse all pages in vote results PDF file. 
	"""
	filename = os.path.basename(filePath)
	url = findUrl(fileUrlList, filePath)
	reader = PdfReader(filePath)
	total = len(reader.pages)
	county = 'UNKNOWN'
	dateTime = 'UNKNOWN'
	county = 'UNKNOWN'
	headerFieldCount = getHeaderFieldCount(formatSpec)

	races = []
	currentRace = {}
	startedRace = False
	# creating a page object
	for pageNo in range(0, total):
		page = reader.pages[pageNo]
		pageTxt = page.extract_text().splitlines()
		# Take county name from each page.
		dateTime = extractDateTime(formatSpec, pageTxt)
		resultStatus = extractResultsType(formatSpec, pageTxt)

		i = 0
		pastHeader = False
		for line in pageTxt:
			# Find the header
			if pastHeader == False and line.startswith(END_OF_HEADER):
				pastHeader = True
				i += 1
				continue

			if line.upper().startswith(FIRST_LINE_KEY):
				currentRace = ElectoralRace(url, filename, usState, usStateAbbrev, formatSpec, county, resultStatus, i, dateTime)
				currentRace.county = county
				currentRace.pageText = pageTxt
				currentRace.page = pageNo
				currentRace.raceStartIndex = i
				currentRace.officeName = OFFICE_NAME
				currentRace.candidateStartIndex = i + headerFieldCount
				startedRace = True
				races.append(currentRace)
			elif startedRace == True and line.upper().startswith(LAST_LINE_KEY):
				currentRace.endPageIndex = i
				currentRace.endPageText = pageTxt
				startedRace = False
			elif startedRace == True and line.upper().startswith(MIDDLE_LINE_KEY):
				currentRace.middlePageIndex = i
				currentRace.middlePageText = pageTxt
			elif line.find(' Election') > 0:
				county = extractCountyName(formatSpec, line)

			# Bump line number
			i += 1

		# End of page
	# End of document
	return races
# End method


###########################
#		MAIN
###########################

def readCountyResults(usState, usStateAbbrev, fmtSpec, candidateList):
	""" 
	Read all races in a county, given a format spec.
	"""
	inputPath = os.path.join(usStateAbbrev, fmtSpec.county, Globals.RESULTS_DIR)
	inputFilePaths = getPdfFiles(inputPath)
	urlLinks = readLinksFile(inputPath)
	fileUrlList = createFileUrlDict(inputFilePaths, urlLinks)

	allRaces = []
	for filePath in inputFilePaths:
		races = parseFile(usState, usStateAbbrev, fmtSpec, filePath, fileUrlList)

		for race in races:
			parseRace(race, candidateList)
			allRaces.append(race)

	printRows(allRaces, candidateList)
# DONE
	

