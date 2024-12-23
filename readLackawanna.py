from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Lackawanna')
fmtSpec.header_field_count = 6
fmtSpec.datetime_value = '11/26/2024 01:16 PM'
fmtSpec.results_type_index = 1
fmtSpec.precinct_name_index = 0
fmtSpec.lineSpec.votes_total_index = 0
fmtSpec.lineSpec.votes_ed_index = 2
fmtSpec.lineSpec.votes_mail_index = 3
fmtSpec.lineSpec.votes_prov_index = 4


readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

