from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Mercer')
fmtSpec.header_field_count = 6
fmtSpec.datetime_value = '11/26/2024 10:10 AM'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)