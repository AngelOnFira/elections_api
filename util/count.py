from tinydb import TinyDB, Query
from collections import defaultdict
import operator

from functions import *

db = TinyDB('../database/database.json')

candidates = load_candidates('../database/candidates.json')

vote = Query()

print("")
results = db.all()

voters = {}

for result in results:
    # See if a voter should be updated with a newer vote
    greater = False
    if (result['user'] in voters):
        greater = True if (int(result['time']) > int(voters[result['user']][0])) else False

    # Add the voter
    if (result['user'] not in voters or greater):
        voters[result['user']] = [
            result['time'],
            result['vote']
        ]

for role in candidates.keys():
    majority = False
    removed_list = []
    num_cand = len(candidates[role])

    print("")
    print("Counting votes for " + role)
    while (majority == False):
        no_conf = 0
        count = defaultdict(int)

        for voter in voters.values():
            vote = voter[1][role]
            
            if (vote['0'] != None):
                no_conf += 1
            else:
                found = False
                for i in range(num_cand):
                    if (vote[str(i + 1)] not in removed_list and not found):
                        count[vote[str(i + 1)]] += 1
                    found = True

                if (not found):
                    print ("Error, no candidate found to count")

        total_votes = sum(list(count.values())) + no_conf
        highest_candidate = max(count.items(), key=operator.itemgetter(1))[0]
        lowest_candidate = min(count.items(), key=operator.itemgetter(1))[0]

        print(dict(count))

        if (is_majority(no_conf, total_votes) == True):
            print("The role of " + role + " has been voted no confidence.")
            majority = True
        else:
            if (is_majority(count[highest_candidate], total_votes)):
                majority = True
                print("The role of " + role + " was won by " + highest_candidate + " with " + str(count[highest_candidate]) + " votes!")
                print("There were " + str(no_conf) + " no confidence votes.")
            else:
                print("Majority not found, removing " + lowest_candidate)
                removed_list.append(lowest_candidate)