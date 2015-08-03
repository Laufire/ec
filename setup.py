#!/usr/bin/env python

try:
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup


with open('README.rst') as readme_file:
  readme = readme_file.read()

requirements = [
  # ToDo: put package requirements here
]

test_requirements = [
  # ToDo: put package test requirements here
]

import ec

setup(
  name='ec',
  version=ec.__version__,
  description="ec - a simpler, yet better implementation of Commander, a module launcher.",
  long_description=readme,
  author=ec.__author__,
  author_email=ec.__email__,
  url='https://github.com/Laufire/ec',
  download_url='https://pypi.python.org/pypi/ec',
  packages=find_packages(),
  platforms='any',
  include_package_data=True,
  install_requires=requirements,
  license="MIT",
  zip_safe=False,
  keywords='ec command line cli interactive launch argument script dir shell dispatch decorator task arg group sub-commands type custom-type',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Natural Language :: English',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development',
    'Topic :: Utilities',
  ],
  entry_points={'console_scripts': ['ec=ec.__main__:main']},
  test_suite='tests',
  tests_require=test_requirements
)
