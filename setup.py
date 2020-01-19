#!/usr/bin/env python3

import os
import glob
from setuptools import setup

GETTEXT_NAME="apturl"
I18NFILES = []
for filepath in glob.glob("locale/*/LC_MESSAGES/*.mo"):
    lang = filepath[len("locale/"):]
    targetpath = os.path.dirname(os.path.join("share/locale", lang))
    I18NFILES.append((targetpath, [filepath]))

setup(
    name='fluxboxlauncher',
    version=0.1,
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
