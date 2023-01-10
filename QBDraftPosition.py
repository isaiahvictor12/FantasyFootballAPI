import csv


with open('draftresults.csv', "r") as r:
    # Create a CSV reader
    reader = csv.reader(r)    
    # Skip the header row
    next(reader)

    qb_draft_spot = {}

    for row in reader:
        name = row[1]
        round = row[2]
        pick = row[3]
        player = row[4]
        position = row[5]
        
        if int(position) == 1 and qb_draft_spot.get(name, 0) == 0:
            qb_draft_spot[name] = (int(round) * 12) + int(pick)

        with open('draftresults.txt', 'a') as f:
            f.write(f'{name} drafted {player} with pick {pick} in round {round}.\n')
print(qb_draft_spot)