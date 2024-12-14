#
# Stanza of results for a single race
#
class ElectoralRace:
    def __init__(self, usState, county, precinct, status, pageNumber, id):
        self.state = usState
        self.county = county
        self.precinct = precinct
        self.resultStatus = status
        self.page = pageNumber
        self.id = id
        self.officeName = 'UNKNOWN'
        self.candidates = []
        self.startIndex = 0 # Index into text of entire section
        self.candidateStartIndex = 0 # Index into text of first candidate
        self.isPresidential = False
        self.endOfDataIndex = 0 # Index into text when section ends
        self.pageText = ''

    # String method
    def __str__(self):
        return f"Results for {self.officeName} in {self.county}/{self.precinct}"
