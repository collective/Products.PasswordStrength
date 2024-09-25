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


Tests
=====

This package is tested using Travis CI on Plone 5.2 and 6.0.
For older

Requires
========

 - PlonePAS and its dependencies
 - Plone 5.2 or 6.0
 - For Plone 4.1, 4.2, 4.3 , 5.0 and 5.1 use Versions <> 0.5 or source-checkouts.

Installation
============

1. Add Products.PasswordStrength to your buildout like any other Plone plugin.
2. Add Products.PasswordStrength in the addon-controlpanel (prefs_install_products_form)
3. You can configure the plugin in teh ZMI in
   /acl_users/password_strength_plugin/manage_propertiesForm

That's it! Test it out.

Implementation
==============

A PAS plugin for Validation checks the password against each regular
expression listed in the properties. Any rules that fail result in
the associated error messages being returned.

TODO
====

1. Do password expiration?


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
- pbauer
