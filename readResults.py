# importing required classes
from pypdf import PdfReader
from Candidate import Candidate
from ElectoralRace import ElectoralRace
from TemplateRecord import TemplateRecord

# constants
ELECTION = '2024 GENERAL'
STATE = 'PENNSYLVANIA'
COUNTY = 'FULTON COUNTY'
PRECINCT = 'AYR TOWNSHIP'
RESULT_STATUS = "OFFICIAL RESULTS"
DATETIME_RETRIEVED = "11/05/2024 11:30 PM"
COUNTY_URL = 'https://www.co.fulton.pa.us/files/elections/live-results/2024/General%20Election/Ayr%20Township.pdf'
COUNTY_FILENAME = 'Ayr Township.pdf'

MODE_ELECTION_DAY = 'ELECTION DAY'
MODE_MAIL_IN = 'MAIL-IN'
MODE_PROVISIONAL = 'PROVISIONAL'

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

INDEX_FIRST_CANDIDATE = 24
INDEX_PARTY = 1
INDEX_VOTES_MAIL = 2
INDEX_VOTES_ED = 4
INDEX_VOTES_PROV = 6

# Presidential candidates have " - presidential candidate" after their name.
# @return name with this removed, else, name unchanged.
#
def extractCandidateName(listedName):
	if " - " in listedName:
		end = listedName.find(" - ")
		return listedName[:end]
	return listedName

def determineIfPresidential(rank):
	if rank == 'PRESIDENTIAL ELECTORS':
		return True
	return False


def addToRows(rows, race, candidate, votes, vote_mode, is_writein):
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
	t.source_url = COUNTY_URL
	t.source_filename = COUNTY_FILENAME
	t.datetime_retrieved = DATETIME_RETRIEVED
	rows.append(t)


# Parse the choices for a section representing a single race.
def parseRace(raceDef):
	print(f"=== Got {raceDef}:")
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
		c = Candidate(office)
		c.name = candidateName
		c.party = party
		c.votes_ed = int(votes_ed)
		c.votes_mail = int(votes_mail)
		c.votes_prov = (votes_prov)
		print(c)
		raceDef.candidates.append(c)
		candidateOffset += candidateColumnCount

###########################
#		MAIN
###########################


def parseFile(usState, county, precinct, status, filename):
	# printing number of pages in pdf file
	reader = PdfReader(filename)
	total = len(reader.pages)
	print(f"This document has {total} pages")

	races = []
	# creating a page object
	for pg in range(0, total):
		print(f"Parsing PAGE {pg}")
		page = reader.pages[pg]
		pageTxt = page.extract_text().splitlines()
		i = 0
		sectionID = 1
		currentRace = ElectoralRace(usState, county, precinct, status, i, sectionID)
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
				sectionID += 1
				currentRace = ElectoralRace(usState, county, precinct, status, i, sectionID)

			# Bump line number
			i += 1

		# End of page
	# End of document
	return races
# End method

filename = 'FultonCounty/AyrTownship.pdf'
races = parseFile(STATE, COUNTY, PRECINCT, RESULT_STATUS, filename)

for race in races:
	parseRace(race)

# Format and print
rows = []
for race in races:
	for c in race.candidates:
		addToRows(rows, race, c, c.votes_ed, MODE_ELECTION_DAY, 0)
		addToRows(rows, race, c, c.votes_prov, MODE_PROVISIONAL, 0)
		addToRows(rows, race, c, c.votes_mail, MODE_MAIL_IN, 0)

for row in rows:
	print(row)

# DONE
