"""
This file parses PDF election results for Iowa.
"""
import os
import re
from pypdf import PdfReader
from Elections.Candidate import Candidate
from Elections.ElectoralRace import ElectoralRace
from Elections.ElectionGlobals import Globals
from Elections.ElectionUtils import extractDateTime, extractResultsType
from Elections.ElectionUtils import readLinksFile, getPdfFiles, getHeaderFieldCount, findUrl
from urllib.parse import unquote

"""
County-specific constants
"""

SEP = ','
LINES_PER_COUNTY = 3
OFFICE_NAME = 'President and Vice President'
END_OF_HEADER = 'Total'
### There are 3 lines per county: Absentee, Election Day, and Total
FIRST_LINE_KEY = 'Election '
MIDDLE_LINE_KEY = 'ABSENTEE '
LAST_LINE_KEY = 'TOTAL '
FIRST_ALT_LINE_KEY = ' Election '

ABSENTEE_TYPE = 'Absentee'
TOTAL_TYPE = 'Total'
ED_TYPE = 'Election Day'

def printRows(races, candidateList):
	""" Print vote totals across a single county. """
	i = 0
	for race in races:
		if i == 0:
			header = 'County' + SEP
			for c in race.candidates:
				if c.name == 'Undervotes' or c.name == 'Overvotes':
					continue
				header = f"{header}{c.name}{SEP}{SEP}{SEP}"
			print(f"{header}")
			header = ' ' + SEP
			for c in race.candidates:
				if c.name == 'Undervotes' or c.name == 'Overvotes':
					continue
				header = f"{header}Election Day{SEP}Absentee{SEP}Total{SEP}"
			print(f"{header}")
			i += 1
		totalLine = race.county + SEP
		for c in race.candidates:
			if c.name == 'Undervotes' or c.name == 'Overvotes':
				continue
			totalLine = f"{totalLine}{c.votes_ed}{SEP}{c.votes_absentee}{SEP}{c.votes_total}{SEP}"
		print(f"{totalLine}")

def findFirstNumber(txt):
	""" Return index of first number in a string. """
	i = 0
	for c in txt:
		if c.isnumeric():
			return i
		i = i + 1
	return i

def findVoteType(line):
	""" Look for key words to see which type of vote count this line is. """
	if line.find(ABSENTEE_TYPE) == 0:
		return ABSENTEE_TYPE
	if line.find(TOTAL_TYPE) == 0:
		return TOTAL_TYPE
	return ED_TYPE
	

def extractCountyName(formatSpec, txt):
	""" County ends with 'Election'. """
	COUNTY_SUFFIX = 'Election '
	p = txt
	suffixInx = p.find(COUNTY_SUFFIX)
	if  suffixInx > 0:
		p = p[0:suffixInx]
	return p.strip()

def consolidateRaces(races, candidateList):
	""" 2020 results are a list of single candidate races"""
	curPrecinct = ''
	newRaces = []
	newCandidates = []
	curRace = False 
	for race in races:
		if curPrecinct != race.precinct:
			curPrecinct = race.precinct
			if curRace != False:
				## Finish old race
				curRace.candidates = newCandidates
				newRaces.append(curRace)
			curRace = race
			newCandidates = []
		
		c = Candidate(OFFICE_NAME)
		oldC = race.candidates[0]
		c.name = oldC.name
		c.party = oldC.party
		c.votes_absentee = oldC.votes_absentee
		c.votes_ed = oldC.votes_ed
		c.votes_total = oldC.votes_total
		print(f"Adding county {race.county} ID {race.raceStartIndex}: {c}")
		newCandidates.append(c)

	# Do last race
	curRace.candidates = newCandidates
	newRaces.append(curRace)
	
	return newRaces

def buildCandidateList(candidateNameList):
	""" Given a list of name/party candidates, build candidate vote counting object. """
	candidateList = []
	for i in range(0, len(candidateNameList)):
		cd = Candidate(OFFICE_NAME)
		cd.name = candidateNameList[i].name
		cd.party = candidateNameList[i].party
		candidateList.append(cd)
	return candidateList

def recordVotes(candidateList, txt, txtOffset):
	""" Votes are in groups of 3 lines (election day, absentee, total) for each candidate. """
	for i in range(0, len(candidateList)):
		candidate = candidateList[i]
		offset = txtOffset + (i * 3)
		if (offset+2) >= len(txt):
			return
		ed_count = txt[offset].strip().replace(',', '')
		abs_count = txt[offset+1].strip().replace(',', '')
		total_count = txt[offset+2].strip().replace(',', '')
		candidate.votes_ed = ed_count
		candidate.votes_absentee = abs_count
		candidate.votes_total = total_count

def recordVotesSingleLine(candidateList, txt, txtOffset):
	""" Handles single line vote counts (2016) """
	line = txt[txtOffset]
	txt = line.replace(',', '')
	startIndx = findFirstNumber(line)
	voteType = findVoteType(line)
	numArr = txt[startIndx:].split(' ')
	for i in range(0, len(candidateList)):
		count = int(numArr[i])
		candidate = candidateList[i]
		if voteType == ED_TYPE:
			candidate.votes_ed = count
		if voteType == ABSENTEE_TYPE:
			candidate.votes_absentee = count
		if voteType == TOTAL_TYPE:
			candidate.votes_total = count


def parseRace(fmtSpec, raceDef, candidateNameList):
	"""
	Parse a single race (section) of the vote results.
	"""
	txt = raceDef.pageText
	if raceDef.hasOnlyWriteIns == True:
		# Nothing to do here
		return

	candidateList = buildCandidateList(candidateNameList)
	for candidate in candidateList:
		raceDef.candidates.append(candidate)

	#  If Single Line:
	if fmtSpec.is_single_line_counts == True:
		recordVotesSingleLine(candidateList, raceDef.pageText, raceDef.raceStartIndex)
		recordVotesSingleLine(candidateList, raceDef.pageText, raceDef.raceStartIndex + 1)
		recordVotesSingleLine(candidateList, raceDef.pageText, raceDef.raceStartIndex + 2)
	else:
		recordVotes(candidateList, raceDef.pageText, raceDef.raceStartIndex)
	# recordVotes(candidateList, raceDef.middlePageText, raceDef.middlePageIndex)
	# recordVotes(candidateList, raceDef.endPageText, raceDef.endPageIndex)
		

def parseFile(usState, usStateAbbrev, formatSpec, filePath, fileUrlList, candidateNameList):
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
	parsed_data = []
	currentRace = {}
	startedRace = False
	# creating a page object
	for pageNo in range(0, total):
		page = reader.pages[pageNo]
		pageTxt = page.extract_text().splitlines()
		# Take county name from each page.
		dateTime = extractDateTime(formatSpec, pageTxt)
		resultStatus = extractResultsType(formatSpec, pageTxt)

		# Special handling for 2020
		if formatSpec.is_2020 == True:
			d = parse_election_data2020(pageTxt, parsed_data)
			parsed_data += d
			continue

		i = 0
		pastHeader = False
		for line in pageTxt:
			# Find the header
			if formatSpec.has_page_header == True and pastHeader == False:
				if line.find(END_OF_HEADER) > 0:
					pastHeader = True
				i += 1
				continue

			if line.find(FIRST_LINE_KEY) > 0:
				county = extractCountyName(formatSpec, line)
				currentRace = ElectoralRace(url, filename, usState, usStateAbbrev, formatSpec, county, resultStatus, i, dateTime)
				currentRace.county = county
				currentRace.pageText = pageTxt
				currentRace.page = pageNo
				currentRace.raceStartIndex = i + formatSpec.start_index_skip  # Ignore 'Absentee' and 'Total'
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
	if formatSpec.is_2020 == True:
		races = createRaces(parsed_data, url, filename, usState, usStateAbbrev, formatSpec, resultStatus, pageNo, dateTime, candidateNameList)
	return races
# End method

""" Support class for Claude.ai """

""" Generated by Claude.ai.   """
def parse_election_data2020(text, curParsedData):
    # List to store all rows of data
    parsed_data = []
    dLen = len(curParsedData)
    
    # Headers for the CSV file
    headers = ["County", "Vote Type", "Trump/Pence (REP)", "Biden/Harris (DEM)", 
               "De La Fuente/Richardson (ALL)", "Blankenship/Mohr (CON)", 
               "King/Chandler (GKH)", "Hawkins/Walker (GRN)", 
               "Jorgensen/Cohen (LIB)", "Pierce/Ballard", 
               "West/Tidball", "Write-in", "Under Votes", "Over Votes", "Total"]
    
    # Add the headers as first row
    if dLen == 0:
        parsed_data.append(headers)
    
    # Split the text into lines
    lines = text # .strip().split('\n')
    
    # Keep track of the current county
    current_county = None
    
    if dLen > 0:
        lastCounty = curParsedData[dLen - 1][0] # First entry is always county
        current_county = lastCounty
    
    # Pattern to match county name line
    county_pattern = re.compile(r'^(.*)\s+Election$')
    
    # Pattern to match data lines
    data_pattern = re.compile(r'^(Day|Absentee|Total)\s+(.+)$')
    
    # Process line by line
    i = 0
    while i < len(lines):
        line = lines[i].replace(',', '').strip()
        
        # Skip page headers and empty lines
        if line.startswith("Page") or line.startswith("Donald J.") or line.startswith("County") or line == "":
            i += 1
            continue
        
        # Check if this is a county name
        county_match = county_pattern.match(line)
        if county_match:
            current_county = county_match.group(1)
            i += 1
            continue
        
        # Check if this is a data line
        data_match = data_pattern.match(line)
        if data_match and current_county:
            vote_type = data_match.group(1)
            
            # Extract all numbers from the line
            data_line = data_match.group(2)
            numbers = re.findall(r'\d+', data_line)
            
            # Create a data row with county and vote type
            row = [current_county, vote_type] + numbers
            parsed_data.append(row)
            
        i += 1
    return parsed_data

def createRaces(parsed_data, url, filename, usState, usStateAbbrev, formatSpec, resultStatus, pageNo, dateTime, candidateNameList):
    races = []
    raceId = 0
    dataLen = len(parsed_data)
    j = 1 # Skip header
    while j < dataLen:
		### XXX WE ARE SKIPPING FIRST COUNTY AFTER PAGE SPLIT.
        prow1 = parsed_data[j] # ED
        if (j+1) >= dataLen:
            break
        prow2 = parsed_data[j+1] # Absentee
        if (j+2) >= dataLen:
            break
        prow3 = parsed_data[j+2] # total
        county = prow1[0]
        candidateList = buildCandidateList(candidateNameList)

        for x in range(len(candidateList)):
            """ One new single-candidate race for each entry. """
            c = candidateList[x]
            c.votes_ed = prow1[x + 2]
            c.votes_absentee = prow2[x + 2]
            c.votes_total = prow3[x + 2]
            race = ElectoralRace(url, filename, usState, usStateAbbrev, formatSpec, county, resultStatus, pageNo, dateTime)
            race.county = county
            race.candidates.append(c)
            race.raceStartIndex = raceId
            races.append(race)
            raceId = raceId + 1

        j = j + 3

    return races

###########################
#		MAIN
###########################

def readCountyResults(usState, usStateAbbrev, fmtSpec, candidateList, fileName):
	""" 
	Read all races in a county, given a format spec.
	"""
	inputPath = os.path.join(usStateAbbrev, fmtSpec.county, Globals.RESULTS_DIR, fileName)
	inputFilePaths = []
	inputFilePaths.append(inputPath)
	fileUrlList = []

	allRaces = []
	for filePath in inputFilePaths:
		races = parseFile(usState, usStateAbbrev, fmtSpec, filePath, fileUrlList, candidateList)

		for race in races:
			if fmtSpec.is_2020 == False:
				parseRace(fmtSpec, race, candidateList)
			allRaces.append(race)

	if fmtSpec.is_2020 == True:
		allRaces = consolidateRaces(races, candidateList)
	printRows(allRaces, candidateList)
# DONE
	

