from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Wayne')
fmtSpec.header_field_count = 2
fmtSpec.precinct_name_index = 13
fmtSpec.multiline_race_field_len = 6
fmtSpec.datetime_value = '11/14/2024 02:14 PM'
fmtSpec.results_type_value = 'OFFICIAL RESULTS'
fmtSpec.lineSpec.candidate_name_index = 0
fmtSpec.lineSpec.votes_ed_index = 2
fmtSpec.lineSpec.votes_mail_index = 3
fmtSpec.lineSpec.votes_prov_index = 4

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)