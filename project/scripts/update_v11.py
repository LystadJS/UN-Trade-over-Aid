"""Reproduce the seven-award review from retained v0.10 data and v0.11 snapshots.
No live access; historical agency action, award identity and current survival are distinct.
"""
from pathlib import Path
import csv,json,collections,hashlib,re
from lxml import etree
import fitz
P=Path(__file__).resolve().parents[1];D=P/'data';H=P/'history/v0_10/data';E=P/'research_v11/evidence'
def read(n,root=H):return list(csv.DictReader((root/(n+'.csv')).open(encoding='utf-8-sig')))
def write(n,rows):
 fields=list(dict.fromkeys(k for r in rows for k in r))
 with (D/(n+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
def join(*s):return ';'.join(dict.fromkeys(t for x in s for t in x.split(';') if t))
def js(n):return json.loads((E/(n+'.json')).read_text())
contracts=[('72067424F00006',291396509),('72067423C00003',291396424),('72067424C00001',291396504)]
newids=[('AID-OAA-A-15-00054',259407464),('AID-AFR-IO-16-00001',259403396)]
court={'72067424F00006':('2025-02-11',2,21),'72067424C00001':('2025-02-11',2,20),'72067423C00003':('2025-02-12',11,182),'72067422CA00003':('2025-02-11',4,54),'72067424C00002':('2025-02-12',11,183),'72067425C00001':('2025-02-12',11,184)}
doc=fitz.open(E/'V11_COURT_20_1_RECAP.pdf')
for aid,(date,page,row) in court.items():assert aid in doc[page-1].get_text(),aid
actions=[]
for aid,internal in contracts+newids:
 sid=f'V11_TRANS_{internal}_1';j=js(sid);assert not j['page_metadata']['hasNext']
 for r in j['results']:
  actions.append(dict(award_id=aid,record_type='federal_transaction_report',action_date=r['action_date'],action_code=r.get('action_type') or '',action_description=r.get('action_type_description') or 'New award; action code blank',modification_number=r.get('modification_number',''),federal_action_obligation_USD=r.get('federal_action_obligation',''),description=r['description'],source_id=sid,source_locator=r['id'],interpretation_limit='Reported transaction, not signed instrument. EX means other non-financial action; a load/update date is not the action date.'))
 # Check the mirrored procurement feed independently for the three contracts.
 if (aid,internal) in contracts:
  root=etree.parse(str(E/f'V11_FPDS_{aid}.xml'));entries=root.xpath('//*[local-name()="entry"]')
  mods=[e.xpath('.//*[local-name()="awardContractID"]/*[local-name()="modNumber"]/text()')[0] for e in entries]
  assert set(mods)=={r['modification_number'] for r in j['results']}
for aid,(date,page,row) in court.items():
 actions.append(dict(award_id=aid,record_type='government_court_filed_notice_roster',action_date=date,action_code='notice_of_termination',action_description='Listed under Notice of Termination in government-filed attachment',modification_number='',federal_action_obligation_USD='',description='DOJ filed the USAID list on February 12, 2025. Cover notice encompasses terminations or stop-work orders; attachment labels these rows Notice of Termination.',source_id='V11_COURT_20_1_RECAP',source_locator=f'ECF 20-1, PDF p. {page}, spreadsheet row {row}',interpretation_limit='Government primary action report; signed award notice not obtained. Historical notice issuance does not certify present termination, reinstatement, delivery or legal effect.'))
write('primary_award_actions_v11',actions)

review=[]
survival=read('legacy_award_survival_v10');byid={r['award_id']:r for r in survival}
for aid,(date,page,row) in court.items():
 r=byid[aid];r['survival_disposition']='government_court_filed_termination_notice'
 r['evidence_basis']=f'Government-filed ECF 20-1 p. {page}, row {row}, lists notice dated {date}; ECF 20 establishes DOJ/agency provenance. Not a signed award modification or proof of current legal or delivery status.'
 if aid=='72067422CA00003':r['evidence_basis']+=' Abt separately reports February 26, 2025 termination; do not collapse the two dates or infer rescission between them.'
 r['source_ids']=join(r['source_ids'],'V11_COURT_20_1_RECAP;V11_COURT_20_RECAP;V11_COURT_OPINION_GPO')
for aid,internal in contracts:
 r=byid[aid];j=js(f'V11_TRANS_{internal}_1');latest=max(j['results'],key=lambda x:x['action_date']);date,page,row=court[aid]
 r['source_ids']=join(r['source_ids'],f'V11_TRANS_{internal}_1;V11_FPDS_{aid}')
 note='No termination-coded action in the returned financial histories; the court-filed primary notice roster supplies the historical action.'
 if aid=='72067424C00001':note+=' P00003 is a March 7, 2025 administrative DEI-related entry with truncated description, not affirmative continuation or rescission.'
 review.append(dict(award_id=aid,recipient=r['recipient'],instrument='Federal procurement contract/task order',identity_status='verified_federal_award',historical_action_status='verified_government_report_of_termination_notice',action_date=date,action_locator=f'ECF 20-1 p. {page}, row {row}',latest_transaction_date=latest['action_date'],latest_transaction_action=latest.get('action_type_description') or 'New award; blank action code',scheduled_end_date=r['scheduled_end_date'],current_continuation='unverified',finding=note,source_ids=r['source_ids'],remaining_requirement='Post-notice contracting-officer action chain, including any rescission/reinstatement and latest SAM record; current operating confirmation.',reviewed_on='2026-10-15'))
for aid,internal in newids:
 j=js(f'V11_AW_{internal}');tr=js(f'V11_TRANS_{internal}_1');latest=max(tr['results'],key=lambda x:x['action_date']);assert j['fain']==aid.replace('-','') and j['uri'].startswith(aid+'-')
 dogesid='V11_DOGE_GRANTS_11' if internal==259407464 else 'V11_DOGE_GRANTS_5';idx=406 if internal==259407464 else 427
 g=js(dogesid)['result']['grants'][idx];assert g['recipient']==j['recipient']['recipient_name'] and g['value']==j['total_obligation'] and g['link'] is None
 finding='Federal FAIN and hyphenated URI resolve identity. DOGE reports a matching recipient/project cancellation dated March 1, 2025, but omits award ID/link; award-level action crosswalk remains qualified. Latest returned transaction is non-financial and predates 2025.'
 ids=f'V11_AW_{internal};V11_TRANS_{internal}_1;{dogesid};V11_LEGACY_ROSTER_MIRROR;V10_SFRC_REPORT'
 survival.append(dict(program_id='USAID02',award_id=aid,award_internal_id=str(internal),recipient=j['recipient']['recipient_name'],description=j['description'],program_link_status='federal_identity_verified_program_link_corroborated_by_government_project_description',reported_awarding_office=j['awarding_agency']['office_agency_name'] or '',scheduled_end_date=j['period_of_performance']['end_date'],last_modified_date=j['period_of_performance']['last_modified_date'],prior_transaction_termination_flag='not_found_in_returned_history',survival_disposition='government_reported_project_cancellation_qualified_award_link',evidence_basis=finding,current_survival_certified='no',source_ids=ids,next_check='Signed agreement-officer termination/rescission/closeout action naming this FAIN; distinguish DOGE project report from award-specific action.',reviewed_on='2026-10-15'))
 review.append(dict(award_id=aid,recipient=j['recipient']['recipient_name'],instrument=j['type_description'],identity_status='resolved_federal_fain_and_uri',historical_action_status='government_project_cancellation_award_link_qualified',action_date='2025-03-01',action_locator=f'{dogesid}, zero-based row {idx}; cancellation date as reported by DOGE',latest_transaction_date=latest['action_date'],latest_transaction_action=latest['action_type_description'],scheduled_end_date=j['period_of_performance']['end_date'],current_continuation='unverified',finding=finding+(' A January 6, 2026 record update is not a 2026 action; latest action remains May 25, 2022.' if internal==259403396 else ''),source_ids=ids,remaining_requirement='Executed 2025 cancellation and subsequent action chain naming the award ID; current owner and delivery status.',reviewed_on='2026-10-15'))
for aid,recipient,page,desc in [('72067424T00001','Commerce / CLDP',283,'Five-year legal/regulatory support to Power Africa governments; generation/transmission investment and project contracting.'),('72067420T00001','U.S. International Development Finance Corporation',277,'Participating Agency Program Agreement for Washington-based deal teams supporting Power Africa.')]:
 review.append(dict(award_id=aid,recipient=recipient,instrument='Interagency agreement (mirrored roster identification)',identity_status='qualified_exact_id_in_mirrored_agency_roster',historical_action_status='unverified_award_specific_agency_action',action_date='',action_locator=f'Mirrored March 6, 2025 roster, PDF p. {page}',latest_transaction_date='',latest_transaction_action='',scheduled_end_date='',current_continuation='unverified',finding=desc+' The exact ID appears in a publicly mirrored agency-origin roster and the Senate report, but no authenticated signed agreement or action chain was obtained. No match in successful USAspending contract, grant, direct-payment or other-assistance searches; that absence does not invalidate an interagency agreement.',source_ids='V11_LEGACY_ROSTER_MIRROR;V10_SFRC_REPORT',remaining_requirement='USAID/State and receiving-agency agreement register, signed IAA/PAPA and amendments/cancellation notices; authorized SAM extract if a procurement record exists.',reviewed_on='2026-10-15'))
order=[x[0] for x in contracts]+['72067424T00001','AID-OAA-A-15-00054','AID-AFR-IO-16-00001','72067420T00001'];review.sort(key=lambda r:order.index(r['award_id']))
write('power_africa_action_review_v11',review);write('legacy_award_survival_v11',survival)
write('legacy_award_followup_ids_v11',[dict(program_id='USAID02',award_id=r['award_id'],identity_status=r['identity_status'],action_status=r['historical_action_status'],finding=r['finding'],source_ids=r['source_ids'],next_check=r['remaining_requirement']) for r in review if r['award_id'] not in {a for a,i in contracts}])

# Retain the agency's public cancellation reports and explicitly reject amount-only joins.
doge=[];coverage={}
for kind in ['contracts','grants']:
 rows=[]
 for f in sorted(E.glob('V11_DOGE_'+kind.upper()+'_*.json')):
  if 'receipt' in f.name:continue
  j=json.loads(f.read_text());rows.extend(j['result'][kind])
 coverage[kind]={'retrieved_rows':len(rows),'distinct_full_row_serializations':len({json.dumps(x,sort_keys=True) for x in rows}),'limit':'Pagination on value may contain ties/duplicates. This is not a certified count of unique awards; absence is not evidence of survival.'}
 if kind=='contracts':
  usaid=[r for r in rows if 'international development' in r.get('agency','').lower() or r.get('agency')=='USAID']
  coverage[kind]['usaid_rows']=len(usaid);coverage[kind]['usaid_rows_with_unavailable_piid']=sum(r.get('piid')=='Unavailable' for r in usaid)
for sid,idx,aid,joinstatus in [('V11_DOGE_GRANTS_11',406,'AID-OAA-A-15-00054','qualified_recipient_project_and_amount'),('V11_DOGE_GRANTS_5',427,'AID-AFR-IO-16-00001','qualified_recipient_project_and_amount'),('V11_DOGE_CONTRACTS_1',238,'','rejected_amount_only'),('V11_DOGE_CONTRACTS_1',248,'','rejected_amount_only'),('V11_DOGE_CONTRACTS_9',404,'','rejected_amount_only')]:
 kind='grants' if 'GRANTS' in sid else 'contracts';g=js(sid)['result'][kind][idx]
 doge.append(dict(source_id=sid,zero_based_row=idx,qualified_award_id=aid,join_status=joinstatus,reported_date=g.get('date') or g.get('deleted_date'),recipient_or_vendor=g.get('recipient') or g.get('vendor'),value_USD=g.get('value'),description=g.get('description'),award_id_exposed=g.get('piid') or '',source_link=g.get('link') or g.get('fpds_link') or '',interpretation_limit='Government-reported cancellation; no signed notice. Never infer an award ID from an amount alone. The public site describes data last updated January 1, 2026.'))
write('doge_cancellation_crosswalk_v11',doge)
(D/'doge_review_coverage_v11.json').write_text(json.dumps(coverage,indent=2))

master=read('program_census');M={x['program_id']:x for x in master};r=M['USAID02']
r['review_result']='Three priority contracts have February 2025 notice dates in a government court filing; two of four unmatched IDs resolve to federal FAINs. Two IAA identities remain qualified. Selected Power Africa audit now has 13 awards; no present continuation certified.'
r['evidence_limit']='Historical termination notices are verified agency reports, not current final status. DOGE project cancellations for CrossBoundary and Scaling Solar omit award IDs; their action crosswalks remain qualified. Two interagency agreements lack authenticated action chains.'
r['review_source_ids']=join(r['review_source_ids'],'V11_COURT_20_1_RECAP;V11_COURT_20_RECAP;V11_AW_259407464;V11_AW_259403396;V11_DOGE_GRANTS_11;V11_DOGE_GRANTS_5')
for n in ['program_census','expanded_inventory']:write(n,master)
for n in ['inventory_view','ownership_review']:
 rows=read(n)
 for x in rows:
  for k in x:
   if k in M[x['program_id']]:x[k]=M[x['program_id']][k]
 write(n,rows)
legacy=read('legacy_reconciliation')
for x in legacy:
 x['v11_resolution']='Prior adjudication retained; this pass focuses on seven Power Africa award gaps.'
 if x['program_id']=='USAID02':
  x['evidence_limit']=r['evidence_limit'];x['award_budget_finding']=r['review_result'];x['v11_resolution']=r['review_result'];x['source_ids']=join(x['source_ids'],r['review_source_ids'])
  x['remaining_requirement']='Retrieve post-notice action chains for three contracts; executed cancellation/closeout records for CrossBoundary and Scaling Solar; authenticated CLDP/DFC interagency agreements and amendments. Current ownership/intake/delivery remain unverified.'
write('legacy_reconciliation',legacy);L={x['program_id']:x for x in legacy}
roster=read('roster_verification_v10')
for x in roster:
 if x['program_id']=='USAID02':
  x['evidence_limit']=r['evidence_limit'];x['next_check']=L['USAID02']['remaining_requirement'];x['source_ids']=join(x['source_ids'],r['review_source_ids'])
  if x['field']=='country_delivery':x['finding']=r['review_result']+' Historical award location is not current country delivery.'
write('roster_verification_v11',roster)
gaps=read('remaining_evidence_gaps')
for x in gaps:
 if x['program_id']=='USAID02':x.update(status=r['review_result'],remaining_requirement=L['USAID02']['remaining_requirement'],specific_next_check=L['USAID02']['remaining_requirement'],source_ids=r['review_source_ids'])
write('remaining_evidence_gaps',gaps)
cor=read('corrections');cor.extend([
 dict(issue='Three Power Africa future-date-only records',prior='Future dates with no verified current continuation',corrected='Primary government filing records February 11–12, 2025 termination notices; current continuation remains unverified',basis='ECF 20 and 20-1; procurement transaction feeds lack corresponding termination codes',affected='Action review, survival table, briefing'),
 dict(issue='Four unmatched legacy IDs',prior='No joined federal award details',corrected='CrossBoundary cooperative agreement and Scaling Solar type-11 assistance now matched by FAIN and URI; CLDP/DFC interagency identities remain qualified',basis='Normalized IDs and broader assistance-category query; no amount-only identity inference',affected='Follow-up table and selected survival cohort expands from 23 to 25'),
 dict(issue='HETA and two other Power Africa notice reports',prior='Recipient/congressional termination reports',corrected='Government court roster supplies earlier notice dates; HETA later February 26 recipient report retained as separate dated evidence',basis='ECF 20-1 pp. 4 and 11',affected='Survival disposition; no current legal-status inference')]);write('corrections',cor)

sources=read('source_registry_v10')
for f in sorted(E.glob('*_receipt.json')):
 x=json.loads(f.read_text());x['purpose']='Seven-award primary action and identifier reconciliation';x['source_url']=x['url'];x['local_path']='research_v11/'+x['snapshot'] if x.get('snapshot') else ''
 x['use_limit']='Transport result is not claim verification; public transaction feeds may lag. Government court filing verifies historical reports only. Mirrored agency-origin roster is a qualified identity lead, not authenticated agency action.'
 if x['local_path']:x['archive_sha256']=hashlib.sha256((P/x['local_path']).read_bytes()).hexdigest()
 for k,v in list(x.items()):
  if isinstance(v,(dict,list)):x[k]=json.dumps(v,ensure_ascii=False)
 sources.append(x)
write('source_registry_v11',sources)
S=json.loads((H/'census_summary.json').read_text());S.update(v11_priority_awards_reviewed=7,v11_priority_contract_notice_dates_verified=3,v11_legacy_ids_federally_resolved=2,v11_legacy_ids_qualified_only=2,v11_current_continuations_verified=0,v11_selected_legacy_awards=25,v11_selected_power_africa_awards=13,v11_primary_transaction_rows=17,v11_court_notice_rows=6,v11_source_attempts=len(list(E.glob('*_receipt.json'))),v11_award_survival_dispositions=dict(collections.Counter(x['survival_disposition'] for x in survival)),v11_new_country_observations=0)
(D/'census_summary.json').write_text(json.dumps(S,indent=2))
(D/'workbook_data.json').write_text(json.dumps({f.stem:list(csv.reader(f.open(encoding='utf-8-sig'))) for f in D.glob('*.csv')},ensure_ascii=False))
assert len(actions)==23 and len(survival)==25 and len(review)==7
print(json.dumps({k:v for k,v in S.items() if k.startswith('v11')},indent=2))
