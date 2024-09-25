# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from Products.PasswordStrength.testing import INTEGRATION_TESTING
from Products.PasswordStrength.testing import PLONE_VERSION
from plone import api

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestInstall(unittest.TestCase):
    """Test installation of collective.contact.plonegroup into Plone."""
    layer = INTEGRATION_TESTING

    def setUp(self):
        super(TestInstall, self).setUp()
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        self.acl = self.portal.acl_users
        self.setup = self.portal.portal_setup

    def test_product_installed(self):
        self.assertTrue(self.installer.is_product_installed('PasswordStrength'))
        auth_plugins = self.acl.plugins.getAllPlugins(plugin_type='IValidationPlugin')
        self.assertEqual(auth_plugins['active'], ('password_strength_plugin', ))

    def test_uninstall(self):
        self.installer.uninstall_product('PasswordStrength')
        self.assertFalse(self.installer.is_product_installed('PasswordStrength'))
        self.setup.runAllImportStepsFromProfile('profile-Products.PasswordStrength:uninstall')
        auth_plugins = self.acl.plugins.getAllPlugins(plugin_type='IValidationPlugin')
        if PLONE_VERSION >= '4.3':
            self.assertEqual(auth_plugins['active'], ('password_policy', ))
        else:
            self.assertEqual(auth_plugins['active'], ())
