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
from ElectionUtils import extractDateTime, extractResultsType, normalizeCandidateName, extractFirstCandidateName, extractOfficeName, extractMultiLineRace
from ElectionUtils import readLinksFile, getPdfFiles, getHeaderFieldCount, findUrl, createFileUrlDict, findFirstNumber, findCandidateParty, votesToInt
from ElectionUtils import printAllRaces, printAllCandidateParties
from urllib.parse import unquote

"""
County-specific constants
"""

# Indices for each page
PRECINCT_PREFIX = 'Precinct '
# Indices of fields starting from candidate name
COLUMN_COUNT = 10

def extractPrecinctName(formatSpec, txt):
	""" Precinct is at a fixed index in page.  It may start with a prefix, so remove it. """
	p = txt[formatSpec.precinct_name_index]
	if p.startswith(PRECINCT_PREFIX):
		p = p.replace(PRECINCT_PREFIX, '')
	return p


def parseRace(raceDef):
	"""
	Parse a single race (section) of the vote results.
	"""
	txt = raceDef.pageText
	candidateOffset = raceDef.candidateStartIndex
	office = raceDef.officeName
	fmtSpec = raceDef.formatSpec
	lineSpec = fmtSpec.lineSpec
	if raceDef.hasOnlyWriteIns == True:
		# Nothing to do here
		return

	# Go through all lines in a section (race)
	for line in range(0, 100):
		dataStart = candidateOffset
		if dataStart >= raceDef.raceEndIndex:
			# We are done with this section.
			return
		
		# Start parsing:
		if raceDef.formatSpec.multiline_race_field_len > 0:
			# Multi-line format
			fields = extractMultiLineRace(raceDef.formatSpec, txt, candidateOffset)
			candidateOffset += (raceDef.formatSpec.multiline_race_field_len - 1)  # advance offset to line before next candidate.
		else:
			# Single line format
			candidateLine = txt[candidateOffset]
			fields = candidateLine.replace(',', '').split(' ')
		if len(candidateLine.strip()) == 0:
			# Weird issue where there are spaces between last candidate and Write-In.  Ignore these.
			candidateOffset += 1
			continue
		party = fields[lineSpec.party_index]
		candidateName = fields[lineSpec.candidate_name_index]
		countStartIndex = findFirstNumber(fields)
		candidateName = extractFirstCandidateName(normalizeCandidateName(countStartIndex, candidateName, fields))
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
		candidateOffset += fmtSpec.candidate_line_increment   # All vote counts for a candidate are in a single line (usually), so just bump by 1.

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
	currentRace = {}
	# creating a page object
	for pageNo in range(0, total):
		if formatSpec.skip_to_page > 0 and pageNo < formatSpec.skip_to_page:
			continue
		page = reader.pages[pageNo]
		pageTxt = page.extract_text().splitlines()
		# Take precinct name from each page.
		precinct = extractPrecinctName(formatSpec, pageTxt)
		dateTime = extractDateTime(formatSpec, pageTxt)
		resultStatus = extractResultsType(formatSpec, pageTxt)

		i = 0
		startedRace = False
		for line in pageTxt:
			# Find the offices
			for rank in Globals.OFFICE_RANKING:
				if line.upper().startswith(rank):
					currentRace = ElectoralRace(url, filename, usState, usStateAbbrev, formatSpec, precinct, resultStatus, i, dateTime)
					currentRace.pageText = pageTxt
					currentRace.page = pageNo
					currentRace.raceStartIndex = i
					currentRace.officeName = extractOfficeName(line)
					currentRace.candidateStartIndex = i + headerFieldCount
					startedRace = True
					break
			# End rank for loop
			# Find end of section
			if line.upper().find(Globals.END_OF_OFFICE_MARKER) >= 0:
				if startedRace is True:
					# We may encounter multiple Write-in lines in a race.  Keep going until we get to the next race.
					currentRace.raceEndIndex = i
					if currentRace.raceEndIndex == currentRace.raceStartIndex:
						# Start and end are same.  This can happen if there are only write-in votes in this race on this page.
						currentRace.hasOnlyWriteIns = True
					startedRace = False
					races.append(currentRace)

			# Bump line number
			i += 1

		# End of page
	# End of document
	return races
# End method


###########################
#		MAIN
###########################

def readCountyResults(usState, usStateAbbrev, fmtSpec):
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
			parseRace(race)
			allRaces.append(race)

	printAllRaces(allRaces)
# DONE
	

