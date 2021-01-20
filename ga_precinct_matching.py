"""
Precinct Maching between 2020 Presidential election data and 2018 Precinct shapefile.
The precinct level election data was downloaded from open-elections (which appears to be scraped
from the SOS's Clarity-base web application for the Official Results.).  The 2018 precinct shapefile
was downloaded from the Georgia General Assembly Legislative and Congressional Reapportionment 
Office’s website.
(https://web.archive.org/web/20201206182139/http://www.legis.ga.gov/Joint/reapportionment/en-US/default.aspx)

Notes:
    * There are 2,659 Precincts in the shapefile.  Of these 30 precincts have 0 votes in the 2018 
        elections; 17 have 0 population wrt the 2010 Census.
    * There are 2,656 precincts in the 2020 election results. Of these 3 precincts have 0 votes in 
        the 2020 presidential election.
    * 2 id columns for shapefile `PREC_x` and `PREC_y`.  They disagree for 501 precincts.
        2383 (89.7%) of the 2,656 2020 precincts match exactly to either the `PREC_x` or `PREC_y`
        columns.  
    * This leaves 273 precincts to be manually audited / matched to the 2018 shapes.
"""

import pandas as pd
import geopandas as gpd
import numpy as np
from tqdm import tqdm

pres20votes = pd.read_csv("data/ga_pres20_precinct_votes.csv")

ga2018shapes = gpd.read_file("shapes/GA_precincts/GA_2018_precincts/GA_2018_precincts.shp")



## Initally 3 more precincts in the shapefile than in the voting results.
print(ga2018shapes.shape[0], pres20votes.shape[0])

ids_match = ga2018shapes.query("PREC_x == PREC_y")
ids_no_match = ga2018shapes.query("PREC_x != PREC_y")

test_exact_match = pd.merge(left=ids_match, right=pres20votes, left_on="PREC_x", right_on="PREC")
test_exact_match_x = pd.merge(left=ids_no_match, right=pres20votes, left_on="PREC_x", right_on="PREC")
test_exact_match_y = pd.merge(left=ids_no_match, right=pres20votes, left_on="PREC_y", right_on="PREC")

print(pres20votes.shape[0] - (test_exact_match.shape[0] + test_exact_match_x.shape[0] 
                                + test_exact_match_y.shape[0]))
print((test_exact_match.shape[0] + test_exact_match_x.shape[0] + test_exact_match_y.shape[0])
       / pres20votes.shape[0])

pres20votes_w_match = pd.concat([test_exact_match,test_exact_match_x,test_exact_match_y], ignore_index=True)

pres20votes_no_match = pres20votes.set_index("PREC").loc[pres20votes.set_index("PREC").index.difference(pres20votes_w_match.PREC)].reset_index()