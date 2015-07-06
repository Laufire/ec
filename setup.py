#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

from ec import __info__

setup(
    name='ec',
    version=__info__.__version__,
    description="ec - a simpler, yet better implementation of Commander, a module launcher.",
    long_description=readme,
    author=__info__.__author__,
    author_email=__info__.__email__,
    url='https://github.com/Laufire/ec',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='ec command line cli interactive launch argument script dir shell dispatch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
        'ec=ec.__main__:main',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements
)
