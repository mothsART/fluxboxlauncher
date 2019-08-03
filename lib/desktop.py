import os
import locale


def get_info(desktopfile):
    """return infos from a .desktop file"""
    name, cmd, icon, generic= "", "", "", ""
    nameloc = False
    geneloc = False
    lang = locale.setlocale(locale.LC_ALL, "")[0:2]
    with open(desktopfile, 'r') as d:
        df = d.readlines()
    for l in df:
        if generic == "" or geneloc == False:
            if l.startswith('GenericName[{0}]='.format(lang)):
                generic = l.replace(
                    'GenericName[{0}]='.format(lang),''
                ).strip()
                geneloc = True
            elif l.startswith('GenericName='.format(lang)):
                generic = l.replace(
                    'GenericName='.format(lang),''
                ).strip()
        if name == "" or nameloc == False:
            if l.startswith('Name[{0}]='.format(lang)):
                name = l.replace(
                    'Name[{0}]='.format(lang),''
                ).strip()
                nameloc = True
            elif l.startswith('Name='):
                name = l.replace('Name=', '').strip()
        if cmd == "" and l.startswith('Exec='):
            cmd = l.replace('Exec=', '').strip()
            cmd = cmd.split('%')[0].strip()
        if icon == "" and l.startswith('Icon='):
            icon = os.path.splitext(
                l.replace('Icon=', '').strip()
            )[0]
    return name, cmd, icon, generic
