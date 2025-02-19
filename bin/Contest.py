
class Candidate:
    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.counties = {}

""" A contest across multiple counties """
class Contest:
    def __init__(self, name):
        self.name = name
        self.candidates = {}

    def addCandidate(self, candidate, party, county, votes):
        if candidate == 'WriteinVotes' or candidate == 'UnderVotes' or candidate == 'OverVotes':
            return
        if self.candidates.get(candidate) == None:
            self.candidates[candidate] = Candidate(candidate, party)
        if votes == 0 or votes.isdigit():
            votes = votes
        elif len(votes) == 0:
            votes = 0
        counties = self.candidates.get(candidate).counties
        if counties.get(county) == None:
            counties[county] = 0
        cur = counties.get(county)
        counties[county] = cur + int(votes)