#!/usr/bin/env python3
"""
Run the existing CLI but provide global `builtins.args` (for our custom filters)
and a safe fallback for `builtins.item` to avoid NameError if a guard uses `item`
outside its loop scope.

Usage:
    python3 run_with_args_shim.py ./arg_scrape.py xv search "threesome" --min-duration 12m --date-from 2025-01-01 --date-to 2025-06-01

If you omit the entry script, it defaults to ./scrape.py.
"""

import sys, re, runpy, builtins
from pathlib import Path

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
    return total or None

class ArgsShim:
    def __init__(self, min_duration=None, date_from=None, date_to=None):
        self.min_duration = min_duration
        self.date_from = date_from
        self.date_to = date_to
    def __getattr__(self, _):
        return None

def extract_flags(argv):
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

def main():
    argv = sys.argv[1:]
    # allow explicit entry script
    entry = None
    if argv and Path(argv[0]).exists() and argv[0].endswith(".py"):
        entry = argv[0]
        argv = argv[1:]
    if entry is None:
        # default
        entry = "scrape.py" if Path("scrape.py").exists() else "arg_scrape.py"

    md, df, dt, forwarded = extract_flags(argv)
    builtins.args = ArgsShim(md, df, dt)
    # provide a safe global fallback so `item` never raises NameError
    builtins.item = {}

    sys.argv = [entry] + forwarded
    runpy.run_path(entry, run_name="__main__")

if __name__ == "__main__":
    main()
