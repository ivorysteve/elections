from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Chester')
fmtSpec.header_field_count = 5

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)
