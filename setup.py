"""
pyutu
-------------

"""
import os
from setuptools import setup
from pyutu import __version__


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


setup(
    name='pyutu',
    version=__version__,
    url='https://github.com/lashex/pyutu',
    license=open("LICENSE").read(),
    author='Brett Francis',
    author_email='brett_francis@me.com',
    description='Python library for interaction with the AWS Pricing API',
    long_description=open_file("README.rst").read(),
    py_modules=['pyutu'],
    zip_safe=False,
    include_package_data=True,
    package_data={'pyutu': ['_version']},
    packages=["pyutu"],
    # package_dir={'pyutu': 'pyutu'},
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