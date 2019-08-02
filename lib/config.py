import os
import toml


def update_stream(lines, start_stream):
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


class Conf:
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

    def _contains(self, toml_stream, cmd):
        for soft in toml_stream:
            if toml_stream[soft]['cmd'].strip() == cmd:
                return True
        return False

    def load(self, lines, start_stream, new_toml):
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
                if self._contains(new_toml, cmd):
                    continue
                new_toml['soft-%s' % str(len(new_toml) + 1)] = {
                    'cmd': cmd,
                    'name': cmd
                }
                first_lines.append('exec %s &\n' % cmd)
                continue
            if line.startswith('# exec '):
                cmd = line.replace('#', '').replace('exec ', '').replace('&', '').strip()
                if self._contains(new_toml, cmd):
                    continue
                new_toml['soft-%s' % str(len(new_toml) + 1)] = {
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

    def save(self, start_stream, new_toml):
        with open(self.start_path, 'r') as f:
            lines = f.readlines()
        stream = self.load(lines, start_stream, new_toml)
        with open(self.start_path, 'w') as f:
            f.write(stream)
        with open(self.toml_path,'w') as f:
            f.write(toml.dumps(new_toml))

    def update(self, start_stream):
        with open(self.start_path, 'r') as f:
           lines = f.readlines()
        stream = update_stream(lines, start_stream)
        with open(self.start_path, 'w') as f:
            f.write(stream)

