# -*- coding: utf-8 -*-

"""URLs for testing %%PROJECTNAME%%."""

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
# authentication callbacks
(r'^callback_googleappsauth/', 'googleappsauth.views.callback')
# admin stuff
(r'^admin/doc/', include('django.contrib.admindocs.urls')),
(r'^admin/(.*)', 'admin.site.root'),
(r'^accounts/login/$', 'django.contrib.auth.views.login'),
(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
(r'^accounts/password_change/$', 'django.contrib.auth.views.password_change'),
(r'^accounts/password_change/done/$', 'django.contrib.auth.views.password_change_done'),
(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset'),
(r'^accounts/password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
# this is where login without source url goes
(r'^accounts/profile/', 'django.views.generic.simple.redirect_to', {'url' : '/'}),

# ensure requests to favicon don't clutter logs
(r'favicon.ico', 'django.views.generic.simple.redirect_to', {'url': 'http://s.hdimg.net/layout06/favicon.png'}),

# include %%PROJECTNAME%%
(r'^%%PROJECTNAME%%/', include('%%PROJECTNAME%%.urls')),
(r'^$', 'django.views.generic.simple.redirect_to', {'url' : '/%%MODULENAME%%/'}),
)

# when in development mode, serve static files 'by hand'
# in production the files should be placed at http://s.hdimg.net/%%MODULENAME%%/
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './media'}),
    )
