from readSingleDoc import readCountyResults
from ElectionGlobals import Globals
from FormatSpec import FormatSpec
from readCandidate import readCandidateMultiLine

fmtSpec = FormatSpec('Lycoming')
fmtSpec.date_index = 6
fmtSpec.time_index = 7
fmtSpec.header_field_count = 1
fmtSpec.candidate_col_count = 6
fmtSpec.parseLineFn = readCandidateMultiLine
fmtSpec.lineSpec.votes_total_index = 1
fmtSpec.lineSpec.votes_ed_index = 3
fmtSpec.lineSpec.votes_mail_index = 4
fmtSpec.lineSpec.votes_prov_index = 5
fmtSpec.lineSpec.party_index = -1  # Yes, they don't give the party for the candidate.

readCountyResults(Globals.STATE, Globals.STATE_ABBREV, fmtSpec)