# A single record of the output
#
# Reference: https://docs.google.com/spreadsheets/d/13IMTlAxVFoon8_DfyJBP58-r2n9kmHLlKdBbI2kDQVQ/edit?gid=272640954#gid=272640954
#
from ElectionGlobals import Globals

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


    def createRecord(race, candidate, votes, vote_mode, is_writein):
        """
        Create record suitable for printing CSV
        @param race ElectoralRace
        @param candidate Candidate
        @param votes count of votes for this vote mode
        @param vote_mod ElectionGlobals.MODE_*
        """
        t = TemplateRecord()
        t.election = Globals.ELECTION
        t.state = race.state
        t.county = race.county + ' COUNTY'
        t.jurisdiction = race.county + ' COUNTY'
        t.precinct = race.precinct
        t.office = candidate.office
        t.candidate = candidate.name
        t.party = candidate.party
        t.vote_mode = vote_mode
        t.votes = votes
        t.writein = is_writein
        t.result_status = race.resultStatus
        t.source_url = race.source_url
        t.source_filename = race.filename
        t.datetime_retrieved = race.dateTime
        return t

    # String method
    def __str__(self):
        return f"{self.election},{self.state},{self.county},{self.precinct},{self.jurisdiction},{self.office},{self.candidate},{self.party},{self.vote_mode},{self.votes},{self.writein},{self.result_status},{self.source_url},{self.source_filename},{self.datetime_retrieved}"

    def header(self):
        return f"election,state,county,precinct,jurisdiction,office,candidate,party,vote_mode,votes,writein,result_status,source_url,source_filename,datetime_retrieved"
