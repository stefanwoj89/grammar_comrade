from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.db import transaction
import urllib2, ATD
from politiburo.models import *


def parse_string(el):
   text = ''.join(el.findAll(text=True))
   return text.strip()

def processArticle(string):
    try:
        site = Site.objects.get(id=1)
        try:
            author = Author.objects.get(id=1)
            article = Article.objects.create(content=string, site=site, author=author)
            article.save()
            print article
        except Author.DoesNotExist:
            author = Author.objects.create()
            author.save()
    except Site.DoesNotExist:
        site = Site.objects.create()
        site.save()


def process_html(text):
	string = ''
	for row in text:
		new_row = row('p')
        for i in new_row:
            #data = map(parse_string, i.findAll('<p>'))
            #data = data[1:]
            #print data
			if new_row.index(i) != 0:
				string+=str(i)
	processArticle(string)

def createNewArticle():
    url = 'http://www.economist.com/news/united-states/21573165-years-republican-candidates-sound-awful-lot-last-years-same-again-please?fsrc=rss|ust'
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    rows = soup('article')
    results = process_html(rows)

def findArticle():
    article = Article.objects.get(id=2)
    print article.content

def index(request):
    #createNewArticle()
    findArticle()
    return render_to_response('home/index.html', {})

def generate_article_score(content):
    ATD.setDefaultKey(settings.ATD_API_KEY)
    metrics = ATD.stats(content)
    error_types = ['grammar','spell','style']
    error_count = 0
    word_count = 0
    grammar_error_count = 0
    spell_error_count = 0
    style_error_count = 0
    for m in metrics:
        if m.type in error_types:
            error_count+=m.value
        if m.type == error_types[0]:
            grammar_error_count+=m.value
        if m.type == error_types[1]:
            spell_error_count+=m.value
        if m.type == error_types[2]:
            style_error_count+=m.value
        if m.type == 'stats' and m.key == 'words':
            word_count = m.value
    return_dict = {
        'error_count':error_count,
        'word_count':word_count,
        'grammar_error_count': grammar_error_count,
        'spell_error_count': spell_error_count,
        'style_error_count': style_error_count,
    }
    return return_dict

def insert_article_score(article):
    try:
        stat_dict = generate_article_score(article.content)
        percent_numerator = stat_dict['word_count'] - stat_dict['error_count']
        percent_score = float(percent_numerator)/float(stat_dict['word_count'])
        article.score = percent_score * 100
        article.grammar_error_count = stat_dict['grammar_error_count']
        article.spell_error_count = stat_dict['spell_error_count']
        article.style_error_count = stat_dict['style_error_count']
        article.word_count = stat_dict['word_count']
    except ZeroDivisionError:
        print  "Word count was apparently 0, oops."

