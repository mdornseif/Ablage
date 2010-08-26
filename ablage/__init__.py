#!/usr/bin/env python
# encoding: utf-8
"""
ablage.py

Created by Maximillian Dornseif on 2010-08-23.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import sys
import os
import hashlib
import base64
import simpledb
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import datetime


sdb = simpledb.SimpleDB(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])

# sdb.create_domain('ablage_documents')
# sdb.create_domain('ablage_akten')
# bucket = s3.create_bucket('ablage_original_documents')

docs = sdb['ablage_documents']
akten = sdb['ablage_akten']
bucket = s3.get_bucket('ablage_original_documents', validate=False)


def store_doc(akte_id, pdfdata, doc_id=None, **kwargs):
    pdf_id = str(base64.b32encode(hashlib.md5(pdfdata).digest()).rstrip('=')) + '.pdf'
    if doc_id and docs[doc_id]: # same as 'if docid and doc_id in docs:' on a dict
        raise ValueError
    if not doc_id:
        doc_id = pdf_id
    doc = dict(akte=akte_id, original_id=pdf_id, created_at=datetime.date.today())
    for key, value in kwargs.items():
        if not key.startswith('akte_'):
            doc[key] = value
    k = Key(bucket)
    k.key = pdf_id
    k.set_contents_from_string(pdfdata)
    # k.set_metadata('meta1', 'This is the first metadata value')
    # print k.generate_url(3600)
    docs[doc_id] = doc

    # Akte anlegen
    doc = akten[akte_id]
    if 'created_at' not in doc:
        doc['created_at'] = datetime.date.today()
    for key, value in kwargs.items():
        if not key.startswith('akte_'):
            if key not in doc:
                doc[key] = value
    for key, value in kwargs.items():
        if key.startswith('akte_'):
            doc[key[5:]] = value
    doc.save()
    return doc_id
