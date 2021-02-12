# Notes on Precinct Merging

## Notes by County

### Barrow
* Matched by number.  Polling places seem to have been merged due to covid?
* merged matched by map in refs

### Bartow
* Hamilton Crossing appears to be a new precinct, doesn't appear in map from county, though is listed on their polling locations.  might use polling location address to merge with another precinct?
* merged with Cassville, based on location of polling place? Looks like Hamilton crossing used
    to be called Beaver's Drive in 2014 map, and that shape is merged with Cassville in our shapefile.

### Camden 
* [County website](https://www.camdencountyga.gov/1043/Voting-Precinct-Locations) specifies name change. 

### Candler
* Precincts appear to have been consolidated base on this [article](http://www.metteradvertiser.com/article_0e8e520e-0922-11e5-acc0-b3d8fd2dfe9f.html)

### Chatham
* Match by precinct number and name, fall back on number if polling place changed.
* New Precincts:
    * CHATHAM, 7-16C POOLER RECREATION CENTER GYMNASIUM: split from 7-12 Pooler Church. 
    * CHATHAM, 8-16C ROYAL CINEMAS AND IMAX: Split from 7-07 ROTHWELL BAPT CH.  
* Cross reference [County GIS data](https://data-sagis.opendata.arcgis.com/datasets/voting-precincts/data?geometry=-81.688%2C31.968%2C-80.534%2C32.172&orderBy=PRECODE&orderByAsc=false&page=3) with 2018 shapes.

### Chattooga
* Cloundland + Teloga merged to Cloundland/Teloga

### Clayton
    * Ellenwood 1 + 2 merged to Ellenwood
* Jonesboro 19 appears to have been split from JB1 and JB17 based on meeting notes (14.7) (Merge all 3 in shapefile?)
* Lovejoy 3 appears to have been split into LJ3, 6, and 7. (See meeting notes in ref folder, 14.7 and 18.8)
* MO10 split from MO5 (meeting notes 14.7)
* MO11 split from MO3 (meeting notes 14.7)
* OAK5 split form OAK3 (meeting notes 14.7)

### Cobb
* Many merges.  See county change records in ref folder

### Columbia
* Reconcile with county change records in ref folder, and between 2016 list there with list
    on [current website](https://www.columbiacountyga.gov/county/voting-and-results/polling-locations).
* Harlem Branch Library split to create Harlem Sr Cntr and Mt. Moriah Bpt Chr
* Blanchard Park and MTZ Col Fire Dept. 4 merged to Blanchard Park

### Cowetta 
* Arts Centre and Jefferson Parkway were merged to create Newnan Centre.  Cross reference shapes in [County GIS](https://cowetamaps.maps.arcgis.com/apps/PanelsLegend/index.html?appid=3586b99a029247d69f69816da79813ac) with 2018 shapes.

### DeKalb
* Cross reference shapes with [County GIS interactive map](https://dekalbgis.maps.arcgis.com/apps/webappviewer/index.html?id=4135bd1868654e3b84aca982395712d8)
* DEKALB, EPWORTH renamed Candler Park
* DEKALB, CLARKSTON COMMUNITY CENTER split from CLARKSTON, the bit of Shaw-Robert Shaw Elem that was split appears to be mostly commercial and not residential
* DEKALB, DECATUR was split form Oakhurst
* DEKALB, KING-ML KING JR HIGH was renamed Snapfinger Rd.
* Dekalb renfroe middle merged with oakhurst

### Douglas
* DOUGLAS, COLONIAL HILLS renamed DOUGLAS, ATLANTA WEST PENTECOSTAL
* see [map on county website](https://www.celebratedouglascounty.com/DocumentCenter/View/1293/Map-of-Commission-District-2-PDF) and that records numbers and [list of numbers with current names](https://www.celebratedouglascounty.com/BusinessDirectoryII.aspx?lngBusinessCategoryID=22).


### Forsyth
* Cross reference shapes with [2020 precinct map on website](https://www.forsythco.com/Portals/0/Documents/Voter/Maps/Precincts_2020_010320.pdf).
* Some of the lines changed a lot, so did best to map to new shapes using vap on blockgroups as reference

### Fulton
* Cross reference shapes with[ county GIS viewer](https://gismaps.fultoncountyga.gov/portalpub/apps/webappviewer/index.html?id=c9290d15d93148eab7412de12ba45629).
* Resolve splits and merges by shape

### Glynn
* Cross reference [2020 County maps](https://www.glynncounty.org/1077/Voting-Precincts), with shapes, also match by precinct number
* GLYNN, BURROUGHS renamed Urbana Perry Parks
* GLYNN, OGLETHORPE POINT renamed GLYNN, HAMPTON RIVER
* GLYNN, MARSHES OF GLYNN renamed GLYNN, BROOKMAN

### Lee
* [County Website](http://www.lee.ga.us/residents/electionlocations.html), list sovereign grace as precinct 8.  this [article](https://www.walb.com/2020/10/26/lee-co-voting-precinct-gets-location-change/) discussing it moving to flint reformed baptist.

### Lowndes
* Trinity split to create Northgate Assembly
* Jaycee split to create Mt. Calvary
* Used [polling location address](https://www.lowndescounty.com/222/Polling-Locations) to assign other extra precincts
* [article about splits](https://www.valdostadailytimes.com/news/local_news/lowndes-adds-two-voting-precincts-for-november/article_36adc875-18e6-53fe-8dc0-1cf1a0ed85ba.html)

### Muscogee
* [2020 County map](https://ccg.maps.arcgis.com/apps/webappviewer/index.html?id=49b1b11294c74854b520a0fe1740801c)
* Cross refrence by name and shape
* MUSCOGEE, FORT/WADDELL renamed Canaan
* MUSCOGEE, ROTHSCHILD renamed Holsey/Buena-Vista

### Oconee
* Cross reference number and shape with [county map](https://www.oconeecounty.com/DocumentCenter/View/10827/Oconee-County-Voting-Precincts-and-Polling-Locations?bidId=) and [county list](https://www.oconeecounty.com/DocumentCenter/View/8957/Oconee-County-Precinct-List)
* OCONEE, ATHENS ACADEMY renamed E. Oconee
* OCONEE, MALCOM BRIDGE renamed Marshwood Hall

### Paulding
* Scrambled mess of a bunch of splits.  Did my best to map new to old using this [county's map](https://www.paulding.gov/DocumentCenter/View/9963/WEBPOLLINGLOCATIONS-FOR-WEB?bidId=)

### Randolph
* [News article](https://www.walb.com/2019/07/11/randolph-elections-board-votes-consolidate-precincts/)
* Carnegie merged with Cuthburt Courthouse
* 4th district and fountain bridge merged with shellman

### Sumter
* Matched by precinct number using county [website list](https://www.sumtercountyga.us/DocumentCenter/View/1354/SUMTER-COUNTY-PRECINCTS?bidId=)
* SUMTER, 28 CHAMBLISS renamed Browns Mill

### Thomas
* Match by location of polling place and only one remaining
* Ellabelle -> Little Ochlocknee baptist church

### Towns
* No documentation on county website.
* Other precincts didn't change names and tate city only borders macedonia. (merged?)

## To merge in shapefile
* Barrow
    * 03 + 12 -> 03
    * 02 + 15 -> 02
    * 04 + 14 -> 04
    * 06 + 10 + 13 -> 13
    * 11 + 16 -> 16
    * 05 + 07 -> 05
    * 08 + 09 -> 08
* Chandler
    * (CANDLER, CANDLER - 1736 + CANDLER, METTER - 1685) -> CANDLER, JACK STRICKLAND COMM CENTER
* Clayton:
    * (CLAYTON, JONESBORO 1 + CLAYTON, JONESBORO 17) -> CLAYTON, JONESBORO 1-17-19
* Columbia
    * Blanchard Park + MTZ Fire 4 -> Blanchard Park
* Coweta
    * (COWETA, ARTS CENTRE + COWETA, JEFFERSON PARKWAY) -> COWETA, NEWNAN CENTRE
* Oconee
    * (OCONEE, ANNEX + OCONEE, CITY HALL) -> OCONEE, CITY HALL
* Fulton
    * (FULTON, ML021 + FULTON, ML022) -> FULTON, ML02A
    * (FULTON, ML023 + FULTON, ML024) -> FULTON, ML02B
    * (FULTON, ML04A + FULTON, ML04B + FULTON, ML04C) -> FULTON, ML04
    * (FULTON, ML05A + FULTON, ML05B + FULTON, ML05C) -> FULTON, ML05



## Missing From shapefile
* BARTOW, HAMILTON CROSSING -> CASSVILLE
* CHATHAM, 1-14C COMPASSION CHRISTIAN CHURCH
* CHATHAM, 3-02C TEMPLE MICKVE ISRAEL
* CHATHAM, 5-07C STATION 1
* CHATHAM, 5-10C TATUMVILLE COMMUNITY CENTER
* CHATHAM, 6-08C CHRIST MEMORIAL BAPTIST CHURCH
* CHATHAM, 6-10C STATION 3
* CHATHAM, 7-16C POOLER RECREATION CENTER GYMNASIUM
* CHATHAM, 8-16C ROYAL CINEMAS AND IMAX
* CLAYTON, JONESBORO 19
* CLAYTON, LOVEJOY 6
* CLAYTON, LOVEJOY 7
* CLAYTON, MORROW 10
* CLAYTON, MORROW 11
* CLAYTON, OAK 5
* COLUMBIA, HARLEM SENIOR CENTER
* COLUMBIA, SECOND MT MORIAH BAPTIST CHURCH
* COWETA, NEWNAN CENTRE
* DEKALB, CANDLER PARK
* DEKALB, CLARKSTON COMMUNITY CENTER
* DEKALB, DECATUR
* DEKALB, SNAPFINGER ROAD
* DOUGLAS, ATLANTA WEST PENTECOSTAL
* FORSYTH, 34 FOWLER
* FORSYTH, 35 JOHNS CREEK
* FORSYTH, 36 NICHOLS
* FORSYTH, 37 SAWNEE
* FULTON, 01I
* FULTON, EP04C
* FULTON, FA01D
* FULTON, FC01
* FULTON, FC02
* FULTON, FC03
* FULTON, JC04C
* FULTON, ML01A
* FULTON, ML02A
* FULTON, ML02B
* FULTON, ML04
* FULTON, ML05
* FULTON, ML07B
* FULTON, SC07D
* FULTON, UC02C
* FULTON, 02A1 -> 02A
* FULTON, 02L1A -> 02L1
* FULTON, 06D1 -> 06D
* FULTON, 06D2 -> 06D
* FULTON, 09K1 -> 09K
* FULTON, 11B1 -> 11B
* FULTON, 11M1 -> 11M
* FULTON, 12A1 -> 12A
* FULTON, JC01A -> JC01
* FULTON, ML03A -> ML03
* FULTON, RW09A -> RW09
* FULTON, RW12A -> RW12
* FULTON, SC15A -> SC15
* GLYNN, BROOKMAN
* GLYNN, HAMPTON RIVER
* GLYNN, URBANA-PERRY PARKS
* JENKINS, PRIMARY SCHOOL
* JENKINS, SENIOR CITIZENS CENTER
* LEE, FLINT REFORMED BAPTIST
* LOWNDES, HAHIRA TRAIN DEPOT
* LOWNDES, JAYCEE SHACK
* LOWNDES, MT CALVARY
* LOWNDES, NORTHGATE ASSEMBLY
* LOWNDES, VSU UC # 2
* MUSCOGEE, CANAAN
* MUSCOGEE, HOLSEY/BUENA VISTA
* OCONEE, EAST OCONEE
* OCONEE, MARSWOOD HALL
* PAULDING, BEULAHLAND BAPTIST CHURCH
* PAULDING, CROSSROADS LIBRARY
* PAULDING, D WRIGHT INNOVATION CTR
* PAULDING, DOBBINS MIDDLE SCHOOL
* PAULDING, EVENTS PLACE
* PAULDING, LEGACY BAPT CHURCH
* PAULDING, MULBERRY ROCK PARK
* PAULDING, PAULDING COUNTY AIRPORT
* PAULDING, PAULDING SR CENTER
* PAULDING, PICKETTS MILL BAPTIST CHURCH
* PAULDING, POPLAR SPRGS BAPT CHURCH
* PAULDING, RUSSOM ELEMENTARY
* PAULDING, SHELTON ELEMENTARY
* PAULDING, WATSON GOVT CMPLX
* PAULDING, WHITE OAK PARK
* SUMTER, BROWNS MILL
* THOMAS, LITTLE OCHLOCKNEE BAPTIST CHURCH