# Copyright (c) 2016 Platform9 systems. All rights reserved

from setuptools import setup, find_packages

setup(
    name='rampage',
    version='0.1',
    description='Break things',
    author='',
    author_email='',
    install_requires=[
        'pylint',
        'python-keystoneclient',
        'python-novaclient',
        'python-cinderclient',
        'python-glanceclient',
        'python-neutronclient',
        'requests'
    ],
    tests_require=[],
    test_suite='rampage.tests',
    packages=find_packages()
)
