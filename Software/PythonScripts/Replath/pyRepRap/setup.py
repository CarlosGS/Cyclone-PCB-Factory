#!/usr/bin/env python

import os
from distutils.core import setup

def getDataFiles():
	data_files = []
	return data_files

setup(
	name='pyRepRap',
	version='0.3',
	author='Stefan Blanke',
	author_email='greenarrow@users.sourceforge.net',
	description='Python library to control RepRap firmware using the SNAP protocol.',
	packages=['reprap'],
	scripts=['scripts/reprapcontrol', 'scripts/wxreprapcontrol'],
	data_files = getDataFiles()
	
)


