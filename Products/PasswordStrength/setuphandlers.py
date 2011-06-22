from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.PasswordStrength.plugin import PROJECTNAME, PLUGIN_ID, PLUGIN_TITLE
from Products.CMFCore.permissions import ManagePortal

# for installing skin
from Products.CMFCore.DirectoryView import addDirectoryViews


def setupPasswordStrength(context):
    if context.readDataFile('passwordstrength.txt') is None:
        return
    site = context.getSite()
    install(site)

def removePasswordStrength(context):
    if context.readDataFile('passwordstrength.txt') is None:
        return
    site = context.getSite()
    uninstall(site)

def install( portal ):

    """ This plugin needs to be installed in two places, the instance PAS where
    logins occur and the root acl_users.

    Different interfaces need to be activated for either case.
    """
    out = StringIO()
    print >> out, "Installing %s:" % PROJECTNAME

    
   #  Place the Product directory 'PasswordStength' in your 'Products/'
   #  directory. Restart Zope.
   #
   #  In your PAS 'acl_users', select 'PasswordStrength' from the add
   #  list.  Give it an id and title, and push the add button.
   #
   #  Enable the 'Validation' plugin interfaces in the after-add screen.
   #  
   #  Click on the properties tab and edit the validation rules
   #  

    plone_pas = getToolByName(portal, 'acl_users')

    # define the interfaces which need to be activated for either PAS
    interfaces_for_paservices = {
        plone_pas: ['IValidationPlugin'],
        }
    for (pas, interfaces) in interfaces_for_paservices.iteritems():
        registry = pas.plugins
        existing = pas.objectIds()
        if PLUGIN_ID not in existing:
            plugin = pas.manage_addProduct[PROJECTNAME]
            plugin.manage_addPasswordStrength(PLUGIN_ID, PLUGIN_TITLE)
            activatePluginSelectedInterfaces(pas, PLUGIN_ID, out, interfaces)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall( portal ):
    out = StringIO()
    print >> out, "Uninstalling %s:" % PROJECTNAME
    plone_pas = getToolByName(portal, 'acl_users')
    for pas in [plone_pas, zope_pas]:
        existing = pas.objectIds()
        if PLUGIN_ID in existing:
            pas.manage_delObjects(PLUGIN_ID)

def activatePluginSelectedInterfaces(pas, plugin, out, selected_interfaces, 
        disable=[]):
    """This is derived from PlonePAS's activatePluginInterfaces, but 
    will only activate the plugin for selected interfaces. 
    
    The PAS instance (either Plone's or Zope's) in which to activate the 
    interfaces is passed as an argument, so portal is not needed.
    """
    plugin_obj = pas[plugin]
    activatable = []
    for info in plugin_obj.plugins.listPluginTypeInfo():
        interface = info['interface']
        interface_name = info['id']
        if plugin_obj.testImplements(interface) and \
                interface_name in selected_interfaces:
            if interface_name in disable:
                disable.append(interface_name)
                print >> out, " - Disabling: " + info['title']
            else:
                activatable.append(interface_name)
                print >> out, " - Activating: " + info['title']
    plugin_obj.manage_activateInterfaces(activatable)
    print >> out, plugin + " activated."

