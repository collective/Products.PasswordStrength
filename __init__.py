
"""PasswordStrength
"""

__author__ = "Dylan Jay <software@pretaweb.com"

from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import registerMultiPlugin
from plugin import PasswordStrength, \
                   manage_addPasswordStrength, \
                   manage_addPasswordStrengthForm

def initialize(context):
    """Initialize the PasswordStrength plugin."""
    registerMultiPlugin(PasswordStrength.meta_type)
    
    context.registerClass(PasswordStrength,
                          permission=add_user_folders,
                          constructors=(manage_addPasswordStrengthForm,
                                        manage_addPasswordStrength),
                          #icon='www/noduplicatelogin.png',
                          visibility=None,
                          )


try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy=None

from Globals import package_home
from Products.CMFCore import utils, CMFCorePermissions, DirectoryView
from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize

import os, os.path


PROJECTNAME = "PasswordStrength"

product_globals=globals()

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/PasswordStrength', product_globals)
DirectoryView.registerDirectory('skins/PasswordStrength_public', product_globals)


