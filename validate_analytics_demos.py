"""Validate all 11 added analytics project datasets and generated report source."""
from pathlib import Path
import csv,json,re,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent/'opportunity-demos';errors=[];projects=sorted(ROOT.glob('*/'))
for folder in projects:
 try:
  model=json.loads((folder/'model.json').read_text());rows=model['rows']
  with (folder/'data.csv').open(newline='',encoding='utf-8') as f: source=list(csv.DictReader(f))
  if len(rows)!=48 or len(source)!=48:errors.append(f'{folder.name}: expected 48 synthetic rows')
  if not (folder/'PowerBI'/'Dashboard.pbip').is_file():errors.append(f'{folder.name}: missing native PBIP entry')
  if not (folder/'PowerBI'/'Model.SemanticModel'/'model.bim').is_file():errors.append(f'{folder.name}: missing semantic model')
  report=json.loads((folder/'PowerBI'/'Dashboard.Report'/'definition'/'report.json').read_text())
  if not report.get('themeCollection'):errors.append(f'{folder.name}: report theme not set')
  html=(folder/'index.html').read_text();script=re.search(r'<script>(.*?)</script>',html,re.S)
  if not script:errors.append(f'{folder.name}: missing browser companion script')
  else:
   with tempfile.NamedTemporaryFile('w',suffix='.js',encoding='utf-8') as f:
    f.write(script.group(1));f.flush();r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
   if r.returncode:errors.append(f'{folder.name}: {r.stderr.strip()}')
 except Exception as exc:errors.append(f'{folder.name}: {exc}')
print(f'Analytics projects checked: {len(projects)}')
print(f'Validation failures: {len(errors)}')
for e in errors:print(e)
sys.exit(bool(errors))
