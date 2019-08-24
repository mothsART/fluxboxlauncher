# FluxboxLauncher

[![Build Status](https://travis-ci.org/mothsART/fluxboxlauncher.png?branch=master)](https://travis-ci.org/mothsART/fluxboxlauncher)

[![LICENSE](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)

[![](./logo.png)]()

## Dependances

python-gtk
python-toml

## launch

```sh
python ./fluxboxlauncher.py USERNAME
```

## i18n

Create pot file :

```sh
pygettext -o fluxboxlauncher.pot ./fluxboxlauncher.py
```

Compile po file to mo :

```sh
msgfmt -o locale/{lang}/LC_MESSAGES/fluxboxlauncher.mo locale/{lang}/LC_MESSAGES/fluxboxlauncher.po
```

## Tests

```sh
python3 -m unittest tests/tests.py
```

## Create a Debian package

```sh
git clone https://github.com/mothsART/fluxboxlauncher.git
cd fluxboxlauncher
dpkg-buildpackage -us -uc
```
