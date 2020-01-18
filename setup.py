from setuptools import setup


setup(
    name='fluxboxlauncher',
    version=0.1,
    description=(
        '...'
    ),
    author='mothsart',
    author_email='ferryjeremie@free.fr',
    url='https://github.com/mothsart/fluxboxlauncher',
    packages=[ 'fluxboxlauncher' ],
    entry_points={
        'console_scripts': [
            'fluxboxlauncher = fluxboxlauncher.main:main'
        ]
    }
)
