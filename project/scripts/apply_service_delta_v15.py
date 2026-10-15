"""Replay the reviewed v15 additions against retained v14 baseline inputs. No network required."""
from pathlib import Path
import csv,json,collections
R=Path(__file__).resolve().parents[1];D=R/'data';B=R/'research_v15/baseline'
def read(n,base=B):return list(csv.DictReader((base/(n+'.csv')).open(encoding='utf-8-sig')))
def write(n,rows):
 with (D/(n+'.csv')).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
ledger=read('country_activity_ledger');adds=[]
def add(pid,cc,sid,stage,asof,start,end,description,role,limit,record='',level='primary_agency_report'):
 rec=json.loads((R/'research_v15/evidence'/('V15_'+sid+'_receipt.json')).read_text());assert rec['status']==200
 x={k:'' for k in ledger[0]};x.update(observation_id=f'OBS{2184+len(adds):05}',program_id=pid,country_code=cc,source_geography=cc,geography_role=role,stage=stage,evidence_as_of=asof,event_start=start,event_end=end,description=description,source_id='V15_'+sid,source_url=rec['url'],source_record_id=record or 'V15_'+sid,evidence_level=level,include_in_program_matrix='yes' if stage=='D' else 'no',limitation=limit);adds.append(x)
add('FAS11','AU','FAS_AU','D','2026-08-30','2026-08-30','','Australian agriculture ministry reports USDA agribusiness mission delegates visiting Melbourne','mission_destination','Ongoing presence reported August 30; not completed mission. Australian notice lists August 30–September 3 while USDA schedule lists August 30–September 2; no end date asserted. Official-page web extraction retained because direct HTTP timed out.',level='primary_host_government_report')
add('FAS11','ID','FAS_ID','D','2026-02-26','2026-02-02','2026-02-05','U.S. Wheat participant account dates USDA Indonesia mission and reports meetings and site visits','mission_destination','Corroborates existing FAS11–ID pair; not another mission or proof that purchase commitments were fulfilled.',level='primary_participant_report')
add('FAS11','PH','FAS_PH','D','2026-04','2026-04-12','2026-04-16','Wisconsin DATCP participant account reports USDA Philippines mission and B2B meetings','mission_destination','Publication date unstated; April is activity month. DATCP gives April 12–16; USDA public itinerary gives April 13–16. Preserved participant travel interval; existing pair not counted again.',level='primary_participant_state_agency_report')
add('USTDA05','PH','USTDA_PH','D','2026-09-14','','','USTDA reports completed Luzon Economic Corridor forum and project-site tours in Batangas, Clark and Subic Bay','delivery_venue','Retrospective report date, not imputed event date. Sponsored forum maps to conference/workshop instrument; not a completed investment, reverse trade mission, study or verified legacy award.')
for cc,aid,date,desc in [('MX','202051014A','2026-03-11','Micro-scale LNG plants feasibility study'),('BR','202051003A','2026-03-03','Santos Dumont Airport safety assessment and improvement plan'),('PH','202031025A','2026-02-19','Metro Cebu intelligent transportation technical assistance'),('PH','202131014A','2026-01-30','Sunkeeper utility-scale solar feasibility study')]:
 add('USTDA01',cc,'USTDA_REPORTS','D','2026-03-26','',date,'Official final-report catalog lists completed '+desc,'project_location','D records reported project-preparation output only. End date is catalog Date Completed, not construction completion, fieldwork date, commercial close or verified continuing activity. Underlying final report not obtained. Source PDF p.1.',record=aid+' / volume 1',level='primary_agency_final_report_catalogue')
add('USTDA04','PH','USTDA_REPORTS','H','2026-03-26','','2025-12-10','Catalog lists PLDT–Cisco grant-training final report completed in 2025','project_location','Historical report-completion metadata; actual training dates and venue not established. Not current delivery or program termination. Source PDF p.1.',record='202131013A / volume 1',level='primary_agency_final_report_catalogue')
add('ITA14','PE','ITA_PE','H','2025-12-09','2025-10','2025-10','Signed ETTAC minutes retrospectively report Expo Agua TEPP matchmaking in Lima in October 2025','delivery_venue','Historical matchmaking explicitly attributed to TEPP; not Gold Key or 2026 delivery. Month precision preserved. PDF p.2.',level='primary_agency_signed_minutes')
write('service_delivery_additions_v15',adds);write('country_activity_ledger',ledger+adds)
a=read('country_program_activity_matrix');s=read('country_program_stage_matrix');ai={r['country_code']:r for r in a};si={r['country_code']:r for r in s};deltas=[]
for x in adds:
 cc,p,c=x['country_code'],x['program_id'],x['stage'];si[cc][p]='+'.join(sorted((set(si[cc][p].split('+'))-{'U'})|{c}))
 if c=='D' and ai[cc][p]=='U':ai[cc][p]='D';deltas.append((cc,p))
write('country_program_activity_matrix',a);write('country_program_stage_matrix',s)
for name in ['program_census','expanded_inventory']:
 rs=read(name)
 for r in rs:
  pid=r['program_id']
  if pid in ['USTDA01','USTDA05']:
   sid='V15_USTDA_REPORTS' if pid=='USTDA01' else 'V15_USTDA_PH';r['operational_evidence']='recent_delivery_reported';r['current_status_verified']='recent_delivery_reported';r['review_source_ids']+=';'+sid;r['reviewed_on']='2026-10-15';r['review_result']='Catalog-reported 2026 final-report completion; underlying reports not obtained.' if pid=='USTDA01' else 'Agency reports completed sponsored forum and site visits in Philippines.'
  if pid in {x['program_id'] for x in adds}:r['country_activity_observations']=str(sum(x['program_id']==pid for x in ledger+adds))
 write(name,rs)
reg=read('source_registry_v11')
for f in sorted((R/'research_v15/evidence').glob('*_receipt.json')):
 rec=json.loads(f.read_text());x={k:'' for k in reg[0]};x.update({k:v for k,v in rec.items() if k in x});x['snapshot']='research_v15/'+rec.get('snapshot','');x['purpose']='v15 matchmaking, USTDA and FAS dated delivery review; see additions and limitations';reg.append(x)
write('source_registry_v11',reg)
ids=[k for k in a[0] if k not in ['country','country_code']]
summary=dict(new_observations=len(adds),new_pairs=deltas,qualifying_pairs=sum(r[p]!='U' for r in a for p in ids),delivered_pairs=sum(r[p]=='D' for r in a for p in ids),observed_programs=sum(any(r[p]!='U' for r in a) for p in ids),countries=sum(any(r[p]!='U' for p in ids) for r in a),ledger_rows=len(ledger+adds))
(R/'validation/service_delta_v15.json').write_text(json.dumps(summary,indent=2));print(summary)
