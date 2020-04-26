![](./ressources/logo.svg)

# FluxboxLauncher

[![Build Status](https://travis-ci.org/mothsART/fluxboxlauncher.png?branch=master)](https://travis-ci.org/mothsART/fluxboxlauncher)
[![LICENSE](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)

## Introduction

Manage application startup when FluxBox is launched :
FluxBoxlauncher is a graphical application with drag-and-drop functionality.

### Last stable version

[![Packaging status](https://repology.org/badge/vertical-allrepos/fluxboxlauncher.svg)](https://repology.org/project/fluxboxlauncher/versions)

- Ubuntu 18.04, 19.10 and 20.04: [PPA](https://launchpad.net/~jerem-ferry/+archive/ubuntu/fluxbox)

## Dependances

python-gtk

## launch

```sh
./fluxboxlauncher.py USERNAME
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

ie : in french

```sh
msgfmt -o locale/fr/LC_MESSAGES/fluxboxlauncher.mo locale/fr/LC_MESSAGES/fluxboxlauncher.po
```

## Tests

```sh
python3 -m unittest flxl/tests/tests.py
```

## Create a Debian package

```sh
git clone https://github.com/mothsART/fluxboxlauncher.git
cd fluxboxlauncher
dpkg-buildpackage -us -uc
```

and launch with :

```sh
sudo dpkg -i ../fluxboxlauncher_*_all.deb
```

## Create a Nix package

```sh
nix-build
```

install locally :

```sh
nix-env -if .
```

launch locally :

```sh
nix run -c fluxboxlauncher
```
