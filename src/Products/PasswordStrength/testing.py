# -*- coding: utf-8 -*-
import pkg_resources
PLONE_VERSION = pkg_resources.get_distribution('Products.CMFPlone').version

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

from plone.testing import z2
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.robotframework.testing import MOCK_MAILHOST_FIXTURE

from Products.PasswordStrength.tests.robot_setup import PasswordStrengthRemoteKeywords

try:
    from Products.CMFPlone.tests.robot.robot_setup import CMFPloneRemoteKeywords
except ImportError:
    from Products.PasswordStrength.tests.backward_robot import CMFPloneRemoteKeywords


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PasswordStrength
        import z3c.jbot
        self.loadZCML(package=z3c.jbot)
        self.loadZCML(package=Products.PasswordStrength)
        # Install product and call its initialize() function
        z2.installProduct(app, 'Products.PasswordStrength')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.PasswordStrength:default')

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='Products.PasswordStrength:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='Products.PasswordStrength:Functional',
)

# Add interesting existing class to default libraries
REMOTE_LIBRARY_BUNDLE_FIXTURE.libraryBases = REMOTE_LIBRARY_BUNDLE_FIXTURE.libraryBases + \
    (CMFPloneRemoteKeywords, PasswordStrengthRemoteKeywords)

ROBOT_TESTING = FunctionalTesting(
    bases=(
        FIXTURE,
        MOCK_MAILHOST_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="ROBOT_TESTING",
)
