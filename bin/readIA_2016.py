from readSingleDocIA import readCountyResults

from Elections.FormatSpec import FormatSpec

class C:
    def __init__(self, name, party):
        self.name = name
        self.party = party


# Columns in table
CANDIDATES = [
    C('Donald J. Trump & Michael R. Pence,', 'Republican'),
    C('Hillary Clinton and Tim Kaine', 'Democrat'),
    C('Darrell L. Castle and Scott N. Bradley', 'Constitution Party'),
    C('Jill Stein and Ajamu Baraka', 'Green Party'),
    C('Dan R. Vacek and Mark G. Elworth', 'Legal Marijuanna Now'),
    C('Gary Johnson and Bill Weld', 'Libertarian'),
    C('Lynn Kahn and Jay Stolba', 'New Independant Party Iowa'),
    C('Gloria La Riva and Dennis J. Banks', 'Party for Socialism and Liberation'),
    C('Rocky Roque De La Fuente and Michael Steinberg', 'Nominated by Petition'),
    C('Evan McMullin and Nathan Johnson', 'Nominated by Petition'),
    C('Write-in', ''),
    C('Undervotes', ''),
    C('Overvotes', ''),
    C('County Total', '')
]

fmtSpec = FormatSpec('Iowa')
fmtSpec.datetime_value = '11/06/2016'
fmtSpec.precinct_name_index = 0
fmtSpec.results_type_value = 'Canvass Summary'
fmtSpec.has_page_header = False
fmtSpec.is_single_line_counts = True

FILENAME = 'IA_PRES_2016gen_canvsummary.pdf'


readCountyResults('Iowa', 'IA', fmtSpec, CANDIDATES, FILENAME)