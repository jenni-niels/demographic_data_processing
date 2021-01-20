"""
2020 Presidential data prep for GA.
The precinct level data here was downloaded from open-elections and county level sums used for qa
were downloaded from the GA Secretary of State's website.

Notes:
    * The code here is the final script I ran to clean this particular data.  This kind of work
      is much more state / (data source) specific than the demographic data.

    * I work using VS code with the python extension and typically use the interactive interpreter
      + the variable inspecter in another tab.  If you are using a Notebook set up, df.head(n) will
      let you view the first n rows of a dataframe.

    * Generally it is good practice to save your dataframe at intermediary steps so that replication
      is easier when you find errors that need to be un-propagated.  Be sure to save the (.csv/.shp)s
      under unique names and not over write files representing prior steps. (a mistake I have made
      too many times)

"""

import pandas as pd
import numpy as np
from tqdm import tqdm

ga_votes_raw = pd.read_csv("data/open_elections_ga_3.11.2020_general.csv")

ga_votes_pres_raw = ga_votes_raw.query("office == 'President'")

ga_votes_pres_raw["total_votes"] = ga_votes_pres_raw[['election_day_votes', 'advanced_votes', 
                                                      'absentee_by_mail_votes', 
                                                      'provisional_votes']].sum(axis=1)

ga_votes_per_party = ga_votes_pres_raw.groupby(["county", "precinct", "party"]).sum()["total_votes"].unstack("party").reset_index()
ga_votes_per_party.columns.name = None

ga_votes_per_party = ga_votes_per_party.rename(columns={"Democrat": "PRES20D", "Libertarian": "PRES20L", 
                                                        "Republican": "PRES20R"})
ga_votes_per_party["PREC"] = (ga_votes_per_party["county"] + ", " + ga_votes_per_party["precinct"]).apply(lambda p: p.upper())

## Check state wide sums against SOS Website: matches
ga_votes_per_party.sum()

cnty_qa = pd.read_csv("data/ga_sos_county_pres_votes.csv", header=[0,1])
cnty_qa.columns = cnty_qa.columns.to_flat_index()
cnty_qa = cnty_qa.rename(columns={('Unnamed: 0_level_0', 'County'): "county",
                        ('Unnamed: 5_level_0', 'Total Votes'): "PRES20R", 
                        ('Unnamed: 10_level_0', 'Total Votes'): "PRES20D", 
                        ('Unnamed: 15_level_0', 'Total Votes'): "PRES20L"},)[["county", "PRES20R", "PRES20D", "PRES20L"]].drop(159).set_index("county")

ga_cnty_votes = ga_votes_per_party.groupby("county").sum()

## Check that it matches at the county level against SoS data.
print((cnty_qa - ga_cnty_votes).sum())

ga_cnty_votes.to_csv("data/ga_pres20_county_votes.csv")

ga_votes_per_party.to_csv("data/ga_pres20_precinct_votes.csv", index=False)