from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Lawrence')
fmtSpec.header_field_count = 5
fmtSpec.candidate_line_increment = 3

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

