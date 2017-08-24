"""
pyutu
-------------

"""
import os
from setuptools import setup


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def parse_version():
    """Extract the version without importing the client

    The client imports third party libraries that aren't guaranteed to be
    available at install time.
    """
    for line in read_file('pyutu/__init__.py').splitlines():
        if line.startswith('__version__'):
            version = line.split("'")[1]
            return version


setup(
    name='pyutu',
    version=parse_version(),
    url='https://github.com/lashex/pyutu',
    license=read_file('LICENSE'),
    author='Brett Francis',
    author_email='brett_francis@me.com',
    description='Python library for interaction with the AWS Pricing API',
    long_description=read_file('README.rst'),
    py_modules=['pyutu'],
    zip_safe=False,
    include_package_data=True,
    packages=['pyutu'],
    # package_dir={'pyutu': 'pyutu'},
    install_requires=[
        'click>=6.2',
        'CacheControl>=0.11.5',
        'requests>=2.9.1',
        'lockfile>=0.12.2'
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
