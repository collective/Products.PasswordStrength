.. contents::

PasswordStrength
================

This plugin works with Plone to allow an administrator to create
a password policy for their site. Once installed it provides a
Pluggable Authentication Service (PAS) plugin where you can create
as many regular expressions rules which will each be applied against
passwords during user registration. For example these rules can
ensure a passwords strength such as minimum length and required
letters or special characters.

In Plone 4.3 and above this plugin works directly with Plones inbuilt
password policy api. In Plone 4.2 and below this plugin contains a patch 
to plone to use PAS validation.

Tests
=====

This package is tested using Travis CI on Plone 4.1, 4.2, 4.3
The current status is :

.. image:: https://travis-ci.org/collective/Products.PasswordStrength.png
    :target: http://travis-ci.org/collective/Products.PasswordStrength

Requires
========

 - PlonePAS and its dependencies
 - Plone 4.1, 4.2 or 4.3
 - better: Products.PasswordResetTool >= 2.0.18 (clearer password reset mail)
 - better: plone.app.locales >= 4.3.5 (clearer translations in password reset mail)

Installation
============

1. Install Products.PasswordStrength using buildout like any other Plone plugin. 
2. Once activated within your site you select ZMI > acl_users > password_strength_plugin
3. Click on the properties tab and edit the validation rules. The rule error text will be used for both
 the password field hint to tell the user what kind of password they can pick, and also if they fail
 to enter a password that matches that rule.

That's it! Test it out.

Implementation
==============

A PAS plugin for Validation checks the password against each regular
expression listed in the properties. Any rules that fail result in
the associated error messages being returned.

Plone doesn't use PAS to validate passwords, so included is a patch to
Products.CMFPlone.RegistrationTool.RegistrationTool.testPasswordValidity
which makes plone use PAS validation plugins.

TODO
====

1. Patch or modify login_password.cpt to display directly the password constraints
   (<div class="formHelp" i18n:translate="" tal:define="constrains python:context.portal_registration.testPasswordValidity('');">
   Enter your new password. <span i18n:name="errors" tal:replace="constrains"/></div>)

2. Do password expiration


Contribute
==========

- Source Code: https://github.com/collective/Products.PasswordStrength/
- Issue Tracker: https://github.com/collective/Products.PasswordStrength/issues


License
==========================

License BSD-ish, see LICENSE.txt

Credits
=======

Original Author: Dylan Jay <software@pretaweb.com>. Sponsored by PretaGov.com

Thanks to Daniel Nouri and BlueDynamics for their
NoDuplicateLogin which served as the base for this.

Thanks to the following for improvements to this plugin:

- sgeulette
- pysailor
- regebro
- macagua
