from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Lebanon')
fmtSpec.header_field_count = 8

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)