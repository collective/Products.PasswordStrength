from Products.PasswordStrength.testing import ROBOT_TESTING
from plone.testing import layered

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('password.robot'),
                layer=ROBOT_TESTING),
    ])
    return suite
