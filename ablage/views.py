#!/usr/bin/env python
# encoding: utf-8
"""
ablage/views.py

Created by Maximillian Dornseif on 2010-11-04.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


import config
config.imported = True

from ablage.models import Akte, Dokument, DokumentFile
from gaetk.handler import BasicHandler
from google.appengine.ext import db
from huTools.calendar.formats import convert_to_date
import base64
import datetime
import hashlib
import huTools.hujson as json
import logging


class MainHandler(BasicHandler):
    def get(self):
        self.response.out.write('Hello world!')


class PdfHandler(BasicHandler):
    def get(self, tenant, akte_id, doc_id):
        logging.info(doc_id)
        dfile = DokumentFile.get_by_key_name(doc_id)
        if not dfile:
            raise RuntimeError('404')
        if dfile.akte and dfile.akte.key().name() != akte_id:
            raise RuntimeError('404')
        if dfile.tenant != tenant:
            raise RuntimeError('404')
        self.response.headers['Content-Type'] = 'application/pdf'
        self.response.out.write(dfile.data)


class DokumentHandler(BasicHandler):
    def get(self, tenant, akte_id, doc_id, format):
        document = Dokument.get_by_key_name(doc_id)
        if document.akte.key().name() != akte_id:
            logging.info(document.akte.key().name())
            raise RuntimeError('404')
        if document.tenant != tenant:
            raise RuntimeError('404')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(dict(document=document.as_dict(self.abs_url))))


class DokumenteHandler(BasicHandler):
    def get(self, tenant, akte_id):
        documents = Dokument.all().filter('akte =', db.Key.from_path('Akte', akte_id)).fetch(50)
        documents = [x.as_dict(self.abs_url) for x in documents if tenant == x.tenant]
        values = dict(documents=documents, success=True)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(values))


class AkteHandler(BasicHandler):
    def get(self, tenant, designator, format):
        if format == 'json':
            akte = Akte.get_by_key_name(designator)
            if akte.tenant != tenant:
                raise RuntimeError('404')
            values = dict(data=akte.as_dict(self.abs_url), success=True)
            self.response.headers['Cache-Control'] = 'max-age=15 private'
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(values))
        else:
            self.render({'designator': designator}, 'akte.html')


class AktenHandler(BasicHandler):
    def get(self, tenant, format):
        if format == 'json':
            query = Akte.all().filter('tenant =', tenant).order('-created_at')
            values = self.paginate(query, datanodename='akten')
            values['akten'] = [akte.as_dict(self.abs_url) for akte in values['akten']]
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(values))
        else:
            self.render({}, 'akten.html')


class SearchHandler(BasicHandler):
    def get(self, tenant):
        designator = self.request.get('designator')
        if designator:
            query1 = Akte.all().filter('tenant =', tenant).filter('designator =', designator)
            query2 = Dokument.all().filter('tenant =', tenant).filter('designator =', designator)
            results = query1.fetch(10) + query2.fetch(20)
            values = dict(results=[x.as_dict(self.abs_url) for x in results.fetch(10)],
                          success=True)
        else:
            querystring = self.request.get('q')
            results = []
            if len(querystring) < 3:
                values = dict(error="query for 3 or more characters", success=False)
            else:
                # would be aswsome to run this in paralell
                for model in [Akte, Dokument]:
                    for field in ['designator', 'name1', 'plz', 'email', 'reference', 'name2', 'ort']:
                        query = model.all().filter('tenant =', tenant
                                                   ).filter('%s >=' % field, querystring
                                                   ).filter('%s <=' % field, querystring + u'\ufffd')
                        results.extend([x.as_dict(self.abs_url) for x in query.fetch(25)])
                # TODO: scoring and deduping
                values = dict(results=results, success=True)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(values))


class UploadHandler(BasicHandler):
    def post(self, tenant):
        pdfdata = self.request.POST['pdfdata'].file.read()
        ref = self.request.POST['ref']
        typ = self.request.POST['typ']
        refs = ref.split()
        if refs:
            akte_designator = refs[0]
        else:
            handmade_key = db.Key.from_path('Akte', 1)
            akte_designator = "ablage%s" % (db.allocate_ids(handmade_key, 1)[0])
        pdf_id = str(base64.b32encode(hashlib.sha1(pdfdata).digest()).rstrip('='))

        # do we already have that document - ignore designator given by uploader
        doc = Dokument.get_by_key_name(pdf_id)
        if doc and doc.akte.designator != akte_designator:
            ref = ' '.join(list(set([akte_designator] + ref.split())))
            akte_designator = doc.akte.designator

        akteargs = dict(typ=typ, designator=akte_designator)
        for key in ('name1', 'name2', 'name3', 'strasse', 'land', 'plz', 'ort', 'email', 'ref_url',
                    'datum'):
            if self.request.POST.get(key):
                akteargs[key] = self.request.POST.get(key)
            if self.request.POST.get('akte_%s' % key):
                akteargs[key] = self.request.POST.get('akte_%s' % key)
            if key == 'datum' and 'datum' in akteargs:
                akteargs[key] = convert_to_date(akteargs[key])
        akte = Akte.get_or_insert(akte_designator, tenant=tenant, **akteargs)
        oldref = akte.ref
        newref = list(set(oldref + self.request.POST.get('ref', '').split()))
        if newref != oldref:
            akte.ref = newref
            akte.put()

        docargs = dict(typ=typ, datum=datetime.date.today())
        for key in ('name1', 'name2', 'name3', 'strasse', 'land', 'plz', 'ort', 'email', 'ref_url',
                    'datum'):
            if self.request.POST.get(key):
                docargs[key] = self.request.POST.get(key)
        dokument = Dokument.get_or_insert(pdf_id, designator=pdf_id, akte=akte, tenant=tenant, **docargs)
        DokumentFile.get_or_insert(pdf_id, dokument=dokument, akte=akte, data=pdfdata,
                                   tenant=tenant, mimetype='application/pdf',
                                   filename=self.request.POST['pdfdata'].filename)
        oldref = dokument.ref
        newref = list(set(oldref + self.request.POST.get('ref', '').split()))
        if newref != oldref:
            dokument.ref = newref
            dokument.put()
        self.redirect(dokument.get_url())
        self.response.set_status(201)
        self.response.headers["Content-Type"] = 'text/plain'
        self.response.out.write('ok:%s\n' % dokument.designator)
