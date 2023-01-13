import csv
import matplotlib.pyplot as plt
import numpy as np

year = 2022

qb_draft_spot_dict = {}
expected_wins_dict = {}

with open('draftresults.csv', "r") as r:
    # Create a CSV reader
    reader = csv.reader(r)    
    # Skip the header row
    next(reader)

    for row in reader:
        name = row[1]
        round = row[2]
        pick = row[3]
        player = row[4]
        position = row[5]
        
        if int(position) == 1 and qb_draft_spot_dict.get(name, 0) == 0:
            qb_draft_spot_dict[name] = (int(round) * 12) + int(pick) - 12

        with open('draftresults.txt', 'a') as f:
            f.write(f'{name} drafted {player} with pick {pick} in round {round}.\n')

with open(f'{year}standings.csv', "r") as r:
    # Create a CSV reader
    reader = csv.reader(r)    
    # Skip the header row
    next(reader)

    for row in reader:
        name = row[1]
        wins = row[2]
        expected_wins = row[3]
        
        expected_wins_dict[name] = expected_wins

plt.title('Expected wins vs draft pick where QB was taken')
plt.axis([0, 140, 0, 12])
plt.xlabel('Pick where team first took a QB')
plt.ylabel('Expected # of wins')

x_arr = []
y_arr = []

for team in qb_draft_spot_dict:
    x = float(qb_draft_spot_dict[team])
    y = float(expected_wins_dict[team])
    plt.plot(x, y, 'ro')
    plt.text(x-10, y+.25, team, fontsize=6)
    x_arr.append(x)
    y_arr.append(y)

#find line of best fit
a, b = np.polyfit(np.array(x_arr), np.array(y_arr), 1)
    
#add line of best fit to plot
plt.plot(np.array(x_arr), a*np.array(x_arr)+b, color='steelblue', linestyle='--', linewidth=2)   

plt.show()



