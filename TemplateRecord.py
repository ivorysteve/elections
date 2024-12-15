# A single record of the output
#
# Reference: https://docs.google.com/spreadsheets/d/13IMTlAxVFoon8_DfyJBP58-r2n9kmHLlKdBbI2kDQVQ/edit?gid=272640954#gid=272640954
#
class TemplateRecord:
    def __init__(self):
        election = ''
        state = '' 
        county  = ''
        precinct = ''
        jurisdiction = ''
        office = ''
        candidate = ''
        party = ''
        vote_mode = ''
        votes = ''
        writein = ''
        result_status = ''
        source_url = ''
        source_filename = ''
        datetime_retrieved = ''

    # String method
    def __str__(self):
        return f"{self.election},{self.state},{self.county},{self.precinct},{self.jurisdiction},{self.office},{self.candidate},{self.party},{self.vote_mode},{self.votes},{self.writein},{self.result_status},{self.source_url},{self.source_filename},{self.datetime_retrieved}"

    def header(self):
        return f"election,state,county,precinct,jurisdiction,office,candidate,party,vote_mode,votes,writein,result_status,source_url,source_filename,datetime_retrieved"
