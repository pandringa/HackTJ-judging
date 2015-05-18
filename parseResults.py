from pprint import pprint
import operator
from json import dumps

assignments = {} ## email: [1, 2, 3, 4, 5]
hacks = {}
with open("hacks.csv", "r") as f:
    for line in f.readlines():
    	cols = line.replace('\n', '').split('\t')
    	hacks[cols[0]] = {
    		"name": cols[1],
            "innovation_betterThan": [],
            "design_betterThan": [],
            "overall_betterThan": [],
            "judgeCount": 0
    	}


with open("assignments.csv", "r") as f:
    for line in f.readlines():
    	cols = line.replace('\n', '').split('\t')
    	assignments[cols[1]] = cols[2:]
        for c in assignments[cols[1]]:
            hacks[c]["judgeCount"] += 1

with open("judging.csv", "r") as f:
    for line in f.readlines():
    	cols = line.replace('\n', '').split('\t')
    	email = cols[2]
        for i in range(0, 6):
            # if 'isMobile' in hacks[ assignments[email][i] ]:
            #     if ("mobile" in cols[2*i+3].lower()) != hacks[ assignments[email][i] ]['isMobile']:
            #         print "ALERT: judge chose different value for mobile for hack at table "+assignments[email][i]
            hacks[ assignments[email][i] ]['isMobile'] = ("mobile" in cols[2*i+3].lower())

            # if 'isWeb' in hacks[ assignments[email][i] ]:
            #     if ("web" in cols[2*i+3].lower()) != hacks[ assignments[email][i] ]['isWeb']:
            #         print "ALERT: judge chose different value for web for hack at table "+assignments[email][i]
            hacks[ assignments[email][i] ]['isWeb'] = ("web" in cols[2*i+3].lower())

            # if 'isBeginner' in hacks[ assignments[email][i] ]:
            #     if ("mobile" in cols[2*i+4].lower()) != hacks[ assignments[email][i] ]['isBeginner']:
            #         print "ALERT: judge chose different value for mobile for hack at table "+assignments[email][i]
            hacks[ assignments[email][i] ]['isBeginner'] = (cols[2*i+4].lower() == "yes")

        innovationRanking = cols[15].replace(' ', '').split(',')
        for i, n in enumerate(innovationRanking):
            if i+1 < len(innovationRanking):
                hacks[ n ]['innovation_betterThan'] += innovationRanking[i+1:]

        designRanking = cols[16].replace(' ', '').split(',')
        for i, n in enumerate(designRanking):
            if i+1 < len(designRanking):
                hacks[ n ]['design_betterThan'] += designRanking[i+1:]

        overallRanking = cols[17].replace(' ', '').split(',')
        for i, n in enumerate(overallRanking):
            if i+1 < len(overallRanking):
                hacks[ n ]['overall_betterThan'] += overallRanking[i+1:]

def innovationScore(hackNum):
    score = 0
    for n in hacks[ hackNum ]['innovation_betterThan']:
        score += len(hacks[n]['innovation_betterThan']) / hacks[n]['judgeCount']; ## Average position of hack in rankings
    return score

def designScore(hackNum):
    score = 0
    for n in hacks[ hackNum ]['design_betterThan']:
        score += len(hacks[n]['design_betterThan']) / hacks[n]['judgeCount']; ## Average position of hack in rankings
    return score

def overallScore(hackNum):
    score = 0
    for n in hacks[ hackNum ]['overall_betterThan']:
        score += len(hacks[n]['overall_betterThan']) / hacks[n]['judgeCount']; ## Average position of hack in rankings
    return score

for n in hacks:
    hacks[n]['designScore'] = designScore(n);
    hacks[n]['innovationScore'] = innovationScore(n);
    hacks[n]['overallScore'] = overallScore(n);

designList = sorted(hacks.values(), key=lambda (item): -1 * item['designScore']);
innovationList = sorted(hacks.values(), key=lambda (item): -1 * item['innovationScore']);
overallList = sorted(hacks.values(), key=lambda (item): -1 * item['overallScore']);

print "Design Ranking:"
for i in range(0, 10):
    pprint(designList[i]["name"]);

print "\nInnovation Ranking:"
for i in range(0, 10):
    pprint(innovationList[i]["name"]);

print "\nOverall Ranking:"
for i in range(0, 10):
    pprint(overallList[i]["name"]);


with open("data.json", "w") as outFile:
    outFile.write(dumps(hacks))
