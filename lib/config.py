import os
from os.path import join, exists

from lib.soft import Soft
from lib.desktop import get_info

class Conf:
    def __init__(self, user):
        """Intialisation fluxboxlauncher config"""
        self.first_lines = []
        self.softs = []
        self.last_lines = []
        self.DEBUG = False
        self.start_path = 'startup'
        if os.path.isdir('.git'):
            self.DEBUG = True
        dirname = "/home/%s/.fluxbox/" % user
        if not os.path.isdir(dirname):
            return
        self.start_path = dirname + 'startup'

    def lines(self):
        """Give a list of lines (softwares detected)"""
        lines = []
        for soft in self.softs:
            lines.append(str(soft))
        return lines

    def __str__(self):
        """String representation of fluxboxlauncher config"""
        return ''.join(
            ''.join(self.first_lines)
            + ''.join(self.lines())
            + ''.join(self.last_lines)
        )

    def _new_soft(self, cmd, disabled):
        """Create a new soft by cmd"""
        path = join('/usr/share/applications', '%s.desktop' % cmd)
        if exists(path):
            new_soft = Soft(*get_info(path))
        else:
            new_soft = Soft(cmd, cmd, '', '')
        new_soft.disabled = disabled
        return new_soft

    def load(self, lines):
        """Load new config"""
        self.first_lines = []
        self.last_lines = []
        after_fluxbox = False
        for line in lines:
            if after_fluxbox or line.strip() == 'exec fluxbox':
                self.last_lines.append(line)
                after_fluxbox = True
                continue
            cmd = None
            if line.startswith('exec '):
                cmd = line.replace('exec ', '').replace(' &', '').strip()
                new_soft = self._new_soft(cmd, False)
            elif line.startswith('# exec '):
                cmd = line.replace('#', '').replace('exec ', '').replace('&', '').strip()
                new_soft = self._new_soft(cmd, True)
            else:
                self.first_lines.append(line)
            if not cmd:
                continue
            for soft in self.softs:
                if soft.cmd == cmd:
                    continue
            self.softs.append(new_soft)

    def open(self):
        """Open conf files"""
        if not os.path.isfile(self.start_path):
            return False
        with open(self.start_path, 'r') as f:
            self.load(f.readlines())
        return True

    def save(self):
        """Save conf files"""
        if not os.path.isfile(self.start_path):
            return False
        with open(self.start_path, 'w') as f:
            f.write(str(self))
        return True

    def add(self, soft):
        """Add a software"""
        for s in self.softs:
            if soft.cmd == s.cmd:
                return False
        self.softs.append(soft)
        return True

    def remove(self, soft):
        """Remove a software"""
        if soft not in self.softs:
            return False
        self.softs.remove(soft)
        return True

    def _change_status(self, soft, is_disabled):
        """Change status of a software"""
        for n, i in enumerate(self.softs):
            if soft == i:
                soft.disabled = is_disabled
                self.softs[n] = soft
                return True
        return False

    def disable(self, soft):
        """Disable a software"""
        return self._change_status(soft, True)

    def enable(self, soft):
        """Enable a software"""
        return self._change_status(soft, False)

    def get_soft(self, cmd):
        """Give a specific software on fluxboxlauncher lis with cmd"""
        for soft in self.softs:
            if soft.cmd == cmd:
                return soft
                break
        return None

    def soft_exist(self, soft):
        """Determine if a software exist on fluxboxlauncher list"""
        for s in self.softs:
            if s.cmd == soft.cmd:
                return True
        return False
