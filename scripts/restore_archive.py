"""Restore the complete research snapshot; Python 3.12+ recommended."""
import argparse, csv, hashlib, json, tarfile
from pathlib import Path

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--archive-dir',type=Path,default=Path(__file__).resolve().parents[1]/'archives/v0.15')
    parser.add_argument('--output',type=Path,default=Path('restored-v0.15'))
    args=parser.parse_args()
    m=json.loads((args.archive_dir/'archive-manifest.json').read_text())
    if args.output.exists(): raise SystemExit('Output already exists; choose a new directory.')
    args.output.mkdir(parents=True)
    joined=args.output/m['archive']
    with joined.open('wb') as out:
        for p in m['parts']:
            src=args.archive_dir/p['name']
            assert src.stat().st_size==p['bytes'],src
            assert sha(src)==p['sha256'],src
            with src.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024),b''):out.write(chunk)
    assert joined.stat().st_size==m['archive_bytes']
    assert sha(joined)==m['archive_sha256']
    with tarfile.open(joined) as tar: tar.extractall(args.output,filter='data')
    root=args.output/'project'
    rows=list(csv.DictReader((root/'MANIFEST_SHA256.csv').open()))
    for row in rows:
        p=root/row['path']
        assert p.stat().st_size==int(row['bytes']),p
        assert sha(p)==row['sha256'],p
    assert len(rows)+1==m['file_count']
    joined.unlink()
    print(f'PASS: {len(rows)} file hashes plus manifest; restored {m["file_count"]} files to {root}')
if __name__=='__main__': main()
