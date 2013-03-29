from django.shortcuts import render_to_response
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
import urllib2, ATD, codecs, re, json
from politiburo.models import *
import httplib, ssl, urllib2, socket
from politiburo.forms import *
from django.template import RequestContext
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from math import sqrt
from urlparse import urlparse


def index(request):
    return render_to_response('home/index.html', {})

def viewSite(request, site_id):
    site = Site.objects.get(pk=site_id)
    reviews = None

    return render_to_response('site.html', {'site': site, 'reviews': reviews })

def viewArticle(request, article_id):
    article = Article.objects.get(pk=article_id)
    reviews = Review.objects.filter(article=article).all()
    sessionid = request.session._session_key
    sess = Session.objects.get(session_key=sessionid)
    uid = sess.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    #TODO if none, don't allow user to post, or allow anonymous
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = Review()
            review.user = user
            review.article = article
            review.comment = review_form.cleaned_data['comment']
            review.score = review_form.cleaned_data['score']
            review.save()
            return HttpResponseRedirect('/')
    else:
        review_form = ReviewForm()
    return render_to_response('article.html', {'article':article, 'reviews':review_sort(reviews), 'review_form': review_form},context_instance=RequestContext(request))

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


def review_sort(reviews):
    sorted_reviews = []
    for r in reviews:
        score = confidence(r.upvote_count,0)
        tup = (r,score)
        sorted_reviews.append(tup)
    return_list = sorted(sorted_reviews, key=itemgetter(1), reverse=True)
    return return_list

def _confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.0 #1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n
    return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)
def calculate_average_site_score(articles):
    cumlative_score = 0
    total_articles = len(articles)
    for article in articles: cumlative_score+=article.score
    try:
        average_score = float(cumlative_score)/float(total_articles)
    except ZeroDivisionError:
        average_score = 0
    return average_score

def list(request):
    sites = Site.objects.all()
    data = { 'sites': [] }

    for site in sites:
        site_meta_data = {
            'id': site.id,
            'average_score': calculate_average_site_score(Article.objects.filter(site=site))
        }
        data['sites'].append(site_meta_data)
    data['sites'] = sorted(data['sites'], key=lambda k: k['average_score'], reverse=True)
    return render_to_response('home/list.html', {
        'sites': data['sites']
    })

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
        article.save()
    except ZeroDivisionError:
        print  "Word count was apparently 0, oops."



################### LOGIN VIEWS #####################

def login(request):
    get_url_list()
    return render_to_response('login/login.html', {
        'login': True,
    })

#################### Pull List, Insert DB #############



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
    return sites_content

def insert_site_content(site, sites_content):
    site = Site.objects.get(id=6)
    return True


