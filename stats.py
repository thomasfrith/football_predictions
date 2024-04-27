from models import Stats_Model_Type
from scrape import get_data

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


# how is the mean for the poisson distribution calculated

def get_poisson_mean(df, team_one, team_two, stats_model):

  if stats_model == Stats_Model_Type.xMAHER:

    #return (df["xGF"].loc[team_one]/np.sqrt(df["xGF"].sum()))*(df["xGA"].loc[team_two]/np.sqrt(df["xGA"].sum()))

    return (df["xGF"].loc[team_one]/df["MP"].loc[team_one])*(df["xGA"].loc[team_two]/df["MP"].loc[team_two])/(df["xGA"].sum()/df["MP"].sum())

  if stats_model == Stats_Model_Type.xMAHER_ODDS_ADJUSTED:

   #return (df["xGF_odds_adjusted"].loc[team_one]/np.sqrt(df["xGF_odds_adjusted"].sum()))*(df["xGA_odds_adjusted"].loc[team_two]/np.sqrt(df["xGA_odds_adjusted"].sum()))

    return (df["xGF_odds_adjusted"].loc[team_one]/df["MP"].loc[team_one])*(df["xGA_odds_adjusted"].loc[team_two]/df["MP"].loc[team_two])/(df["xGA_odds_adjusted"].sum()/df["MP"].sum())

  if stats_model == Stats_Model_Type.xMAHER_MOD:
    return np.sqrt(df["xGF"].loc[team_one]/df["MP"].loc[team_one])*np.sqrt(df["xGA"].loc[team_two]/df["MP"].loc[team_two])

  if stats_model == Stats_Model_Type.xMAHER_MOD_ODDS_ADJUSTED:
    return np.sqrt(df["xGF_odds_adjusted"].loc[team_one]/df["MP"].loc[team_one])*np.sqrt(df["xGA_odds_adjusted"].loc[team_two]/df["MP"].loc[team_two])

  if stats_model == Stats_Model_Type.xGOALS_PER_GAME:
    return df["xGF"].loc[team_one]/df["MP"].loc[team_one]

  if stats_model == Stats_Model_Type.xGOALS_PER_GAME_ODDS_ADJUSTED:
    return df["xGF_odds_adjusted"].loc[team_one]/df["MP"].loc[team_one]

  if stats_model == Stats_Model_Type.GOALS_PER_GAME:
    return df["GF"].loc[team_one]/df["MP"].loc[team_one]

def get_group_rating():
    
    df = get_data()
    df["log_odds"] = np.log(df["odds"])
    df["group_rating"] = 1
    df["log_group_rating"] = 1
    
    for team in df.index.values:
        #log_group_mean = np.mean([df["log_odds"].loc[team]]+[df["log_odds"].loc[opponents] for opponents in df["group_opponents"].loc[team]])
        #df["log_group_rating"] = df["log_odds"] - log_group_mean
        df["log_group_rating"].loc[team]=df["log_odds"].loc[team] - np.mean([df["log_odds"].loc[opponents] for opponents in df["group_opponents"].loc[team]])
        group_mean = np.mean([df["odds"].loc[team]]+[df["odds"].loc[opponents] for opponents in df["group_opponents"].loc[team]])
        df["group_rating"] = df["odds"] - group_mean
        

        
    df.to_json("world_data.json", orient = "index")
    
def get_odds_adjusted_stats():
    
    df = get_data()
    
#    z_xGF = np.polyfit(y=df["xGF"].values, x=df["log_group_rating"].values, deg=1)
#    p_xGF = np.poly1d(z_xGF)
#    
#    z_xGA = np.polyfit(y=df["xGA"].values, x=df["log_group_rating"].values, deg=1)
#    p_xGA = np.poly1d(z_xGA)
    
    z_xGF = np.polyfit(y=df["xGF"].values, x=df["log_group_rating"].values, deg=1)
    p_xGF = np.poly1d(z_xGF)
    
    z_xGA = np.polyfit(y=df["xGA"].values, x=df["log_group_rating"].values, deg=1)
    p_xGA = np.poly1d(z_xGA)
    

#    df["xGF_odds_adjusted"] = p_xGF(0)-p_xGF(df["log_group_rating"])+df["xGF"]
#    df["xGA_odds_adjusted"] = p_xGA(0)-p_xGA(df["log_group_rating"])+df["xGA"]
    
    df["xGF_odds_adjusted"] = df["xGF"]*df["xGF"]/p_xGF(df["log_group_rating"])
    df["xGA_odds_adjusted"] = df["xGA"]*df["xGA"]/p_xGA(df["log_group_rating"])
    
    df.to_json("world_data.json", orient = "index")
    
def print_stats():
    
    stats_model = Stats_Model_Type
    
    for model in stats_model.__dict__.values():
        try:
            df = pd.read_json("world_results_" + model + ".json", orient = "index")
            df = df.sort_values(by=["win_rate"], ascending = False)
            plot = df.plot.bar()
            fig = plot.get_figure()
            fig.savefig("world_results_plot_" + model + ".pdf",bbox_inches='tight')
            
        except:
            pass

  