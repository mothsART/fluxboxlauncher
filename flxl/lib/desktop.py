import os
import locale
global_lang = locale.getlocale()[0]


def get_info(desktopfile, lang=None):
    '''return infos from a .desktop file'''
    if not lang:
        lang = global_lang
    name, cmd, icon, generic = '', '', '', ''
    nameloc = False
    geneloc = False

    with open(desktopfile, 'r') as d:
        df = d.readlines()
    for l in df:
        if generic == '' or not geneloc:
            if l.startswith('GenericName[{0}]='.format(lang)):
                generic = l.replace(
                    'GenericName[{0}]='.format(lang), ''
                ).strip()
                geneloc = True
            elif l.startswith('GenericName='.format(lang)):
                generic = l.replace(
                    'GenericName='.format(lang), ''
                ).strip()
        if name == '' or not nameloc:
            if l.startswith('Name[{0}]='.format(lang)):
                name = l.replace(
                    'Name[{0}]='.format(lang), ''
                ).strip()
                nameloc = True
            elif l.startswith('Name='):
                name = l.replace('Name=', '').strip()
        if cmd == '' and l.startswith('Exec='):
            cmd = l.replace('Exec=', '').strip()
            cmd = cmd.split('%')[0].strip()
        if icon == '' and l.startswith('Icon='):
            icon = l.replace('Icon=', '').strip()
            if not os.path.exists(icon):
                icon = os.path.splitext(
                    icon
                )[0]
    return name, cmd, icon, generic
