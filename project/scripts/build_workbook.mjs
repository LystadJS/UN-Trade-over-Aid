import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';
const root=process.env.TRADE_PACKAGE_DIR || path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(await fs.readFile(root+'/data/workbook_data.json','utf8'));
const stats=JSON.parse(await fs.readFile(root+'/data/census_summary.json','utf8'));
const wb=Workbook.create();
const specs=[['Priority action review','power_africa_action_review_v11'],['Primary actions','primary_award_actions_v11'],['Legacy ID followups','legacy_award_followup_ids_v11'],['Cancellation links','doge_cancellation_crosswalk_v11'],['Office assignments','program_office_assignments_v10'],['Award survival','legacy_award_survival_v11'],['Event links','event_program_links_v10'],['Roster checks','roster_verification_v11'],['Country leads','country_evidence_leads_v10'],['Award crosswalk','program_award_crosswalk_v09'],['Claim audit','claim_audit'],['Corrections','corrections'],['Legacy review','legacy_reconciliation'],['Selected awards','award_evidence'],['Award actions','award_actions'],['Budget evidence','budget_evidence'],['Inventory','inventory_view'],['Ownership','ownership_review'],['Changes','inventory_changes'],['Eligibility','eligibility_matrix'],['Scope profiles','program_scope_profiles'],['Geographic rules','program_geographic_rules'],['MCC forecast','mcc_procurement_forecast'],['Evidence gaps','remaining_evidence_gaps'],['Sources','expansion_sources'],['Codebook','codebook'],['Country activity','country_program_activity_matrix'],['Country stages','country_program_stage_matrix'],['DFC unallocated','dfc_unallocated_activity_matrix'],['Activity ledger','country_activity_ledger'],['Activity coverage','activity_coverage'],['EXIM FY2026','exim_fy2026_authorizations'],['DFC portfolio','dfc_active_portfolio'],['MCC lifecycle','mcc_lifecycle'],['MDCP targets','mdcp_country_targets'],['Current sources','source_registry_v11'],['Activity codes','activity_codebook'],['Agency frame','agency_coverage_screen']];
const summary=wb.worksheets.add('Read first');summary.showGridLines=false;
const text=[['U.S. trade facilitation census and country evidence'],['Evidence snapshot 15 October 2026. Defined research frame; agency-complete census not certified.'],['124 screened records; 62 direct-tool records. Counts are analyst-defined, not statutory program counts.'],['Country activity uses financing, reported delivery and project stages with separate definitions.'],['U means no qualifying observation in this collection, never zero activity or ineligibility.'],['Screened records',124],['Unknown eligibility cells'],['Conditional eligibility cells'],['EXIM off-cover cells'],['Direct-tool records',62],['Supporting services',20],['Overlapping initiatives',17],['Unresolved candidates',11],['Adjacent routes',3],['Excluded records',10],['Alias',1],['Observed country-program pairs',stats.observed_program_country_pairs],['Country evidence: 18 inventory records across 121 country or territory codes; see Activity codes.'],['Ledger has 2,170 observations. Shared events and overlapping products must not be summed as deals.'],['61 official offers alone do not confirm delivery; 18 records remain operationally unresolved.'],['7 priority awards reviewed: 3 historical notices verified; 2 legacy IDs resolved; 2 IAA leads qualified.'],['Eligibility and office/network matrices retain the earlier 62-tool scope; country activity is separate.'],['25 selected awards; 0 current continuations verified. Older audit tabs are historical; v0.11 reviews govern.']];
summary.getRange('A1').write(text.map(r=>[r[0],r[1]??null]));
summary.getRange('A1:B23').format.font={name:'Arial',size:11,color:'#172534'};
summary.getRange('A1:B1').merge();summary.getRange('A1').format.font={size:15,bold:true};
for(const r of [2,3,4,5,18,19,20,21,22,23])summary.getRange(`A${r}:J${r}`).merge();
summary.getRange('A1:J23').format.rowHeight=25;
summary.getRange('A:A').format.columnWidth=52;summary.getRange('B:B').format.columnWidth=24;summary.getRange('C:J').format.columnWidth=10;
for(const [title,key] of specs){
 const rows=data[key].map((r,i)=>i===0?r:r.map((v,j)=>['federal_action_obligation_USD','record_count','award_internal_id','direct_tool_records'].includes(data[key][0][j]) && v!=='' ? Number(v) : v));const sh=wb.worksheets.add(title);sh.showGridLines=false;
 const n=rows.length,m=rows[0].length;sh.getRangeByIndexes(0,0,n,m).values=rows;
 const all=sh.getRangeByIndexes(0,0,n,m);all.format.font={name:'Arial',size:10,color:'#172534'};all.format.rowHeight=23;all.format.verticalAlignment='top';
 const header=sh.getRangeByIndexes(0,0,1,m);header.format.fill='#203E58';header.format.font={bold:true,color:'#FFFFFF'};header.format.rowHeight=32;
 all.format.columnWidth=18;sh.freezePanes.freezeRows(1);
 if(key.endsWith('_matrix')){
  sh.freezePanes.freezeColumns(2);sh.getRange('A:A').format.columnWidth=15;sh.getRange('B:B').format.columnWidth=32;
  sh.getRangeByIndexes(0,2,n,m-2).format.columnWidth=12;
  const grid=sh.getRangeByIndexes(1,2,n-1,m-2);
  for(const [code,fill] of [['U','#F0F1F2'],['C','#E1EDF5'],['O','#FBE7E5'],['X','#FBE7E5'],['S','#FBE7E5'],['NA','#F0F1F2']])grid.conditionalFormats.add('cellIs',{operator:'equal',formula:`"${code}"`,format:{fill}});
 }else{
  sh.tables.add(sh.getRangeByIndexes(0,0,n,m),true,key.replace(/_/g,'')+'Table');
  sh.getRangeByIndexes(0,1,n,Math.min(m-1,2)).format.columnWidth=38;
  if(title==='Inventory'){sh.getRange('A:A').format.columnWidth=14;sh.getRange('B:B').format.columnWidth=58;sh.getRange('C:D').format.columnWidth=24;sh.getRange('E:G').format.columnWidth=60;}
  if(title==='Codebook'){sh.getRange('C:C').format.columnWidth=95;}
  if(title==='Programs'){sh.getRange('B:B').format.columnWidth=80;sh.getRange('E:E').format.columnWidth=90;}
  if(title==='Sources'){sh.getRange('A:A').format.columnWidth=30;sh.getRange('B:B').format.columnWidth=100;}
  if(title==='Evidence gaps'){sh.getRange('B:B').format.columnWidth=14;sh.getRange('C:C').format.columnWidth=30;sh.getRange('D:E').format.columnWidth=95;}
  if(title==='DFC reconciliation'){sh.getRange('C:D').format.columnWidth=28;sh.getRange('E:E').format.columnWidth=75;sh.getRange('H:H').format.columnWidth=95;}
  if(['Claim audit','Corrections','Legacy review','Selected awards','Award actions','Budget evidence','Inventory','Ownership','Changes','Geographic rules','Scope profiles','MCC forecast'].includes(title)){all.format.wrapText=true;all.format.rowHeight=100;all.format.columnWidth=38;header.format.rowHeight=48;}
  if(title==='Sources'){sh.getRange('B:B').format.wrapText=true;sh.getRangeByIndexes(1,0,n-1,m).format.rowHeight=40;}
  if(title==='Evidence gaps'){sh.getRange('C:F').format.wrapText=true;sh.getRangeByIndexes(1,0,n-1,m).format.rowHeight=80;}
 }
}
const numericFields=new Set(['source_row','project_number','approval_year','commitment_USD','country_units_with_observations','source_observations','country_activity_observations','Fiscal Year','Approved/Declined Amount','Disbursed/Shipped Amount','Undisbursed Exposure Amount','Outstanding Exposure Amount','Small Business Authorized Amount','Woman Owned Authorized Amount','Minority Owned Authorized Amount','status','bytes','rows']);
const dateFields=new Set(['evidence_as_of','event_start','event_end','as_of','listed_end_date']);
for(const [title,key] of specs){
 if(!['Priority action review','Primary actions','Legacy ID followups','Cancellation links','Office assignments','Award survival','Event links','Roster checks','Country leads','Award crosswalk','Inventory','Ownership','Legacy review','Evidence gaps','Country activity','Country stages','DFC unallocated','Activity ledger','Activity coverage','EXIM FY2026','DFC portfolio','MCC lifecycle','MDCP targets','Current sources','Activity codes','Agency frame'].includes(title))continue;
 const sh=wb.worksheets.getItem(title),rows=data[key],n=rows.length,m=rows[0].length;
 if(!key.endsWith('_matrix')){
  const all=sh.getRangeByIndexes(0,0,n,m);all.format.wrapText=true;all.format.columnWidth=34;all.format.rowHeight=78;
  sh.getRangeByIndexes(0,0,1,m).format.rowHeight=42;
  for(let j=0;j<m;j++){
   const field=rows[0][j];let values=rows.slice(1).map(r=>r[j]??'');
   if(numericFields.has(field)){values=values.map(v=>v!==''&&Number.isFinite(Number(v))?Number(v):v);sh.getRangeByIndexes(1,j,n-1,1).values=values.map(v=>[v]);sh.getRangeByIndexes(1,j,n-1,1).setNumberFormat(['Fiscal Year','approval_year','project_number','status'].includes(field)?'0':(field.includes('Amount')||field==='commitment_USD'?'#,##0.00':'#,##0'));}
   if(dateFields.has(field)){values=values.map(v=>/^\d{4}-\d{2}-\d{2}$/.test(v)?(Date.parse(v+'T00:00:00Z')-Date.UTC(1899,11,30))/86400000:v);sh.getRangeByIndexes(1,j,n-1,1).values=values.map(v=>[v]);sh.getRangeByIndexes(1,j,n-1,1).setNumberFormat('yyyy-mm-dd');}
   if(['finding','interpretation_limit','description','project','remaining_requirement','evidence_basis','basis','award_budget_finding','finding','evidence_limit','next_check'].includes(field))sh.getRangeByIndexes(0,j,n,1).format.columnWidth=75;
  }
  // Fit populated data cells without shrinking text. Long raw source text remains fully available in the CSV.
  for(let i=1;i<n;i++){
   let lines=1;
   for(let j=0;j<m;j++){const f=rows[0][j],wide=['finding','interpretation_limit','description','project','remaining_requirement','evidence_basis','basis','award_budget_finding','finding','evidence_limit','next_check'].includes(f);lines=Math.max(lines,...String(rows[i][j]??'').split('\n').map(t=>Math.ceil(t.length/(wide?80:36))));}
   sh.getRangeByIndexes(i,0,1,m).format.rowHeight=Math.min(409,Math.max(32,lines*13+12));
  }
 }
}

wb.worksheets.getItem('DFC unallocated').getRange('C:D').format.columnWidth=36;
wb.worksheets.getItem('DFC unallocated').getRange('A1:D1').format.wrapText=true;
function col(i){let s='';while(i){i--;s=String.fromCharCode(65+i%26)+s;i=Math.floor(i/26);}return s;}
const end=col(data.eligibility_matrix[0].length);
summary.getRange('B7').formulas=[[`=COUNTIF(Eligibility!C2:${end}250,"U")`]];
summary.getRange('B8').formulas=[[`=COUNTIF(Eligibility!C2:${end}250,"C")`]];
summary.getRange('B9').formulas=[[`=COUNTIF(Eligibility!C2:${end}250,"O")`]];
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'Read first'!A6:B17",include:'values,formulas',tableMaxRows:12,tableMaxCols:2,maxChars:2200})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},summary:'formula error scan',maxChars:1000})).ndjson);
await fs.mkdir(root+'/validation/workbook_render',{recursive:true});
for(const name of ['Priority action review','Primary actions','Legacy ID followups','Cancellation links','Read first','Office assignments','Award survival','Event links','Roster checks','Country leads','Award crosswalk','Legacy review','Inventory','Ownership','Evidence gaps','Country activity','Country stages','DFC unallocated','Activity ledger','Activity coverage','EXIM FY2026','DFC portfolio','MCC lifecycle','MDCP targets','Current sources','Activity codes','Agency frame']){
 if(process.env.TRADE_RENDER_SHEETS && !process.env.TRADE_RENDER_SHEETS.split(',').includes(name))continue;
 const range=name==='Read first'?'A1:J23':(['Country activity','Country stages'].includes(name)?'A1:I9':name==='DFC unallocated'?'A1:D9':'A1:D6');
 const p=await wb.render({sheetName:name,range,scale:1,format:'png'});
 await fs.writeFile(root+'/validation/workbook_render/'+name.replaceAll(' ','_')+'.png',new Uint8Array(await p.arrayBuffer()));
}
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(root+'/deliverables/US_Trade_Facilitation_Inventory_v0_11.xlsx');
console.log('EXPORTED');
