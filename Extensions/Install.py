from Products.CMFCore.utils import getToolByName,manage_addTool
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.ExternalMethod.ExternalMethod import ExternalMethod


from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes import listTypes
from Products.PasswordStrength import PROJECTNAME,product_globals

from zExceptions import NotFound

from StringIO import StringIO
import sys

class PloneSkinRegistrar:
    """
    Controls (un)registering of a layer in the skins tool:
     - the layer in the content of the skin tool
     - the layer in the path of all skins
    @author: U{Gilles Lenfant <glenfant@bigfoot.com>}
    @version: 0.1.0
    @ivar _layer: Name of the Product's subdirectory that contains
        the various layers for the Product.
    @type _layer: string
    @ivar _prodglobals: Globals from this Product.
    @type _propglobals: mapping object
    """

    def __init__(self, skinsdir, prodglobals):
        """Constructor
        @param skinsdir: Name of the Product's subdirectory that
            contains the various layers for the Product.
        @type skinsdir: string
        @param prodglobals: Globals from this Product.

            should be provided by Product's C{__init__.py} like this:

            C{product_globals = globals()}

        @type propglobals: mapping object
        @return: None
        """

        self._skinsdir = skinsdir
        self._prodglobals = prodglobals
        return

    def install(self, aq_obj,position=None,mode='after',layerName=None):
        """Installs and registers the skin resources
        @param aq_obj: object from which cmf site object is acquired
        @type aq_obj: any Zope object in the CMF
        @return: Installation log
        @rtype: string
        """

        rpt = '=> Installing and registering layers from directory %s\n' % self._skinsdir
        skinstool = getToolByName(aq_obj, 'portal_skins')

        # Create the layer in portal_skins

        try:
            if self._skinsdir not in skinstool.objectIds():
                addDirectoryViews(skinstool, self._skinsdir, self._prodglobals)
                rpt += 'Added "%s" directory view to portal_skins\n' % self._skinsdir
            else:
                rpt += 'Warning: directory view "%s" already added to portal_skins\n' % self._skinsdir
        except:
            # ugh, but i am in stress
            rpt += 'Warning: directory view "%s" already added to portal_skins\n' % self._skinsdir


        # Insert the layer in all skins
        # XXX FIXME: Actually assumes only one layer directory with the name of the Product
        # (should be replaced by a smarter solution that finds individual Product's layers)

        if not layerName:
            layerName = self._prodglobals['__name__'].split('.')[-1]

        skins = skinstool.getSkinSelections()

        for skin in skins:
            layers = skinstool.getSkinPath(skin)
            layers = [layer.strip() for layer in layers.split(',')]
            if layerName not in layers:
                try:
                    pos=layers.index(position)
                    if mode=='after': pos=pos+1
                except ValueError:
                    pos=len(layers)

                layers.insert(pos, layerName)

                layers = ','.join(layers)
                skinstool.addSkinSelection(skin, layers)
                rpt += 'Added "%s" to "%s" skin\n' % (layerName, skin)
            else:
                rpt += '! Warning: skipping "%s" skin, "%s" is already set up\n' % (skin, type)
        return rpt

    def uninstall(self, aq_obj):
        """Uninstalls and unregisters the skin resources
        @param aq_obj: object from which cmf site object is acquired
        @type aq_obj: any Zope object in the CMF
        @return: Uninstallation log
        @rtype: string
        """

        rpt = '=> Uninstalling and unregistering %s layer\n' % self._skinsdir
        skinstool = getToolByName(aq_obj, 'portal_skins')

        # Removing layer from portal_skins
        # XXX FIXME: Actually assumes only one layer directory with the name of the Product
        # (should be replaced by a smarter solution that finds individual Product's layers)

        if not layerName:
            layerName = self._prodglobals['__name__'].split('.')[-1]

        if layerName in skinstool.objectIds():
            skinstool.manage_delObjects([layerName])
            rpt += 'Removed "%s" directory view from portal_skins\n' % layerName
        else:
            rpt += '! Warning: directory view "%s" already removed from portal_skins\n' % layerName

        # Removing from skins selection

        skins = skinstool.getSkinSelections()
        for skin in skins:
            layers = skinstool.getSkinPath(skin)
            layers = [layer.strip() for layer in layers.split(',')]
            if layerName in layers:
                layers.remove(layerName)
                layers = ','.join(layers)
                skinstool.addSkinSelection(skin, layers)
                rpt += 'Removed "%s" to "%s" skin\n' % (layerName, skin)
            else:
                rpt += 'Skipping "%s" skin, "%s" is already removed\n' % (skin, layerName)
        return rpt
# /class PloneSkinRegistrar

def install(self):
    portal=getToolByName(self,'portal_url').getPortalObject()
    out = StringIO()
    classes=listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)

    print >> out, "Successfully installed %s." % PROJECTNAME
    sr = PloneSkinRegistrar('skins', product_globals)
    print >> out,sr.install(self)
    #sr = PloneSkinRegistrar('skins', product_globals)
    print >> out,sr.install(self,position='custom',mode='after',layerName=PROJECTNAME+'_public')

    #register folderish classes in use_folder_contents
    props=getToolByName(self,'portal_properties').site_properties
    use_folder_tabs=list(props.use_folder_tabs)
    print >> out, 'adding classes to use_folder_tabs:'
    for cl in classes:
        print >> out,  'type:',cl['klass'].portal_type
        if cl['klass'].isPrincipiaFolderish and not cl['klass'].portal_type in []:
            use_folder_tabs.append(cl['klass'].portal_type)

    props.use_folder_tabs=tuple(use_folder_tabs)

    #autoinstall tools
    for t in []:
        try:
            portal.manage_addProduct[PROJECTNAME].manage_addTool(t)
            # tools are not content. dont list it in navtree
        except:
            #heuristics for testing if an instance with the same name already exists
            #only this error will be swallowed.
            #Zope raises in an unelegant manner a 'Bad Request' error
            e=sys.exc_info()
            if e[0] != 'Bad Request':
                raise

    #hide tools in the navigation
    for t in []:
        try:
            if t not in self.portal_properties.navtree_properties.metaTypesNotToList:
                self.portal_properties.navtree_properties.metaTypesNotToList= \
                   list(self.portal_properties.navtree_properties.metaTypesNotToList) + \
                      [t]
        except TypeError, e:
            print 'Attention: could not set the navtree properties:',e

    # register tool in control panel
    try:
        portal_control_panel=getToolByName(self,'portal_control_panel_actions')
    except AttributeError:
        #portal_control_panel has been renamed in RC1 (grumpf)
        portal_control_panel=getToolByName(self,'portal_controlpanel',None)

    #auto build


    portal.left_slots=list(portal.left_slots)+[]
    portal.right_slots=list(portal.right_slots)+[]

    #try to call a custom install method
    #in 'AppInstall.py' method 'install'
    try:
        install = ExternalMethod('temp','temp',PROJECTNAME+'.AppInstall', 'install')
    except:
        install=None

    if install:
        print >>out,'Custom Install:'
        res=install(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom install'

    #try to call a workflow install method
    #in 'InstallWorkflows.py' method 'installWorkflows'
    try:
        installWorkflows = ExternalMethod('temp','temp',PROJECTNAME+'.InstallWorkflows', 'installWorkflows').__of__(self)
    except NotFound:
        installWorkflows=None

    if installWorkflows:
        print >>out,'Workflow Install:'
        res=installWorkflows(self,out)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no workflow install'

    return out.getvalue()

def uninstall(self):
    out = StringIO()
    classes=listTypes(PROJECTNAME)

    #unregister folderish classes in use_folder_contents
    props=getToolByName(self,'portal_properties').site_properties
    use_folder_tabs=list(props.use_folder_tabs)
    print >> out, 'removing classes from use_folder_tabs:'
    for cl in classes:
        print >> out,  'type:', cl['klass'].portal_type
        if cl['klass'].isPrincipiaFolderish and not cl['klass'].portal_type in []:
            if cl['klass'].portal_type in use_folder_tabs:
                use_folder_tabs.remove(cl['klass'].portal_type)

    props.use_folder_tabs=tuple(use_folder_tabs)

    #autouninstall tools
    for t in []:
        # undo: tools are not content. dont list it in navtree
        try:
            self.portal_properties.navtree_properties.metaTypesNotToList=list(self.portal_properties.navtree_properties.metaTypesNotToList)
            self.portal_properties.navtree_properties.metaTypesNotToList.remove(t)
        except ValueError:
            pass
        except:
            raise
    # unregister tool in control panel
    try:
        portal_control_panel=getToolByName(self,'portal_control_panel_actions')
    except AttributeError:
        #portal_control_panel has been renamed in RC1 (grumpf)
        portal_control_panel=getToolByName(self, 'portal_controlpanel', None)
    #auto build




    #try to call a custom uninstall method
    #in 'AppInstall.py' method 'uninstall'
    try:
        uninstall = ExternalMethod('temp','temp',PROJECTNAME+'.AppInstall', 'uninstall')
    except:
        uninstall=None

    if uninstall:
        print >>out,'Custom Uninstall:'
        res=uninstall(self)
        if res:
            print >>out,res
        else:
            print >>out,'no output'
    else:
        print >>out,'no custom uninstall'

    return out.getvalue()
