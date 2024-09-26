Changes
=======

0.5.0 (2024-09-26)
------------------

- Add support for Python 3, Plone 5.2 and Plone 6. Drop support for Plone 5.1 and older.
  [pbauer, djay]

- Fix can not change weak password
  [ivanteoh]


0.4 (2015-06-05)
----------------

- Updated Spanish translation.
  [macagua]
- Removed old code and templates
  [djay]
- Added buildout and robot tests for Plone 4.1, 4.2, 4.3
  [sgeulette]
- Dont't skip password validation for manager
  [sgeulette]
- Skip password validation for generated password
  [sgeulette]
- Added i18n and french translation.
  [sgeulette]
- Added travis configuration
  [sgeulette]
- Added pwreset_form and test
  [sgeulette]

0.3.2 (2015-06-05)
------------------

- Updated README file. [macagua]
- Added QA and testing buildout configuration. [macagua]
- Added more strings classifiers items for this packages. [macagua]
- Added Spanish translation. [macagua]
- Added i18n support. [macagua]

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
