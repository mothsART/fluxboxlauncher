#!/usr/bin/env python3

import glob
import os

from flxl import __version__

from setuptools import setup

I18NFILES = []
for filepath in glob.glob('flxl/locale/*/LC_MESSAGES/*.mo'):
    lang = filepath[len('flxl/locale/'):]
    targetpath = os.path.dirname(os.path.join('share/locale', lang))
    I18NFILES.append((targetpath, [filepath]))

setup(
    name='fluxboxlauncher',
    version=__version__,
    description=(
        'A Gui editor (gtk) ',
        'to configure applications launching on a fluxbox session'
    ),
    author='mothsart',
    author_email='ferryjeremie@free.fr',
    url='https://github.com/mothsart/fluxboxlauncher',
    packages=['flxl', 'flxl.lib'],
    data_files=I18NFILES,
    entry_points={
        'console_scripts': [
            'fluxboxlauncher = flxl.main:main'
        ]
    }
)
