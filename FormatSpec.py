# Spec that defines specifics of how to parse a county results file.

class LineSpec:
    def __init__(self):
        ''' Spec for a line of a candidate in a race. '''
        self.candidate_name_index = 0
        self.party_index = 0
        self.votes_ed_index = 0
        self.votes_mail_index = 0
        self.votes_prov_index = 0
        self.votes_total_index = 0
        self.parse_line_lambda = lambda a : { a }
        
class FormatSpec:
    def __init__(self, countyName):
        self.county = countyName
        self.precinct_name_index = 5
        self.date_index = -1
        self.time_index = -1
        self.results_type_index = 3
        self.datetime_search_string = 'Precinct Summary - '
        self.header_field_count = 0  # Field count from office title to first candidate
        self.end_of_office_marker = ''
        self.line = LineSpec()
