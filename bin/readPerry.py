from readSingleDocSpanning import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Perry')
fmtSpec.header_field_count = 2
fmtSpec.page_header_len = 13
fmtSpec.precinct_name_index = 13
fmtSpec.multiline_race_field_len = 6
fmtSpec.datetime_value = '11/25/2024 10:41 PM'
fmtSpec.results_type_value = 'OFFICIAL RESULTS'
fmtSpec.lineSpec.candidate_name_index = 0
fmtSpec.lineSpec.votes_ed_index = 2
fmtSpec.lineSpec.votes_mail_index = 3
fmtSpec.lineSpec.votes_prov_index = 4
fmtSpec.lineSpec.party_index = -1

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)