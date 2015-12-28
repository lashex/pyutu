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
    long_description=open("README.rst").read(),
    py_modules=['pyutu'],
    zip_safe=False,
    include_package_data=True,
    package_dir={'pyutu': 'pyutu'},
    install_requires=[
        'click>=6.2',
        'CacheControl>=0.11.5',
        'requests>=2.9.1'
    ],
    entry_points='''
        [console_scripts]
        pyutu=pyutu.cli:cli
        ''',
    test_suite='test_pyutu.suite',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)