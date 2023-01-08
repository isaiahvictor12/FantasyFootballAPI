import csv

# Open the CSV file
with open("2021_matchups.csv", "r") as f:
    # Create a CSV reader
    reader = csv.reader(f)
    
    # Skip the header row
    next(reader)
    
    # Initialize a dictionary to store the scores for each team
    scores = {}
    
    # Initialize a dictionary to store the total rank for each team
    total_ranks = {}
    
    # initialize the current week
    current_week = "1"
    
    # Loop through the rows in the CSV
    for row in reader:
        # Get the Week, Name1, Score1, Name2, and Score2 from the row
        week = row[1]
        team1 = row[2]
        score1 = row[3]
        team2 = row[4]
        score2 = row[5]
        game_type = row[6]

        if week != current_week:
            # Calculate the ranks for each team
            ranks = {}
            for team, score in scores.items():
                rank = sum(score > s for s in scores.values())
                ranks[team] = rank
            
            # Update the total rank for each team
            for team, rank in ranks.items():
                total_ranks[team] = total_ranks.get(team, 0) + (rank / 11)

            # Reset the scores and update the current week
            scores = {}
            current_week = week

        # If this is a regular season game, update the scores for each team
        if game_type == "Regular":
            if score1:
                score1 = float(score1)
            else:
                score1 = 0
            if score2:
                score2 = float(score2)
            else:
                score2 = 0
            scores[team1] = scores.get(team1, 0) + score1
            scores[team2] = scores.get(team2, 0) + score2
        # If this is not a regular season game or not week 1, stop updating the scores
        elif game_type != "Regular":
            break

    # Print the total rank for each team
    for team, total_rank in total_ranks.items():
        print("{} had a total rank of {}".format(team, round(total_rank, 2)))
