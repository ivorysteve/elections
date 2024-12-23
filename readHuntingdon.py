from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Huntingdon')
fmtSpec.header_field_count = 8
fmtSpec.datetime_value = '11/08/2024 12:56 PM'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

