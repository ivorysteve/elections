from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Montour')
fmtSpec.header_field_count = 2
fmtSpec.precinct_name_index = 0
fmtSpec.results_type_value = 'OFFICIAL RESULTS'
fmtSpec.multiline_race_field_len = 2
fmtSpec.has_candidate_double_line = True
fmtSpec.lineSpec.votes_ed_index = 2
fmtSpec.lineSpec.votes_mail_index = 3
fmtSpec.lineSpec.votes_prov_index = 4

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

