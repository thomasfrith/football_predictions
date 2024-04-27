import urllib.request
import urllib.parse

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

# list the group names for search purposes later
GROUPS = ["A", "B", "C", "D", "E", "F", "G", "H"]

# list the group headers for data format
RESULTS_INDEX = [
        "MP", "W", "D", "L", "GF", "GA", "GD", "PTS", "xGF", "xGA", "xGD", "xGAve"
        ]


def refresh_data():


  # scrape data from fbref
  url = "https://fbref.com/en/comps/106/Womens-World-Cup-Stats"

  # pretend we are a web browser
  headers = {
      "User-Agent":
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
  }

  # request the url with the filter data
  request = urllib.request.Request(url, headers=headers)
  request_open = urllib.request.urlopen(request)

  # read the html data
  html_bytes = request_open.read()
  html = html_bytes.decode("utf-8")

  # conver html into soup
  soup = BeautifulSoup(html_bytes, "html.parser")

  # find the table in the soup
  soup_group = soup.find("div", id="div_Group stage")

  # initiate dictionary
  results = {}

  # for each group, extract the team data
  for group in GROUPS:

      # find each group from the table
      teams_html = soup_group.find("div", id="all_results20231061" + str(group))

      # find each team from the group
      teams = teams_html.find_all("tr")
      # remove the first result (not a team)
      teams.pop(0)

      # for each team, extract the data
      for team in teams:

          # find the data entries in the html
          data_entries = team.find_all("td")
          # extract the team name
          team_name = data_entries[0].text
          team_name = team_name[team_name.index(" ")+1:len(team_name)]
          # now remove the team name (as this is used as column header)
          data_entries.pop(0)
          data_entries = data_entries[:len(data_entries)-2]

          # initiate nested dictionary
          results[team_name] = {}

          # populate the dictionary with the stats
          results[team_name] = {header: float(data_entry.text) for header, data_entry in zip(RESULTS_INDEX,data_entries)}
          
          results[team_name]["group"] = group    
          
  # convert to data frame
  df = pd.DataFrame(data=results)

  # convert to csv
  df.to_json("world_data.json")


# get euro data from file and convert to data format
# add columns for attack and defences stats
def get_data():

  # read euro data from old file
  df = pd.read_json("world_data.json", orient="index")

  return df

  

  
  



