import unittest2 as unittest

import robotsuite
from Products.PasswordStrength.testing import ROBOT_TESTING
from Products.PasswordStrength.testing import PLONE_VERSION
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('password.robot'),
                layer=ROBOT_TESTING),
    ])
    # inline validation
    if PLONE_VERSION >= '4.3':
        suite.addTests([
            layered(robotsuite.RobotTestSuite('password_inline_validation.robot'),
                    layer=ROBOT_TESTING),
        ])
    return suite
