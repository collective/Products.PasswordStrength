Changes
=======

0.3.2 (unreleased)
------------------

- Added buildout and robot tests [sgeulette]
- Dont't skip password validation for manager [sgeulette]
- Skip password validation for generated password [sgeulette]
- Added i18n and french translation. [sgeulette]
- Added travis [sgeulette]

0.3.1 (2013-11-20)
------------------

- Bugfix for use inside change-password
- Don't validate password strength of old password
  [pysailor]

0.3 (2013-08-18)
----------------

- Added a monkey-patch for the zope.schema Password field to validate
  the password. This is necessary for the Plone 4 @@new-user form to
  work well. [regebro]


Earlier versions
----------------

0.2 - Packaged as egg. Plone 3.1 compatible

0.1 - Initial version. Plone 2.5 compatible
