from pathlib import Path
import csv,json,collections,hashlib
P=Path(__file__).resolve().parents[1];D=P/'data'
def read(n):return list(csv.DictReader((D/(n+'.csv')).open(encoding='utf-8-sig')))
r=read('roster_verification_v09');assert len(r)==45
assert len({(x['program_id'],x['field']) for x in r})==45
assert all(v==3 for v in collections.Counter(x['program_id'] for x in r).values())
assert {x['field'] for x in r}=={'ownership','intake','country_delivery'}
S={x['source_id']:x for x in read('source_registry_v09')}
for row in r:
 for sid in row['source_ids'].split(';'):
  if sid.startswith('V09_'):assert sid in S,sid
for src in S.values():
 if src.get('local_path'):assert (P/src['local_path']).is_file(),src['source_id']
 if src.get('archive_sha256'):assert hashlib.sha256((P/src['local_path']).read_bytes()).hexdigest()==src['archive_sha256'],src['source_id']
master={x['program_id']:x for x in read('program_census')}
for b in read('legacy_reconciliation'):
 for field in ['current_owner','ownership_evidence','intake_status','evidence_limit']:assert master[b['program_id']][field]==b[field]
counts=dict(collections.Counter(x['operational_evidence'] for x in master.values()))
assert counts==json.loads((D/'census_summary.json').read_text())['operational_evidence_counts']
assert counts['funding_intake_or_approval_action']==14 and counts['current_official_offer_only']==61
same=[]
for n in ['country_activity_ledger','country_program_activity_matrix','country_program_stage_matrix','eligibility_matrix','overseas_presence_matrix','embassy_presence_matrix','service_coverage_matrix','sector_scope_matrix','sector_priority_matrix']:
 assert (D/(n+'.csv')).read_bytes()==(P/'history/v0_8/data'/(n+'.csv')).read_bytes(),n
 same.append(n)
leads=read('country_evidence_leads_v09');assert len(leads)==2
assert all(x['admission_status'].startswith('quarantined') for x in leads)
step=next(x for x in r if x['program_id']=='SBA05' and x['field']=='ownership')
assert step['disposition']=='verified_agency_or_published_contact'
assert '5.2.3' in step['finding']
api=json.loads((P/'research_v09/evidence/V09_STEP_API.json').read_text())
assert api['data']['id']==363144 and api['data']['opportunityNumber']=='SB-OIT-STEP-2026-01'
assert 'sessionToken' not in api
ownership=collections.Counter(x['disposition'] for x in r if x['field']=='ownership')
assert ownership['unresolved_program_assignment']==8
assert ownership['qualified_scope_or_role']==3
assert ownership['verified_agency_or_published_contact']==4
out={'programs_reviewed':15,'field_assessments':45,'ownership_dispositions':dict(ownership),'new_country_admissions':0,'quarantined_country_leads':2,'unchanged_tables':same,'source_links_and_archive_hashes_checked':True,'master_legacy_fields_agree':True,'step_api_id_checked':True,'independence':'Same assistant review; automated consistency checks are not independent external validation'}
(P/'validation/roster_verification_v09.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
