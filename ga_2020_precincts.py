import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from numpy.random import RandomState, uniform
import matplotlib.pyplot as plt
import maup

pres20cols = ["PRES20D", "PRES20R", "PRES20L"]

ga2018shapes = gpd.read_file("shapes/GA_precincts/GA_2018_precincts/GA_2018_precincts.shp")

pres20votes = pd.read_csv("data/ga_pres20_precinct_votes_precinct_matches.csv")

merged_votes = pres20votes.groupby("PREC_match").sum()[pres20cols].reset_index()


shapes_to_merge = {
                    # Barrow
                    "BARROW, 06 WINDER BARROW HIGH SCHOOL": "BARROW, 13 WINDER COMMUNITY CENTER",
                    "BARROW, 07 STATHAM ELEMENTARY SCHOOL": "BARROW, 05 FIRE STATION 1 (STATHAM)",
                    "BARROW, 09 LIONS CLUB": "BARROW, 08 FIRST BAPTIST CHURCH",
                    "BARROW, 10 LEISURE SERVICES CENTER": "BARROW, 13 WINDER COMMUNITY CENTER",
                    "BARROW, 11 APALACHEE HIGH SCHOOL": "BARROW, 16 THE CHURCH AT WINDER",
                    "BARROW, 12 MIDWAY UNITED METHODIST CHURCH": "BARROW, 03 BRAMLETT ELEMENTARY SCHOOL",
                    "BARROW, 14 CEDAR CREEK BAPTIST CHURCH": "BARROW, 04 WESTSIDE MIDDLE SCHOOL",
                    "BARROW, 15 COUNTY LINE ELEMENTARY SCHOOL": "BARROW, 02 BETHLEHEM CHURCH - 211",
                    # Candler
                    "CANDLER, CANDLER-1736": "CANDLER, JACK STRICKLAND COMM CENTER",
                    "CANDLER, METTER -1685": "CANDLER, JACK STRICKLAND COMM CENTER",
                    # Clayton
                    "CLAYTON, JONESBORO 1": "CLAYTON, JONESBORO 1-17-19",
                    "CLAYTON, JONESBORO 17": "CLAYTON, JONESBORO 1-17-19",
                    # Columbia
                    "COLUMBIA, MTZ COL FIRE DEPT #4": "COLUMBIA, BLANCHARD PARK",
                    # Coweta
                    "COWETA, ARTS CENTRE": "COWETA, NEWNAN CENTRE",
                    "COWETA, JEFFERSON PARKWAY": "COWETA, NEWNAN CENTRE",
                    # DeKalb
                    "DEKALB, RENFROE MIDDLE": "DEKALB, OAKHURST",
                    # Oconee
                    "OCONEE, ANNEX": "OCONEE, CITY HALL",
                    "OCONEE, CITY HALL": "OCONEE, CITY HALL",
                    # Fulton
                    "FULTON, ML012": "FULTON, ML01B",
                    "FULTON, ML021": "FULTON, ML02A",
                    "FULTON, ML022": "FULTON, ML02A",
                    "FULTON, ML023": "FULTON, ML02B",
                    "FULTON, ML024": "FULTON, ML02B",
                    "FULTON, ML04A": "FULTON, ML04",
                    "FULTON, ML04B": "FULTON, ML04",
                    "FULTON, ML04C": "FULTON, ML04",
                    "FULTON, ML05A": "FULTON, ML05",
                    "FULTON, ML05B": "FULTON, ML05",
                    "FULTON, ML05C": "FULTON, ML05",
                    "FULTON, ML071": "FULTON, ML072",
                    # Randolph
                    'RANDOLPH, 4TH DISTRICT': "RANDOLPH, SHELLMAN",
                    'RANDOLPH, CARNEGIE': "RANDOLPH, CUTHBERT/COURTHOUSE",
                    'RANDOLPH, FOUNTAIN BRIDGE-5TH': "RANDOLPH, SHELLMAN",
                    # Towns
                    'TOWNS, TATE CITY': "TOWNS, MACEDONIA",
                    # Troup
                  }

ga2018shapes["PREC_match"] = ga2018shapes.apply(lambda r: r.ID if r.PREC_y == None else shapes_to_merge[r.PREC_y] if r.PREC_y in shapes_to_merge.keys() else r.PREC_y, axis=1)
# ga2018shapes.loc[ga2018shapes.PREC_y.apply(lambda x: x in shapes_to_merge.keys())]


len(ga2018shapes["PREC_match"].unique())
len(merged_votes)

sum_cols = [
            # elects
            'AG18D','COA18D', 'COI18D', 'COL18D', 'GOV18D', 'LG18D', 'SOS18D', 'SSS18D',
            'USH18D', 'AG18L', 'COA18L', 'COI18L', 'COL18L', 'GOV18L', 'LG18L',
            'SOS18L', 'SSS18L', 'USH18L', 'AG18R', 'COA18R', 'COI18R', 'COL18R',
            'GOV18R', 'LG18R', 'SOS18R', 'SSS18R', 'USH18R',
            ## pop
            'TOTPOP', 'NH_WHITE', 'NH_BLACK', 'NH_AMIN',
            'NH_ASIAN', 'NH_NHPI', 'NH_OTHER', 'NH_2MORE', 'HISP', 'H_WHITE',
            'H_BLACK', 'H_AMIN', 'H_ASIAN', 'H_NHPI', 'H_OTHER', 'H_2MORE', 'VAP',
            'HVAP', 'WVAP', 'BVAP', 'AMINVAP', 'ASIANVAP', 'NHPIVAP', 'OTHERVAP',
            '2MOREVAP',
            # other
            "AREA"
           ]
col_aggs = {c: "sum" if c in sum_cols else "first" for c in ga2018shapes.columns if (c not in ["geometry", "PREC_match"])}

ga_to_merge = ga2018shapes.dissolve(by="PREC_match", aggfunc=col_aggs).reset_index()

ga_to_merge.plot()

# ga2018shapes[ga2018shapes.PREC_match.isna()].loc[1448].PREC_match == None

ga_precincts_2020 = pd.merge(left=ga_to_merge, right=merged_votes, on="PREC_match", how="left")

ga_precincts_2020.to_file("shapes/GA_precincts/GA_precincts_2020_votes.shp")

ga_blocks_demo = gpd.read_file("shapes/GA_blocks/ga_blocks_2010_demo_18acs.shp")

block_demo_cols = ["TOTPOP", "NH_WHITE", "NH_BLACK", "NH_AMIN", "NH_ASIAN", "NH_NHPI", "NH_OTHER", "NH_2MORE",
        "HISP", "H_WHITE", "H_BLACK", "H_AMIN", "H_ASIAN", "H_NHPI", "H_OTHER", "H_2MORE",
        "WHITE_ANY", "BLACK_ANY", "AMIN_ANY", "ASIAN_ANY", "NHPI_ANY", "OTHER_ANY",

        # vap
        "VAP", "HVAP", "WVAP", "BVAP", "AMINVAP", "ASIANVAP", "NHPIVAP", "OTHERVAP", "2MOREVAP",
        "AMINVAP*",
        
        #acs
        'HCVAP', 'NHCVAP', '2MORECVAP', 'AMINCVAP',
       'BAMINCVAP', 'WAMINCVAP', 'ASIANCVAP', 'WASIANCVAP', 'BCVAP', 'BWCVAP',
       'NHPICVAP', 'WCVAP', 'CVAP', 'HCPOP', 'NHCPOP', '2MORECPOP', 'AMINCPOP',
       'BAMINCPOP', 'WAMINCPOP', 'ASIANCPOP', 'WASIANCPOP', 'BCPOP', 'BWCPOP',
       'NHPICPOP', 'WCPOP', 'CPOP', 'AMINCVAP*', 'AMINCPOP*']

ga_blocks_demo = ga_blocks_demo.to_crs(ga_precincts_2020.crs)

assign = maup.assign(ga_blocks_demo, ga_precincts_2020)

ga_precincts_2020[block_demo_cols] = ga_blocks_demo[block_demo_cols].groupby(assign).sum()

ga_precincts_2020.to_file("shapes/GA_precincts/GA_2020_precincts/GA_2020_precincts.shp")

ga_precincts_2020[["PRES20D", "PRES20R", "PRES20L"]].sum()