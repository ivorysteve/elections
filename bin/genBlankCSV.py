from ElectionUtils import printAllRaces
from ElectoralRace import ElectoralRace
from Candidate import Candidate
from ElectionGlobals import Globals
from FormatSpec import FormatSpec

class CandidateSpec:
    def __init__(self, name, party):
        self.name = name
        self.party = party

class OfficeSpec:
    def __init__(self, officeName, candidateSpecs):
        self.officeName = officeName
        self.candidates = candidateSpecs

OLIST = [
    OfficeSpec('PRESIDENTIAL ELECTORS', [
            CandidateSpec('KAMALA HARRIS', 'DEM'),
            CandidateSpec('DONALD TRUMP', 'REP'),
            CandidateSpec('OLIVER', 'LIB'),
            CandidateSpec('JILL STEIN', 'GRN'),
        ]),
    OfficeSpec('UNITED STATES SENATOR', [
        CandidateSpec('ROBERT P. CASEY', 'DEM'),
        CandidateSpec('DAVE MCCORMICK', 'REP'),
        CandidateSpec('JOHN C. THOMAS', 'LIB'),
    ]),
    OfficeSpec('ATTORNEY GENERAL', [
        CandidateSpec('EUGENE DEPASQUALE', 'DEM'),
        CandidateSpec('DAVE SUNDAY', 'REP'),
        CandidateSpec('ROBERT COWBURN', 'LIB'),
        CandidateSpec('RICHARD L WEISS', 'GRN'),
        CandidateSpec('JUSTIN L MAGILL', 'CST'),
        CandidateSpec('ERIC SETTLE', 'FWD'),
    ]),
    OfficeSpec('STATE TREASURER', [
        CandidateSpec('ERIN MCCLELLAND', 'DEM'),
        CandidateSpec('STACY GARRITY', 'REP'),
        CandidateSpec('NICKOLAS CIESIELSKI', 'LIB'),
        CandidateSpec('TROY BOWMAN', 'CST'),
        CandidateSpec('CHRIS FOSTER', 'FWD'),
    ]),
    OfficeSpec('REPRESENTATIVE IN CONGRESS', [
        CandidateSpec('ZACH WOMER', 'DEM'),
        CandidateSpec('GLEN GT THOMPSON', 'REP'),
    ])
]
]

PRECINCTS = [
    'Barnett',
    'Green',
    'Harmony',
    'Hickory',
    'Jenks',
    'Kingsley',
    'Tionesta'
]


def genRaces(url, usState, usStateAbbrev, fmtSpec, precinctList, status, dateTime):
    races = []
    i = 0
    for precinctName in precinctList:
        filename = f"{precinctName}.pdf"
        for office in OLIST:
            currentRace = ElectoralRace(url, filename, usState, usStateAbbrev, fmtSpec, precinctName, status, i, dateTime)
            for c in office.candidates:
                candidate = Candidate(office.officeName)
                candidate.name = c.name
                candidate.party = c.party
                currentRace.candidates.append(candidate)
            races.append(currentRace)
            i += 1
    return races

A_URL = 'https://cms6.revize.com/revize/forestcounty/Elections/Barnett.pdf'

A_STATUS = 'OFFICIAL RESULTS'
A_DATE_TIME = '11/05/24 10:23 PM'
A_COUNTY = 'FOREST'


fmtSpec = FormatSpec(A_COUNTY)

races = genRaces(A_URL, Globals.STATE, Globals.STATE_ABBREV, fmtSpec, PRECINCTS, A_STATUS, A_DATE_TIME)
printAllRaces(races)