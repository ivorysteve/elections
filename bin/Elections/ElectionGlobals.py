
class Globals:
    ELECTION = '2024 GENERAL'
    STATE = 'PENNSYLVANIA'
    STATE_ABBREV = 'PA'
    
    # Where PDF files are
    RESULTS_DIR = 'Results_PDF'
    # Per-count list of URLs corresponding to this county
    URL_LIST_FILENAME = "URL_List.txt"
    # Use this to indicate the end of useful data in a race.  We ignore all write-ins.
    END_OF_OFFICE_MARKER = 'WRITE-IN'

    # Modes of vote result
    MODE_ELECTION_DAY = 'ELECTION DAY'
    MODE_MAIL_IN = 'MAIL-IN'
    MODE_PROVISIONAL = 'PROVISIONAL'
    MODE_TOTAL = 'TOTAL'

    # All the ways an office may be indicated in a results doc.
    OFFICE_RANKING = [
        'PRESIDENTIAL ELECTORS',
        'PRESIDENT OF THE UNITED STATES',
        'UNITED STATES SENATOR',
        'ATTORNEY GENERAL',
        'AUDITOR GENERAL',
        'STATE TREASURER',
        'SENATOR IN THE',
        'SEN IN THE GEN ASSEM',
        'SENATOR GENERAL',
        'SENATOR  GENERAL',
        'REPRESENTATIVE IN CONGRESS',
        'REP IN CONGRESS',
        'REP CONGRESS',
        'REPRESENTATIVE IN THE',
        'REPRESENTATIVEIN THE', # Misspelling in one of the counties
        'REP IN THE GEN ASSEM',
        'REP IN THE GENERAL',
        'CHARTER REVIEW COMMISSION'
    ]

    """ If there is no party listed for a candidate, as a last-ditch effort, we use this last-name-to-party table. """
    """ Note: this only has state-wide offices. """
    CANDIDATE_PARTY_LIST = [
        # President
        ("HARRIS", "DEM"),
        ("TRUMP", "REP"),
        ("STEIN", "GRN"),
        ("OLIVER", "LIB"),
        # US Senator
        ("CASEY", "DEM"),
        ("MCCORMICK", "REP"),
        ("THOMAS", "LIB"),
        ("HAZOU", "GRN"),
        ("SELKER", "CST"),
        # Attorney General
        ("DEPASQUALE", "DEM"),
        ("SUNDAY", "REP"),
        ("COWBURN", "LIB"),
        ("WEISS", "GRN"),
        ("MAGILL", "CST"),
        ("SETTLE", "FWD"),
        # Auditor General
        ("KENYATTA", "DEM"),
        ("DEFOOR", "REP"),
        ("SMITH", "LIB"),
        ("ANTON", "ASP"),
        ("GOODRICH", "CST"),
        # State Treasurer
        ("MCCLELLAND", "DEM"),
        ("GARRITY", "REP"),
        ("CIESIELSKI", "LIB"),
        ("BOWMAN", "CST"),
        ("FOSTER", "FWD")
    ]