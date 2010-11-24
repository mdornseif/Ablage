#!/usr/bin/env python
# encoding: utf-8
"""
ablage/views.py

Created by Maximillian Dornseif on 2010-11-04.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


import config
config.imported = True

from ablage.models import Credential, Akte, Dokument, DokumentFile
from gaetk.handler import BasicHandler, HTTP400_BadRequest, HTTP413_TooLarge
from google.appengine.ext import db
from huTools import hujson
from huTools.calendar.formats import convert_to_date
import base64
import datetime
import gaetk.tools
import hashlib
import huTools.hujson as json
import logging


class CredentialsHandler(BasicHandler):
    """Empfänger-Konfiguration - Write only."""
    def post(self):
        """Empfänger-Konfiguration updaten."""
        user = self.login_required()
        self.response.headers["Content-Type"] = "application/json"
        tenant = user.tenant
        # tenant = self.request.get('tenant')
        text = self.request.get('text', '')
        email = self.request.get('email')
        credential = Credential.create(tenant=tenant, text=text, email=email)
        self.response.set_status(201)
        self.response.out.write(hujson.dumps(dict(uid=credential.uid, secret=credential.secret)))


class MainHandler(BasicHandler):
    def get(self):
        self.response.out.write('Hello world!')


class PdfHandler(BasicHandler):
    def get(self, tenant, akte_id, doc_id):
        user = self.login_required()
        dfile = DokumentFile.get_by_key_name("%s-%s" % (tenant, doc_id))
        if not dfile:
            logging.error('DocumentFile(%s-%s) not found' % (tenant, doc_id))
            raise RuntimeError('404')
        if user.tenant != tenant:
            logging.error('DocumentFile(%s-%s) wrong tenant for user' % (tenant, doc_id))
            raise RuntimeError('404')
        if dfile.tenant != tenant:
            logging.error('DocumentFile(%s-%s) wrong tenant found' % (tenant, doc_id))
            raise RuntimeError('404')
        if dfile.akte and dfile.akte.key().name() != ("%s-%s" % (tenant, akte_id)):
            logging.error('DocumentFile(%s-%s) wrong akte: %s %s', tenant, doc_id, akte_id,
                            dfile.akte.key().name())
            raise RuntimeError('404')
        self.response.headers['Content-Type'] = 'application/pdf'
        self.response.out.write(dfile.data)


class DokumentHandler(BasicHandler):
    def get(self, tenant, akte_id, doc_id, format):
        user = self.login_required()
        document = Dokument.get_by_key_name("%s-%s" % (tenant, doc_id))
        if (not document) or (user.tenant != tenant):
            raise RuntimeError('404')
        if document.akte.key().name() != akte_id:
            logging.info(document.akte.key().name())
            raise RuntimeError('404')
        if document.tenant != tenant:
            raise RuntimeError('404')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(dict(document=document.as_dict(self.abs_url))))


class DokumenteHandler(BasicHandler):
    def get(self, tenant, akte_id):
        user = self.login_required()
        if (user.tenant != tenant):
            raise RuntimeError('404')
        documents = Dokument.all().filter('tenant =', tenant).filter(
                              'akte =', db.Key.from_path('Akte', "%s-%s" % (tenant, akte_id))).fetch(50)
        documents = [x.as_dict(self.abs_url) for x in documents if tenant == x.tenant]
        values = dict(documents=documents, success=True)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(values))


class AkteHandler(BasicHandler):
    def get(self, tenant, designator, format):
        user = self.login_required()
        if format == 'json':
            akte = Akte.get_by_key_name("%s-%s" % (tenant, designator))
            if (not akte) or (akte.tenant != tenant) or (user.tenant != tenant):
                raise RuntimeError('404')
            values = dict(data=akte.as_dict(self.abs_url), success=True)
            self.response.headers['Cache-Control'] = 'max-age=15 private'
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(values))
        else:
            self.render({'designator': designator}, 'akte.html')


class AktenHandler(BasicHandler):
    def get(self, tenant, format):
        user = self.login_required()
        if user.tenant != tenant:
            raise RuntimeError('404')
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
        user = self.login_required()
        if user.tenant != tenant:
            raise RuntimeError('404')
        designator = self.request.get('designator')
        if designator:
            query1 = Akte.all().filter('tenant =', tenant).filter('designator =', designator)
            query2 = Dokument.all().filter('tenant =', tenant).filter('designator =', designator)
            query3 = Dokument.all().filter('tenant =', tenant).filter('ref =', designator)
            query4 = Dokument.all().filter('tenant =', tenant).filter('ref =', designator)
            results = list(set(query1.fetch(10) + query2.fetch(10) + query3.fetch(10) + query4.fetch(10)))
            values = dict(results=[x.as_dict(self.abs_url) for x in results],
                          success=True)
        else:
            results = []
            # 'Term1 "Term2 and Term3"'.split() -> ['Term1', 'Term2 and Term3']
            for part in gaetk.tools.split(self.request.get('q')):
                # would be aswsome to run this in paralell
                for model in [Akte, Dokument]:
                    for field in ['designator', 'name1', 'plz', 'email', 'ref', 'name2', 'ort']:
                        query = model.all().filter('tenant =', tenant
                                                   ).filter('%s >=' % field, part
                                                   ).filter('%s <=' % field, part + u'\ufffd')
                        results.extend([x.as_dict(self.abs_url) for x in query.fetch(25)])
            # TODO: scoring and deduping
            values = dict(results=results, success=True)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(values))


class UploadHandler(BasicHandler):
    def post(self, tenant):
        user = self.login_required()
        tenant = user.tenant
        if not hasattr(self.request.POST['pdfdata'], 'file'):
            logging.debug(dir(self.request))
            logging.debug(vars(self.request))
            HTTP400_BadRequest('pdfdata not a file')
        pdfdata = self.request.POST['pdfdata'].file.read()
        if len(pdfdata) > 900000:
            raise HTTP413_TooLarge('PDF bigger than 900k')
        ref = self.request.POST['ref']
        typ = self.request.POST['type']
        refs = ref.split()
        if refs:
            akte_designator = refs[0]
        else:
            handmade_key = db.Key.from_path('Akte', 1)
            akte_designator = "ablage%s" % (db.allocate_ids(handmade_key, 1)[0])
        pdf_id = str(base64.b32encode(hashlib.sha1(pdfdata).digest()).rstrip('='))
        key_name = "%s-%s" % (tenant, pdf_id)
        
        # do we already have that document - ignore designator given by uploader
        doc = Dokument.get_by_key_name(key_name)
        if doc and doc.akte.designator != akte_designator:
            ref = ' '.join(list(set([akte_designator] + ref.split())))
            akte_designator = doc.akte.designator
        akte_key = "%s-%s" % (tenant, akte_designator)

        akteargs = dict(type=typ, designator=akte_designator,
                        datum=convert_to_date(self.request.POST.get('datum')))
        for key in ('name1', 'name2', 'name3', 'strasse', 'land', 'plz', 'ort', 'email', 'ref_url',
                    'datum'):
            if self.request.POST.get(key):
                akteargs[key] = self.request.POST.get(key)
            if self.request.POST.get('akte_%s' % key):
                akteargs[key] = self.request.POST.get('akte_%s' % key)
            if key == 'datum' and 'datum' in akteargs:
                akteargs[key] = convert_to_date(akteargs[key])
        akte = Akte.get_or_insert(akte_key, tenant=tenant, **akteargs)
        oldref = akte.ref
        newref = list(set(oldref + self.request.POST.get('ref', '').split()))
        newseit = oldseit = akte.seit
        if self.request.POST.get('datum'):
            postseit = convert_to_date(self.request.POST.get('datum'))
            if postseit and postseit and (postseit < postseit):
                newseit = postseit
        if (newref != oldref) or (newseit != oldseit):
            akte.seit = newseit
            akte.ref = newref
            akte.put()

        docargs = dict(type=typ, datum=datetime.date.today(), file_length=len(pdfdata))
        for key in ('name1', 'name2', 'name3', 'strasse', 'land', 'plz', 'ort', 'email', 'ref_url',
                    'datum' 'quelle'):
            if self.request.POST.get(key):
                docargs[key] = self.request.POST.get(key)
        if 'datum' in docargs:
            docargs['datum'] = convert_to_date(docargs['datum'])
        dokument = Dokument.get_or_insert(key_name, designator=pdf_id, akte=akte, tenant=tenant, **docargs)
        # resave if it existed but something had changed
        for key in docargs.keys():
            if getattr(dokument, key) != docargs[key]:
                logging.debug('%s: key %s has changed', pdf_id, key)
                dokument.put()
                break
        DokumentFile.get_or_insert(key_name, dokument=dokument, akte=akte, data=pdfdata,
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
