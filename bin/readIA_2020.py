from readSingleDocIA import readCountyResults

from Elections.FormatSpec import FormatSpec

class C:
    def __init__(self, name, party):
        self.name = name
        self.party = party


# Columns in table
CANDIDATES = [
    C('Donald J. Trump & Michael R. Pence,', 'Republican'),
    C('Joseph R. Biden & Kamala D. Harris', 'Democrat'),
    C('Roque Rocky De La Fuente & Darcy G. Richardson,', 'ALL'),
    C('Don Blankenship & William Alan Mohr,', 'Constitution Party'),
    C('Ricki Sue King & Dayna R. Chandler', 'GKH'),
    C('Howie Hawkins & Angela Nicole Walker', 'Green Party'),
    C('Jo Jorgensen & Jeremy Cohen,', 'Libertarian'),
    C('Brock Pierce & Karla Ballard', ''),
    C('Kanye West & Michelle Tidball', ''),
    C('Write-in', ''),
    C('Undervotes', ''),
    C('Overvotes', ''),
    C('County Total', '')
]

fmtSpec = FormatSpec('Iowa')
fmtSpec.datetime_value = '11/06/2020'
fmtSpec.precinct_name_index = 0
fmtSpec.results_type_value = 'Canvass Summary'
fmtSpec.is_single_line_counts = True
fmtSpec.is_2020 = True

FILENAME = 'IA_PRES_2020Gen_canvsummary.pdf'


readCountyResults('Iowa', 'IA', fmtSpec, CANDIDATES, FILENAME)