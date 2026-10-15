from pathlib import Path
import csv,hashlib
p=Path(__file__).resolve().parents[1]
a=list(csv.DictReader(open(p/'MANIFEST_SHA256.csv')))
for r in a:
 f=p/r['path'];assert f.stat().st_size==int(r['bytes']);assert hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'],r['path']
print('Verified',len(a),'manifest entries')
