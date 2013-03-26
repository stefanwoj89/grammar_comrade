from django.conf.urls import patterns, include, url

import politiburo.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'politiburo.views.index', name='index'),
    #(r'^accounts/', include('registration.urls')),
    url(r'^list', 'politiburo.views.list', name='list'),
    url(r'', include('social_auth.urls')),
    url(r'^politiburo/site/(?P<site_id>\d+)/$', politiburo.views.viewSite, name='view_site'),
    url(r'^politiburo/article/(?P<article_id>\d+)/$', politiburo.views.viewArticle, name='view_article'),

    # url(r'^grammar_comrade/', include('grammar_comrade.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
