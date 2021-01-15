# Data Prep Documentation
## JN Matthews - 15.1.2021

### Sources:
* ACS Special Tabulation: https://www.census.gov/programs-surveys/decennial-census/about/voting-rights/cvap.2018.html
* TIGER/Line Shapefiles: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
* 2010 Decennial Census Data from the Census API


### Files:
* `filter_cvap_data_ga.py`: trims the nation wide BlockGroup csv from the ACS special tab to just the state of Georgia
* `decennial_scraper.py`: Defines functions used to pull 2010 decennial data down using the Census API
* `ga_acs_bg_data.py`: Cleans Georgia ACS data (outputted from `filter_cvap_data_ga.py`) and merges it with block group shapefile
* `ga_block_data.py`: Collects block level data from the Census API, and cleans up the downloaded columns/tables; merges with block shape file; Uses maup to aggregate decennial block data to block group file and disaggregate ACS citizenship data from block groups to blocks and save results;

### Notes on Election Data and 2020 Precinct shapefiles:

Michigan and Wisconsin both have State run GIS Portal with Precincts/Wards for 2020.

#### General:
* Open Elections (https://github.com/openelections) has 2020 data posted for GA, MI, AZ, NV, and some data fro WI.
* Open Elections Clarity site scraper (GA uses this company for election results posting): https://github.com/openelections/clarify

#### Arizona
* Maricopa County publishes voting precinct shapefiles: https://recorder.maricopa.gov/electionmaps/
* We have a 2018 precinct shapefile, not sure how well it maps to 2020.
* SOS Election Results: https://azsos.gov/elections

#### Georgia
* GA SOS Election Results: https://sos.ga.gov/index.php/Elections/current_and_past_elections_results
* We have a 2018 precinct shapefile (https://web.archive.org/web/20201206182139/http://www.legis.ga.gov/Joint/reapportionment/en-US/default.aspx), not sure how well it maps to 2020.

#### Michigan
* Michigan Open GIS Data: https://gis-michigan.opendata.arcgis.com
* 2020 Voting Precincts: https://gis-michigan.opendata.arcgis.com/datasets/2020-voting-precincts?geometry=-101.989%2C40.989%2C-70.349%2C46.537

#### Nevada
* Precinct level 2020 results from SOS: https://www.nvsos.gov/sos/elections/election-information/precinct-level-results

#### Wisconsin
* WI Election Results: https://elections.wi.gov/elections-voting/results
* Wisconsin GIS Portal: https://data-ltsb.opendata.arcgis.com
* 2012-20 election data on 2017 wards?: https://geodata.wisc.edu/catalog/145055E1-87EF-4D13-B138-4DC3907F3677
* 2020 Municipal Wards: https://data-ltsb.opendata.arcgis.com/datasets/wi-municipal-wards-january-2020