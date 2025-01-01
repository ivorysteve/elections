import os
from ElectionGlobals import Globals
from FileUrlEntry import FileUrlEntry
from TemplateRecord import TemplateRecord
from urllib.parse import urlparse, unquote

"""
Common methods used by all parsers.
"""

"""
URL - File dictionary methods.
"""
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

def getPdfFiles(resultsDir):
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


"""
Field Extraction and Normalization
"""

PRECINCT_PREFIX = 'Precinct '

def extractPrecinctName(formatSpec, txt):
	""" Assumes precinct is at a fixed index in page.  It may start with a prefix, so remove it. """
	p = txt[formatSpec.precinct_name_index]
	if p.startswith(PRECINCT_PREFIX):
		p = p.replace(PRECINCT_PREFIX, '')
	return p

def getHeaderFieldCount(fmtSpec):
	""" Returns Number of fields from office to first candidate name. """
	return fmtSpec.header_field_count

def extractDateTime(formatSpec, txt):
	""" The date/time sometimes at an index, but is often on a line like: 'Precinct Summary - 11/21/2024 10:39 AM """
	""" However, sometimes it is just easier to set the value up front rather than try to parse it from the doc. """
	if formatSpec.date_index > 0:
		d = txt[formatSpec.date_index]
		t = txt[formatSpec.time_index]
		return f"{d} {t}"
	if len(formatSpec.datetime_value) > 0:
		# Hard-wired value
		return formatSpec.datetime_value
	for line in txt:
		indx = line.find(formatSpec.datetime_search_string)
		if indx >= 0:
			rtnLine = line[indx + len(formatSpec.datetime_search_string):len(line)]
			pgIndex = rtnLine.find('Page')
			if pgIndex > 0:
				rtnLine = rtnLine[0:pgIndex] #  Remove any page number after the date/time
			return rtnLine.strip()
	return 'UNKNOWN'

def extractResultsType(formatSpec, txt):
	""" If value is set, use that; otherwise, default to index. """
	if len(formatSpec.results_type_value) > 0:
		return formatSpec.results_type_value
	return txt[formatSpec.results_type_index]

def extractOfficeName(oname):
	""" Office name may have a '(Vote for 1)' prefix; remove it. """
	indx = oname.upper().find('(VOTE ')
	if indx > 0:
		return oname[0:indx].strip()
	return oname

def extractMultiLineRace(fmtSpec, txtArray, startIndex):
	""" Copy a subset of a text array and return contents. """
	fields = []
	for i in range(0, fmtSpec.multiline_race_field_len):
		fields.append(txtArray[startIndex + i])
	return fields

def collapseCandidateDoubleLine(fields):
	""" Weird format where each candidate result is spit into 2 lines.  Just concatenate the two sets of tokens """
	""" into a single list, filtering out blanks.  Used on Montour.  """""
	rtnFields = []
	for x in fields[0].split(' '):
		if len(x) > 0:
			rtnFields.append(x)
	for y in fields[1].split(' '):
		if len(y) > 0:
			rtnFields.append(y)
	return rtnFields

def calculateProvisionalVotes(votes_total, votes_ed, votes_mail):
	""" Northampton data smashes provisional and vote percentage columns together.  So we calculate provisional. """
	prov = votes_total - (votes_ed + votes_mail)
	return prov

def extractFirstCandidateName(listedName):
	"""
	Presidential candidates may have " - presidential candidate" or ", president" 
	or " and <VP>" after their name.
	Return name with this removed, else, name unchanged.
	"""
	nameUpper = listedName.upper()
	tag = nameUpper.find("PRESIDENT")
	if tag > 0:
		listedName = nameUpper.replace("PRESIDENT", '')
	if " - " in listedName:
		end = listedName.find(" - ")
		listedName = listedName[:end]
	vpIndx = listedName.find(" and ")
	if vpIndx > 0:
		listedName = listedName[:vpIndx]
	return listedName.strip()

def normalizeCandidateName(indexToCounts, name, fields):
	""" Gather up all tokens up to first number.  Remove VP if starts with '/'.  """
	n = name
	if (indexToCounts > 1):
		for j in range(2, indexToCounts):
			if fields[j] == '/':
				break
			n = n + ' ' + fields[j]
	return n

def findFirstNumber(strArray):
	""" Find first numeric field in an array of strings. """
	i = 0
	for line in strArray:
		if line.replace(',', '').isnumeric():
			return i
		i += 1
	return -1

def votesToInt(strVotes):
	""" Convert string to integer. """
	str2 = strVotes.replace(',', '') # Remove any commas
	return int(str2)

def findCandidateParty(name):
	""" Find candidate last name in our hard-wired candidate/party dictionary. Return corresponding party. """
	for candidate in Globals.CANDIDATE_PARTY_LIST:
		lastName = candidate[0]
		if name.upper().find(lastName) >= 0:
			return candidate[1]
	return 'UNKNOWN'

"""
Printing
"""
def printAllRaces(races):
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

def printAllCandidateParties(races):
	if len(races) == 0:
		print("No races found!")
		return
	for race in races:
		for c in race.candidates:
			print(f"(\"{c.name}\", \"{c.party}\")")