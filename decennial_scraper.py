import pandas as pd
import requests
import numpy as np
from tqdm import tqdm

variables = [
    # pop
    "P005001", "P005003", "P005004", "P005005", "P005006", "P005007", "P005008", "P005009", "P005010",
    "P005011", "P005012", "P005013", "P005014", "P005015", "P005016", "P005017",
    # vap
    "P011001", "P011002", "P011005", "P011006",  "P011007", "P011008", "P011009", "P011010", "P011011",
]

keys = [
    # pop
    "TOTPOP", "NH_WHITE", "NH_BLACK", "NH_AMIN ", "NH_ASIAN", "NH_NHPI", "NH_OTHER", "NH_2MORE",
    "HISP", "H_WHITE", "H_BLACK", "H_AMIN", "H_ASIAN", "H_NHPI", "H_OTHER", "H_2MORE",
    # vap
    "VAP", "HVAP", "WVAP", "BVAP", "AMINVAP", "ASIANVAP", "NHPIVAP", "OTHERVAP", "2MOREVAP",
]

def counties(state_fips):
    resp = requests.get(
        "https://api.census.gov/data/2010/dec/sf1"
        "?get=NAME&for=county:*&in=state:{}".format(state_fips)
    )
    header, *rows = resp.json()
    county_column_index = header.index("county")
    county_fips_codes = set(row[county_column_index] for row in rows)
    return county_fips_codes

def block_data_for_county(state_fips, county_fips, variables, keys):
    num_col_chunks = int(np.ceil(len(variables) / 50))
    chunks = [variables[i::num_col_chunks] for i in range(num_col_chunks)]
    variable_lookup = dict(zip(variables, keys))
    data = pd.DataFrame()
    for chunk in chunks:
        url = (
            "https://api.census.gov/data/2010/dec/sf1"
            + "?get={}&for=block:*".format(",".join(chunk))
            + "&in=state:{}&in=county:{}&in=tract:*".format(state_fips, county_fips)
        )
        # print(url)
        resp = requests.get(url)
        header, *rows = resp.json()
        columns = [variable_lookup.get(column_name, column_name) for column_name in header]

        dtypes = {key: int for key in columns}
        dtypes.update({key: str for key in ["state", "county", "tract", "block"]})
        df = pd.DataFrame.from_records(rows, columns=columns).astype(dtypes)
        if data.empty: 
            data = df
        else:
            data = pd.merge(data, df, on=["state", "county", "tract", "block"])

    data["geoid"] = data["state"] + data["county"] + data["tract"] + data["block"]
    return data

def tract_data_for_county(state_fips, county_fips, variables=variables, keys=keys):
    num_col_chunks = int(np.ceil(len(variables) / 50))
    chunks = [variables[i::num_col_chunks] for i in range(num_col_chunks)]
    variable_lookup = dict(zip(variables, keys))
    data = pd.DataFrame()
    for chunk in chunks:
        url = (
            "https://api.census.gov/data/2010/dec/sf1"
            + "?get={}&for=tract:*".format(",".join(chunk))
            + "&in=state:{}&in=county:{}".format(state_fips, county_fips)
        )
        # print(url)
        resp = requests.get(url)
        header, *rows = resp.json()
        columns = [variable_lookup.get(column_name, column_name) for column_name in header]

        dtypes = {key: int for key in chunk}
        dtypes.update({key: str for key in ["state", "county", "tract"]})
        df = pd.DataFrame.from_records(rows, columns=columns).astype(dtypes)
        if data.empty: 
            data = df
        else:
            data = pd.merge(data, df, on=["state", "county", "tract"])

    data["geoid"] = data["state"] + data["county"] + data["tract"]
    return data

def block_data_for_state(state_fips, variables=variables, keys=keys):
    county_fips_codes = counties(state_fips)
    return pd.concat(
        [
            block_data_for_county(state_fips, county_fips, variables, keys)
            for county_fips in tqdm(county_fips_codes)
        ]
    )