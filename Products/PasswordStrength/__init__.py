
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


PROJECTNAME = "PasswordStrength"
