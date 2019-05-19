#!/usr/bin/env python
# coding=utf-8

from setuptools import find_packages, setup

setup(
    name='titamu',
    version=0.10,
    description=(
        'A command line tool to talk with RHV environment'
    ),
    long_description=open('README.rst').read(),
    author='Chen Chen',
    author_email='cchenlp@qq.com',
    license='BSD License',
    packages=['titamu'],
    platforms=["all"],
    url='https://github.com/cchen666/titamu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],
    scripts=['titamu/bin/titamu'],
    install_requires=[
    'ovirt-engine-sdk-python >= 4.2.9',
    'prettytable >= 0.7.2',
    ],
)
