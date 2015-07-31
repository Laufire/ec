"""An autodoc inspired sphinx exetnsion, that could document ec based scripts and their members."""

import os
import sys
from setuptools import setup, find_packages

requirements = [
	'sphinx',
]

test_requirements = [
	'docutils>=0.10',  'sphinx'
]

from eccontrib import sphinxdoc

setup(
	name='eccontrib-sphinxdoc',
	version=sphinxdoc.__version__,
	url='https://github.com/Laufire/ec/sphinxdoc',
	# download_url='http://pypi.python.org/pypi/eccontrib-sphinxdoc',
	license='MIT',
	author=sphinxdoc.__author__,
	author_email=sphinxdoc.__email__,
	description='A sphinx extension for documenting ec based scripts.',
	long_description=__doc__,
	zip_safe=False,
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Console',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Topic :: Documentation',
		'Topic :: Utilities',
		'Framework :: Sphinx',
		'Framework :: Sphinx :: Extension',
	],
	keywords='sphinxdoc sphinx contrib extension laufire ec',
	platforms='any',
	packages=find_packages(),
	include_package_data=True,
	install_requires=requirements,
	test_suite='tests',
	tests_require=test_requirements,
	namespace_packages=['eccontrib']
)