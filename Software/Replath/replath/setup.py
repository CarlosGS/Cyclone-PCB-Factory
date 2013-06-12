#!/usr/bin/env python

import os
from distutils.core import setup

def getDataFiles():
	data_files = []
	files = []
	for f in os.listdir('replath/graphics'):
		if f != ".svn":
			files.append( os.path.join('replath/graphics', f) )
	data_files.append( ('share/replath/icons', files) )

	data_files += [
		( 'share/applications',
			['replath/misc/replath.desktop'] ),
		( 'share/replath/plugins/import',
			['replath/plugins/import/dxf_lib.py',
			'replath/plugins/import/dxf_import.py',
			'replath/plugins/import/dxf_prefpanel.py',
			'replath/plugins/import/gerber_lib.py',
			'replath/plugins/import/gerber_import.py',
			'replath/plugins/import/gerber_prefpanel.py',
			'replath/plugins/import/svg_lib.py',
			'replath/plugins/import/svg_import.py',
			'replath/plugins/import/svg_prefpanel.py',
			'replath/plugins/import/itl_import.py',
			'replath/plugins/import/itl_prefpanel.py'] ),
		( 'share/replath/plugins/toolhead',
			['replath/plugins/toolhead/pen_toolhead.py',
			'replath/plugins/toolhead/pen_prefpanel.py',
			'replath/plugins/toolhead/router_toolhead.py',
			'replath/plugins/toolhead/paintbrush_toolhead.py'] ),
		( 'share/replath/plugins/output',
			['replath/plugins/output/reprap_output.py',
			'replath/plugins/output/reprap_prefpanel.py',
			'replath/plugins/output/itl_output.py',
			'replath/plugins/output/itl_prefpanel.py',
			'replath/plugins/output/svg_output.py',
			'replath/plugins/output/gcode_output.py',
			'replath/plugins/output/gcode_prefpanel.py'] )
	]
	return data_files

setup(
	name='pyRepRap',
	version='0.3',
	author='Stefan Blanke',
	author_email='greenarrow@users.sourceforge.net',
	description='Python library to control RepRap firmware using the SNAP protocol.',
	packages=['replath'],
	scripts=['scripts/replath'],
	data_files = getDataFiles()
	
)


