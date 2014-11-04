from Products.PluggableAuthService.interfaces.plugins import IValidationPlugin
from Products.CMFCore.utils import getToolByName
from Products.PasswordStrength import _
from plone.app.users.browser.register import BaseRegistrationForm
from plone.app.users.browser.personalpreferences import PasswordAccountPanel


# monkey patch to be used for Plone < 4.3
def testPasswordValidity(self, password, confirm=None):

    """ Verify that the password satisfies the portal's requirements.

    o If the password is valid, return None.
    o If not, return a string explaining why.
    """
    if confirm is not None and confirm != password:
        return _('Your password and confirmation did not match. Please try again.')

    if not password:
        err = [_('You must enter a password')]
    else:
        err = []

    # We escape the test if it looks like a generated password
    if password and password.startswith('G-') and len(password) == len(self.origGeneratePassword()) + 2:
        return None

    # Use PAS to test validity
    pas_instance = self.acl_users
    plugins = pas_instance._getOb('plugins')
    validators = plugins.listPlugins(IValidationPlugin)
    for validator_id, validator in validators:
        user = None
        set_id = ''
        set_info = {'password': password}
        errors = validator.validateUserInfo(user, set_id, set_info)
        err += [info['error'] for info in errors if info['id'] == 'password']
    if err:
        return '. '.join(err)
    else:
        return None


# monkey patch to be used for Plone < 4.3
def updateRegistrationForm(self):
    # Change the password description based on PAS Plugin
    # The user needs a list of instructions on what kind of password is required.
    # We'll reuse password errors as instructions e.g. "Must contain a letter and a number".
    # Assume PASPlugin errors are already translated
    if self.form_fields and self.form_fields.get('password', None):
        registration = getToolByName(self.context, 'portal_registration')
        err_str = registration.testPasswordValidity('')
        if err_str:
            self.form_fields['password'].field.description = err_str
    super(BaseRegistrationForm, self).update()


def updatePasswordAccountPanel(self):
    if self.form_fields and self.form_fields.get('new_password', None):
        registration = getToolByName(self.context, 'portal_registration')
        err_str = registration.testPasswordValidity('')
        if err_str:
            self.form_fields['new_password'].field.description = err_str
    super(PasswordAccountPanel, self).update()
