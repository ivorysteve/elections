from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec
from readCandidate import readCandidateSingleLine

fmtSpec = FormatSpec('Lebanon')
fmtSpec.header_field_count = 8
fmtSpec.parseLineFn = readCandidateSingleLine

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)