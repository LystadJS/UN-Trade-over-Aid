"""Reconcile v0.9 retained data with the explicitly adjudicated v0.10 evidence.
Run on this release or a copy of its v0.9 baseline; does not infer survival from award dates.
"""
from pathlib import Path
import csv,json,collections,hashlib,shutil
P=Path(__file__).resolve().parents[1]; D=P/'data'; E=P/'research_v10/evidence'; H=P/'history/v0_9/data'
def read(n,root=D):return list(csv.DictReader((root/(n+'.csv')).open(encoding='utf-8-sig')))
def write(n,rows):
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with (D/(n+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def join(*parts):return ';'.join(dict.fromkeys(x for p in parts for x in p.split(';') if x))

# Archive brief attributed research notes for non-federal copyrighted sources.
notes={
'V10_CRDF_BALKANS': 'CRDF Global reports participating in the Western Balkans Digital Transformation Accelerator in Skopje, North Macedonia. Its account explicitly identifies DCCP funding and State organization with CLDP. The page has no publication date. Commerce independently supplies June 10–11, 2026 event dates and State/CDP as convenor. This verifies a reported event, not an award identifier, funding amount, effectiveness, embassy footprint or region-wide delivery.',
'V10_ABT_DISCLOSURE': 'Abt Global, procurement proposal dated March 18, 2025, Nebraska solicitation 121165 O3, PDF page 15 (printed page 7): the disclosure table identifies HETA award 72067422CA00003 and reports termination for government convenience on February 26, 2025. The table was visually checked against the PDF. This is the recipient’s dated report, not an executed agency modification, and does not establish whether the action was later rescinded.',
'V10_RTI_EECA': 'RTI’s June 23, 2023 announcement identifies RTI as implementer of USAID Power Africa’s Empower East and Central Africa project. USAspending award 72067423C00003 matches the project name and recipient. This supports historical attribution; a 2023 announcement does not establish 2026 delivery or survival.',
'V10_ECODIT_PAISM': 'ECODIT’s project page identifies Power Africa Initiative Support Mechanism Activity and displays an October 2024–October 2029 period. This is historical project attribution and a planned period, not proof of uninterrupted performance after the assistance review.',
'V10_PK_SECONDARY_LINKS': 'Global News Pakistan’s agriculture webinar story supplied a link to the U.S. Embassy Islamabad official social-media post 2085347506485940617. The secondary article is used only for primary-source discovery. Official embed metadata identifies the embassy and August 6, 2026 but exposes only a shortened link, without the event text. No country delivery is admitted.'}
raw=P.parent.parent/'research_v10_raw';raw.mkdir(exist_ok=True)
for sid,note in notes.items():
 receipt=json.loads((E/(sid+'_receipt.json')).read_text())
 note_path=E/(sid+'_evidence_note.txt')
 note_path.write_text('Source: '+receipt['url']+'\nRetrieved: '+receipt['retrieved_utc']+'\nOriginal SHA256: '+receipt.get('sha256','')+'\n\n'+note+'\n')
 for f in list(E.glob(sid+'*')):
  if f.suffix in ['.html','.pdf'] or f.name==sid+'.txt' or f.name==sid+'_links.json':
   shutil.copy2(f,raw/f.name);f.unlink()
 receipt['archive_note_path']=str(note_path.relative_to(P));receipt['archival_treatment']='Attributed paraphrase retained; original retrieved hash preserved; full third-party text omitted from release.'
 (E/(sid+'_receipt.json')).write_text(json.dumps(receipt,indent=2))
for f in E.glob('V10_ABT_page_*.png'):shutil.copy2(f,raw/f.name);f.unlink()

# Indexed official pages are retained as qualified leads when full retrieval fails.
indexed={
'V10_FAM_CDP':('https://fam.state.gov/fam/01fam/01fam0490.html','1 FAM 495, CT:ORG-659 dated 2024-05-03, assigns CDP Strategy, Programs and Communications (CDP/SPC) management of bureau foreign assistance, including DCCP. Search-index evidence only; full page returned HTTP 502. This is a qualified functional assignment, not verified current staffing.'),
'V10_FAM_AF':('https://fam.state.gov/fam/01fam/01fam0120.html','Indexed 1 FAM 125.7, dated 2025-02-07, identifies AF/ERA liaison responsibilities for Prosper Africa and Power Africa. Liaison is not award management. A later office-code change requires checking any transfer; full page retrieval failed.'),
'V10_FAH_CODES':('https://fam.state.gov/fam/04FAH01/04FAH010420.html','Indexed 4 FAH-1 H-421.40 includes AF/CE Office of Commercial and Economic Affairs effective 2025-09-21 and CDP/SPC Strategy, Programs and Communications, code 253201, effective 2024-01-28. The retrieved index cites CT:FMH-360 dated 2026-08-18. It does not independently transfer legacy initiative management. Full page retrieval failed.'),
'V10_USAID_ESA':('https://www.usaid.gov/sites/default/files/2023-12/2023-USAID-COP28-Announcements.pdf','USAID COP28 announcements, December 2023, page 4, identify Empowering Southern Africa as a Power Africa program. USAspending separately identifies Chemonics award 72067424C00001 with that project title. This is a qualified project-title crosswalk, not a directly published program-to-award-ID crosswalk or survival evidence. Full URL returned an administrative-leave landing page; the announcement content is index-only.')}
for sid,(url,txt) in indexed.items():
 (E/(sid+'_index_note.txt')).write_text('Official URL: '+url+'\nIndex reviewed: 2026-10-15\n\n'+txt+'\n')

master=read('program_census',H); M={r['program_id']:r for r in master}
d=M['STATE09']
d.update(tier='overlay',counting_unit='overlay',status='reported_current_delivery_component',operational_evidence='recent_delivery_reported',current_status_verified='recent_delivery_reported',country_activity_observations='1',activity_distribution_status='one_verified_reported_event_venue',
 current_owner='State Bureau of Cyberspace and Digital Policy (CDP) for the verified Skopje component; full component ownership map unverified',
 ownership_evidence='Commerce names State/CDP as convenor in June 2026; CRDF explicitly names DCCP funding. Indexed FAM identifies CDP/SPC foreign-assistance management, but full FAM retrieval failed.',
 owner_source_ids='V10_CLDP_BALKANS;V10_CRDF_BALKANS;V10_FAM_CDP;V10_FAH_CODES',
 intake_status='No current umbrella intake verified. Specific DCCP-Pacific award termination remains recorded; Skopje delivery is separately reported.',
 evidence_limit='One component and event do not establish all DCCP owners, countries, intake or award survival. Suboffice assignment remains qualified.',
 review_result='Admitted DCCP-linked Skopje event, June 10–11, 2026; current component bureau verified, suboffice lead qualified; Costa Rica remains quarantined.')
d['review_source_ids']=join(d['review_source_ids'],d['owner_source_ids']);d['fresh_primary_retrievals']='2'
for pid in ['USAID01','USAID02']:
 r=M[pid];r['ownership_evidence']+=' Indexed AF/ERA liaison role predates the AF/CE office-code change; no program transfer to AF/CE established.'
 r['owner_source_ids']=join(r['owner_source_ids'],'V10_FAM_AF;V10_FAH_CODES')
 r['review_source_ids']=join(r['review_source_ids'],'V10_FAM_AF;V10_FAH_CODES')
M['USAID02']['evidence_limit']='No surviving component certified. HETA recipient reports February 2025 termination; five additional selected awards have congressional-reported termination, not executed modifications. Future end dates and old obligations do not establish survival.'
M['USAID02']['review_result']='Expanded selected Power Africa roster from nine to eleven; one recipient-reported termination, five congressional-reported terminations, two elapsed periods and three future-date records without verified survival.'
M['USAID02']['review_source_ids']=join(M['USAID02']['review_source_ids'],'V10_ABT_DISCLOSURE;V10_SFRC_REPORT;V10_RTI_EECA;V10_USAID_ESA')
for n in ['program_census','expanded_inventory']:write(n,master)
for n in ['inventory_view','ownership_review']:
 rows=read(n,H)
 for r in rows:
  for k in list(r):
   if k in M[r['program_id']]:r[k]=M[r['program_id']][k]
 write(n,rows)
legacy=read('legacy_reconciliation',H)
for r in legacy:
 pid=r['program_id']
 for f in ['current_owner','ownership_evidence','intake_status','evidence_limit']:r[f]=M[pid][f]
 r['v10_resolution']='Prior adjudication retained; no stronger program-specific current evidence found in this pass.'
 if pid=='STATE09':
  r['award_budget_finding']='DCCP-funded Skopje event is explicitly reported by CRDF and independently dated by Commerce. No link to a specific award ID. Seven selected legacy DCCP awards have elapsed end dates; Pacific termination remains recorded.'
  r['remaining_requirement']='Retrieve full CDP/SPC operating assignment and current funding/intake roster; crosswalk Skopje to award ID; recover full Costa Rica event record.'
  r['v10_resolution']=M[pid]['review_result']
 if pid=='USAID02':
  r['award_budget_finding']=M[pid]['review_result']
  r['remaining_requirement']='Obtain executed termination/rescission or continuation documents and current State implementing-award roster; verify three future-date-only records and four unmatched congressional award IDs.'
  r['v10_resolution']=M[pid]['review_result']
 if pid=='USAID01':r['v10_resolution']='Five selected award details refreshed; recorded termination actions retained. AF liaison/code records do not resolve the current program owner.'
 r['source_ids']=join(r['source_ids'],M[pid]['review_source_ids'])
write('legacy_reconciliation',legacy)
L={r['program_id']:r for r in legacy}
roster=read('roster_verification_v09',H)
for r in roster:
 pid=r['program_id']
 if pid=='STATE09':
  r['source_ids']=join(r['source_ids'],d['owner_source_ids']);r['evidence_limit']=d['evidence_limit'];r['next_check']=L[pid]['remaining_requirement']
  if r['field']=='ownership':r.update(disposition='qualified_scope_or_role',finding=d['current_owner']+' | '+d['ownership_evidence'])
  if r['field']=='country_delivery':r.update(disposition='verified_reported_component_delivery',finding='Skopje, North Macedonia, June 10–11, 2026. CRDF explicitly identifies DCCP funding; Commerce independently supplies dates and CDP convenor. Shared event with DOC01, not a second deal.')
  if r['field']=='intake':r['finding']=d['intake_status']
 if pid in ['USAID01','USAID02'] and r['field']=='ownership':r['finding']=M[pid]['current_owner']+' | '+M[pid]['ownership_evidence'];r['source_ids']=join(r['source_ids'],'V10_FAM_AF;V10_FAH_CODES')
 if pid=='USAID02' and r['field']=='country_delivery':r['finding']=M[pid]['review_result'];r['source_ids']=join(r['source_ids'],'V10_ABT_DISCLOSURE;V10_SFRC_REPORT');r['evidence_limit']=M[pid]['evidence_limit']
write('roster_verification_v10',roster)
offices=[]
for pid in ['STATE01','STATE02','STATE03','STATE04','STATE07','USAID01','USAID02','STATE09']:
 r=next(x for x in roster if x['program_id']==pid and x['field']=='ownership')
 offices.append(dict(program_id=pid,name=M[pid]['name'],assignment_status=r['disposition'],agency_or_bureau=M[pid]['current_owner'],suboffice=('CDP/SPC — indexed functional assignment only' if pid=='STATE09' else 'Unverified program-specific assignment'),basis=r['finding'],intake_status=M[pid]['intake_status'],source_ids=r['source_ids'],remaining_requirement=L[pid]['remaining_requirement'],reviewed_on='2026-10-15'))
write('program_office_assignments_v10',offices)

ledger=read('country_activity_ledger',H)
old=next(x for x in ledger if x['observation_id']=='OBS02148');old['description']='CLDP reports Western Balkans digital transformation workshop; DCCP attribution separately supported in OBS02170';old['source_record_id']='WESTERN_BALKANS_20260610'
ledger.append(dict(observation_id='OBS02170',program_id='STATE09',country_code='MK',source_geography='North Macedonia',geography_role='delivery_venue',stage='D',evidence_as_of='2026-06-11',event_start='2026-06-10',event_end='2026-06-11',description='DCCP-funded Western Balkans Digital Transformation Accelerator in Skopje; State/CDP convenor with CLDP',source_id='V10_CRDF_BALKANS',source_url='https://crdfglobal.org/news/crdf-global-supports-western-balkans-digital-transformation-accelerator/',source_record_id='WESTERN_BALKANS_20260610',evidence_level='participant_primary_with_official_date_corroboration',include_in_program_matrix='yes',limitation='Commerce source V10_CLDP_BALKANS supplies dates and bureau. Same event as OBS02148. No additional participant-country delivery, award ID, embassy office or effectiveness inferred.'))
write('country_activity_ledger',ledger)
for n in ['country_program_activity_matrix','country_program_stage_matrix']:
 rows=read(n,H);next(x for x in rows if x['country_code']=='MK')['STATE09']='D';write(n,rows)
coverage=read('activity_coverage',H);c=next(x for x in coverage if x['program_id']=='STATE09');c.update(country_units_with_observations='1',source_observations='1',stages='D',coverage_limit='One event venue; shared CLDP/DCCP event, not complete program footprint.');write('activity_coverage',coverage)
write('event_program_links_v10',[dict(event_id='WESTERN_BALKANS_20260610',observation_id=oid,program_id=pid,country_code='MK',event_start='2026-06-10',event_end='2026-06-11',role=role,source_id=sid,counting_limit='One shared event; do not sum program links as independent deals.') for oid,pid,role,sid in [('OBS02148','DOC01','convening_and_technical_delivery','V10_CLDP_BALKANS'),('OBS02170','STATE09','named_funding_partnership','V10_CRDF_BALKANS')]])
leads=read('country_evidence_leads_v09',H)
for r in leads:
 if r['country_code']=='PK':
  r['finding']='Official embassy social-post URL recovered; official embed identifies author and August 6, 2026 but no event text. Shortened link did not resolve. Direct Line program/event content still unverified.'
  r['source_url']='https://x.com/usembislamabad/status/2085347506485940617';r['source_id']='V10_TWITTER_OEMBED';r['admission_status']='quarantined_primary_metadata_only'
 if r['country_code']=='CR':r['finding']+=' Additional DOCX retrieval returned HTTP 403; no new admission.'
write('country_evidence_leads_v10',leads)

# Selected award survival audit; retain prior action history without interpreting False as survival.
awards=[x for x in read('award_evidence',H) if x['program_id'] in ['USAID01','USAID02','STATE09']]
for aid,i in [('72067423C00003','291396424'),('72067424C00001','291396504')]:awards.append(dict(program_id='USAID02',award_internal_id=i,award_id=aid,match_status='project_name_and_recipient_crosswalk' if i=='291396424' else 'qualified_project_title_crosswalk',termination_text_or_action_in_returned_records='not_reviewed',source_id='',description=''))
reported={'72067425C00001','72067424C00002','72067425F00001','72067424CA00007','72067423FA00007'}
survival=[]
for a in awards:
 sid='V10_AW_'+a['award_internal_id'];rec=json.loads((E/(sid+'_receipt.json')).read_text());j=json.loads((P/'research_v10'/rec['snapshot']).read_text());pop=j['period_of_performance'];aid=a['award_id'];ids=sid
 if a['termination_text_or_action_in_returned_records']=='True':status='recorded_termination_action';basis='Specific termination-related action retained from prior transaction audit; current award detail refreshed. No umbrella-wide or final closeout inference.';ids=join(ids,a['source_id'])
 elif aid=='72067422CA00003':status='recipient_reported_termination';basis='Abt March 18, 2025 proposal reports February 26 termination; PDF page 15, printed page 7. No executed notice or later rescission record obtained.';ids=join(ids,'V10_ABT_DISCLOSURE;V10_SFRC_REPORT')
 elif aid in reported:status='congressional_reported_termination';basis='July 2025 SFRC minority staff report cites this award ID in Power Africa termination discussion, footnote 365. Not an executed contracting/agreement officer modification.';ids=join(ids,'V10_SFRC_REPORT')
 elif pop['end_date']<'2026-10-15':status='scheduled_period_elapsed';basis='Returned period end predates review. This does not establish final closeout or continuation elsewhere.'
 else:status='future_date_survival_unverified';basis='Future recorded period end with no primary current continuation evidence. Award obligations and date alone cannot establish survival.'
 if aid=='72067423C00003':ids=join(ids,'V10_RTI_EECA')
 if aid=='72067424C00001':ids=join(ids,'V10_USAID_ESA')
 survival.append(dict(program_id=a['program_id'],award_id=aid,award_internal_id=a['award_internal_id'],recipient=j['recipient']['recipient_name'],description=j['description'],program_link_status=a['match_status'],reported_awarding_office=j['awarding_agency']['office_agency_name'],scheduled_end_date=pop['end_date'],last_modified_date=pop['last_modified_date'],prior_transaction_termination_flag=a['termination_text_or_action_in_returned_records'],survival_disposition=status,evidence_basis=basis,current_survival_certified='no',source_ids=ids,next_check='Current agency award roster plus executed continuation/termination/rescission record; distinguish historic reporting office from operating owner.',reviewed_on='2026-10-15'))
write('legacy_award_survival_v10',survival)
write('legacy_award_followup_ids_v10',[dict(program_id='USAID02',award_id=x,source_id='V10_SFRC_REPORT',finding='Named in July 2025 report footnote 365; not joined to award details in this selected audit.',next_check='Resolve exact award identifier and executed administrative action; do not count as surviving delivery.') for x in ['72067424T00001','AID-OAA-A-15-00054','AID-AFR-IO-16-00001','72067420T00001']])
gaps=read('remaining_evidence_gaps',H)
for r in gaps:
 if r['program_id'] in ['STATE09','USAID01','USAID02']:
  l=L[r['program_id']];r.update(status=l['v10_resolution'],remaining_requirement=l['remaining_requirement'],specific_next_check=l['remaining_requirement'],source_ids=l['source_ids'])
write('remaining_evidence_gaps',gaps)
changes=read('inventory_changes',H);changes.append(dict(program_id='STATE09',change_type='verified_component_delivery',before='candidate; operational status unresolved; no admitted country pair',after_tier='overlay',finding=d['review_result'],source_ids=d['owner_source_ids'],remaining_requirement=L['STATE09']['remaining_requirement']));write('inventory_changes',changes)
cor=read('corrections',H);cor.extend([dict(issue='DCCP Balkan attribution',prior='CLDP event had no explicit DCCP linkage in retained source',corrected='CRDF primary participant report explicitly names DCCP funding; one MK delivery pair admitted',basis='V10_CRDF_BALKANS with V10_CLDP_BALKANS date/office corroboration',affected='Current ledger, matrices, inventory and briefing'),dict(issue='Power Africa selected award coverage',prior='Nine selected awards; no current component survival established',corrected='Eleven selected awards; recipient-reported HETA termination added; no survival certified',basis='Two additional award IDs; Abt disclosure; SFRC secondary termination evidence kept separate',affected='Current survival table; prior award_evidence retained as historical audit')]);write('corrections',cor)

sources=read('source_registry_v09',H)
for f in sorted(E.glob('*_receipt.json')):
 r=json.loads(f.read_text());r['purpose']=r.get('purpose','Priority ownership, award survival or primary country-record validation');r['source_url']=r['url']
 r['local_path']=r.get('archive_note_path',('research_v10/'+r['snapshot']) if r.get('snapshot') else '')
 if r.get('archive_note_path'):r.pop('archive_note_path')
 if r['source_id'] in indexed:
  r['receipt_note']=indexed[r['source_id']][1]
  if not r['local_path'] or r['source_id']=='V10_USAID_ESA':r['local_path']='research_v10/evidence/'+r['source_id']+'_index_note.txt'
 if r['local_path']:r['archive_sha256']=hashlib.sha256((P/r['local_path']).read_bytes()).hexdigest()
 r['use_limit']='Source-specific qualifications apply; retrieval success is not operational confirmation. Full-page failures and indexed leads do not establish staffing or current delivery.'
 for k,v in list(r.items()):
  if isinstance(v,(dict,list)):r[k]=json.dumps(v,ensure_ascii=False)
 sources.append(r)
write('source_registry_v10',sources)
S=json.loads((H/'census_summary.json').read_text());S.update(tier_counts=dict(collections.Counter(r['tier'] for r in master)),operational_evidence_counts=dict(collections.Counter(r['operational_evidence'] for r in master)),observed_program_country_pairs=276,observed_program_records=18,ledger_observations=2170,v10_office_assignments_reviewed=8,v10_roster_programs=15,v10_field_assessments=45,v10_new_country_observations=1,v10_selected_legacy_awards=23,v10_selected_power_africa_awards=11,v10_verified_surviving_awards=0,v10_source_attempts=len(list(E.glob('*_receipt.json'))),v10_country_leads_quarantined=2,v10_award_survival_dispositions=dict(collections.Counter(r['survival_disposition'] for r in survival)))
(D/'census_summary.json').write_text(json.dumps(S,indent=2))
(D/'workbook_data.json').write_text(json.dumps({f.stem:list(csv.reader(f.open(encoding='utf-8-sig'))) for f in D.glob('*.csv')},ensure_ascii=False))
print(json.dumps({k:v for k,v in S.items() if k.startswith('v10')},indent=2))
