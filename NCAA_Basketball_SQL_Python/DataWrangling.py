
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Set up Python to enable MySQL access to the 'root' account
engine = create_engine('mysql+mysqlconnector://root:xxxxx@127.0.0.1:3306/mydb', echo=False)



# Stadium Data:
print("Importing Stadium Data ...")

stadium = pd.read_json('Stadium.json')

# # Select six specific fields for the teams table to be added to MySQL
stadium2 = stadium[['StadiumID', 'Active', 'Name', 'Address', 'City', 'State', 'Zip', 'Country', 'Capacity', 'GeoLat', 'GeoLong']]

# Players Data being transferred to SQL
stadium2.to_sql(name='stadium', con=engine, if_exists = 'append', index=False)




# Importing Teams Data:

print("Importing Teams Data ...")

# Reading data from JSON file.
teams = pd.read_json('Teams.json')

# # Delete the Active columm from teams before converting the stadium dict
del teams['Active']

# # Rename the Name column to Mascot
teams.rename(columns={'Name':'Mascot'}, inplace=True)

# # Convert the dict information in the Stadium field to individual fields
teams = teams.join(pd.DataFrame(teams["Stadium"].to_dict()).T)

# # Observing what data is there, to import later to SQL
print(teams.columns)

# Dropping rows having fields empty within the StadiumID column
teams = teams.dropna(subset=["StadiumID"])

# # Select six specific fields for the teams table to be added to MySQL
teams2 = teams[['TeamID','School','Mascot','Wins','Losses','Conference','ConferenceWins','ConferenceLosses','ApRank','StadiumID']]

# # Teams Data being transferred to SQL
teams2.to_sql(name='teams', con=engine, if_exists = 'append', index=False)




# Player data:

print("Importing Player Data ...")

# Reading data from JSON file
players = pd.read_json('PlayerDetailsbyActive.json')

# Creating copy of players data
players_copy = players.copy()

# Removing data that do not match original set of TeamIDs imported from Teams Data
for index, row in players_copy.iterrows():
    if row['TeamID'] not in list(teams['TeamID']):
       players.drop(index, inplace = True)


# # Selecting specific fields for the teams table to be added to MySQL
players2 = players[['PlayerID', 'FirstName', 'LastName', 'TeamID', 'Team', 'Jersey', 'Position', 'Class', 'Height', 'Weight']]        

# Players Data being transferred to SQL
players2.to_sql(name='player', con=engine, if_exists = 'append', index=False)





# Importing Game Data:

print("Importing Games Data ...")

# Reading Data from JSON file.
games = pd.read_json('GameData.json')

# # Converting DateTime column to datetime format:
pd.to_datetime(games['DateTime'])

# #Convert the dict information in the Stadium field to individual fields
games = games.join(pd.DataFrame(games["Stadium"].to_dict()).T)

# Deleting duplicates
games = games.drop_duplicates(subset=["GameID"], keep=False)


# # Selecting specific fields for the teams table to be added to MySQL
games2 = games[['GameID', 'Season', 'SeasonType', 'Status', 'DateTime', 'AwayTeam', 'HomeTeam', 'AwayTeamID', 'HomeTeamID', 'AwayTeamScore', 'HomeTeamScore', 'PointSpread', 'OverUnder', 'AwayPointSpreadPayout', 'HomePointSpreadPayout', 'OverPayout', 'UnderPayout', 'StadiumID', 'AwayTeamMoneyLine', 'HomeTeamMoneyLine']]

# Converting periods to dataframe
periods = pd.DataFrame(columns=['PeriodID', 'GameID', 'Number', 'Name', 'Type', 'AwayScore', 'HomeScore'])
for i in games['Periods']:
    for j in range(len(i)):
        periods = periods.append(i[j], ignore_index = True)

# # Selecting specific fields for the teams table to be added to MySQL        
periods2 = periods[['PeriodID', 'GameID', 'Number', 'Name', 'Type', 'AwayScore', 'HomeScore']]

# Games and Periods Data being transferred to SQL
games2.to_sql(name='games', con=engine, if_exists = 'append', index=False)
periods2.to_sql(name='periods', con=engine, if_exists = 'append', index=False)




# Player and TeamSeasonStats.json

print("Importing Player Season Stats and Team Season Stats Data ...")

#Reading Player Season Stats from JSON File
pstats = pd.read_json('PlayerSeasonStats.json')

# Only taking rows that match with TeamIDs and PlayerIDs imported earlier
pstats = pstats[pstats.TeamID.isin(teams.TeamID) & pstats.PlayerID.isin(players.PlayerID)]


# # Selecting  specific fields for the teams table to be added to MySQL
pstats2 = pstats[['StatID', 'TeamID', 'PlayerID', 'SeasonType', 'Season', 'Team', 'Games', 'Minutes', 'FieldGoalsMade', 'FieldGoalsAttempted', 'FieldGoalsPercentage', 'TwoPointersMade', 'TwoPointersAttempted', 'TwoPointersPercentage', 'ThreePointersMade', 'ThreePointersAttempted', 'ThreePointersPercentage', 'FreeThrowsMade', 'FreeThrowsAttempted', 'FreeThrowsPercentage', 'OffensiveRebounds', 'DefensiveRebounds', 'Rebounds', 'Assists', 'Steals', 'BlockedShots','Turnovers', 'PersonalFouls', 'Points']]

# Player Season Stats being transferred to SQL
pstats2.to_sql(name='seasonstats', con=engine, if_exists = 'append', index=False)

#Reading Team Season Stats from JSON File
tstats = pd.read_json('TeamSeasonStats.json')

# Only taking rows that match with TeamIDs imported earlier
tstats = tstats[tstats.TeamID.isin(teams.TeamID)]

# # Selecting  specific fields for the teams table to be added to MySQL
tstats2 = tstats[['StatID', 'TeamID', 'SeasonType', 'Season', 'Team', 'Wins','Losses', 'ConferenceWins', 'ConferenceLosses', 'Games','Minutes', 'FieldGoalsMade', 'FieldGoalsAttempted','FieldGoalsPercentage', 'TwoPointersMade', 'TwoPointersAttempted','TwoPointersPercentage', 'ThreePointersMade', 'ThreePointersAttempted','ThreePointersPercentage', 'FreeThrowsMade', 'FreeThrowsAttempted','FreeThrowsPercentage', 'OffensiveRebounds', 'DefensiveRebounds','Rebounds', 'Assists', 'Steals', 'BlockedShots', 'Turnovers','PersonalFouls', 'Points']]

# Team Season Stats Data being transferred to SQL
tstats2.to_sql(name='seasonstats', con=engine, if_exists = 'append', index=False)

