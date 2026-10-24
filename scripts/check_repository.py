#!/usr/bin/env python3
"""Check self-contained skill metadata and relative Markdown links."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
items=[]
for entry in sorted((root/'skills').glob('*/SKILL.md')):
 text=entry.read_text();assert text.startswith('---\n'),entry
 front=text.split('---',2)[1]
 name=re.search(r'^name:\s*(.+)$',front,re.M).group(1)
 desc=re.search(r'^description:\s*(.+)$',front,re.M).group(1)
 assert name==entry.parent.name and re.fullmatch(r'[a-z0-9-]{1,64}',name),entry
 assert '[TODO' not in text,entry
 items.append(dict(name=name,description=desc,path=entry.relative_to(root).as_posix()))
for file in root.rglob('*.md'):
 if '.git' in file.parts:continue
 for link in re.findall(r'\]\(([^)]+)\)',file.read_text()):
  if '://' in link or link.startswith('#'):continue
  assert (file.parent/link.split('#')[0]).exists(),(file,link)
assert items,'No skills'
print(json.dumps(items,ensure_ascii=False,indent=2))
