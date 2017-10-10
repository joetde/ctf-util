
from string import printable, ascii_letters, digits

class ManyPadSolver(object):
    BASIC_CHARS = ascii_letters + digits + ' [](){},.;:-'

    def __init__(self, binary, block_size):
        self._mapping = {}
        self._binary = binary
        self._block_size = block_size

    @staticmethod
    def _highest_freq(l):
        map = {}
        for i in l:
            if i in map:
                map[i] += 1
            else:
                map[i] = 1
        max_el = 0
        max = 0
        for (k,v) in map.iteritems():
            if v > max:
                max_el = k
                max = v
        return max_el

    def _print_stats(self):
        print("found %s out of %s" % (len(self._mapping.keys()), self._block_size))

    def build(self, allowed_chars = BASIC_CHARS):
        for off in range(len(self._binary) / self._block_size):
            for k in range(self._block_size):
                possibles = []
                for c in range(255):
                    ok = True
                    for i in range(k, len(self._binary), self._block_size):
                        dc = ord(self._binary[i]) ^ c
                        if not chr(dc) in allowed_chars:
                            ok = False
                            break
                    if ok:
                        if chr(c ^ ord(self._binary[k + off * self._block_size])) in allowed_chars:
                            possibles.append(c)
                if (len(possibles) == 1):
                    if k in self._mapping:
                        self._mapping[k].append(possibles[0])
                    else:
                        self._mapping[k] = [possibles[0]]

        self._mapping = {k : ManyPadSolver._highest_freq(l)
                         for (k, l) in self._mapping.iteritems()}
        self._print_stats()

    def get_solved_output(self, unknown_char = '*', format_block = False):
        s = ""
        for i in range(len(self._binary)):
            if not (i % self._block_size) in self._mapping:
                s += unknown_char
            else:
                s += chr(ord(self._binary[i]) ^ self._mapping[i % 32])
            if format_block and i % 32 == 31:
                s += '\n'
        return s

    def fix(self, help_replace):
        base_string = self.get_solved_output()
        for (orig, new) in help_replace:
            pos = base_string.find(orig)
            if pos == -1:
                raise Exception("Original string '%s' not found" % orig)
            count = 0
            for c in new:
                self._mapping[(pos+count) % 32] = ord(self._binary[pos+count]) ^ ord(c)
                count += 1
        self._print_stats()

    def get_solved_key(self, unknown_char = 'XX'):
        s = ""

        for i in range(self._block_size):
            if i in self._mapping:
                s += hex(self._mapping[i])[2:]
            else:
                s += unknown_char

        return s
