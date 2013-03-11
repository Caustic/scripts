import urllib2
import re
from BeautifulSoup import BeautifulSoup
import json
import codecs, locale, sys

googleapi = "http://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&sensor=false"
soup = BeautifulSoup(urllib2.urlopen('http://sfbay.craigslist.org/search/apa/nby?zoomToPosting=&altView=&query=&srchType=A&minAsk=&maxAsk=&bedrooms=&nh=99&nh=117&nh=103&nh=105'))
concurrent = 10

results = []
while(soup('h4', {'class':'ban'})[0]('span', {'style':'float: right;'})[0]('a')):
    for l in soup('p', {'class':'row'}):
        record = {}
        rent_bed_sqft = l('span', {'class': 'itemph'})[0].text
        record['rent'] = re.sub('/.*', '', re.sub('^\$', '', rent_bed_sqft)) if '$' in rent_bed_sqft else ''
        record['bed'] = re.sub('br.*', '', re.sub('^.*/ ', '', rent_bed_sqft)) if 'br' in rent_bed_sqft else ''
        record['sqft'] = re.sub('ft&.*', '', re.sub('.*(- |/ )', '', rent_bed_sqft)) if 'ft' in rent_bed_sqft else ''
        record['post_date'] = l('span', {'class': 'itemdate'})[0].text
        record['neighborhood'] = l('span', {'class': 'itempn'})[0].text
        record['title'] = l('a')[0].text
        record['link'] = l('a')[0].get('href')
        record['latitude'] = l.get('data-latitude')
        record['longitude'] = l.get('data-longitude')
        results.append(record)
    parsedurl = soup('h4', {'class':'ban'})[0]('span', {'style':'float: right;'})[0]('a')[0].get('href')
    soup = BeautifulSoup(urllib2.urlopen(parsedurl))

print "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format('rent', 'bed', 'sqft', 'post_date', 'neighborhood', 'address', 'title', 'link', 'latitude', 'longitude')
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
for x in results:
    if x.get('latitude', '0') != '0':
        page = urllib2.urlopen(googleapi.format(x.get('latitude'), x.get('longitude')))
        res = json.loads(page.read())
        try:
            x['address'] = res.get('results')[0].get('formatted_address', '')
        except:
            x['address'] = ''
    else:
        x['address'] = 'N/A'

    try:
        x['title'] = unicode(x.get('title', ''))
    except UnicodeEncodeError:
        x['title'] = unicode(x.get('title', ''), 'utf-8')

    print u"{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
        x.get('rent',''),
        x.get('bed',''),
        x.get('sqft',''),
        x.get('post_date',''),
        x.get('neighborhood',''),
        x.get('address',''),
        x.get('title',''),
        x.get('link',''),
        x.get('latitude',''),
        x.get('longitude',''))

