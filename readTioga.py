from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Tioga')
fmtSpec.header_field_count = 6
fmtSpec.datetime_value = '11/19/2024 1:01 PM'
fmtSpec.skip_to_page = 4 # Pages 0 - 3 are summary

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)