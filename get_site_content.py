
import grequests, urllib2

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
#from politiburo.models import *
from urlparse import urlparse



def get_url_list():
    url_list = {
        'Name': 'The Economist',
        'urls': []
    }

    url = 'http://www.economist.com/feeds/print-sections/77729/china.xml'
    xml = BeautifulStoneSoup(urllib2.urlopen(url).read())
    urls = xml('link')
    for greped_url in urls:
        clean_url = str(greped_url).replace('<link>', '').replace('</link>', '')
        url_obj = urlparse(clean_url)
        if url_obj.path:
            url_list['urls'].append(clean_url)
    return url_list

def get_site_content(url_list):
    sites_content = []

    reqs=grequests.map((grequests.get(u) for u in url_list['urls']))
    for r in reqs:
        print r.content
        print '###############################################'
        print '###############################################'
        print '###############################################'
        print '###############################################'
        print '###############################################'
        print '###############################################'
        print '###############################################'
    return sites_content

def insert_site_content(site, sites_content):
    #site = Site.objects.get(id=6)
    return True


print get_site_content(get_url_list())

print 'Complete.'
