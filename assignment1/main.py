#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

def response_score(r1, r2, qdist):
    score = 0.0
    for i in range(len(r1)):
        if r1[i] == r2[i]:
            score += 0.03/(1 + qdist[i][r1[i]])
    return score

def compute_score(user1, user2, qdist):
    finalscore = 0.0
    if user1.gender == user2.preferences[0]:
        finalscore += 0.35
    if user2.gender == user1.preferences[0]:
        finalscore += 0.35
    finalscore += 0.12 - (abs(user1.grad_year - user2.grad_year)) * 0.03
    finalscore += response_score(user1.responses, user2.responses, qdist)
    return finalscore

if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    qdist = [ [0]*6 for _ in range(len(users[0].responses)) ]

    for i in range(len(users)):
        for j in range(len(users[i].responses)):
            qdist[j][users[i].responses[j]] += 1

    for i in range(len(qdist)):
        total = sum(qdist[i])
        if total != 0:
            for j in range(len(qdist[i])):
                qdist[i][j] /= total

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2, qdist)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
