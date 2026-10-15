"""Validate release counts, joins, uploaded actions and numerical projection; raises on discrepancy."""
from pathlib import Path
import csv,json,hashlib,sys,platform,importlib.metadata
import numpy as np
from scipy.spatial.distance import pdist
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];D=R/'data'
def read(n):
    with (D/(n+'.csv')).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
status=read('country_program_status_v13');assert len(status)==27390
assert len({(r['country_code'],r['program_id']) for r in status})==27390
observed=[r for r in status if r['activity_code']!='U'];assert len(observed)==276
assert len({r['country_code'] for r in observed})==121
assert len({r['program_id'] for r in observed})==18
assert all(r['activity_source_ids'] and r['activity_source_urls'] and r['source_evidence_dates'] for r in observed)
assert not any(r['program_id']=='USAID02' and r['activity_code']!='U' for r in status)
assert len(read('program_census'))==124
coords=read('similarity_coordinates_v13');excl=read('similarity_exclusions_v13')
assert len(coords)==13 and len(excl)==49
assert len({r['program_id'] for r in coords+excl})==62
xy=[]
for group in range(1,8):
    members=[r for r in coords if int(r['group'])==group]
    assert len({(r['x'],r['y']) for r in members})==1
    xy.append([float(members[0]['x']),float(members[0]['y'])])
pairs=read('similarity_pair_distances_v13');target=np.array([float(r['combined_distance']) for r in pairs])
stress=float(np.sqrt(sum((pdist(xy)-target)**2)/sum(target**2)))
assert abs(stress-json.loads((D/'visualization_summary_v13.json').read_text())['similarity_stress'])<1e-10
assert min(int(r['shared_country_units']) for r in pairs)==179
tx=read('uploaded_prime_actions_v13');assert len(tx)==10
for aid,internal in [('72067424F00006','291396509'),('72067423C00003','291396424'),('72067424C00001','291396504')]:
    old=json.loads((R/f'post_notice_review_v12/research/evidence/V12_TRANS_{internal}.json').read_text())['results']
    for row in old:
        match=[r for r in tx if r['award_id']==aid and r['modification_number']==row['modification_number']];assert len(match)==1
        t=match[0];assert t['action_date']==row['action_date'] and float(t['obligation'])==row['federal_action_obligation'] and t['description']==row['description']
sub=read('uploaded_subaward_actions_v13');assert len(sub)==43
post=[r for r in sub if r['award_id']=='72067423C00003' and r['action_date']>'2025-02-12'];assert len(post)==1
assert post[0]['amount']=='40250.00' and post[0]['country']==''
for r in read('uploaded_file_manifest_v13'):
    b=(R/'research_v13/uploaded_records'/r['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['sha256']
paper=R/'deliverables/US_Trade_Facilitation_Informative_Paper_v0_13.pdf'
assert len(PdfReader(paper).pages)==3
assert len(PdfReader(R/'deliverables/Trade_Program_Evidence_Atlas_v0_13.pdf').pages)==14
runtime={'python':sys.version,'platform':platform.platform(),'packages':{k:importlib.metadata.version(k) for k in ['numpy','scipy','matplotlib','python-docx','pypdf']}}
(R/'validation/runtime_v13.json').write_text(json.dumps(runtime,indent=2))
result=dict(status='PASS',country_cells=27390,qualifying_pairs=276,source_linkage_complete_for_qualifying_pairs=True,prime_transactions_matched=10,uploaded_subaward_rows=43,paper_pages=3,atlas_pages=14,similarity_stress=stress,legacy_status_not_promoted=True)
(R/'validation/checks_v13.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
