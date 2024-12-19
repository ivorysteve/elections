from readMultiDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

fmtSpec = FormatSpec('Fulton')

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)
