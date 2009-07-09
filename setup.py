#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='TrendStream', version='0.1',
    description='Visualises a stream of tweets on the current trending topics.',
    author='Adam Greig', author_email='random@randomskk.net',
    url='http://randomskk.net/',
    py_modules=['trendstream', 'twitter', 'gui'],
    requires=['simplejson', 'Tkinter'],
    data_files=[('', 'README')]
    )
