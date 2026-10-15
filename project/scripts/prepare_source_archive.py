"""Preserve full public federal records; distribute attributed notes for third-party articles."""
from pathlib import Path
import csv,json,hashlib,re,html
P=Path(__file__).resolve().parents[1];E=P/'research_v08/evidence'
notes={
'PHOENIX_SL':'The implementer reported on February 9, 2026 that the Slovak SMR feasibility study was completed. It explicitly places Project Phoenix under State\'s FIRST program and names similar ongoing assistance in Estonia, Ukraine and Slovenia. The other countries in the stated regional total are not individually identified. This is implementer-reported assistance, not proof of reactor construction or a sale.',
'PHOENIX_SEAS_CURRENT':'The Slovak electricity utility reported the SMR feasibility-study findings on January 15, 2026 and identified U.S. support through Phoenix/FIRST. Four Slovak candidate locations were assessed. The release establishes reported study completion, not construction or a reactor procurement.',
'DAI_ATI':'DAI states that its Africa Trade and Investment project was terminated following the Secretary of State\'s 2025 foreign-assistance review. The page identifies ATI as a Prosper Africa flagship component. Its duration header says 2021–2024, which conflicts with the narrative termination year; the research does not supply an exact termination date or infer termination of the entire Prosper Africa umbrella.',
'RAPP_NASDA':'NASDA attributes a June 1–6, 2026 inbound forest-bioeconomy mission from Finland to USDA RAPP support. The event took place in Maine. NASDA also attributes an October 25–30, 2025 UK-origin sustainable-aviation-fuel mission in Illinois, Iowa and Nebraska to RAPP. Foreign delegation origin is not the U.S. delivery venue and does not override program target-market restrictions. The Finland account is repeated under a 2025 heading; the stated event year is 2026.',
'SBA_FL_STEP':'The Florida SBDC page states that its administration of STEP concluded on October 1, 2026. This is a state-provider finding, not evidence that the nationwide federal program ended.',
'NASEM_INTRO':'A National Academies introductory resource was examined as a discovery lead. No positive country-program activity observation in the v0.8 ledger relies on this page.',
'NASEM_ITSI':'A National Academies ITSI resource was examined as a discovery lead. No positive country-program activity observation in the v0.8 ledger relies on this page.',
'BASE_DOE02_103':'The retrieved Lab Partnering Service page exposed a page title but insufficient operating detail. Current service operation remains unresolved.'}
sources={r['source_id']:r for r in csv.DictReader(open(P/'data/source_registry_v08.csv',encoding='utf-8-sig'))};treat=[]
for sid,note in notes.items():
 r=sources[sid];url=r.get('url','');message='ATTRIBUTED EVIDENCE NOTE — NOT THE ORIGINAL PAGE\nSource: '+url+'\nRetrieved: 15 October 2026\n\n'+note+'\n'
 for ext in ['.html','.txt']:
  p=E/(sid+ext)
  if p.exists():
   p.write_text('<!doctype html><meta charset="utf-8"><title>Evidence note</title><pre>'+html.escape(message)+'</pre>' if ext=='.html' else message)
   treat.append({'source_id':sid,'delivered_file':str(p.relative_to(P)),'treatment':'Attributed paraphrase; original retrieval checksum retained separately in original receipt/source register','delivered_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_url':url})
# Search-response text can reproduce third-party articles. Keep identifiers and URLs as discovery provenance instead.
search=P/'research_v08/search';index=[]
for p in search.glob('*.json'):
 raw=p.read_text();index.append({'original_response_file':p.name,'original_response_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_urls':';'.join(sorted(set(re.findall(r'https?://[^\s"<>\\)]+',raw)))),'treatment':'Full search result text omitted; primary government snapshots and attributed third-party evidence notes retained'})
 p.unlink()
for name,rows in [('snapshot_archival_treatment',treat),('search_discovery_index',index)]:
 with open(P/'data'/(name+'.csv'),'w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
(P/'research_v08/ARCHIVE_POLICY.txt').write_text('Federal public records and factual data extracts are retained in full. Third-party articles are represented by attributed evidence notes and source URLs. These notes occupy the original HTML/TXT paths for source-link continuity and are clearly labeled. Source-registry and receipt SHA256 values identify original retrieval bytes; the release MANIFEST_SHA256.csv identifies the bytes actually delivered. The archival-treatment table provides the mapping. Search discovery provenance retains source URLs and original response checksums, without reproducing complete article text. This treatment does not alter the structured evidence ledger or classifications. Re-fetching a source requires independent access to the cited URL.\n')
print('Prepared',len(treat),'third-party note files and',len(index),'search provenance entries')
