from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Snyder')
fmtSpec.header_field_count = 8
fmtSpec.datetime_value = '11/22/2024 12:07 PM'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)