import csv

# Read the games data
games_data = []
with open('games_ha.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        games_data.append(row)

# Read the boxscores data
boxscores_data = []
with open('boxscores.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        boxscores_data.append(row)

# Create a dictionary to store boxscores by game_id
boxscores_dict = {}
for row in boxscores_data:
    game_id = row['game_id']
    if game_id not in boxscores_dict:
        boxscores_dict[game_id] = []
    boxscores_dict[game_id].append(row)

# Define the list of statistics you want to include
stats = ['mp', 'fg', 'fga', 'fg_pct', 'fg2', 'fg2a', 'fg2_pct', 'fg3', 'fg3a', 'fg3_pct',
         'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts',
         'ts_pct', 'efg_pct', 'fg3a_per_fga_pct', 'fta_per_fga_pct', 'orb_pct', 'drb_pct',
         'trb_pct', 'ast_pct', 'stl_pct', 'blk_pct', 'tov_pct', 'usg_pct', 'off_rtg', 'def_rtg']



# Create a new dataset
new_dataset = []

# Combine the data
for game in games_data:
    game_id = game['game_id']
    if game_id in boxscores_dict:
        boxscores = boxscores_dict[game_id]
        boxscores = boxscores[0]
        home_won = int(game['home_won'])
        loser_stats = [boxscores[f"l_{stat}"] for stat in stats]
        winner_stats = [boxscores[f"w_{stat}"] for stat in stats]

        # Determine home and away teams based on home_won
        if home_won:
            home_team = game['winner']
            away_team = game['loser']
            home_team_stats = winner_stats
            away_team_stats = loser_stats
        else:
            home_team = game['loser']
            away_team = game['winner']
            home_team_stats = loser_stats
            away_team_stats = winner_stats
    
        # Create a row for the new dataset
        new_row = [away_team, home_team, game_id, game['date'], home_won] + home_team_stats + away_team_stats 

        # Append to the new dataset
        new_dataset.append(new_row)

# Write the new dataset to a CSV file
with open('ha_boxscores.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    header = ['away_team', 'home_team', 'game_id', 'date', 'home_won'] + [f'h_{stat}' for stat in stats] + [f'a_{stat}' for stat in stats] 
    csv_writer.writerow(header)
    csv_writer.writerows(new_dataset)
