from setuptools import setup, find_packages
import os

version = '0.4'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='Products.PasswordStrength',
    version=version,
    description="This Pluggable Authentication Service (PAS) plugin adds a password policy "
                "giving the possibility to define up to 5 regular expressions to validate "
                "a password. Default constrains are length, capital and lower letters, "
                "number and special characters.",
    long_description=(
        read('README.rst')
        + '\n\n' +
        read('CHANGES.rst')
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
        'plone.api',
        'collective.monkeypatcher',
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
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
