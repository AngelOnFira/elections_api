import json

def validate_vote(client_vote, candidates):

    # Next, validate the number of categories submitted
    if (len(client_vote.keys()) != len(candidates.keys())):
        return [-1, "Error, number of submitted candidates is wrong"]

    # Next, validate the proper candidates
    for role in candidates.keys():
        if (role in client_vote):
            client_candidate = client_vote[role]
        else:
            return [-1, "Error, candidates not valid"]

        if (client_candidate["0"] == None and client_candidate["1"] == None):
            return [-1, "Error, an option must be choosen for " + role]

        if (client_candidate["0"] != None and client_candidate["0"] != "NO CONFIDENCE"):
            return [-1, "Error, bad no confidence"]

    return [1, "Valid"]

def load_candidates(file_loc):
    with open(file_loc) as f:
        candidates_db = json.load(f)

    candidates = {}
    for role in candidates_db.keys():
        candidates[role] = []
        for candidate in candidates_db[role]:
           candidates[role].append(candidate)

    return candidates

def is_majority(votes, total):
    if (votes > int(total / 2)):
        return True
    else:
        return False

if __name__ == "__main__":
    import json
    load_candidates()