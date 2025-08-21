#!/usr/bin/env python3
"""
Repair previously injected filter guards so they don't crash with NameError.
# removed injected inline filter guard (handled by smutscrape/filters.py)
- Replaces 'args' with 'builtins.args' inside those guards (so scope doesn't matter).
- Ensures 'import builtins' exists in patched files.
Idempotent: safe to run more than once.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SKIP_PARTS = ("venv", ".venv", "env", ".env", "__pycache__", "build", "dist")

def should_skip(p: Path) -> bool:
    s = str(p)
    return any(part in s for part in SKIP_PARTS)

def ensure_import_builtins(text: str) -> str:
    if re.search(r'^\s*import\s+builtins\b', text, re.M):
        return text
    # Insert after first block of imports
    lines = text.splitlines()
    insert_at = 0
    # find last consecutive import at top
    for i, ln in enumerate(lines):
        if ln.startswith("import ") or ln.startswith("from "):
            insert_at = i + 1
        else:
            # stop once we pass initial import run (allow blank lines)
            if ln.strip() == "":
                insert_at = i + 1
                continue
            break
    lines.insert(insert_at, "import builtins")
    return "\n".join(lines)

def repair_file(path: Path) -> bool:
    txt = path.read_text(encoding="utf-8", errors="ignore")
    # removed injected inline filter guard (handled by smutscrape/filters.py)
        return False

    orig = txt
    lines = txt.splitlines()
    out = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        out.append(line)

        # Detect a 'for <var> in ...:' loop
        m_for = re.match(r'^(\s*)for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+.*:\s*$', line)
        if m_for:
            base_indent = len(m_for.group(1))
            loop_var = m_for.group(2)

            # Look ahead up to the next block of lower/equal indent or 12 lines
            j = i + 1
            while j < len(lines):
                ln = lines[j]
                # stop scanning this loop block if dedented to same or less indent (non-blank)
                if ln.strip() and (len(ln) - len(ln.lstrip())) <= base_indent:
                    break

                # removed injected inline filter guard (handled by smutscrape/filters.py)
                # common shapes:
                # removed injected inline filter guard (handled by smutscrape/filters.py)
                # removed injected inline filter guard (handled by smutscrape/filters.py)
                # possibly inside try: ... except: blocks
                call_match = re.search(
                    # removed injected inline filter guard (handled by smutscrape/filters.py)
                    ln
                )
                if call_match:
                    full = call_match.group(1)
                    arg1 = call_match.group(2)
                    arg2 = call_match.group(3)

                    # Fix first arg to the real loop var
                    if arg1 != loop_var:
                        ln_fixed = ln.replace(
                            # removed injected inline filter guard (handled by smutscrape/filters.py)
                        )
                        ln = ln_fixed
                        changed = True

                    # Normalize second arg to builtins.args (so scope-proof)
                    # If it's already builtins.args, leave as-is
                    if "builtins.args" not in ln:
                        # Replace any 'args' or anything else before ')' with builtins.args
                        ln = re.sub(
                            # removed injected inline filter guard (handled by smutscrape/filters.py)
                            r'\1builtins.args\3',
                            ln
                        )
                        changed = True

                    # Write back the modified line
                    out[-1] = out[-1]  # keep prior line
                    out.append(ln)
                    j += 1
                    # Copy the remaining lookahead block without double-adding current ln
                    i = j - 1  # main loop will add lines[j] next
                    # continue scanning inside the same loop block
                    continue

                j += 1

        i += 1

    new_txt = "\n".join(out)
    if changed:
        new_txt = ensure_import_builtins(new_txt)
        path.write_text(new_txt, encoding="utf-8")
        print(f"[fixed] {path}")
        return True
    else:
        return False

def main():
    any_changed = False
    for py in ROOT.rglob("*.py"):
        if should_skip(py):
            continue
        try:
            if repair_file(py):
                any_changed = True
        except Exception as e:
            print(f"[warn] failed to repair {py}: {e}")
    if not any_changed:
        print("[info] no guard lines required repair (already aligned)")

if __name__ == "__main__":
    main()