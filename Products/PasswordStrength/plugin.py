"""PasswordStrength.
    Rejects passwords which aren't strong enough
"""

__author__ = "Dylan Jay <software@pretaweb.com>"

from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from OFS.Cache import Cacheable
from plone.api import portal
from Products.CMFPlone import PloneMessageFactory as _p
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.RegistrationTool import RegistrationTool
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PasswordStrength import _
from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from zope.i18n import translate

import logging
import re

try:
    from plone.app.users.browser.personalpreferences import IPasswordSchema
except:
    from plone.app.users.browser.passwordpanel import IPasswordSchema

log = logging.getLogger('PasswordStrength')


PROJECTNAME = 'PasswordStrength'
PLUGIN_ID = 'password_strength_plugin'
PLUGIN_TITLE = _('Create your own rules for enforcing password strength')

RegistrationTool.origGeneratePassword = RegistrationTool.generatePassword


# Monkey patch of registration tool method to mark generated password
# Don't think it decreases security... ?
def generatePassword(self):
    return "G-%s" % self.origGeneratePassword()


# Monkey patch of registration tool method to avoid skipping validation for manager
def testPasswordValidity(self, password, confirm=None):
    # We escape the test if it looks like a generated password (with default length of 56 chars)
    if password is not None and password.startswith('G-') and len(password) == len(self.origGeneratePassword()) + 2:
        return None
    session = self.REQUEST.get('SESSION', {}) or {}
    # We also skip the test if a skip_password_check session variable is set
    if password is not None and session.get('skip_password_check'):
        return None
    err = self.pasValidation('password', password)
    if err:
        return err

    if confirm is not None and confirm != password:
        return _p(u'Your password and confirmation did not match. '
                  u'Please try again.')

    return None


manage_addPasswordStrengthForm = PageTemplateFile(
    'www/passwordStrengthAdd',
    globals(),
    __name__='manage_addPasswordStrengthForm')


def manage_addPasswordStrength(dispatcher,
                               id,
                               title=None,
                               REQUEST=None):
    """Add a PasswordStrength plugin to a Pluggable Auth Service."""

    obj = PasswordStrength(id, title)
    dispatcher._setObject(obj.getId(), obj)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace?manage_tabs_message='
                                     'PasswordStrength+plugin+added.'
                                     % dispatcher.absolute_url())

DEFAULT_POLICIES = [(r'.{10}.*', 'Minimum 10 characters'),
                    (r'.*[A-Z].*', 'Minimum 1 capital letter'),
                    (r'.*[a-z].*', 'Minimum 1 lower case letter'),
                    (r'.*[0-9].*', 'Minimum 1 number'),
                    (r'.*[^0-9a-zA-Z ].*', 'Minimum 1 non-alpha character'),
                    ]


class PasswordStrength(BasePlugin, Cacheable):

    """PAS plugin that ensures strong passwords
    """

    meta_type = 'Password Strength Plugin'
    security = ClassSecurityInfo()

    _properties = ({'id': 'title',
                    'label': 'Title',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p1_re',
                    'label': 'Policy 1 Regular Expression',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p1_err',
                    'label': 'Policy 1 Error Message',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p2_re',
                    'label': 'Policy 2 Regular Expression',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p2_err',
                    'label': 'Policy 2 Error Message',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p3_re',
                    'label': 'Policy 3 Regular Expression',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p3_err',
                    'label': 'Policy 3 Error Message',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p4_re',
                    'label': 'Policy 4 Regular Expression',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p4_err',
                    'label': 'Policy 4 Error Message',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p5_re',
                    'label': 'Policy 5 Regular Expression',
                    'type': 'string',
                    'mode': 'w',
                    },
                   {'id': 'p5_err',
                    'label': 'Policy 5 Error Message',
                    'type': 'string',
                    'mode': 'w',
                    },
                   )

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

        i = 1
        for reg, err in DEFAULT_POLICIES:
            setattr(self, 'p%i_re' % i, reg)
            setattr(self, 'p%i_err' % i, err)
            i += 1

    security.declarePrivate('validateUserInfo')
    def validateUserInfo(self, user, set_id, set_info):
        """ -> ( error_info_1, ... error_info_N )

        o Returned values are dictionaries, containing at least keys:

          'id' -- the ID of the property, or None if the error is not
                  specific to one property.

          'error' -- the message string, suitable for display to the user.
        """

        errors = []
        site = portal.getSite()
        if set_info and set_info.get('password', None) is not None:
            password = set_info['password']
            i = 1
            while True:
                reg = getattr(self, 'p%i_re' % i, None)
                if not reg:
                    break
                if not re.match(reg, password):
                    err = getattr(self, 'p%i_err' % i, None)
                    if err:
                        errors += [translate(safe_unicode(err), domain='Products.PasswordStrength',
                                             context=site.REQUEST)]
                i += 1

            errors = [{'id': 'password', 'error': e} for e in errors]
        return errors


classImplements(PasswordStrength,
                IValidationPlugin)

InitializeClass(PasswordStrength)

# Monkey patch for Password fields, to get validation before form submission.
# This is required for this to be useable in Plone 4s @@new-user form.

from zope.schema import Password
from zope.schema.interfaces import ValidationError
from Products.CMFCore.utils import getToolByName


class CustomPasswordError(ValidationError):
    __doc__ = _("This password doesn't match requirements for passwords")


def validate(self, value):
    try:
        existing = bool(self.get(self.context))
    except AttributeError:
        existing = False
    if value is self.UNCHANGED_PASSWORD and existing:
        # Allow the UNCHANGED_PASSWORD value, if a password is set already
        return

    skip = False

    # Do not validate old password when changing passwords as logged in user
    if getattr(self, '__name__', '') == 'current_password':
        skip = True

    if IPasswordSchema.providedBy(self.context):
        # We need to get the context's context
        context = self.context.context
    else:
        context = self.context
    if not skip:
        # no context for a schema.Password field when Zope starts (issue #6)
        # no acquisition for a RecordsProxy object
        try:
            reg_tool = getToolByName(context, 'portal_registration')
        except AttributeError:
            return
        errors = reg_tool.testPasswordValidity(value)
        if errors:
            raise CustomPasswordError(errors)

    return super(Password, self).validate(value)

Password.validate = validate
