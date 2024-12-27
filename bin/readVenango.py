from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Venango')
fmtSpec.header_field_count = 8
fmtSpec.datetime_value = '11/25/2024 8:38 AM'
#  votes_total_index is already 0
fmtSpec.lineSpec.votes_ed_index = 2
fmtSpec.lineSpec.votes_mail_index = 3
fmtSpec.lineSpec.votes_prov_index = 4

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)