tileMapSystem:
a set of Python scripts that implements Bing maps tile system to automatically download
aerial imagery (maximum resolution available) given a lat/lon bounding box

Packages:
-mpmath
-urllib2
-json
-math
-argparse
-logging
-PIL
-time

Instruction:
cd pathTo/tileMapSystem
python main.py 'lat1,lon1,lat2,lon2' (bottom left corner, top right corner)

Example:
python main.py 16.7058,48.2663,16.71037,48.2668

Other:
- the aerial imagery will be saved in the same directory as the tileMapSystm
- the output file is named by the current time and date
- output file is in png format
- only 200 tiles can be downloaded from Bing Aerial Maps 