PasswordStrength
================

This Pluggable Authentication Service (PAS) plugin validates
passwords against regular expression rules. These rules can
ensure a passwords strength such as minimum lenth and required
characters.
This plugin contains a patch to plone to use PAS validation.

Requires
--------

- PluggableAuthService and its dependencies

- (optional) PlonePAS and its dependencies

- Plone 4.1 or 4.2.


Installation
------------

Install ``Products.PasswordStength`` by adding it to your buildout: ::

   [buildout]

    ...

    eggs =
        Products.PasswordStength


and then running ``bin/buildout`` ans start the Zope services.

To use with plone, you need to install PasswordStrength using
``portal_quickinstaller`` from ZMI.

Then go to the ``acl_users`` into Plone object and click on
``password_strength_plugin``, click on the ``Properties`` tab and
edit the validation rules.

That's it! Test it out.

----

**Zope2 product**

Place the Product directory 'PasswordStength' in your 'Products/'
directory. Restart Zope.

In your PAS 'acl_users', select 'PasswordStrength' from the add
list.  Give it an id and title, and push the add button.

Enable the 'Validation' plugin interfaces in the after-add screen.

Click on the properties tab and edit the validation rules

That's it! Test it out.

**Note:** PasswordStength doesn't currently generate new passwords. This means that
you will need to change Plones security settings such that users manually enter
passwords rather than autogenerate them.


Implementation
--------------

A PAS plugin for Validation checks the password against each regular
expression listed in the properties. Any rules that fail result in
the associated error messages being returned.

Plone doesn't use PAS to validate passwords so included is a patch to
Products.CMFPlone.RegistrationTool.RegistrationTool.testPasswordValidity
which makes plone use PAS validation plugins.

TODO
----

#. Do password generation from regexp. This looks possible
     http://stackoverflow.com/questions/492716/reversing-a-regular-expression-in-python

#. Do password expiration


Contribute
----------

- Source Code: https://github.com/collective/Products.PasswordStrength/
- Issue Tracker: https://github.com/collective/Products.PasswordStrength/issues


License
-------

Copyright, License, Author

  Copyright (c) 2007, PretaWeb, Australia,
   and the respective authors. All rights reserved.

  Author: Dylan Jay <software@pretaweb.com>

  License BSD-ish, see LICENSE.txt


Credits
-------

  Thanks to Daniel Nouri and BlueDynamics for their
  `NoDuplicateLogin <https://pypi.python.org/pypi/Products.NoDuplicateLogin>`_ which served as the base for this.