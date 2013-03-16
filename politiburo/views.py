from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulSoup
import urllib2

def index(request):
	url = 'http://www.economist.com/news/united-states/21573165-years-republican-candidates-sound-awful-lot-last-years-same-again-please?fsrc=rss|ust'
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	return render_to_response('home/index.html', {})

