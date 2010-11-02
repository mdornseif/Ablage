#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import config

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.runtime import DeadlineExceededError
import ablage
from ablage.models import *
import huTools.hujson as json
from gaetk.handler import BasicHandler


class MainHandler(webapp.RequestHandler):
    def get(self):
        try:
            ablage.convert()
        except DeadlineExceededError:
            self.response.out.write('spaeter mehr')
            return
        self.response.out.write('Hello world!')


class PdfHandler(webapp.RequestHandler):
    def get(self, tenant, akte_id, doc_id):
        dfile = DokumentFile.get_by_key_name(doc_id)
        if dfile.akte.key().name() != akte_id:
            logging.info(document.akte.key().name())
            raise RuntimeError('404')
        if dfile.tenant != tenant:
            raise RuntimeError('404')
        self.response.headers['Content-Type'] = 'application/pdf'
        self.response.out.write(dfile.data)


class DocumentHandler(webapp.RequestHandler):
    def get(self, tenant, akte_id, doc_id):
        document = Dokument.get_by_key_name(doc_id)
        if document.akte.key().name() != akte_id:
            logging.info(document.akte.key().name())
            raise RuntimeError('404')
        if document.tenant != tenant:
            raise RuntimeError('404')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(dict(document=document.as_dict())))


class AkteHandler(webapp.RequestHandler):
    def get(self, tenant, akte_id):
        akte = Akte.get_by_key_name(akte_id)
        if akte.tenant != tenant:
            raise RuntimeError('404')
        documents = Dokument.all().filter('akte =', akte).fetch(50)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(dict(akte=akte, documents=documents)))


class AktenHandler(BasicHandler):
    def get(self, tenant):
        tenant = 'CYLGI'
        query = Akte.all().filter('tenant =', tenant).order('-created_at')
        self.response.headers['Content-Type'] = 'application/json'
        
        ret = self.paginate(query, datanodename='akten')
        ret['akten'] = [akte.as_dict(self.abs_url) for akte in ret['akten']]
        self.response.out.write(json.dumps(ret))


def main():
    application = webapp.WSGIApplication(
    [
     ('/(\w+)/akten/(\w+)/pdf/(\w+)', PdfHandler),
     ('/(\w+)/akten/(\w+)/docs/(\w+)', DocumentHandler),
     ('/(\w+)/akten/(\w+)', AkteHandler),
     ('/(\w+)/akten', AktenHandler),
     ('/', MainHandler),
    ],
    debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
