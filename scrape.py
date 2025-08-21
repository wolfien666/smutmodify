#!/usr/bin/env python3
"""
Smutscrape - Main Entry Point

This is the main entry point for the Smutscrape application.
It routes between CLI mode and API server mode based on the --server flag.
"""

import sys


def parse_duration_str(val):
    """Convert duration like 120, 90s, 12m, 1h20m into seconds."""
    if val is None:
        return None
    if isinstance(val, int):
        return val
    val = str(val).strip().lower()
    if val.isdigit():
        return int(val)
    total = 0
    match = re.findall(r"(\d+)([hms])", val)
    if not match:
        raise ValueError(f"Invalid duration string: {val}")
    for num, unit in match:
        num = int(num)
        if unit == "h":
            total += num * 3600
        elif unit == "m":
            total += num * 60
        elif unit == "s":
            total += num
    return total

def parse_duration_str(val):
    """Convert duration like 120, 90s, 12m, 1h20m into seconds."""
    import re
    if val is None:
        return None
    if isinstance(val, int):
        return val
    val = str(val).strip().lower()
    if val.isdigit():
        return int(val)
    total = 0
    match = re.findall(r"(\d+)([hms])", val)
    if not match:
        raise ValueError(f"Invalid duration string: {val}")
    for num, unit in match:
        num = int(num)
        if unit == "h":
            total += num * 3600
        elif unit == "m":
            total += num * 60
        elif unit == "s":
            total += num
    return total


def parse_duration_str(val):
    """Convert duration like 120, 90s, 12m, 1h20m into seconds."""
    import re
    if val is None:
        return None
    if isinstance(val, int):
        return val
    val = str(val).strip().lower()
    if val.isdigit():
        return int(val)
    total = 0
    match = re.findall(r"(\d+)([hms])", val)
    if not match:
        raise ValueError(f"Invalid duration string: {val}")
    for num, unit in match:
        num = int(num)
        if unit == "h":
            total += num * 3600
        elif unit == "m":
            total += num * 60
        elif unit == "s":
            total += num
    return total


def parse_duration_str(val):
    """Convert duration like 120, 90s, 12m, 1h20m into seconds."""
    import re
    if val is None:
        return None
    if isinstance(val, int):
        return val
    val = str(val).strip().lower()
    if val.isdigit():
        return int(val)
    total = 0
    match = re.findall(r"(\d+)([hms])", val)
    if not match:
        raise ValueError(f"Invalid duration string: {val}")
    for num, unit in match:
        num = int(num)
        if unit == "h":
            total += num * 3600
        elif unit == "m":
            total += num * 60
        elif unit == "s":
            total += num
    return total


def main():
    """Route to appropriate mode based on command line arguments."""
    # Check if we're in server mode early (before full argument parsing)
    if "--server" in sys.argv or "-s" in sys.argv:
        from smutscrape.api import main as api_main
        api_main()
    else:
        from smutscrape.cli import main as cli_main
        cli_main()

if __name__ == "__main__":
	main()
# Note: --date-from/--date-to added by patcher (in case parse block wasn't found)
