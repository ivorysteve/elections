from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Potter')
fmtSpec.header_field_count = 3
fmtSpec.datetime_value = '11/25/2024 08:38 AM'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)
