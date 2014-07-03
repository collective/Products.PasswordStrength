from setuptools import setup, find_packages
import sys, os

version = '0.3.2.dev0'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='Products.PasswordStrength',
      version=version,
      description="This Pluggable Authentication Service (PAS) plugin adds a password policy "
                  "giving the possibility to define up to 5 regular expressions to validate "
                  "a password. Default constrains are length, capital and lower letters, "
                  "number and special characters.",
      long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zope PAS',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='http://plone.org/products/Products.PasswordStrength',
      license='GPL',
      packages=find_packages(),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          # Products.PluggableAuthService is a dep, but can't be explicit in Plone 3.
      ],
      extras_require={
          'test': [
              'plone.app.robotframework',
              'plone.app.testing',
              'plone.browserlayer',
              'robotsuite',
              'unittest2',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
