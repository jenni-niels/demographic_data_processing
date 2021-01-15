import geopandas as gpd
import pickle
from gerrychain import Graph, Partition
import matplotlib.pyplot as plt
import maup
import pandas as pd
import requests
from tqdm import tqdm
import numpy as np
from decennial_scraper import block_data_for_state

# We typically use tables P5 and P11 for demographic breakdowns of POP and VAP (see vars/keys in 
# decennial_scraper script)  Here we want AMIN + any so we use the P10 table for a full break down of
# all 63 race combos.  (The P11 table only has that breakdown for the non-Hispanic population)
# For reference we will also use the P6 table for POP

variables = [
            # pop
            "P005001", "P005003", "P005004", "P005005", "P005006", "P005007", "P005008", 
            "P005009", "P005010",
            "P005011", "P005012", "P005013", "P005014", "P005015", "P005016", "P005017",
            
            "P006001","P006003", "P006004","P006005","P006006","P006007",

            # vap
            "P011001", "P011002", "P011005", "P011006",  "P011007", "P011008", "P011009", 
            "P011010", "P011011",
            ## amin vap cols
            "P010005", "P010012","P010016","P010020","P010021","P010022","P010027",
            "P010031","P010032","P010033","P010037","P010038","P010039", "P010043",
            "P010044","P010045","P010048","P010049","P010050", "P010054","P010055",
            "P010056","P010058","P010059","P010060","P010062", "P010064","P010065",
            "P010066","P010068","P010069", "P010071",]
keys = [
        # pop
        "TOTPOP", "NH_WHITE", "NH_BLACK", "NH_AMIN ", "NH_ASIAN", "NH_NHPI", "NH_OTHER", "NH_2MORE",
        "HISP", "H_WHITE", "H_BLACK", "H_AMIN", "H_ASIAN", "H_NHPI", "H_OTHER", "H_2MORE",
        "WHITE_ANY", "BLACK_ANY", "AMIN_ANY", "ASIAN_ANY", "NHPI_ANY", "OTHER_ANY",

        # vap
        "VAP", "HVAP", "WVAP", "BVAP", "AMINVAP", "ASIANVAP", "NHPIVAP", "OTHERVAP", "2MOREVAP",
        
        ## amin vap cols
        "P010005", "P010012","P010016","P010020","P010021","P010022","P010027",
        "P010031","P010032","P010033","P010037","P010038","P010039", "P010043",
        "P010044","P010045","P010048","P010049","P010050", "P010054","P010055",
        "P010056","P010058","P010059","P010060","P010062", "P010064","P010065",
        "P010066","P010068","P010069", "P010071",
]

amin_any_vap_cols = ["P010005","P010012","P010016","P010020","P010021","P010022","P010027",
                     "P010031","P010032","P010033","P010037","P010038","P010039", "P010043",
                     "P010044","P010045","P010048","P010049","P010050", "P010054","P010055",
                     "P010056","P010058","P010059","P010060","P010062", "P010064","P010065",
                     "P010066","P010068","P010069", "P010071",]

columns_to_merge = [
        # pop
        "TOTPOP", "NH_WHITE", "NH_BLACK", "NH_AMIN ", "NH_ASIAN", "NH_NHPI", "NH_OTHER", "NH_2MORE",
        "HISP", "H_WHITE", "H_BLACK", "H_AMIN", "H_ASIAN", "H_NHPI", "H_OTHER", "H_2MORE",
        "WHITE_ANY", "BLACK_ANY", "AMIN_ANY", "ASIAN_ANY", "NHPI_ANY", "OTHER_ANY",

        # vap
        "VAP", "HVAP", "WVAP", "BVAP", "AMINVAP", "ASIANVAP", "NHPIVAP", "OTHERVAP", "2MOREVAP",
        "AMINVAP*",
        
        ## state information
        "geoid"]

# Collect block level census data from the Census API
ga_blocks = block_data_for_state(13, variables, keys)

# Create column AMINVAP* of the voting age population which selected AMIN as part of their race.
ga_blocks["AMINVAP*"] = ga_blocks[amin_any_vap_cols].sum(axis=1)


# Shapefiles come from TIGER/Line website:
# https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
ga_blk_shapes = gpd.read_file("shapes/GA_blocks/tl_2019_13_tabblock10.shp")

ga_blks_shape_w_demo = pd.merge(left=ga_blk_shapes, right=ga_blocks[columns_to_merge], 
                                left_on="GEOID10", right_on="geoid")

ga_blks_shape_w_demo.to_file("shapes/GA_blocks/ga_blocks_2010_demo.shp")

ga_bgs_shape_w_demo = gpd.read_file("shapes/GA_bgs/ga_bgs_2010_demo.shp")


## Maup data between decennial on blocks and ACS on bgs.
assignment = maup.assign(ga_blks_shape_w_demo, ga_bgs_shape_w_demo)

block_to_bgs_cols = ["TOTPOP", "NH_WHITE", "NH_BLACK", "NH_AMIN ", "NH_ASIAN", "NH_NHPI", "NH_OTHER", "NH_2MORE",
        "HISP", "H_WHITE", "H_BLACK", "H_AMIN", "H_ASIAN", "H_NHPI", "H_OTHER", "H_2MORE",
        "WHITE_ANY", "BLACK_ANY", "AMIN_ANY", "ASIAN_ANY", "NHPI_ANY", "OTHER_ANY",

        # vap
        "VAP", "HVAP", "WVAP", "BVAP", "AMINVAP", "ASIANVAP", "NHPIVAP", "OTHERVAP", "2MOREVAP",
        "AMINVAP*",]

bgs_to_blocks_cols = ['HCVAP', 'NHCVAP', '2MORECVAP', 'AMINCVAP',
       'BAMINCVAP', 'WAMINCVAP', 'ASIANCVAP', 'WASIANCVAP', 'BCVAP', 'BWCVAP',
       'NHPICVAP', 'WCVAP', 'CVAP', 'HCPOP', 'NHCPOP', '2MORECPOP', 'AMINCPOP',
       'BAMINCPOP', 'WAMINCPOP', 'ASIANCPOP', 'WASIANCPOP', 'BCPOP', 'BWCPOP',
       'NHPICPOP', 'WCPOP', 'CPOP', 'AMINCVAP*', 'AMINCPOP*']

## Aggregate decennial data on blocks to block groups
ga_bgs_shape_w_demo[block_to_bgs_cols] = ga_blks_shape_w_demo[block_to_bgs_cols].groupby(assignment).sum()

## Disaggregate ACS data on blockgroups to blocks
weights = ga_blks_shape_w_demo.VAP / assignment.map(ga_bgs_shape_w_demo.VAP)
prorated = maup.prorate(assignment, ga_bgs_shape_w_demo[bgs_to_blocks_cols], weights)
ga_blks_shape_w_demo[bgs_to_blocks_cols] = prorated

ga_blks_shape_w_demo.to_file("shapes/GA_blocks/ga_blocks_2010_demo_18acs.shp")
ga_bgs_shape_w_demo.to_file("shapes/GA_bgs/ga_bgs_2010_demo_18acs.shp")