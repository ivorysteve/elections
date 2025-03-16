#
# Stanza of results for a single race
#
class ElectoralRace:
    def __init__(self, url, filename, usState, usStateAbbrev, formatSpec, precinct, status, pageNumber, dateTime):
        self.source_url = url
        self.filename = filename
        self.state = usState
        self.stateAbbrev = usStateAbbrev
        self.formatSpec = formatSpec
        self.county = formatSpec.county.upper()
        self.precinct = precinct
        self.resultStatus = status
        self.page = pageNumber
        self.dateTime = dateTime
        self.officeName = 'UNKNOWN'
        self.candidates = []
        self.raceStartIndex = 0 # Index into text of start of section
        self.raceEndIndex = 0 # Index into text when section ends
        self.candidateStartIndex = 0 # Index into text of first candidate
        self.isPresidential = False
        self.pageText = ''
        self.hasOnlyWriteIns = False

    # String method
    def __str__(self):
        return f"Results for {self.officeName} in {self.county}/{self.precinct}"
