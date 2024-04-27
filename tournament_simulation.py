from stats import get_poisson_mean
import numpy as np

# determine the winner. If the game is a draw, run the game again (extra time) until there is a winner

def simulate_game(df, team_one, team_two, stats_model):
  
  teams = [team_one, team_two]
  x_goals = {}

  for team in teams:

    for opposition in teams: 

      if opposition!=team:

        x_mean = get_poisson_mean(df, team, opposition, stats_model)
        x_goals[team] = {
          "x_goal": np.random.poisson(x_mean)
          }

  if x_goals[team_one]["x_goal"]>x_goals[team_two]["x_goal"]:
    return team_one

  elif x_goals[team_one]["x_goal"]==x_goals[team_two]["x_goal"]:
    return simulate_game(df, team_one, team_two, stats_model)

  else:
    return team_two


def simulate_tournament(df, teams, stats_model):

  qualified = []

  for i in range(int(len(teams)/2)):
    winner = simulate_game(df, teams[2*i], teams[2*i+1], stats_model)
    qualified.append(winner)
    
  if len(qualified)>1:
    return simulate_tournament(df, qualified, stats_model)
  else:
    return winner




