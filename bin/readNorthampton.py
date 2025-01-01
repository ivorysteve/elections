from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Northampton')
fmtSpec.header_field_count = 5
fmtSpec.has_northampton_bug = True

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

