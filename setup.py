from setuptools import setup, find_packages
import sys, os

version = '0.3.2'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='Products.PasswordStrength',
      version=version,
      description="This Pluggable Authentication Service (PAS) plugin will lock a \
                   login after a predetermined number of incorrect attempts. Once \
                   locked, the user will be shown a page that tells them to contact \
                   their administrator to unlock.",
      long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.txt')
        ),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Zope2",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Zope",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        ],
      keywords='PAS Plugins Zope password strength',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='https://plone.org/products/passwordstrength',
      license='BSD',
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
              'plone.app.testing',
              'plone.app.robotframework'
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
