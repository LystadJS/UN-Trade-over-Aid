from pathlib import Path
import csv,json,collections,hashlib
P=Path(__file__).resolve().parents[1];D=P/'data'
def read(n,root=D):return list(csv.DictReader((root/(n+'.csv')).open(encoding='utf-8-sig')))
r=read('roster_verification_v10');assert len(r)==45
assert len({(x['program_id'],x['field']) for x in r})==45
assert all(v==3 for v in collections.Counter(x['program_id'] for x in r).values())
S={x['source_id']:x for x in read('source_registry_v10')}
for name in ['roster_verification_v10','program_office_assignments_v10','legacy_award_survival_v10','event_program_links_v10']:
 for row in read(name):
  for sid in (row.get('source_ids') or row.get('source_id') or '').split(';'):
   if sid.startswith(('V09_','V10_')):assert sid in S,sid
for src in S.values():
 if src.get('local_path'):assert (P/src['local_path']).is_file(),src['source_id']
 if src.get('archive_sha256'):assert hashlib.sha256((P/src['local_path']).read_bytes()).hexdigest()==src['archive_sha256'],src['source_id']
master={x['program_id']:x for x in read('program_census')}
for b in read('legacy_reconciliation'):
 for field in ['current_owner','ownership_evidence','intake_status','evidence_limit']:assert master[b['program_id']][field]==b[field]
counts=dict(collections.Counter(x['operational_evidence'] for x in master.values()))
assert counts==json.loads((D/'census_summary.json').read_text())['operational_evidence_counts']
assert counts['recent_delivery_reported']==8 and counts['current_operation_unresolved']==18
same=[]
for n in ['eligibility_matrix','overseas_presence_matrix','embassy_presence_matrix','service_coverage_matrix','sector_scope_matrix','sector_priority_matrix']:
 assert (D/(n+'.csv')).read_bytes()==(P/'history/v0_9/data'/(n+'.csv')).read_bytes(),n;same.append(n)
old={x['observation_id']:x for x in read('country_activity_ledger',P/'history/v0_9/data')}
new={x['observation_id']:x for x in read('country_activity_ledger')}
assert set(new)-set(old)=={'OBS02170'}
assert [i for i in old if old[i]!=new[i]]==['OBS02148']
assert new['OBS02170']['source_record_id']==new['OBS02148']['source_record_id']
for name in ['country_program_activity_matrix','country_program_stage_matrix']:
 before={x['country_code']:x for x in read(name,P/'history/v0_9/data')}
 after=read(name);diff=[(r['country_code'],k,before[r['country_code']][k],v) for r in after for k,v in r.items() if before[r['country_code']][k]!=v]
 assert diff==[('MK','STATE09','U','D')],diff
leads=read('country_evidence_leads_v10');assert len(leads)==2 and all(x['admission_status'].startswith('quarantined') for x in leads)
ownership=collections.Counter(x['disposition'] for x in r if x['field']=='ownership')
assert ownership=={'unresolved_program_assignment':7,'qualified_scope_or_role':4,'verified_agency_or_published_contact':4}
aw=read('legacy_award_survival_v10');assert len(aw)==len({x['award_id'] for x in aw})==23
assert collections.Counter(x['program_id'] for x in aw)=={'USAID01':5,'USAID02':11,'STATE09':7}
assert all(x['current_survival_certified']=='no' for x in aw)
heta=next(x for x in aw if x['award_id']=='72067422CA00003')
assert heta['survival_disposition']=='recipient_reported_termination' and heta['scheduled_end_date']=='2027-10-06'
out={'programs_reviewed':15,'field_assessments':45,'ownership_dispositions':dict(ownership),'priority_office_rows':8,'selected_awards_reviewed':23,'new_power_africa_awards':2,'current_survival_certified':0,'new_country_admissions':1,'shared_event_links':2,'quarantined_country_leads':2,'unchanged_tables':same,'source_links_and_archive_hashes_checked':True,'master_legacy_fields_agree':True,'matrix_delta_checked':'MK/STATE09 only','independence':'Same assistant review; automated consistency checks are not independent external validation'}
(P/'validation/roster_verification_v10.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
