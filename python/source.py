import re
import sys
import urllib2
import BeautifulSoup

usage = "Run the script: ./geolocate.py IPAddress"

# FIX: do we need to print usage?
if len(sys.argv)!=2:
    print(usage)
    sys.exit(0)

if len(sys.argv) > 1:
    ipaddr = sys.argv[1]

# REFACTOR: turn page read into function
geody = "http://www.geody.com/geoip.php?ip=" + ipaddr
html_page = urllib2.urlopen(geody).read()
soup = BeautifulSoup.BeautifulSoup(html_page)

# Filter paragraph containing geolocation info.
paragraph = soup('p')[3]

# DOCS: explain what the regular expression does
# Remove html tags using regex.
geo_txt = re.sub(r'<.*?>', '', str(paragraph))
print geo_txt[32:].strip()
