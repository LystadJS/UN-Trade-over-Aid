from pathlib import Path
import csv,json,hashlib,collections
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];D=R/'data';B=R/'research_v15/baseline'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
a=read(D/'country_program_activity_matrix.csv');old=read(B/'country_program_activity_matrix.csv');ids=[k for k in a[0] if k not in ['country','country_code']]
delta=[(r['country_code'],p,o[p],r[p]) for r,o in zip(a,old) for p in ids if r[p]!=o[p]]
assert len(delta)==5 and all(x[2:] == ('U','D') for x in delta)
assert {(x[0],x[1]) for x in delta}=={('AU','FAS11'),('PH','USTDA05'),('MX','USTDA01'),('BR','USTDA01'),('PH','USTDA01')}
ledger=read(D/'country_activity_ledger.csv');adds=read(D/'service_delivery_additions_v15.csv');assert len(ledger)==2193 and len(adds)==10
assert ledger[:2183]==read(B/'country_activity_ledger.csv')
assert sum(r[p]!='U' for r in a for p in ids)==286
assert sum(any(r[p]!='U' for p in ids) for r in a)==124
assert sum(r[p]=='D' for r in a for p in ids)==36
assert len(read(D/'country_program_status_v15.csv'))==27390
for r in adds:
 rec=json.loads((R/'research_v15/evidence'/(r['source_id']+'_receipt.json')).read_text());p=R/'research_v15'/rec['snapshot'];assert rec['status']==200 and hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256']
assert len(PdfReader(R/'deliverables/US_Trade_Facilitation_Informative_Paper_v0_15.pdf').pages)==3
assert len(PdfReader(R/'deliverables/Trade_Program_Evidence_Atlas_v0_15.pdf').pages)==14
inv=read(D/'program_census.csv');prev=read(B/'program_census.csv');changed=[r['program_id'] for r,o in zip(inv,prev) if r['operational_evidence']!=o['operational_evidence']];assert set(changed)=={'USTDA01','USTDA05'}
summary=json.loads((D/'visualization_summary_v15.json').read_text());assert summary['evidence_categories']['recent_delivery_reported']==11
assert len(read(D/'similarity_coordinates_v15.csv'))==13
out=dict(status='PASS',new_pairs=delta,ledger_rows=len(ledger),new_observations=len(adds),qualifying_pairs=286,delivered_pairs=36,country_units=124,program_category_changes=changed,paper_pages=3,atlas_pages=14)
(R/'validation/checks_v15.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
