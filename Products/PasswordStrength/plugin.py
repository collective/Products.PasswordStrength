
"""PasswordStrength.
    Rejects passwords which aren't strong enough
"""

__author__ = "Dylan Jay <software@pretaweb.com>"

import logging

from urllib import quote, unquote

from BTrees.OOBTree import OOBTree
from DateTime import DateTime
from AccessControl import ClassSecurityInfo, Permissions
from AccessControl.Permissions import view
from AccessControl import AuthEncoding
from Globals import InitializeClass
from OFS.Cache import Cacheable
from OFS.Folder import Folder

from zExceptions import Unauthorized

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.permissions import ManageUsers
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import \
    IValidationPlugin, IPropertiesPlugin

import re

from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from patch import wrapAllMethods
from Products.CMFPlone.RegistrationTool import RegistrationTool
import hashlib
import random
import pkg_resources
try:
    pkg_resources.get_distribution('plone.app.users')
    from plone.app.users.browser.personalpreferences import IPasswordSchema
except pkg_resources.DistributionNotFound:
    from zope.interface import Interface
    class IPasswordSchema(Interface):
        pass

log = logging.getLogger('PasswordStrength')


PROJECTNAME = 'PasswordStrength'
PLUGIN_ID = 'password_strength_plugin'
PLUGIN_TITLE = 'Create your own rules for enforcing password strength'





class RegistrationToolPatch:
    def testPasswordValidity(self, password, confirm=None):

        """ Verify that the password satisfies the portal's requirements.

        o If the password is valid, return None.
        o If not, return a string explaining why.
        """
        if confirm is not None and confirm != password:
            return ( 'Your password and confirmation did not match. '
                   + 'Please try again.' )

        if not password:
            err = [ 'You must enter a password.' ]
        else:
            err = []

        # Use PAS to test validity
        pas_instance = self.acl_users
        plugins = pas_instance._getOb('plugins')
        validators = plugins.listPlugins(IValidationPlugin)
        for validator_id, validator in validators:
            user = None
            set_id = ''
            set_info = {'password':password}
            errors = validator.validateUserInfo( user, set_id, set_info )
            err += [info['error'] for info in errors if info['id'] == 'password' ]
        if err:
            return ' '.join(err)
        else:
            return None

wrapAllMethods(RegistrationToolPatch,RegistrationTool)


manage_addPasswordStrengthForm = PageTemplateFile(
    'www/passwordStrengthAdd',
    globals(),
    __name__='manage_addPasswordStrengthForm' )

def manage_addPasswordStrength(dispatcher,
                               id,
                               title=None,
                               REQUEST=None):
    """Add a PasswordStrength plugin to a Pluggable Auth Service."""

    obj = PasswordStrength(id, title
                           )
    dispatcher._setObject(obj.getId(), obj)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace?manage_tabs_message='
                                     'PasswordStrength+plugin+added.'
                                     % dispatcher.absolute_url())

DEFUALT_POLICIES = [(r'.{20}.*','Minimum 20 characters.')
                    ,(r'.*[A-Z].*','Minimum 1 capital letter.')
                    ,(r'.*[a-z].*','Minimum 1 lower case letter.')
                    ,(r'.*[0-9].*','Minimum 1 number.')
                    ,(r'.*[^0-9a-zA-Z ].*','Minimum 1 non-alpha character.')
                    ]



class PasswordStrength(BasePlugin, Cacheable):

    """PAS plugin that ensures strong passwords
    """

    meta_type = 'Password Strength Plugin'
    security = ClassSecurityInfo()

    _properties = ( { 'id'    : 'title'
                    , 'label' : 'Title'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p1_re'
                    , 'label' : 'Policy 1 Regular Expression'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p1_err'
                    , 'label' : 'Policy 1 Error Message'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p2_re'
                    , 'label' : 'Policy 2 Regular Expression'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p2_err'
                    , 'label' : 'Policy 2 Error Message'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p3_re'
                    , 'label' : 'Policy 3 Regular Expression'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p3_err'
                    , 'label' : 'Policy 3 Error Message'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p4_re'
                    , 'label' : 'Policy 4 Regular Expression'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p4_err'
                    , 'label' : 'Policy 4 Error Message'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p5_re'
                    , 'label' : 'Policy 5 Regular Expression'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  , { 'id'    : 'p5_err'
                    , 'label' : 'Policy 5 Error Message'
                    , 'type'  : 'string'
                    , 'mode'  : 'w'
                    }
                  )


    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

        i = 1
        for reg,err in DEFUALT_POLICIES:
            setattr(self, 'p%i_re' % i, reg)
            setattr(self, 'p%i_err' % i, err)
            i+=1




    security.declarePrivate('validateUserInfo')
    def validateUserInfo(self, user, set_id, set_info ):

        """ -> ( error_info_1, ... error_info_N )

        o Returned values are dictionaries, containing at least keys:

          'id' -- the ID of the property, or None if the error is not
                  specific to one property.

          'error' -- the message string, suitable for display to the user.
        """

        errors = []

        if set_info and set_info.get('password', None) is not None:
            password = set_info['password']

            i = 1
            while True:
                reg = getattr(self, 'p%i_re' % i, None)
                if not reg:
                    break
                if not re.match(reg, password):
                    err = getattr(self, 'p%i_err' % i, None)
                    errors += [err]
                i += 1

            errors = [{'id':'password','error':e} for e in errors]
        return errors

    def getPropertiesForUser(self, user, request=None):
        # HACK to get
        hash = hashlib.md5(str(random.random())).hexdigest()
        return {'generated_password':'A-'+hash}

classImplements(PasswordStrength,
                IValidationPlugin)
classImplements(PasswordStrength,
                IPropertiesPlugin)

InitializeClass(PasswordStrength)

# Monkey patch for Password fields, to get validation before form submission.
# This is required for this to be useable in Plone 4s @@new-user form.

from zope.schema import Password
from zope.schema.interfaces import ValidationError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

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
    if IPasswordSchema.providedBy(self.context):
        # We need to get the context's context
        context = self.context.context
        # Do not validate existing passwords
        if getattr(self, '__name__', '') == 'current_password':
            skip = True
    else:
        context = self.context
    if not skip:
        reg_tool = getToolByName(context, 'portal_registration')
        errors = reg_tool.testPasswordValidity(value)
        if errors:
            raise CustomPasswordError(errors)

    return super(Password, self).validate(value)

Password.validate = validate
