"""Scoped, evidence-coded update. Run once on a copy of v0.8; never synthesizes activity."""
from pathlib import Path
import csv,json,shutil,collections,hashlib
P=Path(__file__).resolve().parents[1];D=P/'data';E=P/'research_v09/evidence'
def read(n):return list(csv.DictReader((D/(n+'.csv')).open(encoding='utf-8-sig')))
def write(n,rows,fields=None):
 fields=fields or list(dict.fromkeys(k for r in rows for k in r))
 with (D/(n+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
H=P/'history/v0_8'
if H.exists():raise RuntimeError('Already updated; restore clean v0.8 before rerunning')
for folder in ['data','deliverables','scripts','validation']:
 shutil.copytree(P/folder,H/folder)
L=read('legacy_reconciliation');B={r['program_id']:r for r in L}
def amend(pid,**kw):B[pid].update(kw)
functional='An August 12–18, 2026 State vacancy assigns commercial-affairs functions and CDCM platform duties to EEB/CBA. This is not a staffing count or a named legacy-program assignment.'
for pid in ['STATE01','STATE02','STATE04','STATE07']:
 amend(pid,ownership_evidence=functional,source_ids=B[pid]['source_ids']+';V09_USAJOBS_CBA;V09_TPCC',v09_resolution='Current commercial-affairs function identified; named program ownership and intake unresolved')
amend('STATE02',evidence_limit='A secondary August 7 report describes an August 6, 2026 Pakistan-focused Direct Line webinar. No primary event record retrieved; retained as a lead, not a verified activity cell.')
amend('STATE03',source_ids=B['STATE03']['source_ids']+';V09_TPCC',v09_resolution='Live Commerce catalog lists TAF, but does not establish current owner, funding or intake')
amend('USAID01',award_budget_finding='DAI confirms ATI termination. Indexed USAID grant-manual and annual-report text associates ATI with contract 7200AA21C00056, the same identifier as the retained PATI award. Prior assertion of a separate component is withdrawn; full crosswalk document retrieval remains incomplete.',evidence_limit='Five selected awards are not an umbrella census. Indexed original contract text is a crosswalk lead, not a fully archived document. Do not infer all Prosper Africa components terminated.',remaining_requirement='Retrieve ATI contract/manual text in full; obtain surviving Prosper Africa project roster and current umbrella assignment.',source_ids=B['USAID01']['source_ids']+';V09_ATI_CROSSWALK;V09_ATI_REPORT;V09_ATI_INDEX',v09_resolution='Unsupported separate-component claim removed; matching contract identifier recorded with retrieval limitation')
amend('USAID02',v09_resolution='No current program-specific operating roster established; conditional State succession remains')
amend('STATE08',current_owner='State; EEB named by the ASU ITSI Skills Accelerator implementer; Under Secretary for Economic Affairs for the 2026 Pax Silica solicitation. Whole-fund allocation map unresolved.',ownership_evidence='ASU component portal identifies State EEB and ASU implementation. This does not assign every ITSI allocation to the same office.',intake_status='Pax Silica DFOP0019193 closed August 20, 2026. ASU Skills Accelerator publishes a technical-training license request route, subject to availability; form submission and acceptance not tested. No general ITSI intake established.',evidence_limit='Implementer portal contains placeholder testimonials and counters; no participant totals or country outcomes accepted. A component training request is not a grant competition or proof of delivery.',remaining_requirement='Obtain current ITSI award/allocation roster and dated country cohort completion records; confirm component license availability.',source_ids=B['STATE08']['source_ids']+';V09_PAX;V09_ITSI_ABOUT;V09_ITSI_TECH;V09_ITSI_PORTAL',v09_resolution='Component-level office and published training intake route identified; country delivery unresolved')
amend('STATE09',source_ids=B['STATE09']['source_ids']+';V09_FCC_DCCP;V09_FCC_DCCP_TXT;V09_FCC_INDEX',v09_resolution='Costa Rica indexed official lead retained; full speech inaccessible, so no new activity admitted')
amend('STATE10',source_ids=B['STATE10']['source_ids']+';V09_FIRST_ROSTER',v09_resolution='Prior recipient/implementer delivery evidence retained; current FIRST website maintenance notice adds no roster or intake evidence')
for pid,sid in [('FAS05','V09_FAS_RAPP2'),('FAS12','V09_FAS_ATP2')]:
 amend(pid,current_owner='USDA/FAS; Program Operations Division is the published program contact',ownership_evidence='Current FAS program roster and named program page list Program Operations Division contact. This establishes an agency contact, not a live funding round.',source_ids=B[pid]['source_ids']+';V09_FAS_ROSTER;'+sid,v09_resolution='Agency and published division contact confirmed; dated funding evidence governs intake')
amend('SBA05',current_owner='SBA Office of Manufacturing and Trade (national STEP management); state entities administer local business applications',ownership_evidence='SBA assigns national STEP management to OMT. FY2026 NOFO section 1.1.15 identifies an OED program manager; section 5.2.3 assigns Tier II evaluation to OED and OMT. These are documented distinct roles, not a demonstrated ownership contradiction.',intake_status='FY2026 federal competition SB-OIT-STEP-2026-01 closed August 18, 2026; archived September 9. Connecticut publishes FY2025-funded applications for activities July 22, 2026–September 29, 2027, due July 1, 2027 subject to funds. Florida administration ended October 1, 2026.',award_budget_finding='Grants.gov opportunity 363144 and revised FY2026 NOFO verify the competition and $20 million announced ceiling. Expected awards and a planned September 30 start are not award selections, obligations or delivery.',evidence_limit='Federal application closure is not program closure. Connecticut explicitly labels its funding FY2025, not FY2026. Published federal and state application routes do not prove award selection or delivery; no applications submitted.',remaining_requirement='Obtain FY2026 award selections/obligations and state recipient roster; obtain funded overseas activity reports.',source_ids='SBA_STEP_DIR;SBA_FL_STEP;V09_SBA_OMT;V09_SBA_GRANTS;V09_STEP_API;V09_STEP_NOFO2026;V09_STEP_CT',v09_resolution='Federal competition and national management resolved; state route evidenced; FY2026 awards and foreign delivery unverified')
amend('ITA21',ownership_evidence='Commerce/ITA current program and active-award pages remain available; named staff capacity and project extensions not established.',source_ids=B['ITA21']['source_ids']+';V09_MDCP_MAIN;V09_MDCP',v09_resolution='Current agency roster and no-announced-FY2027-competition statement reaffirmed; seven stale award end dates remain')
amend('USTDA06',ownership_evidence='USTDA sector archive retains GPI. A current staff biography describes GPI management as a former role; it is not evidence of the current GPI lead.',evidence_limit='Latest visible archive posts are 2025. Current program lead, intake and dated 2026 country delivery remain unverified. One older staff URL returns 404; no closure inference.',remaining_requirement='Obtain current GPI project/country roster, responsible team and engagement intake channel.',source_ids=B['USTDA06']['source_ids']+';V09_GPI_ROSTER;V09_GPI_RANDOLPH;V09_GPI_LEADERSHIP',v09_resolution='Agency attribution retained; former staff role excluded as current owner evidence')
for r in L:r['reviewed_on']='2026-10-15'
write('legacy_reconciliation',L)
inv=read('program_census')
for r in inv:
 if r['program_id'] not in B:continue
 b=B[r['program_id']]
 for k in ['current_owner','ownership_evidence','intake_status','evidence_limit','reviewed_on']:r[k]=b[k]
 r['review_source_ids']=';'.join(dict.fromkeys((r['review_source_ids']+';'+b['source_ids']).split(';')))
 r['owner_source_ids']=b['source_ids'];r['review_result']=b['v09_resolution']
 if r['program_id']=='SBA05':r['operational_evidence']='funding_intake_or_approval_action'
write('program_census',inv);write('expanded_inventory',inv)
write('core_inventory',[r for r in inv if r['tier']=='core'])
for name in ['inventory_view','ownership_review']:
 fields=list(read(name)[0]);write(name,inv,fields)
gaps=read('remaining_evidence_gaps')
for r in gaps:
 if r['program_id'] in B:
  b=B[r['program_id']];r.update(status=b['v09_resolution'],remaining_requirement=b['remaining_requirement'],source_ids=b['source_ids'],specific_next_check=b['remaining_requirement'])
write('remaining_evidence_gaps',gaps)
owner={p:'unresolved_program_assignment' for p in B}
for p in ['FAS05','FAS12','ITA21','SBA05']:owner[p]='verified_agency_or_published_contact'
for p in ['STATE08','STATE10','USTDA06']:owner[p]='qualified_scope_or_role'
intake={p:'unresolved' for p in B}
intake.update(SBA05='federal_round_closed_state_route_published',FAS05='no_new_awards_dated_agency_decision',ITA21='no_next_competition_announced',STATE08='closed_competition_component_route_published')
country={p:'no_qualifying_current_delivery_in_collection' for p in B}
country.update(STATE10='reported_delivery_four_countries_retained',FAS05='US_delivery_foreign_origin_not_overseas_delivery')
R=[]
for b in L:
 p=b['program_id']
 for field,disp,claim in [('ownership',owner[p],b['current_owner']+' | '+b['ownership_evidence']),('intake',intake[p],b['intake_status']),('country_delivery',country[p],('No new country observation admitted in v0.9. '+b['award_budget_finding']))]:
  R.append(dict(program_id=p,name=b['name'],field=field,disposition=disp,finding=claim,source_ids=b['source_ids'],evidence_limit=b['evidence_limit'],next_check=b['remaining_requirement'],reviewed_on='2026-10-15'))
write('roster_verification_v09',R)
leads=[dict(program_id='STATE09',country_code='CR',country='Costa Rica',reported_event_date='2026-03-14',geography_role='reported_event_venue',admission_status='quarantined_official_index_only',finding='Indexed FCC speech thanks CLDP and DCCP at Costa Rica event; full source not retrieved.',source_url='https://docs.fcc.gov/public/attachments/DOC-419808A1.pdf',source_id='V09_FCC_INDEX',next_check='Obtain full FCC speech or primary CLDP event record explicitly naming DCCP.'),dict(program_id='STATE02',country_code='PK',country='Pakistan',reported_event_date='2026-08-06',geography_role='virtual_event_market_focus',admission_status='quarantined_secondary_only',finding='Secondary report identifies Direct Line webinar; cannot infer physical overseas venue or complete country delivery.',source_url='https://www.pakistantoday.com.pk/2026/08/07/us-sees-scope-for-deeper-agricultural-technology-partnership-with-pakistan',source_id='V09_DIRECTLINE_PK_LEAD',next_check='Find Embassy Islamabad, State, BCIU or Commerce original event record.')]
write('country_evidence_leads_v09',leads)
write('program_award_crosswalk_v09',[dict(program_id='USAID01',program_label='Africa Trade and Investment (ATI)',award_label='Prosper Africa Trade and Investment (PATI)',contract_number='7200AA21C00056',retained_award_id='291386309',disposition='same_identifier_in_indexed_primary_text_full_document_pending',finding='Remove prior separate-component assertion. Do not count this linkage as a second award or extend component termination to all Prosper Africa.',source_ids='V09_ATI_INDEX;V09_ATI_CROSSWALK;V09_ATI_REPORT;DAI_ATI',source_url='https://pdf.usaid.gov/pdf_docs/PA00ZBRJ.pdf')])
cor=read('corrections')
cor += [dict(issue='ATI/PATI component relationship',prior='ATI described as a separate component from retained PATI termination',corrected='Separate-component assertion withdrawn; indexed USAID text shows matching contract 7200AA21C00056; full document still pending',basis='V09_ATI_INDEX; retained PATI award metadata',affected='Current legacy review, paper and award crosswalk; v0.8 preserved as superseded'),dict(issue='STEP federal intake and owner',prior='FY2026 competition unresolved; owner wording included lending offices',corrected='FY2026 competition closed August 18; national management assigned to OMT, program contact to OED, and Tier II evaluation to both offices',basis='V09_STEP_API;V09_STEP_NOFO2026;V09_SBA_GRANTS',affected='Current inventory, ownership, legacy review, paper and counts')]
write('corrections',cor)
notes={'V09_ATI_INDEX':('https://pdf.usaid.gov/pdf_docs/PA00ZBRJ.pdf','Indexed USAID ATI grants manual and annual-report text show contract 7200AA21C00056. Full manual failed retrieval; annual-report URL redirects to USAID home. Identifier lead only.'),'V09_FCC_INDEX':(leads[0]['source_url'],leads[0]['finding']),'V09_DIRECTLINE_PK_LEAD':(leads[1]['source_url'],leads[1]['finding'])}
for sid,(url,note) in notes.items():
 (E/(sid+'.txt')).write_text('Attributed evidence note, not full source\nURL: '+url+'\nReviewed 2026-10-15\n'+note+'\n')
 (E/(sid+'_receipt.json')).write_text(json.dumps(dict(source_id=sid,url=url,status='index_or_secondary_lead',snapshot='evidence/'+sid+'.txt',retrieved_utc='2026-10-15',use_limit='Not admitted to current delivery matrix; full primary text required'),indent=2))
# Keep third-party originals outside delivered archive; provide brief attributed factual notes.
raw=P.parent.parent/'research_v09_raw';raw.mkdir(exist_ok=True)
asu_notes={'V09_ITSI_PORTAL':'ASU ITSI portal identifies the Skills Accelerator. Placeholder testimonials, counters and unrelated sample content make it unsuitable as an outcomes source. No participant counts accepted.', 'V09_ITSI_ABOUT':'Implementer page identifies State Bureau of Economic, Energy and Business Affairs as partner and ASU as implementer. It describes regional contacts and training license availability. This supports component attribution only.', 'V09_ITSI_TECH':'The technical-training page publishes a license request link. No application submitted or acceptance tested. A request route does not establish enrollment, current delivery, or country eligibility.'}
for sid,note in asu_notes.items():
 for ext in ['html','txt']:
  f=E/(sid+'.'+ext)
  if f.exists():
   shutil.copy2(f,raw/f.name);f.write_text('ARCHIVE EVIDENCE NOTE: original copyrighted page omitted.\n'+note+'\nSee source receipt for URL and original retrieval hash.\n')
sources=read('source_registry_v08')
for f in sorted(E.glob('*_receipt.json')):
 r=json.loads(f.read_text());r['purpose']='v0.9 legacy roster, intake and delivery validation';r['source_url']=r.get('url','')
 r['local_path']='research_v09/'+r['snapshot'] if r.get('snapshot') else ''
 r['use_limit']=r.get('use_limit','Retrieval is not proof of current operation; field-level decision in roster_verification_v09.')
 if r['source_id']=='V09_ATI_REPORT':r['use_limit']='Redirected to USAID homepage; requested report NOT retrieved.'
 if r['source_id'] in asu_notes:r['use_limit']='Attributed brief evidence note replaces original page; original retrieval hash retained.'
 if r['local_path'] and (P/r['local_path']).exists():r['archive_sha256']=hashlib.sha256((P/r['local_path']).read_bytes()).hexdigest()
 sources.append(r)
write('source_registry_v09',sources)
S=json.loads((D/'census_summary.json').read_text());S['operational_evidence_counts']=dict(collections.Counter(r['operational_evidence'] for r in inv));S['v09_roster_programs']=15;S['v09_field_assessments']=45;S['v09_new_country_observations']=0;S['v09_source_attempts']=len(list(E.glob('*_receipt.json')))-3;S['v09_country_leads_quarantined']=2
(D/'census_summary.json').write_text(json.dumps(S,indent=2))
book=json.loads((D/'workbook_data.json').read_text())
for n in list(book)+['source_registry_v09','roster_verification_v09','country_evidence_leads_v09','program_award_crosswalk_v09']:
 if (D/(n+'.csv')).exists():book[n]=list(csv.reader((D/(n+'.csv')).open(encoding='utf-8-sig')))
(D/'workbook_data.json').write_text(json.dumps(book,ensure_ascii=False))
print(json.dumps(S,indent=2))
