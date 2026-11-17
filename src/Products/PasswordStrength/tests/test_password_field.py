# -*- coding: utf-8 -*-
from Products.PasswordStrength.plugin import CustomPasswordError
from Products.PasswordStrength.testing import INTEGRATION_TESTING
from zope.schema import Password

import unittest


try:
    from plone.base.interfaces import ILoginFormSchema
except ImportError:
    from Products.CMFPlone.interfaces import ILoginFormSchema


class TestPasswordField(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def test_login_form_password_not_validated(self):
        portal = self.layer['portal']
        # a user with a weak password (set before the policy) can still log in
        ILoginFormSchema['ac_password'].bind(portal).validate(u'admin')
        # a new password is still validated
        field = Password(__name__='password').bind(portal)
        self.assertRaises(CustomPasswordError, field.validate, u'admin')
