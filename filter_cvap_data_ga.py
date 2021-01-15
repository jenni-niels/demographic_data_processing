import csv

## The nation wide file comes from the ACS special tab:
## https://www.census.gov/programs-surveys/decennial-census/about/voting-rights/cvap.2018.html

fin = open("../../ACS/CVAP_2014-2018_ACS_csv_files/BlockGr.csv", "r")
read = csv.reader(fin)
headers = next(read)

fout = open("data/GA_cvap_2014_2018.csv", "w")
write = csv.writer(fout)
write.writerow(headers)

for row in read:
    if "Georgia" in row[0]:
        write.writerow(row)