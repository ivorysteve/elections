"""
FLORIDA FORMAT
"""
class CsvRow:
    def __init__(self, arr):
        self.countyCode = arr[0]
        self.county = arr[1]
        self.electionNumber = arr[2]
        self.date = arr[3]
        self.electionName = arr[4]
        self.precinct_id = arr[6]
        self.precinctLocation = arr[7]
        self.totalRegisteredVoters = arr[8]
        self.contest = arr[11]
        self.candidate = arr[14]
        self.party = arr[15]
        self.candidateNumber = arr[17]
        self.precinctVotes = arr[18]


        # String method
    def __str__(self):
        return f"{self.electionName}: {self.county} ({self.precinct_id}), {self.contest}, {self.candidate} ({self.party}): {self.precinctVotes}"
