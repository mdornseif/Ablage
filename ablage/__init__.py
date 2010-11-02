#!/usr/bin/env python
# encoding: utf-8
"""
ablage.py

Created by Maximillian Dornseif on 2010-08-23.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config

import sys
import os
import hashlib
import base64
import simpledb
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import datetime
from google.appengine.ext import db
import base64
import warnings
import collections
import logging
import re
import huTools.calendar.formats
from huTools.calendar.formats import convert_to_date, convert_to_datetime
from ablage.models import *

import cs.keychain
import simplejson as json

sdb = simpledb.SimpleDB(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])

# sdb.create_domain('ablage_documents')
# sdb.create_domain('ablage_akten')
# bucket = s3.create_bucket('ablage_original_documents')

ldocs = sdb['ablage_documents']
lakten = sdb['ablage_akten']
lbucket = s3.get_bucket('ablage_original_documents', validate=False)

def store_doc(akte_id, pdfdata, **kwargs):
    doc_id = kwargs.get('doc_id')
    # Akte anlegen
    akteargs = {}
    for key, value in kwargs.items():
        if key.startswith('akte_'):
            if key == 'akte_created_at':
                akteargs[key[5:]] = convert_to_datetime(value)
            else:
                akteargs[key[5:]] = value
        else:
            if key == 'created_at':
                akteargs[key] = convert_to_datetime(value)
            else:
                akteargs[key] = value
    if not akte_id:
        handmade_key = db.Key.from_path('Akte', 1)
        akte_id = "ablage%s" % (db.allocate_ids(handmade_key, 1)[0])
    akteargs['designator'] = akte_id
    logging.info(akteargs)
    akte = Akte.get_or_insert(akte_id, **akteargs)
    
    # Dokument anlegen
    pdf_id = str(base64.b32encode(hashlib.md5(pdfdata).digest()).rstrip('='))
    if not doc_id:
        doc_id = pdf_id
    docargs = {}
    for key, value in kwargs.items():
        if (not key.startswith('akte_')) and key != 'akte':
            if key in ['datum']:
                docargs[key] = convert_to_date(value)
            elif key in ['created_at']:
                docargs[key] = convert_to_datetime(value)
            else:
                docargs[key] = value
    if 'datum' not in docargs:
        docargs['datum'] = datetime.date.today()
        warnings.warn("don't call store_doc() without a datum", RuntimeWarning, stacklevel=2)
    dokument = Dokument.get_or_insert(doc_id, designator=doc_id, akte=akte, **docargs)
    docfile = DokumentFile.get_or_insert(pdf_id, dokument=dokument, akte=akte, data=pdfdata, mimetype='application/pdf')


def convert():
    #aktenexport = {}
    #for akte in lakten.all():
    #    aktenexport[str(akte.name)] = {}
    #    for k, v in akte.items():
    #        aktenexport[str(akte.name)][k] = v
    #open('aktenexport.json', 'w').write(json.dumps(aktenexport))
    
    docsexport = {}
    for doc in ldocs.all():
        docsexport[str(doc.name)] = {}
        for k, v in doc.items():
            docsexport[str(doc.name)][k] = v
        k = Key(lbucket)
        k.key = doc['original_id']
        pdfdata = k.get_contents_as_string()
        store_doc(doc['akte'], pdfdata, **docsexport[str(doc.name)])
        
        # "land": "DE",
        # "akte": "WL20003303",
        # "created_at": "2010-09-17",
        # "datum": "2010-09-17",
        # "plz": "56072",
        # "person": "W\u00fcst Karin ",
        # "original_id": "EJP4YFBXOGTORYX45AKQUACNFA.pdf",
        # "name1": "W\u00fcst Karin",
        # "name2": null,
        # "strasse": "Am M\u00fchlbach 47",
        # "type": "Mahnung",
        # "email": "karinwuest2@gmx.de"
    
    #open('docsexport.json', 'w').write(json.dumps(docsexport))
