#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="django-onesky-trans",
    version='0.1.5',
    url='http://github.com/django-onesky-trans',
    author='Bahattin Cinic',
    author_email='bahattincinic@gmail.com',
    description='OneSky integration for your Django app',
    packages=find_packages(),
    install_requires=[
        'django>=1.4',
        'polib>=1.0',
        'requests>=2.0'
    ],
    license='MIT',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ]
)
