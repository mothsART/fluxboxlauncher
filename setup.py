#!/usr/bin/env python3

import os
import glob
from setuptools import setup
from flxl import __version__

I18NFILES = []
for filepath in glob.glob("flxl/locale/*/LC_MESSAGES/*.mo"):
    lang = filepath[len("flxl/locale/"):]
    targetpath = os.path.dirname(os.path.join("share/locale", lang))
    I18NFILES.append((targetpath, [filepath]))

setup(
    name='fluxboxlauncher',
    version=__version__,
    description=(
        '...'
    ),
    author='mothsart',
    author_email='ferryjeremie@free.fr',
    url='https://github.com/mothsart/fluxboxlauncher',
    packages=[ 'flxl', 'flxl.lib' ],
    data_files= I18NFILES,
    entry_points={
        'console_scripts': [
            'fluxboxlauncher = flxl.main:main'
        ]
    }
)
