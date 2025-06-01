from readSingleDocIA import readCountyResults

from Elections.FormatSpec import FormatSpec

class C:
    def __init__(self, name, party):
        self.name = name
        self.party = party


# Columns in table
CANDIDATES = [
    C('Mitt Romney & Paul Ryan', 'Republican'),
    C('Barak Obama & Joe Biden', 'Democrate'),
    C('Virgil Goode & James Clymer', 'Constitution'),
    C('Jill Stein & Cheri Honkala', 'Iowa Green Party'),
    C('Gary Johnson & James P. Gray', 'Party for Socialism & Liberation'),
    C('Gloria LaRiva & Stefanie Beacham', 'Socialist Workers Party'),
    C('James Harris & Alyson Kennedy', 'Nominated by Petition'),
    C('Jerry Litzel & Jim Litzel', ''),
    C('Write-in', ''),
    C('Undervotes', ''),
    C('Overvotes', ''),
    C('County Total', '')
]

fmtSpec = FormatSpec('Iowa')
fmtSpec.datetime_value = '11/06/2012'
fmtSpec.precinct_name_index = 0
fmtSpec.results_type_value = 'Canvass Summary'
fmtSpec.start_index_skip = 3

# FILENAME = 'IA_PRES_2020Gen_canvsummary.pdf'
FILENAME = 'IA_PRES_2012Gen_canvsummary.pdf'


readCountyResults('Iowa', 'IA', fmtSpec, CANDIDATES, FILENAME)