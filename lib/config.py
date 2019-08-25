import os

from lib.soft import Soft

class Conf:
    def __init__(self, user):
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

    def sort_softs(self, soft):
        return int(soft.replace('soft-', ''))

    def load(self, lines):
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
                new_soft = Soft(cmd, cmd, '', '')
            elif line.startswith('# exec '):
                cmd = line.replace('#', '').replace('exec ', '').replace('&', '').strip()
                new_soft = Soft(cmd, cmd, '', '')
                new_soft.disabled = True
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
        if os.path.isfile(self.start_path):
            with open(self.start_path, 'r') as f:
                self.load(f.readlines())

    def save(self):
        with open(self.start_path, 'w') as f:
            f.write(str(self))

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
        pass

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
