from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Mifflin')
fmtSpec.header_field_count = 1
fmtSpec.precinct_name_index = 0
fmtSpec.datetime_value = '11/25/2024 09:39AM'
fmtSpec.results_type_value = 'OFFICIAL RESULTS'

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)

