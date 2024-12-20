from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Lycoming')
fmtSpec.date_index = 6
fmtSpec.time_index = 7
fmtSpec.header_field_count = 1
fmtSpec.results_type_index = 0
fmtSpec.precinct_name_index = 14

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)