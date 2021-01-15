import geopandas as gpd
import pandas as pd
import pickle
from gerrychain import Graph, Partition
import matplotlib.pyplot as plt
import maup
import requests
from tqdm import tqdm
import numpy as np

ga_cvap_bgs = pd.read_csv("data/GA_cvap_2014_2018.csv")

race_names = {"Total": "TOT",
              "Not Hispanic or Latino": "NH",
              "American Indian or Alaska Native Alone": "NH_AMIN",
              "Asian Alone": "NH_ASIAN",
              "Black or African American Alone": "NH_BLACK",
              "Native Hawaiian or Other Pacific Islander Alone": "NH_NHPI",
              "White Alone": "NH_WHITE",
              "American Indian or Alaska Native and White": "NH_AMIN_WHITE",
              "Asian and White": "NH_ASIAN_WHITE",
              "Black or African American and White": "NH_BLACK_WHITE",
              "American Indian or Alaska Native and Black or African American": "NH_AMIN_BLACK",
              "Remainder of Two or More Race Responses": "NH_2MORE",
              "Hispanic or Latino": "HISP"}

ga_cvap_bgs.replace(to_replace=race_names, inplace=True)


ga_cvap_bgs = ga_cvap_bgs.groupby(["geoname", "lntitle", 
                                   "geoid"]).agg({'cit_est':'sum', 'cvap_est': "sum",}).reset_index()
ga_cvap_bgs = ga_cvap_bgs.pivot(index='geoid', columns='lntitle', values = ['cvap_est', 'cit_est'])
ga_cvap_bgs.rename(columns={"cvap_est": "CVAP", "cit_est": "CPOP"}, inplace=True)

ga_cvap_bgs.columns = ['_'.join(col).strip() for col in ga_cvap_bgs.columns.values]
ga_cvap_bgs = ga_cvap_bgs.rename(columns={"GEOID_": "GEOID"})

to_rename = {'CVAP_HISP': "HCVAP", 'CPOP_HISP': "HCPOP",
             'CVAP_NH': "NHCVAP", 'CPOP_NH': "NHCPOP",
             'CVAP_NH_2MORE': "2MORECVAP", 'CPOP_NH_2MORE': "2MORECPOP",
             'CVAP_NH_AMIN': "AMINCVAP", 'CPOP_NH_AMIN': "AMINCPOP",
             'CVAP_NH_ASIAN': "ASIANCVAP", 'CPOP_NH_ASIAN': "ASIANCPOP",
             'CVAP_NH_BLACK':'BCVAP', 'CPOP_NH_BLACK': "BCPOP",
             'CVAP_NH_NHPI': "NHPICVAP", 'CPOP_NH_NHPI': "NHPICPOP",
             'CVAP_NH_WHITE': "WCVAP",'CPOP_NH_WHITE': "WCPOP",
             'CVAP_TOT': "CVAP",'CPOP_TOT': "CPOP",
             "CVAP_NH_AMIN_WHITE": "WAMINCVAP", "CPOP_NH_AMIN_WHITE": "WAMINCPOP",
             "CVAP_NH_ASIAN_WHITE": "WASIANCVAP", "CPOP_NH_ASIAN_WHITE": "WASIANCPOP",
             "CVAP_NH_BLACK_WHITE": "BWCVAP", "CPOP_NH_BLACK_WHITE": "BWCPOP",
             "CVAP_NH_AMIN_BLACK": "BAMINCVAP", "CPOP_NH_AMIN_BLACK": "BAMINCPOP",}

ga_cvap_bgs = ga_cvap_bgs.rename(columns=to_rename)
ga_cvap_bgs.reset_index(inplace=True)
ga_cvap_bgs["GEOID"] = ga_cvap_bgs["geoid"].apply(lambda x: x[7:])

ga_cvap_bgs["AMINCVAP*"] = ga_cvap_bgs[["AMINCVAP", "BAMINCVAP", "WAMINCVAP"]].sum(axis=1)
ga_cvap_bgs['AMINCPOP*'] = ga_cvap_bgs[["AMINCPOP", "BAMINCPOP", "WAMINCPOP"]].sum(axis=1)

# Shapefiles come from TIGER/Line website:
# https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
ga_bgs_shapes = gpd.read_file("shapes/GA_bgs/tl_2012_13_bg.shp")

ga_bgs_shape_w_demo = pd.merge(left=ga_bgs_shapes, right=ga_cvap_bgs, 
                               left_on="GEOID", right_on="GEOID")

ga_bgs_shape_w_demo.to_file("shapes/GA_bgs/ga_bgs_2010_demo.shp")