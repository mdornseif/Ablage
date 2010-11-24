#!/usr/bin/env python
# encoding: utf-8
"""
config.py - general configuration for Ablage

Created by Maximillian Dornseif on 2010-11-01.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config
config.imported = True

from gaetk import webapp2
from ablage.views import CredentialsHandler, MainHandler, PdfHandler, DokumentHandler, DokumenteHandler
from ablage.views import AkteHandler, AktenHandler, SearchHandler, UploadHandler


def main():
    application = webapp2.WSGIApplication(
    [
     ('/([a-z.-]+)/akten/(\w+)/pdf/(\w+)\.pdf', PdfHandler),
     ('/([a-z.-]+)/akten/(\w+)/docs/(\w+)[./]?(json)?', DokumentHandler),
     ('/([a-z.-]+)/akten/(\w+)/docs.json', DokumenteHandler),
     ('/([a-z.-]+)/akten/(\w+)[./]?(html|json)?', AkteHandler),
     ('/([a-z.-]+)/akten[./]?(html|json)?', AktenHandler),
     ('/([a-z.-]+)/docs', UploadHandler),
     ('/([a-z.-]+)/search', SearchHandler),
     ('/credentials', CredentialsHandler),
     ('/', MainHandler),
    ],
    debug=True)
    application.run()


if __name__ == '__main__':
    main()
