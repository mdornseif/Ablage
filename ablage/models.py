#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Maximillian Dornseif on 2010-09-20.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

import config
config.imported = True

from google.appengine.ext import db


class Akte(db.Model):
    designator = db.StringProperty(required=True)
    tenant = db.StringProperty(required=True, default='CYLGI')
    name1 = db.StringProperty(required=False)
    name2 = db.StringProperty(required=False)
    name3 = db.StringProperty(required=False)
    strasse = db.StringProperty(required=False)
    land = db.StringProperty(required=False)
    plz = db.StringProperty(required=False)
    ort = db.StringProperty(required=False)
    email = db.EmailProperty(required=False)
    typ = db.StringProperty(required=False)
    ref = db.StringListProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    created_by = db.UserProperty(required=False, auto_current_user_add=True, indexed=False)
    updated_by = db.UserProperty(required=False, auto_current_user=True, indexed=False)

    def as_dict(self, abs_url=lambda x: x):
        """Format a Akte to be converted to JOSN or XML."""
        ret = {}
        for fieldname in """designator tenant name1 name2 name3 strasse land plz ort email typ
                         created_at updated_at""".split():
            if getattr(self, fieldname):
                ret[fieldname] = getattr(self, fieldname)
        ret['url'] = abs_url('/%s/akten/%s' % (self.tenant, self.designator))
        ret['docs'] = abs_url('/%s/akten/%s/docs' % (self.tenant, self.designator))
        ret['object'] = 'Akte'
        # designator = db.StringProperty(required=True)
        # akte = db.ReferenceProperty(Akte, required=True)
        # created_by = db.UserProperty(required=False, auto_current_user_add=True, indexed=False)
        # updated_by = db.UserProperty(required=False, auto_current_user=True, indexed=False)
        return ret


class Dokument(db.Model):
    designator = db.StringProperty(required=True)
    akte = db.ReferenceProperty(Akte, required=True)
    datum = db.DateProperty(required=True)
    tenant = db.StringProperty(required=True, default='CYLGI')
    name1 = db.StringProperty(required=False)
    name2 = db.StringProperty(required=False)
    name3 = db.StringProperty(required=False)
    strasse = db.StringProperty(required=False)
    land = db.StringProperty(required=False)
    plz = db.StringProperty(required=False)
    ort = db.StringProperty(required=False)
    email = db.EmailProperty(required=False)
    typ = db.StringProperty(required=False)
    ref = db.StringListProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    created_by = db.UserProperty(required=False, auto_current_user_add=True, indexed=False)
    updated_by = db.UserProperty(required=False, auto_current_user=True, indexed=False)

    def get_url(self, abs_url=lambda x: x):
        return abs_url('/%s/akten/%s/docs/%s' % (self.tenant, self.akte.designator, self.designator))

    def as_dict(self, abs_url=lambda x: x):
        """Format a Dokument to be converted to JSON or XML."""
        ret = {}
        for fieldname in """designator datum tenant name1 name2 name3 strasse land plz ort email typ
                         created_at updated_at""".split():
            if getattr(self, fieldname):
                ret[fieldname] = getattr(self, fieldname)
        ret['akte'] = abs_url('/%s/akten/%s' % (self.tenant, self.akte.designator))
        ret['url'] = abs_url('/%s/akten/%s/docs/%s' % (self.tenant, self.akte.designator, self.designator))
        ret['pdf'] = abs_url('/%s/akten/%s/pdf/%s.pdf' % (self.tenant, self.akte.designator, self.designator))
        ret['object'] = 'Dokument'
        # designator = db.StringProperty(required=True)
        # akte = db.ReferenceProperty(Akte, required=True)
        # created_by = db.UserProperty(required=False, auto_current_user_add=True, indexed=False)
        # updated_by = db.UserProperty(required=False, auto_current_user=True, indexed=False)
        return ret


class DokumentFile(db.Model):
    dokument = db.ReferenceProperty(Dokument, required=True)
    akte = db.ReferenceProperty(Akte, required=False)
    tenant = db.StringProperty(required=False, default='CYLGI')
    data = db.BlobProperty(required=True)
    mimetype = db.StringProperty(required=True)
    filename = db.StringProperty()
