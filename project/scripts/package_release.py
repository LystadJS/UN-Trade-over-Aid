from pathlib import Path
import csv,hashlib,json,zipfile
P=Path(__file__).resolve().parents[1]
for f in (P/'deliverables').glob('*.inspect.ndjson'):f.replace(P/'validation'/f.name)
entries=[]
for f in sorted(P.rglob('*')):
 if not f.is_file() or f.name=='MANIFEST_SHA256.csv' or '__pycache__' in f.parts:continue
 entries.append({'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
with open(P/'MANIFEST_SHA256.csv','w',newline='') as h:
 w=csv.DictWriter(h,['path','bytes','sha256']);w.writeheader();w.writerows(entries)
z=P.with_suffix('.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for f in sorted(P.rglob('*')):
  if f.is_file() and '__pycache__' not in f.parts:out.write(f,str(Path(P.name)/f.relative_to(P)))
with zipfile.ZipFile(z) as f:assert f.testzip() is None;files=len(f.namelist())
receipt={'zip_path':str(z),'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'files':files,'manifest_entries':len(entries)}
z.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
