from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulSoup
from django.conf import settings
import urllib2, ATD
from politiburo.models import *

def process_html(text):
	string = ''
	for row in text:
		new_row = row('p')
		for i in new_row:
			if new_row.index(i) != 0:
				string+=str(i)
	print string

def index(request):
	url = 'http://www.economist.com/news/united-states/21573165-years-republican-candidates-sound-awful-lot-last-years-same-again-please?fsrc=rss|ust'
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	rows = soup('article')
	process_html(rows)

	return render_to_response('home/index.html', {})

def generate_article_score(content):
    ATD.setDefaultKey(settings.ATD_API_KEY)
    metrics = ATD.stats(content)
    error_count = 0
    error_types = ['grammar','spell','style']
    word_count = 0
    for m in metrics:
        if m.type in error_types:
            error_count+=m.value
        if m.type == 'stats' and m.key == 'words':
            word_count = m.value
    return error_count, word_count

def insert_article_score(article):
    #TODO: test for zero division and commiting changes to db
    error_count, word_count = generate_article_score(article.content)
    percent_numerator = word_count - error_count
    percent_score = float(percent_numerator)/float(word_count)
    article.score = percent_score * 100

def get_atd_response(text):
    ATD.setDefaultKey(settings.ATD_API_KEY)
    errors = ATD.checkDocument(text)
    for error in errors:
            print "%s error for: %s **%s**" % (error.type, error.precontext, error.string)
            print "some suggestions: %s" % (", ".join(error.suggestions),)
