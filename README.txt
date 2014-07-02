PasswordStrength

  This Pluggable Authentication Service (PAS) plugin validates
  passwords against regular expression rules. These rules can
  ensure a passwords strength such as minimum lenth and required
  characthers.
  This plugin contains a patch to plone to use PAS validation.

Requires:

 - PluggableAuthService and its dependencies

 - (optional) PlonePAS and its dependencies
 
 - Plone 4.3.


Installation

  Place the Product directory 'PasswordStength' in your 'Products/'
  directory. Restart Zope.

  In your PAS 'acl_users', select 'PasswordStrength' from the add
  list.  Give it an id and title, and push the add button.

  Enable the 'Validation' plugin interfaces in the after-add screen.
  
  Click on the properties tab and edit the validation rules
  
  To use with plone, you need to install PasswordStrength using quickinstaller

  That's it! Test it out.

Implementation

  A PAS plugin for Validation checks the password against each regular
  expression listed in the properties. Any rules that fail result in
  the associated error messages being returned.
  
  Included is a patch to Products.CMFPlone.RegistrationTool.RegistrationTool.testPasswordValidity.

TODO

  1. Patch or modify login_password.cpt to display directly the password constrains
     (<div class="formHelp" i18n:translate="" tal:define="constrains python:context.portal_registration.testPasswordValidity('');">
      Enter your new password. <span i18n:name="errors" tal:replace="constrains"/>
      </div>)
  
  2. Patch or modify passwordreset view to display directly the password constrains
  
  3. Do password expiration


Copyright, License, Author

  Copyright (c) 2007, PretaWeb, Australia,
   and the respective authors. All rights reserved.
 
  Author: Dylan Jay <software@pretaweb.com>

  License BSD-ish, see LICENSE.txt


Credits

  Thanks to Daniel Nouri and BlueDynamics for their
  NoDuplicateLogin which served as the base for this.
