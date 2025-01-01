from readMultiDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Forest')

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)
