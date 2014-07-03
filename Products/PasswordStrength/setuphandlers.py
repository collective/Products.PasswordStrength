from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.PasswordStrength.plugin import PROJECTNAME, PLUGIN_ID, PLUGIN_TITLE
PLONE_POLICY = 'password_policy'


def setupPasswordStrength(context):
    if context.readDataFile('passwordstrength.txt') is None:
        return
    site = context.getSite()
    install(site)


def removePasswordStrength(context):
    if context.readDataFile('passwordstrength-uninstall.txt') is None:
        return
    site = context.getSite()
    uninstall(site)


def install(portal):
    """
    This plugin needs to be installed in two places, the instance PAS where
    logins occur and the root acl_users.
    Different interfaces need to be activated for either case.
    """
    out = StringIO()
    print >> out, "Installing %s:" % PROJECTNAME

    plone_pas = getToolByName(portal, 'acl_users')

    existing = plone_pas.objectIds()
    if PLUGIN_ID not in existing:
        plugin = plone_pas.manage_addProduct[PROJECTNAME]
        plugin.manage_addPasswordStrength(PLUGIN_ID, PLUGIN_TITLE)
    activatePluginSelectedInterfaces(plone_pas, PLUGIN_ID, out, 'IValidationPlugin')
    activated = plone_pas.plugins.getAllPlugins(plugin_type='IValidationPlugin')['active']
    if PLUGIN_ID in activated and PLONE_POLICY in activated:
        activatePluginSelectedInterfaces(plone_pas, PLONE_POLICY, out, 'IValidationPlugin',
                                         disable=['IValidationPlugin'])

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()


def uninstall(portal):
    out = StringIO()
    print >> out, "Uninstalling %s:" % PROJECTNAME
    plone_pas = getToolByName(portal, 'acl_users')
    existing = plone_pas.objectIds()
    if PLUGIN_ID in existing:
#        plone_pas.manage_delObjects(PLUGIN_ID)
        activatePluginSelectedInterfaces(plone_pas, PLUGIN_ID, out, 'IValidationPlugin',
                                         disable=['IValidationPlugin'])
    if PLONE_POLICY in existing:
        activatePluginSelectedInterfaces(plone_pas, PLONE_POLICY, out, 'IValidationPlugin')


def activatePluginSelectedInterfaces(pas, plugin, out, selected_interfaces, disable=[]):
    """
    This is derived from PlonePAS's activatePluginInterfaces, but
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
