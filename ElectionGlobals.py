
class Globals:
    ELECTION = '2024 GENERAL'
    STATE = 'PENNSYLVANIA'
    STATE_ABBREV = 'PA'
    
    # Where PDF files are
    RESULTS_DIR = 'Results_PDF'
    # Per-count list of URLs corresponding to this county
    URL_LIST_FILENAME = "URL_List.txt"

    # Modes of vote result
    MODE_ELECTION_DAY = 'ELECTION DAY'
    MODE_MAIL_IN = 'MAIL-IN'
    MODE_PROVISIONAL = 'PROVISIONAL'
    MODE_TOTAL = 'TOTAL'

    OFFICE_RANKING = [
        'PRESIDENTIAL ELECTORS',
        'UNITED STATES SENATOR',
        'ATTORNEY GENERAL',
        'AUDITOR GENERAL',
        'STATE TREASURER',
        'SENATOR IN THE',
        'REPRESENTATIVE IN CONGRESS',
        'REPRESENTATIVE IN THE',
        'REPRESENTATIVEIN THE', # Misspelling in one of the counties
        'CHARTER REVIEW COMMISSION'
    ]