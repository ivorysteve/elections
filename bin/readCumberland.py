from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Cumberland')
fmtSpec.header_field_count = 3
fmtSpec.datetime_search_string = 'Result Book - Precinct Report - '
fmtSpec.results_type_index = 0
fmtSpec.precinct_name_index = 3

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

