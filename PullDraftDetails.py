import csv
import requests
import pandas as pd
import numpy as np


# Define URL parameters
# league_id = 348540 # main league
league_id = 943736814 # twitter league
# league_id = 41507016 # random league
year = 2022
week = 1

# Define the URL with our parameters
url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}"



# Convert the response to a JSON
draft_response = requests.get(url, params={"view" : "mDraftDetail"})
draft_json = draft_response.json()
draft_df = pd.json_normalize(draft_json['draftDetail']['picks'])

draft_column_names = {
    'roundId':'Round',
    'roundPickNumber':'Pick',
    'teamId':'Team',
    'playerId':'Player'
}
draft_df = draft_df.reindex(columns=draft_column_names).rename(columns=draft_column_names)


team_response = requests.get(url, 
                                params={"leagueId" : league_id,
                                       "seasonId" : year,
                                       "matchupPeriodId" : week,
                                       "view": "mTeam"})
team_json = team_response.json()
team_df = pd.json_normalize(team_json['teams'])
team_column_names = {
    'id':'id',
    'location':'Name1',
    'nickname':'Name2'
}
team_df = team_df.reindex(columns=team_column_names).rename(columns=team_column_names)
team_df['Name'] = team_df['Name1'] + ' ' + team_df['Name2']
team_df = team_df.filter(['id', 'Name'])

draft_df = draft_df.rename(columns={"Team":"id"})
draft_df = draft_df.merge(team_df, on=['id'], how='left')
draft_df = draft_df[['Round', "Pick", "Player", "Name"]]

# Make a request to the ESPN API
player_response = requests.get(url + '?view=mMatchup&view=mMatchupScore',
                    params={'scoringPeriodId': week, 'matchupPeriodId': week})

# Transform response into a JSON string
player_name = []
player_id = []
player_pos = []

player_json = player_response.json()
# Loop through each team
for team in range(0, len(player_json['teams'])):
    
    # Loop through each roster slot in each team
    for slot in range(0, len(player_json['teams'][team]['roster']['entries'])):
        # Append player name, player fantasy team, and player ro
        player_df = pd.json_normalize(player_json['teams'][team]['roster']['entries'][slot]['playerPoolEntry']['player'])
        name = player_df['firstName'] + ' ' + player_df['lastName']
        player_name.append(str(name)[5:-14])
        player_id.append(player_df['id'])
        posId = player_df['defaultPositionId']
        player_pos.append(str(posId)[5:-38])
print(player_pos)

 # Put the lists into a dictionary
player_dict = {
    'PlayerName' : player_name,
    'id' : player_id,
    'PositionId': player_pos
}

# Transform the dictionary into a DataFrame
player_df = pd.DataFrame.from_dict(player_dict)

draft_df = draft_df.rename(columns={"Player":"id"})

player_df['id'] = np.array(player_df['id'], dtype=np.int32)
# draft_df['id'] = np.array(draft_df['id'], dtype=np.int32)

player_df['id'] = player_df['id'].astype(str)
draft_df['id'] = draft_df['id'].astype(str)

draft_df = draft_df.merge(player_df, on=['id'], how='left')
draft_df = draft_df[["Name", 'Round', "Pick", "PlayerName", "PositionId"]]
draft_df.to_csv('draftresults.csv')

with open('draftresults.txt', 'w') as f:
    print('draft results cleared')

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

        
        with open('draftresults.txt', 'a') as f:
            f.write(f'{name} drafted {player} with pick {pick} in round {round}.\n')

