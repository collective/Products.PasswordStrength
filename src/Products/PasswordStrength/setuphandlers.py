import logging
from smtplib import SMTPException
from six import StringIO
from Products.CMFCore.utils import getToolByName
from plone import api
from Products.PasswordStrength.plugin import PROJECTNAME, PLUGIN_ID, PLUGIN_TITLE
PLONE_POLICY = 'password_policy'
logger = logging.getLogger('Products.PasswordStrength: setuphandlers')


def setupPasswordStrength(context):
    site = api.portal.get()
    install(site)


def removePasswordStrength(context):
    site = api.portal.get()
    uninstall(site)


def install(portal):
    """
    This plugin needs to be installed in two places, the instance PAS where
    logins occur and the root acl_users.
    Different interfaces need to be activated for either case.
    """
    out = StringIO()
    print("Installing %s:" % PROJECTNAME, file=out)

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

    print("Successfully installed %s." % PROJECTNAME, file=out)
    return out.getvalue()


def uninstall(portal):
    out = StringIO()
    print("Uninstalling %s:" % PROJECTNAME, file=out)
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
                print(" - Disabling: " + info['title'], file=out)
            else:
                activatable.append(interface_name)
                print(" - Activating: " + info['title'], file=out)
    plugin_obj.manage_activateInterfaces(activatable)
    print(plugin + " activated.", file=out)


def list_append(lst, elem):
    """
        Append in a list and return the appended element
    """
    lst.append(elem)
    return elem


def reset_passwords(context):
    """
        Reset all users passwords
    """
    portal = api.porta.get()
    regtool = portal.portal_registration
    logs = []
    logger.info(list_append(logs, "Resetting all users passwords"))
    for user in portal.portal_membership.listMembers():
        pw = regtool.generatePassword()
        user.setSecurityProfile(password=pw)
        # copy from plone.app.controlpanel.usergroups.py
        immediate = not portal.MailHost.smtp_queue
        try:
            regtool.mailPassword(user.id, portal.REQUEST, immediate=immediate)
        except SMTPException as e:
            logger.exception(list_append(logs, str(e)))
    logger.info(list_append(logs, "Reset done"))
    return '\n'.join(logs)
