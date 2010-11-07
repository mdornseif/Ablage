#!/usr/bin/env python
# encoding: utf-8
"""
config.py - general configuration for Ablage

Created by Maximillian Dornseif on 2010-11-01.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config
config.imported = True

from google.appengine.ext.webapp import util
from gaetk import webapp2
from ablage.views import MainHandler, PdfHandler, DokumentHandler, DokumenteHandler
from ablage.views import AkteHandler, AktenHandler, SearchHandler, UploadHandler


def main():
    application = webapp2.WSGIApplication(
    [
     ('/(\w+)/akten/(\w+)/pdf/(\w+)\.pdf', PdfHandler),
     ('/(\w+)/akten/(\w+)/docs/(\w+)[./]?(json)?', DokumentHandler),
     ('/(\w+)/akten/(\w+)/docs.json', DokumenteHandler),
     ('/(\w+)/akten/(\w+)[./]?(html|json)?', AkteHandler),
     ('/(\w+)/akten[./]?(html|json)?', AktenHandler),
     ('/(\w+)/docs', UploadHandler),
     ('/(\w+)/search', SearchHandler),
     ('/', MainHandler),
    ],
    debug=True)
    application.run()


if __name__ == '__main__':
    main()
