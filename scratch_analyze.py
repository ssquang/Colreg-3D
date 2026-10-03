import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
print(f"Total lines: {len(lines)}")

# Find sections
for i, line in enumerate(lines):
    s = line.strip()
    if s.startswith('<!--') and s.endswith('-->'):
        print(f"L{i+1}: {s}")
    elif '<style>' in s:
        print(f"L{i+1}: Style start")
    elif '</style>' in s:
        print(f"L{i+1}: Style end")
    elif '<script>' in s:
        print(f"L{i+1}: Script start")
    elif '<div id="' in s and ('panel' in s or 'container' in s or 'modal' in s or 'hud' in s or 'control' in s):
        print(f"L{i+1}: {s[:90]}")
