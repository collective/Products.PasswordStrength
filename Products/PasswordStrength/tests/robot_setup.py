# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary

from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.PasswordStrength.testing import PLONE_VERSION


class PasswordStrengthRemoteKeywords(RemoteLibrary):
    """Robot Framework remote keywords library
    """

    def the_inline_validation_disabled(self):
        portal = getSite()
        jst = getToolByName(portal, 'portal_javascripts')
        js = jst.getResource('inline_validation.js')
        if js and js.getEnabled():
            js.setEnabled(False)

    def the_inline_validation_enabled(self):
        portal = getSite()
        jst = getToolByName(portal, 'portal_javascripts')
        js = jst.getResource('inline_validation.js')
        if js and not js.getEnabled():
            js.setEnabled(True)

    def get_plone_version(self):
        return PLONE_VERSION

    def extract_reset_url(self, mail):
        url = ''
        for line in mail.split('\n'):
            line = line.strip()
            if line.startswith('http'):
                url = line[line.index('passwordreset'):]
                if url.endswith('='):
                    url = url[:-1]
                    continue
                else:
                    return url
            elif url:
                return url + line
        return ''
