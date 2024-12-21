from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Lackawanna')
fmtSpec.header_field_count = 6
fmtSpec.datetime_search_string = 'LACKAWANNA PRECINCT - '
fmtSpec.results_type_index = 0
fmtSpec.precinct_name_index = 0

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

