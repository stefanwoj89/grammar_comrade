from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
import urllib2, ATD, codecs, re, json
from politiburo.models import *
import httplib, ssl, urllib2, socket
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)

class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))

def run_scorer():
    f = open('wootles','a')
    f.write( "run_scorer ran")
    f.close()

def run_scraper():
    print "run_scraper ran"

def parse_string(el):
   text = ''.join(el.findAll(text=True))
   return text.strip()


def processArticle(string):
    print string
    try:
        site = Site.objects.get(id=24)
        try:
            author = Author.objects.get(id=16)
            article = Article.objects.create(content=string, site=site, author=author)
            article.save()
            print article.id
        except Author.DoesNotExist:
            author = Author.objects.create()
            author.save()
            processArticle(string)
    except Site.DoesNotExist:
        site = Site.objects.create()
        site.save()
        processArticle(string)


def process_html(text):
	string = ''
	for row in text:
		new_row = row('p')
        for i in new_row:
			if new_row.index(i) != 0:
				string+=str(i)
	processArticle(string)

def createNewArticle():
    #url = 'http://www.economist.com/news/united-states/21573165-years-republican-candidates-sound-awful-lot-last-years-same-again-please?fsrc=rss|ust'
    #url = 'http://www.theatlantic.com/technology/print/2013/03/a-lizard-robot-to-delight-you-and-or-haunt-your-dreams/274263/'
    url = 'http://www.economist.com/blogs/schumpeter/2013/03/bail-out-cyprus-0'
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    rows = soup('article')
    for g in rows:
        print g('p')
        #print g.find('div', { 'class' : 'article-content'})
    #print new_rows
    #print rows
    results = process_html(new_rows)

def findArticle():
    try:
        article = Article.objects.get(id=10)
        content = article.content.replace('<p>', '').replace('</p>', '').encode('utf-8')
        #santized_content = generate_article_score(content)
        insert_article_score(article, content)
    except Article.DoesNotExist:
        createNewArticle()

def index(request):
    createNewArticle()
    #findArticle()
    return HttpResponse(json.dumps({ 'complete': True }), mimetype="application/json")
    #return render_to_response('home/index.html', {})

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

def insert_article_score(article, santized_content):
    try:
        stat_dict = generate_article_score(santized_content)
        print stat_dict
        percent_numerator = stat_dict['word_count'] - stat_dict['error_count']
        percent_score = float(percent_numerator)/float(stat_dict['word_count'])
        article.score = percent_score * 100
        article.grammar_error_count = stat_dict['grammar_error_count']
        article.spell_error_count = stat_dict['spell_error_count']
        article.style_error_count = stat_dict['style_error_count']
        article.word_count = stat_dict['word_count']
        #article.save()
    except ZeroDivisionError:
        print  "Word count was apparently 0, oops."

