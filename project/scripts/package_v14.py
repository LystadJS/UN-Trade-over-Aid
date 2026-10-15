"""Package this release and validate ZIP integrity. Run after verification."""
from pathlib import Path
import hashlib,csv,zipfile,json
R=Path(__file__).resolve().parents[1]
assert json.loads((R/'validation/checks_v14.json').read_text())['status']=='PASS'
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='MANIFEST_SHA256.csv')
with (R/'MANIFEST_SHA256.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['path','bytes','sha256'])
    for p in files:w.writerow([str(p.relative_to(R)),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
z=R.with_suffix('.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as out:
    for p in files+[R/'MANIFEST_SHA256.csv']:out.write(p,str(p.relative_to(R.parent)))
with zipfile.ZipFile(z) as archive:assert archive.testzip() is None
print(json.dumps(dict(path=str(z),bytes=z.stat().st_size,files=len(files)+1,sha256=hashlib.sha256(z.read_bytes()).hexdigest())))
