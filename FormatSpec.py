"""
 Spec that defines specifics of how to parse a county results file.
"""
from Candidate import Candidate

# Default index values
INDEX_PARTY = 0
INDEX_CANDIDATE_NAME = 1
INDEX_VOTES_MAIL = 2
INDEX_VOTES_ED = 1
INDEX_VOTES_PROV = 3
INDEX_VOTES_TOTAL = 0

class LineSpec:
    def __init__(self):
        ''' Spec for a line of a candidate in a race. '''
        self.candidate_name_index = INDEX_CANDIDATE_NAME
        self.party_index = INDEX_PARTY
        self.votes_ed_index = INDEX_VOTES_ED
        self.votes_mail_index = INDEX_VOTES_MAIL
        self.votes_prov_index = INDEX_VOTES_PROV
        self.votes_total_index = INDEX_VOTES_TOTAL
        self.parseLineFn = lambda office,line,txt,offset,lineSpec : { Candidate(office) }
        
class FormatSpec:
    def __init__(self, countyName):
        self.county = countyName
        self.precinct_name_index = 0
        self.date_index = -1
        self.time_index = -1
        self.datetime_search_string = ''
        self.header_field_count = 0  # Field count from office title to first candidate
        self.candidate_col_count = 1 # Lines from a candidate to the next
        self.end_of_office_marker = ''
        self.lineSpec = LineSpec()
