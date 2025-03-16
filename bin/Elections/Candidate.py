#
# A candidate who received votes.
#
class Candidate:
    def __init__(self, office):
        self.office = office
        self.name = 'UNKNOWN'
        self.votes_ed = 0
        self.votes_mail = 0
        self.votes_prov = 0
        self.votes_absentee = 0
        self.votes_total = 0
        self.party = 'UNKNOWN'

    # String method
    def __str__(self):
        return f"{self.name}: {self.votes_ed} election day, {self.votes_mail} mail-in, {self.votes_prov} provisional: {self.votes_total} total"
