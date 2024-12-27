from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Mckean')
fmtSpec.header_field_count = 4
fmtSpec.datetime_value = '12/09/2024 09:26 AM'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)