import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

FINALISTS = ["Switzerland", "Spain", "Netherlands", "South Africa", "Japan", "Norway", "Sweden", "USA", "England", "Nigeria", "Colombia", "Jamaica", "Australia", "Denmark", "France", "Morocco"]

df = pd.read_json("world_data.json", orient="index")

df["GFave"] = df["xGF"]/df["MP"]
df["GAave"] = df["xGA"]/df["MP"]

def game(team1, team2):

  team1_goals = np.random.poisson(np.sqrt(df.loc[team1]["GFave"]*df.loc[team2]["GAave"]))
  
  team2_goals = np.random.poisson(np.sqrt(df.loc[team2]["GFave"]*df.loc[team1]["GAave"]))

  if team1_goals>team2_goals:
    return team1
  elif team1_goals==team2_goals:
    return game(team1,team2)
  else:
    return team2

def tournament(teams):
  teams_remaing = len(teams)
  num_games = int(teams_remaing/2)
  qualified = []
  
  for i in range(num_games):
    winner = game(teams[2*i],teams[2*i+1])
    qualified.append(winner)

  if len(qualified)>1:
    return tournament(qualified)
  else:
    return winner

n = 1000
winner_dict = {team: 0 for team in FINALISTS}

def monte_carlo():
  for i in range(n):
    winner = tournament(FINALISTS)
    winner_dict[winner]+=1
  
  winner_df = pd.DataFrame(data = winner_dict, index = ["win_rate"])
  winner_df = winner_df/n
  
  winner_df.to_json("world_results.json")

monte_carlo()

df = pd.read_json("world_results.json", orient = "index")

df = df.sort_values(by=["win_rate"], ascending = False)

plot = df.plot.bar()
fig = plot.get_figure()
fig.savefig("world_results_plot.pdf",bbox_inches='tight')