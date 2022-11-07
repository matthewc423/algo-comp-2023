import numpy as np
import random
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    preferences = []
    for i in range(len(scores)):
        for j in range(len(scores[i])):
            if i == j:
                scores[i][j] = (j, -10)
            elif (gender_id[i] == "Nonbinary" and gender_id[j] != "Nonbinary") or (gender_id[i] == "Nonbinary" and gender_id == "Nonbinary"):
                scores[i][j] = (j, 0)
            elif (gender_pref[i] == "Bisexual" and gender_pref[j] == gender_id[i]) or (gender_pref[j] == "Bisexual" and gender_pref[i] == gender_id[j]):
                scores[i][j] = (j, scores[i][j])
            elif gender_pref[i] != gender_id[j] or gender_pref[j] != gender_id[i]:
                scores[i][j] = (j, 0)
            else:
                scores[i][j] = (j, scores[i][j])
        valids = sorted(scores[i], key = lambda x: x[1], reverse = True)
        valids = [v[0] for v in valids]
        preferences.append(valids)

    proposers = []
    receivers = []
    while len(proposers) < len(gender_id) // 2:
        rint = random.randint(0, len(gender_id) - 1)
        if rint not in proposers:
            proposers.append(rint)
    print(proposers)

    for i in range(len(gender_id)):
        if i not in proposers:
            receivers.append(i)

    print(receivers)

    divpreferences = []
    for i in range(len(preferences)):
        divpreferences.append([])

    for i in range(len(preferences)):
        for j in range(len(preferences[i])):
            if i in proposers and preferences[i][j] in receivers:
                divpreferences[i].append(preferences[i][j])
            elif i in receivers and preferences[i][j] in proposers:
                divpreferences[i].append(preferences[i][j])
    print(divpreferences)
    proposed = divpreferences

    matches = [None] * len(scores)
    while len(proposers) > 0:
        m = proposers.pop(0)
        if proposed[m] != []:
            i = 0
            w = proposed[m].pop(0)
            mp = matches[w]
            if mp == None:
                matches[w] = m 
                matches[m] = w 
            elif divpreferences[w].index(m) < divpreferences[w].index(mp):
                matches[w] = m 
                matches[m] = w
                matches[mp] = None
                proposers.append(mp) 
            else:
                proposers.append(m)

    matchlist = []
    for i in range(len(scores)):
        if matches[i] != None:
            matchlist.append((i, matches[i]))
            matches[matches[i]] = None
    for m in matchlist:
        print(m)
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
