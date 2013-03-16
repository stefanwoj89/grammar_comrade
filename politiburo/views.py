from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulSoup
from django.conf import settings
import urllib2, ATD

def index(request):
	url = 'http://www.economist.com/news/united-states/21573165-years-republican-candidates-sound-awful-lot-last-years-same-again-please?fsrc=rss|ust'
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	return render_to_response('home/index.html', {})


def get_atd_response(text):
    ATD.setDefaultKey(settings.ATD_API_KEY)
    errors = ATD.checkDocument(text)
    for error in errors:
            print "%s error for: %s **%s**" % (error.type, error.precontext, error.string)
            print "some suggestions: %s" % (", ".join(error.suggestions),)
