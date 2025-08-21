#!/usr/bin/env python3
import sys, re, builtins, runpy

def parse_duration_str(val):
    if val is None:
        return None
    s = str(val).strip().lower()
    if not s:
        return None
    if s.isdigit():
        return int(s)
    total = 0
    for num, unit in re.findall(r'(\d+)\s*([hms])', s):
        n = int(num)
        if unit == 'h':
            total += n * 3600
        elif unit == 'm':
            total += n * 60
        elif unit == 's':
            total += n
    if total == 0:
        # tolerate weird inputs by returning None instead of crashing
        return None
    return total

class ArgsShim:
    def __init__(self, min_duration=None, date_from=None, date_to=None):
        self.min_duration = min_duration
        self.date_from = date_from
        self.date_to = date_to
    def __getattr__(self, _):
        # Any other attribute the code might look for will resolve to None
        return None

def extract_flags(argv):
    """Pull out just the flags we injected earlier; leave everything else untouched."""
    md = None; df = None; dt = None
    out = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--min-duration' and i+1 < len(argv):
            md = parse_duration_str(argv[i+1])
            out.extend([a, argv[i+1]]); i += 2; continue
        if a.startswith('--min-duration='):
            md = parse_duration_str(a.split('=',1)[1])
            out.append(a); i += 1; continue
        if a == '--date-from' and i+1 < len(argv):
            df = argv[i+1]; out.extend([a, argv[i+1]]); i += 2; continue
        if a.startswith('--date-from='):
            df = a.split('=',1)[1]; out.append(a); i += 1; continue
        if a == '--date-to' and i+1 < len(argv):
            dt = argv[i+1]; out.extend([a, argv[i+1]]); i += 2; continue
        if a.startswith('--date-to='):
            dt = a.split('=',1)[1]; out.append(a); i += 1; continue
        out.append(a); i += 1
    return md, df, dt, out

if __name__ == '__main__':
    # Create a global builtins.args so any bare 'args' resolves
    md, df, dt, forwarded = extract_flags(sys.argv[1:])
    builtins.args = ArgsShim(md, df, dt)

    # Now execute the real CLI script in this same interpreter.
    # This does not modify your files.
    sys.argv = ['scrape.py'] + forwarded
    runpy.run_path('scrape.py', run_name='__main__')
