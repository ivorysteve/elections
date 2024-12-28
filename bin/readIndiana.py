from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Indiana')
fmtSpec.header_field_count = 8
fmtSpec.datetime_value = ' 11/05/2024 10:22 PM'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)