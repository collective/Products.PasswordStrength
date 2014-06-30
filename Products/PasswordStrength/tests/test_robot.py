import unittest2 as unittest

import robotsuite
from Products.PasswordStrength.testing import ROBOT_TESTING
from plone.testing import layered


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('password.robot'),
                layer=ROBOT_TESTING),
    ])
    return suite
