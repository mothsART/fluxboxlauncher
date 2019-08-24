import os
import toml

from lib.i18n import _corrupt_toml
from lib.soft import Soft

class Conf:
    def __init__(self, user):
        self.first_lines = []
        self.softs = []
        self.last_lines = []
        self.toml_stream = {}
        self.DEBUG = False
        self.toml_path = 'start.toml'
        self.start_path = 'startup'
        if os.path.isdir('.git'):
            self.DEBUG = True
        dirname = "/home/%s/.fluxbox/" % user
        if not os.path.isdir(dirname):
            return
        self.toml_path  = dirname + 'start.toml'
        self.start_path = dirname + 'startup'

    def lines(self):
        lines = []
        for soft in self.softs:
            lines.append(str(soft))
        return lines

    def __str__(self):
        return ''.join(
            ''.join(self.first_lines)
            + ''.join(self.lines())
            + ''.join(self.last_lines)
        )

    def _contains(self, cmd):
        for soft in self.toml_stream:
            if self.toml_stream[soft]['cmd'].strip() == cmd:
                return True
        return False

    def sort_softs(self, soft):
        return int(soft.replace('soft-', ''))

    def _load_toml(self, toml):
        self.cmd_list = []
        if toml == None or toml == {}:
            return
        for soft_index in sorted(toml, key=self.sort_softs):
            soft_conf = toml[soft_index]
            if 'cmd' not in soft_conf:
                continue
            if soft_conf['cmd'] in self.cmd_list:
                continue

            cmd = soft_conf['cmd']
            self.cmd_list.append(cmd)
            name = ''
            if 'name' in soft_conf:
                name = soft_conf['name']
            icon = ''
            if 'icon' in soft_conf:
                icon = soft_conf['icon']
            generic = ''
            if 'generic' in soft_conf:
                soft.generic = soft_conf['generic']
            disabled = ''
            if 'disabled' in soft_conf:
                disabled = soft_conf['disabled']
            soft = Soft(name, cmd, icon, generic)
            new_toml = dict(
                self.toml_stream, 
                **soft.to_dict(len(self.softs))
            )
            self.softs.append(soft)

    def _load_lines(self, lines):
        self.first_lines = []
        self.last_lines = []
        after_fluxbox = False
        for line in lines:
            if after_fluxbox or line.startswith('exec fluxbox'):
                self.last_lines.append(line)
                after_fluxbox = True
                continue
            cmd = None
            if line.startswith('exec '):
                cmd = line.replace('exec ', '').replace(' &', '').strip()
                self.toml_stream['soft-%s' % str(len(self.toml_stream) + 1)] = {
                    'cmd': cmd,
                    'name': cmd
                }
                new_soft = Soft(cmd, cmd, '', '')
            elif line.startswith('# exec '):
                cmd = line.replace('#', '').replace('exec ', '').replace('&', '').strip()
                self.toml_stream['soft-%s' % str(len(self.toml_stream) + 1)] = {
                    'cmd': cmd,
                    'name': cmd,
                    'disabled': True
                }
                new_soft = Soft(cmd, cmd, '', '')
                new_soft.disabled = True
            else:
                self.first_lines.append(line)
            if not cmd:
                continue
            for soft in self.softs:
                if soft.cmd == cmd:
                    continue
            #new_toml = dict(
            #    toml_stream, 
            #    **soft.to_dict(len(self.softs))
            #)
            self.softs.append(new_soft)

    def load(self, lines, toml = None):
        self._load_toml(toml)
        self._load_lines(lines)


    def open(self):
        """Open conf files"""
        if os.path.isfile(self.start_path):
            with open(self.start_path, 'r') as f:
                self.load(f.readlines())
        if os.path.isfile(self.toml_path):
            with open(self.toml_path, 'r') as d:
                try:
                    self.toml_stream = toml.loads(d.read())
                except:
                    print(
                        _corrupt_toml.format(self.toml_path)
                    )

    def save(self):
        with open(self.start_path, 'w') as f:
            f.write(str(self))
        with open(self.toml_path,'w') as f:
            f.write(toml.dumps(self.toml_stream))

    def add(self, soft):
        for s in self.softs:
            if soft.cmd == s.cmd:
                return False
        self.softs.append(soft)
        return True

    def remove(self, soft):
        if soft not in self.softs:
            return False
        self.softs.remove(soft)
        return True

    def change_status(self, is_disabled):
        start_stream = []
        inc = 0
        new_toml = {}
        for s in self.softs:
            inc = inc + 1
            new_toml = dict(
                new_toml, 
                **s.to_dict(inc)
            )

    def get_soft(self, cmd):
        for soft in self.softs:
            if soft.cmd == cmd:
                return soft
                break
        return None

    def soft_exist(self, soft):
        for s in self.softs:
            if s.cmd == soft.cmd:
                return True
        return False
