import requests
import pandas as pd
import numpy as np


# Define URL parameters
# league_id = 348540 # main league
league_id = 943736814 # twitter league
# league_id = 41507016
year = 2022
week = 1

# Define the URL with our parameters
url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{year}/segments/0/leagues/{league_id}"
# Pull team and matchup data from the URL
matchup_response = requests.get(url, 
                                params={"leagueId" : league_id,
                                       "seasonId" : year,
                                       "matchupPeriodId" : week,
                                       "view": "mMatchup"})

team_response = requests.get(url, 
                                params={"leagueId" : league_id,
                                       "seasonId" : year,
                                       "matchupPeriodId" : week,
                                       "view": "mTeam"})
# Transform the response into a json
matchup_json = matchup_response.json()
team_json = team_response.json()
# Transform both of the json outputs into DataFrames
matchup_df = pd.json_normalize(matchup_json['schedule'])
team_df = pd.json_normalize(team_json['teams'])
# Define the column names needed
matchup_column_names = {
    'matchupPeriodId':'Week', 
    'away.teamId':'Team1', 
    'away.totalPoints':'Score1',
    'home.teamId':'Team2', 
    'home.totalPoints':'Score2',
}

team_column_names = {
    'id':'id',
    'location':'Name1',
    'nickname':'Name2'
}

# Reindex based on column names defined above
matchup_df = matchup_df.reindex(columns=matchup_column_names).rename(columns=matchup_column_names)
team_df = team_df.reindex(columns=team_column_names).rename(columns=team_column_names)

# Add a new column for regular/playoff game based on week number
matchup_df['Type'] = ['Regular' if week<=13 else 'Playoff' for week in matchup_df['Week']]

# Concatenate the two name columns
team_df['Name'] = team_df['Name1'] + ' ' + team_df['Name2']

# Drop all columns except id and Name
team_df = team_df.filter(['id', 'Name'])
# (1) Rename Team1 column to id
matchup_df = matchup_df.rename(columns={"Team1":"id"})

# (1) Merge DataFrames to get team names instead of ids and rename Name column to Name1
matchup_df = matchup_df.merge(team_df, on=['id'], how='left')
matchup_df = matchup_df.rename(columns={'Name':'Name1'})

# (1) Drop the id column and reorder columns
matchup_df = matchup_df[['Week', 'Name1', 'Score1', 'Team2', 'Score2', 'Type']]
# (2) Rename Team1 column to id
matchup_df = matchup_df.rename(columns={"Team2":"id"})

# (2) Merge DataFrames to get team names instead of ids and rename Name column to Name2
matchup_df = matchup_df.merge(team_df, on=['id'], how='left')
matchup_df = matchup_df.rename(columns={'Name':'Name2'})

# (2) Drop the id column and reorder columns
matchup_df = matchup_df[['Week', 'Name1', 'Score1', 'Name2', 'Score2', 'Type']]
# Filter down to the week in question
week_matchup_df = matchup_df[matchup_df['Week'] == week]

away_win_df = week_matchup_df[week_matchup_df['Score1'] > week_matchup_df['Score2']].reset_index()

away_loss_df = week_matchup_df[week_matchup_df['Score1'] < week_matchup_df['Score2']].reset_index()

home_win_df = week_matchup_df[week_matchup_df['Score2'] > week_matchup_df['Score1']].reset_index()

home_loss_df = week_matchup_df[week_matchup_df['Score2'] < week_matchup_df['Score1']].reset_index()
# Calculate average score for the week
average_score = (week_matchup_df['Score1'].sum() + week_matchup_df['Score2'].sum()) / 10

matchup_df.to_csv(f'{year}_matchups.csv')