from pathlib import Path
import csv,json,collections,hashlib
P=Path(__file__).resolve().parents[1];D=P/'data'
def read(n):return list(csv.DictReader(open(D/(n+'.csv'),encoding='utf-8-sig')))
inv=read('program_census');ids={x['program_id'] for x in inv};assert len(ids)==len(inv)==124
src={x['source_id']:x for x in read('source_registry_v11')};ledger=read('country_activity_ledger');cc={x['country_code'] for x in read('countries')}
assert len({r['observation_id'] for r in ledger})==len(ledger)==2170
for x in ledger:
 assert x['source_id'] in src,x['source_id']
 assert x['program_id'] in ids or x['program_id'] in ['DFC_FINANCE_UNALLOCATED','DFC_LEGACY_UNALLOCATED']
 assert x['country_code'] in cc|{'','US'}
 assert x['evidence_as_of']<='2026-10-15'
 if x['event_start']:assert x['event_start']<='2026-10-15'
 if x['event_end'] and x['stage']=='D':assert x['event_end']<='2026-10-15'
 assert not(x['geography_role']=='participant_origin' and x['include_in_program_matrix']=='yes')
positive={'A','C','D','I'};pairs=collections.defaultdict(set)
for x in ledger:
 if x['include_in_program_matrix']=='yes' and x['stage'] in positive:pairs[(x['country_code'],x['program_id'])].add(x['stage'])
mat=read('country_program_activity_matrix');matrixids=set(mat[0])-{'country_code','country'}
assert len(mat)==249 and len(matrixids)==110
for r in mat:
 for pid in matrixids:assert r[pid]==('+'.join(sorted(pairs[(r['country_code'],pid)])) or 'U')
assert sum(r[p]!='U' for r in mat for p in matrixids)==276
assert len({r['program_id'] for r in ledger if r['include_in_program_matrix']=='yes' and r['stage'] in positive})==18
ex=read('exim_fy2026_authorizations');included=[r for r in ex if r['included_non_cancelled']=='yes'];assert len(included)==908
assert len({r['Unique Identifier'] for r in ex})==909
assert sum(r['country_code'] in cc for r in included)==283
assert sum(not r['country_code'] for r in included)==550
assert sum(r['country_code']=='US' for r in included)==75
dfc=read('dfc_active_portfolio');assert len(dfc)==1085
assert collections.Counter(r['mapped_program_id'] for r in dfc)['DFC_FINANCE_UNALLOCATED']==294
assert all(r['mapped_program_id']=='DFC_LEGACY_UNALLOCATED' for r in dfc if r['project_type']=='Legacy')
assert len([r for r in dfc if r['instrument_code']=='TPL IG' and r['project_type']=='Finance'])==276
assert len([r for r in dfc if r['instrument_code']=='COPS IG' and r['project_type']=='Finance'])==38
assert len(read('mcc_lifecycle'))==97
assert len({r['award_id'] for r in read('mdcp_country_targets')})==12
assert len({r['award_id'] for r in read('mdcp_country_targets') if r['listed_end_date']<'2026-10-15'})==7
unchanged=[]
for n in ['eligibility_matrix','overseas_presence_matrix','embassy_presence_matrix','service_coverage_matrix','sector_scope_matrix','sector_priority_matrix']:
 a=D/(n+'.csv');b=P/'history/v0_7/data'/(n+'.csv')
 if a.exists() and b.exists():assert a.read_bytes()==b.read_bytes();unchanged.append(n)
missing=[]
for x in src.values():
 if x.get('local_path') and not (P/x['local_path']).exists():missing.append((x['source_id'],x['local_path']))
assert not missing,missing
report={'inventory_ids_unique':124,'ledger_rows':len(ledger),'matrix_cells_checked':249*110,'positive_pairs_verified':276,'source_links_resolved':True,'exim_cancelled_excluded':1,'dfc_json_xlsx_reconciled':json.load(open(D/'dfc_xlsx_reconciliation.json')),'unchanged_baseline_matrices':unchanged,'no_origin_geography_in_delivery_matrix':True,'review_independence':'Same assistant; automated reconciliation is not external peer review'}
(P/'validation/census_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
