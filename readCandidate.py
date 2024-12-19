from Candidate import Candidate

def votesToInt(strVotes):
	""" Convert string to integer. """
	str2 = strVotes.replace(',', '') # Remove any commas
	return int(str2)

def findFirstNumber(strArray):
	""" Find first numeric field in an array of strings. """
	i = 0
	for line in strArray:
		if line.isnumeric():
			return i
		i += 1
	return -1

def normalizeCandidateName(indexToCounts, name, fields):
    """ Return normalized candidate name. """
    n = name
    if (indexToCounts > 1):
        for j in range(2, indexToCounts):
            """ Remove VP from names of format 'Pres / VP', concat everything else. """
            if fields[j] == '/':
                break
            n = n + ' ' + fields[j]
    """	
    Presidential candidates can have " - presidential candidate" after their name.
    Remove this
    """
    if " - " in n:
        end = n.find(" - ")
        n = n[:end]
    """ Remove any commas - they confuse the CSV file. """
    n = n.replace(',', '')
    return n

def readCandidateSingleLine(office, candidateLine, txt, offset, lineSpec):
    """ 
    Parse votes for a candidate that appear on a single line. 
    Indices are into a single string with space-separated fields.
    """
    c = Candidate(office)
    # Parse the fields on this line.
    fields = candidateLine.replace(',', '').split(' ')
    party = fields[lineSpec.party_index]
    candidateName = fields[lineSpec.candidate_name_index]
    countStartIndex = findFirstNumber(fields)
    candidateName = normalizeCandidateName(countStartIndex, candidateName, fields)
    votes_mail = fields[lineSpec.votes_mail_index + countStartIndex]
    votes_ed = fields[lineSpec.votes_ed_index + countStartIndex]
    votes_prov = fields[lineSpec.votes_prov_index+ countStartIndex]
    votes_total = fields[lineSpec.votes_total_index + countStartIndex]
    c = Candidate(office)
    c.name = candidateName
    c.party = party
    c.votes_ed = votesToInt(votes_ed)
    c.votes_mail = votesToInt(votes_mail)
    c.votes_prov = votesToInt(votes_prov)
    c.votes_total = votesToInt(votes_total)
    return c


def readCandidateMultiLine(office, candidateLine, txt, offset, lineSpec):
    """ 
    Parse votes for a candidate that appear on multiple lines. 
    Indices are into an array of strings starting from the candidate name.
    """
    c = Candidate(office)
    candidateName = normalizeCandidateName(0, txt[offset], [])
    if lineSpec.party_index > 0:
        party = txt[lineSpec.party_index + offset]
    else:
         party = 'UNKNOWN'
    votes_mail = txt[lineSpec.votes_mail_index + offset]
    votes_ed = txt[lineSpec.votes_ed_index + offset]
    votes_prov = txt[lineSpec.votes_prov_index + offset]
    votes_total = txt[lineSpec.votes_total_index + offset]
    c = Candidate(office)
    c.name = candidateName
    c.party = party
    c.votes_ed = votesToInt(votes_ed)
    c.votes_mail = votesToInt(votes_mail)
    c.votes_prov = votesToInt(votes_prov)
    c.votes_total = votesToInt(votes_total)
    return c
