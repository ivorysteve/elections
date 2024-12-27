from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Elk')
fmtSpec.header_field_count = 7

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

