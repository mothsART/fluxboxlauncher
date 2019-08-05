import os
import toml

from lib.i18n import _corrupt_toml
from lib.soft import Soft

class Conf:
    softs = []
    startup_stream = ''
    toml_stream = {}

    def __init__(self, user):
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

    def _contains(self, cmd):
        for soft in self.toml_stream:
            if self.toml_stream[soft]['cmd'].strip() == cmd:
                return True
        return False

    def sort_softs(self, soft):
        return int(soft.replace('soft-', ''))

    def load(self, lines):
        start_stream  = []
        self.cmd_list = []
        for soft_index in sorted(self.toml_stream, key=self.sort_softs):
            soft_conf = self.toml_stream[soft_index]
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
            if disabled:
                start_stream.append('# exec %s &\n' % cmd)
            else:
                start_stream.append('exec %s &\n' % cmd)
            soft = Soft(name, cmd, icon, generic)
            new_toml = dict(
                self.toml_stream, 
                **soft.to_dict(len(self.softs))
            )
            self.softs.append(soft)

        first_lines = []
        final_lines = []
        after_fluxbox = False
        for line in lines:
            if after_fluxbox or line.startswith('exec fluxbox'):
                final_lines.append(line)
                after_fluxbox = True
                continue
            if line.startswith('exec '):
                cmd = line.replace('exec ', '').replace(' &', '').strip()
                if self._contains(cmd):
                    continue
                self.toml_stream['soft-%s' % str(len(self.toml_stream) + 1)] = {
                    'cmd': cmd,
                    'name': cmd
                }
                first_lines.append('exec %s &\n' % cmd)
                continue
            if line.startswith('# exec '):
                cmd = line.replace('#', '').replace('exec ', '').replace('&', '').strip()
                if self._contains(cmd):
                    continue
                self.toml_stream['soft-%s' % str(len(self.toml_stream) + 1)] = {
                    'cmd': cmd,
                    'name': cmd,
                    'disabled': True
                }
                first_lines.append('# exec %s &\n' % cmd)
                continue
            first_lines.append(line)
        return ''.join(
            ''.join(first_lines)
            + ''.join(start_stream)
            + ''.join(final_lines)
        )

    def update_stream(self, lines, start_stream):
        first_lines = []
        final_lines = []
        after_fluxbox = False
        for line in lines:
            if after_fluxbox or line.startswith('exec fluxbox'):
                final_lines.append(line)
                after_fluxbox = True
                continue
            if line.startswith('exec '):
                continue
            if line.startswith('# exec '):
                continue
            first_lines.append(line)
        return ''.join(
            ''.join(first_lines)
            + ''.join(start_stream)
            + ''.join(final_lines)
        )

    def open(self):
        """Open conf files"""
        lines = []
        if os.path.isfile(self.start_path):
            with open(self.start_path, 'r') as f:
                lines = f.readlines()
        if os.path.isfile(self.toml_path):
            with open(self.toml_path, 'r') as d:
                try:
                    self.toml_stream = toml.loads(d.read())
                except:
                    print(
                        _corrupt_toml.format(self.toml_path)
                    )
        if len(self.toml_stream) == 0:
            return lines
        return lines

    def save(self):
        lines = self.open()
        # parse conf
        stream = self.load(lines)
        # save conf files
        with open(self.start_path, 'w') as f:
            f.write(stream)
        with open(self.toml_path,'w') as f:
            f.write(toml.dumps(self.toml_stream))
        if self.softs == []:
            self.load(lines)

    def update(self, start_stream, new_toml):
        with open(self.start_path, 'r') as f:
           lines = f.readlines()
        stream = self.update_stream(lines, start_stream)
        with open(self.start_path, 'w') as f:
            f.write(stream)
        with open(self.toml_path,'w') as f:
            f.write(toml.dumps(new_toml))

    def add(self, soft):
        for s in self.softs:
            if soft.cmd == s.cmd:
                return False
        start_stream = []
        for s in self.softs:
            if s.disabled:
                start_stream.append('# exec %s &\n' % s.cmd)
                continue
            start_stream.append('exec %s &\n' % s.cmd)
        self.softs.append(soft)
        self.update(
            start_stream,
            soft.to_dict(len(self.softs))
        )
        return True

    def remove(self, soft):
        if soft not in self.softs:
            return False
        self.softs.remove(soft)
        new_toml = {}
        inc = 0
        start_stream = []
        for s in self.softs:
            inc = inc + 1
            if s.disabled:
                start_stream.append('# exec %s &\n' % s.cmd)
            else:
                start_stream.append('exec %s &\n' % s.cmd)
            new_toml = dict(
                new_toml,
                **s.to_dict(inc)
            )
        self.update(start_stream, new_toml)
        return True


    def change_status(self, is_disabled):
        start_stream = []
        inc = 0
        new_toml = {}
        for s in self.softs:
            inc = inc + 1
            if is_disabled:
                start_stream.append('# exec %s &\n' % s.cmd)
            else:
                start_stream.append('exec %s &\n' % s.cmd)
            new_toml = dict(
                new_toml, 
                **s.to_dict(inc)
            )
        self.update(start_stream, new_toml)
