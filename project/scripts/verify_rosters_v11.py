"""Check exact primary IDs, date semantics, scope limits and unchanged matrices."""
from pathlib import Path
import csv,json,hashlib,collections,re,fitz
P=Path(__file__).resolve().parents[1];D=P/'data';E=P/'research_v11/evidence';H=P/'history/v0_10/data'
def read(n,root=D):return list(csv.DictReader((root/(n+'.csv')).open(encoding='utf-8-sig')))
S={x['source_id']:x for x in read('source_registry_v11')}
for src in S.values():
 if src.get('local_path'):assert (P/src['local_path']).is_file(),src['source_id']
 if src.get('archive_sha256'):assert hashlib.sha256((P/src['local_path']).read_bytes()).hexdigest()==src['archive_sha256'],src['source_id']
for name in ['power_africa_action_review_v11','primary_award_actions_v11','legacy_award_survival_v11','legacy_award_followup_ids_v11','roster_verification_v11']:
 for r in read(name):
  for sid in (r.get('source_ids') or r.get('source_id') or '').split(';'):
   if sid.startswith(('V09_','V10_','V11_')):assert sid in S,sid
rows=read('power_africa_action_review_v11');assert len(rows)==len({r['award_id'] for r in rows})==7
assert collections.Counter(r['historical_action_status'] for r in rows)=={'verified_government_report_of_termination_notice':3,'government_project_cancellation_award_link_qualified':2,'unverified_award_specific_agency_action':2}
assert all(r['current_continuation']=='unverified' for r in rows)
doc=fitz.open(E/'V11_COURT_20_1_RECAP.pdf')
for aid,pg,date in [('72067424F00006',2,'2/11/2025'),('72067424C00001',2,'2/11/2025'),('72067423C00003',11,'2/12/2025')]:
 text=doc[pg-1].get_text(sort=True)
 assert re.search(re.escape(date)+r'\s+'+aid,text),(aid,text[:300])
for aid,internal,lastdate in [('AID-OAA-A-15-00054',259407464,'2018-07-12'),('AID-AFR-IO-16-00001',259403396,'2022-05-25')]:
 j=json.loads((E/f'V11_AW_{internal}.json').read_text());t=json.loads((E/f'V11_TRANS_{internal}_1.json').read_text())
 assert j['fain']==aid.replace('-','') and j['uri'].startswith(aid+'-')
 assert max(x['action_date'] for x in t['results'])==lastdate
 assert not t['page_metadata']['hasNext']
 assert next(r for r in rows if r['award_id']==aid)['latest_transaction_date']==lastdate
assert json.loads((E/'V11_AW_259403396.json').read_text())['type']=='11'
actions=read('primary_award_actions_v11');assert len(actions)==23
assert collections.Counter(r['record_type'] for r in actions)=={'federal_transaction_report':17,'government_court_filed_notice_roster':6}
esa=[r for r in actions if r['award_id']=='72067424C00001' and r['modification_number']=='P00003'][0]
assert esa['action_code']=='M' and esa['action_date']=='2025-03-07'
aw=read('legacy_award_survival_v11');assert len(aw)==len({r['award_id'] for r in aw})==25
assert collections.Counter(x['program_id'] for x in aw)=={'USAID01':5,'USAID02':13,'STATE09':7}
assert all(x['current_survival_certified']=='no' for x in aw)
assert set(r['award_id'] for r in aw)-set(r['award_id'] for r in read('legacy_award_survival_v10',H))=={'AID-OAA-A-15-00054','AID-AFR-IO-16-00001'}
doge=read('doge_cancellation_crosswalk_v11');assert len(doge)==5
assert all(not x['qualified_award_id'] for x in doge if x['join_status']=='rejected_amount_only')
roster=read('roster_verification_v11');assert len(roster)==45
own=collections.Counter(r['disposition'] for r in roster if r['field']=='ownership');assert own=={'unresolved_program_assignment':7,'qualified_scope_or_role':4,'verified_agency_or_published_contact':4}
master={x['program_id']:x for x in read('program_census')}
for r in read('legacy_reconciliation'):
 for field in ['current_owner','ownership_evidence','intake_status','evidence_limit']:assert r[field]==master[r['program_id']][field]
same=['eligibility_matrix','overseas_presence_matrix','embassy_presence_matrix','service_coverage_matrix','sector_scope_matrix','sector_priority_matrix','country_program_activity_matrix','country_program_stage_matrix','country_activity_ledger']
for n in same:assert (D/(n+'.csv')).read_bytes()==(H/(n+'.csv')).read_bytes(),n
report={'priority_awards_reviewed':7,'primary_historical_notice_dates_verified':3,'legacy_id_matches_verified':2,'interagency_action_chains_unresolved':2,'current_continuations_verified':0,'selected_awards':25,'selected_power_africa_awards':13,'financial_transaction_rows':17,'court_notice_rows':6,'source_paths_hashes_checked':len(S),'unchanged_tables':same,'ownership_dispositions':dict(own),'amount_only_joins_rejected':3,'independence':'Same assistant; automated source and consistency checks are not external peer review.'}
(P/'validation/roster_verification_v11.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
