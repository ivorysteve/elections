from readSingleDocIA import readCountyResults
from Elections.ElectionGlobals import Globals
from Elections.FormatSpec import FormatSpec

# Columns in table
CANDIDATES = [
    'Donald J. Trump',
    'Joseph R. Biden',
    'Roque Rocky De La Fuente',
    'Don Blankenship',
    'Ricki Sue King',
    'Howie Hawkins',
    'Jo Jorgensen',
    'Brock Pierce',
    'Kanye West',
    'Write-in',
    'Undervotes',
    'Overvotes',
    'County Total'
]

fmtSpec = FormatSpec('Iowa')
fmtSpec.datetime_value = '11/30/2020'
fmtSpec.precinct_name_index = 0
fmtSpec.results_type_value = 'Canvass Summary'


readCountyResults('Iowa', 'IA', fmtSpec, CANDIDATES)