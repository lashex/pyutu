"""
pyutu
-------------

"""
from setuptools import setup

import os

setup(
    name='pyutu',
    version=open(os.path.join('pyutu', '_version')).read().strip(),
    url='https://github.com/lashex/pyutu',
    license=open("LICENSE").read(),
    author='Brett Francis',
    author_email='brett_francis@me.com',
    description='Python library for interaction with the AWS Pricing API',
    long_description=__doc__,
    py_modules=['pyutu'],
    zip_safe=False,
    include_package_data=True,
    package_dir={'pyutu': 'pyutu'},
    install_requires=[
        'click', 'CacheControl', 'requests'
    ],
    entry_points='''
        [console_scripts]
        pyutu=pyutu.cli:cli
        ''',
    test_suite='pyutu.suite',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)