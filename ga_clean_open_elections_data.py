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

ga_votes_per_party.to_csv("data/ga_pres20_precinct_votes.csv", index=False)