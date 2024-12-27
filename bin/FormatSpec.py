# Spec that defines specifics of how to parse a county results file.

# Default value for single line.
INDEX_PARTY = 0
# Default values for single line columns after candidate.
INDEX_VOTES_ED = 1
INDEX_VOTES_MAIL = 2
INDEX_VOTES_PROV = 3
INDEX_VOTES_TOTAL = 0

class LineSpec:
    def __init__(self):
        ''' Spec for a line of a candidate in a race. '''
        self.candidate_name_index = 1
        self.party_index = 0
        self.votes_ed_index = INDEX_VOTES_ED
        self.votes_mail_index = INDEX_VOTES_MAIL
        self.votes_prov_index = INDEX_VOTES_PROV
        self.votes_total_index = INDEX_VOTES_TOTAL
        self.parse_line_lambda = lambda a : { a }
        
class FormatSpec:
    """ Default values set here. """
    def __init__(self, countyName):
        self.county = countyName
        self.precinct_name_index = 5
        self.datetime_search_string = 'Precinct Summary - '
        self.date_index = -1
        self.time_index = -1
        self.datetime_value = ''
        self.results_type_index = 3
        self.results_type_value = ''
        self.header_field_count = 0  # Field count from office title to first candidate
        self.end_of_office_marker = ''
        self.skip_to_page = 0
        self.page_header_len = 0
        self.multiline_race_field_len = 0 # If race is multiple lines (instead of fields in single line), count of lines (incl name).
        self.lineSpec = LineSpec()
