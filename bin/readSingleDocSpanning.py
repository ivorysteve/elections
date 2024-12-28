"""
This file parses PDF election results that are collated into a single file, but
races may straddle pages.  So we collect each precinct and all its races first.
"""
import os
from pypdf import PdfReader
from Candidate import Candidate
from ElectoralRace import ElectoralRace
from TemplateRecord import TemplateRecord
from FileUrlEntry import FileUrlEntry
from FormatSpec import FormatSpec
from ElectionGlobals import Globals
from ElectionUtils import extractDateTime, extractResultsType, extractFirstCandidateName, normalizeCandidateName, extractOfficeName, extractMultiLineRace, getHeaderFieldCount
from ElectionUtils import readLinksFile, getPdfFiles, findUrl, createFileUrlDict, findFirstNumber, votesToInt
from ElectionUtils import printAllRaces

"""
County-specific constants
"""

class Precinct:
	def __init__(self, pname, pageNo, startIndex):
		self.name = pname
		self.pageNo = pageNo
		self.text = []
		self.startIndex = startIndex

# Delimits start of precinct.  May span pages.
PRECINCT_PREFIX = 'Precinct '

def collectPrecincts(fmtSpec, filePath):
	""" 
	parse all pages into precincts first. 
	"""
	reader = PdfReader(filePath)
	total = len(reader.pages)

	precincts = []
	currentPrecinct = False
	for pageNo in range(0, total):
		page = reader.pages[pageNo]
		pageTxt = page.extract_text().splitlines()
		i = 0
		for line in pageTxt:
			if i < fmtSpec.page_header_len:
				# Skip header
				i +=1
				continue
			if line.startswith('Page:'):
				# Page number may show up at the end of the page.  Ignore it.
				i += 1
				continue
			if line.startswith(PRECINCT_PREFIX):
				# New precinct
				if currentPrecinct != False:
					precincts.append(currentPrecinct)
				pname = line.replace(PRECINCT_PREFIX, '')
				currentPrecinct = Precinct(pname, pageNo, i)
			else:
				if currentPrecinct != False:
					currentPrecinct.text.append(line)
			i += 1
		# End line loop
	# End page loop
	precincts.append(currentPrecinct)
	reader.close()
	return precincts

def parseRace(raceDef):
	"""
	Parse a single race (section) of the vote results.
	"""
	txt = raceDef.pageText
	candidateOffset = raceDef.candidateStartIndex
	office = raceDef.officeName
	lineSpec = raceDef.formatSpec.lineSpec
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
		party = 'UNKNOWN'
		if lineSpec.party_index > 0:
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
		candidateOffset += 1   # All vote counts for a candidate are in a single line, so just bump by 1.

def parsePrecincts(usState, usStateAbbrev, formatSpec, filePath, fileUrlList, precincts):
	races = []
	filename = os.path.basename(filePath)
	url = findUrl(fileUrlList, filePath)
	for precinct in precincts:
		pageTxt = precinct.text
		dateTime = extractDateTime(formatSpec, pageTxt)
		resultStatus = extractResultsType(formatSpec, pageTxt)
		headerFieldCount = getHeaderFieldCount(formatSpec)
		i = 0
		startedRace = False
		for line in pageTxt:
			# Find the offices
			for rank in Globals.OFFICE_RANKING:
				if line.upper().startswith(rank):
					currentRace = ElectoralRace(url, filename, usState, usStateAbbrev, formatSpec, precinct.name, resultStatus, i, dateTime)
					currentRace.pageText = pageTxt
					currentRace.page = precinct.pageNo
					currentRace.raceStartIndex = i
					currentRace.officeName = extractOfficeName(line)
					currentRace.candidateStartIndex = i + headerFieldCount
					startedRace = True
					break
			# End rank for loop
			# Find end of section
			if line.upper().startswith(Globals.END_OF_OFFICE_MARKER):
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

		# End of precinct
	return races


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
		precincts = collectPrecincts(fmtSpec, filePath)
		races = parsePrecincts(usState, usStateAbbrev, fmtSpec, filePath, fileUrlList, precincts)

		for race in races:
			parseRace(race)
			allRaces.append(race)

	printAllRaces(allRaces)
# DONE
	

