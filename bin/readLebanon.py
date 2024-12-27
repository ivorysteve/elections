from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Lebanon')
fmtSpec.header_field_count = 8
fmtSpec.datetime_value = '11/15/2024  4:38 PM'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)