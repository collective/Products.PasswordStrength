# -*- coding: utf-8 -*-
from plone.app.robotframework.remote import RemoteLibrary
from Products.PasswordStrength.testing import PLONE_VERSION


class PasswordStrengthRemoteKeywords(RemoteLibrary):
    """Robot Framework remote keywords library
    """

    def get_plone_version(self):
        return PLONE_VERSION

    def extract_reset_url(self, mail):
        mail = mail.replace('=\r\n', '').replace('=\n', '')
        assert("passwordreset/" in mail)
        mail = mail[mail.index('passwordreset/'):]
        url = mail.split()[0]
        return url
