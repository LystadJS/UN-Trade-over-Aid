"""Rebuild v0.15 analytical figures and CSVs from retained inputs; no network needed.
Run: python scripts/build_evidence_views_v15.py
Dependencies: numpy, scipy, matplotlib. Input source rows retain original evidence dates.
"""
from pathlib import Path
import csv,json,collections,hashlib,zipfile,io,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon,Patch
from scipy.optimize import least_squares
from scipy.spatial.distance import pdist,squareform
from scipy.stats import spearmanr

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=ROOT/'deliverables'; FIG=ROOT/'figures/v15'
FIG.mkdir(parents=True,exist_ok=True);OUT.mkdir(exist_ok=True)
def read(name):
    with (DATA/(name+'.csv')).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    assert rows
    with (DATA/(name+'.csv')).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
inventory=read('program_census'); lookup={r['program_id']:r for r in inventory}
activity=read('country_program_activity_matrix'); stages=read('country_program_stage_matrix'); eligibility=read('eligibility_matrix')
visual=read('program_visual_crosswalk'); legacy=read('legacy_award_survival_v11')
codes=read('activity_codebook'); ledger=read('country_activity_ledger')
ids=[k for k in activity[0] if k not in ['country_code','country']]
observed=[p for p in ids if any(r[p]!='U' for r in activity)]
assert len(inventory)==124 and len(ids)==110 and len(observed)==21
assert sum(r[p]!='U' for r in activity for p in ids)==286

# Reconcile uploaded exports, distinguishing prime actions from subaward reporting.
uploads=[];txs=[];subs=[]
for f in sorted((ROOT/'research_v13/uploaded_records').iterdir()):
    uploads.append(dict(file=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size))
    if f.suffix!='.zip':continue
    with zipfile.ZipFile(f) as z:
        for n in z.namelist():
            if 'TransactionHistory' not in n and 'Sub-Awards' not in n:continue
            rows=list(csv.DictReader(io.StringIO(z.read(n).decode('utf-8-sig'))))
            if 'TransactionHistory' in n:
                for r in rows:txs.append(dict(award_id=n.split('_')[1],action_date=r['action_date'],modification_number=r['modification_number'],action_type=r['action_type'],obligation=r['federal_action_obligation'],description=r['transaction_description'],source_file=f.name,source_member=n))
            else:
                for r in rows:subs.append(dict(award_id=n.split('_')[1],subaward_id=r['subaward_number'],action_date=r['subaward_action_date'],amount=r['subaward_amount'],recipient=r['subawardee_name'],country=r['subaward_primary_place_of_performance_country_name'],description=r['subaward_description'],source_file=f.name,source_member=n,interpretation='Reported subaward action; not proof of prime reinstatement or current delivery'))
assert len(txs)==10 and len(subs)==43
write('uploaded_file_manifest_v15',uploads);write('uploaded_prime_actions_v15',txs);write('uploaded_subaward_actions_v15',subs)

# All 249 x 110 country cells retain multi-stage evidence and separate eligibility.
emap={r['country_code']:r for r in eligibility}; amap={r['country_code']:r for r in activity}
evidence_index={(r['country_code'],r['program_id']):r for r in read('country_program_evidence')}
activity_index=collections.defaultdict(list)
for r in ledger:
    if r['geography_role']!='participant_origin':activity_index[(r['country_code'],r['program_id'])].append(r)
country_rows=[]
for r in stages:
    for pid in ids:
        raw=r[pid];parts=set(raw.split('+'));e=emap[r['country_code']].get(pid,'U')
        if parts & {'A','C','D','I'}: status='Documented financing or delivery'
        elif parts & {'B','G','N','P','S','T'}:status='Approval, pipeline or target only'
        elif parts & {'H','X'}:status='Historical or terminated project'
        elif e in {'C','B'}:status='Conditional geographic route only'
        elif e in {'O','X','R','L'}:status='Geographic restriction or not listed'
        elif e=='NA':status='Domestic location axis'
        else:status='Unresolved / no qualifying observation'
        ev=evidence_index.get((r['country_code'],pid),{});obs=activity_index[(r['country_code'],pid)]
        country_rows.append(dict(country_code=r['country_code'],country=r['country'],program_id=pid,program=lookup[pid]['name'],evidence_status=status,activity_code=amap[r['country_code']][pid],all_stage_codes=raw,eligibility_code=e,program_evidence=lookup[pid]['operational_evidence'],activity_source_ids=';'.join(sorted({o['source_id'] for o in obs})),activity_source_urls=' | '.join(sorted({o['source_url'] for o in obs})),source_evidence_dates=';'.join(sorted({o['evidence_as_of'] for o in obs})),eligibility_source_ids=ev.get('eligibility_source_ids',''),presence_code=ev.get('presence','U'),embassy_code=ev.get('embassy','U'),presence_source_ids=ev.get('presence_source_ids',''),source_lookup='country_activity_ledger.csv; country_program_evidence.csv',review_as_of='2026-10-15'))
write('country_program_status_v15',country_rows)

# Exploratory similarity: documented foreign-country route + harmonized scope.
# Minimum 70% resolved foreign-country entries. Missing values are omitted pairwise.
# Geographic route is not actual activity and C/B are not unconditional eligibility.
harm={'C':'route','B':'route','O':'restricted','X':'restricted','R':'restricted','L':'not_listed'}
scope=lambda s:'broad_goods_services' if s=='broad_export_goods_services' else s
selected=[]; excluded=[]
for v in visual:
    p=v['program_id']; known=sum(r[p] in harm for r in eligibility)
    if known/len(eligibility)>=.70:selected.append(dict(v,known=known,scope_harmonized=scope(v['scope_type'])))
    else:excluded.append(dict(program_id=p,program=v['program'],reason='Below 70% comparable foreign-country route coverage (domestic NA excluded)',known_country_entries=known,total_country_units=len(eligibility)))
assert len(selected)==13
write('similarity_exclusions_v15',excluded)
vectors={v['program_id']:[harm.get(r[v['program_id']]) for r in eligibility] for v in selected}
groups={}
for v in selected:groups.setdefault((tuple(vectors[v['program_id']]),v['scope_harmonized']),[]).append(v)
groupvals=list(groups.values());n=len(groupvals);geo=np.zeros((n,n));sd=np.zeros((n,n));pairrows=[]
for i,a in enumerate(groupvals):
    for j,b in enumerate(groupvals):
        va=vectors[a[0]['program_id']];vb=vectors[b[0]['program_id']];pairs=[(x,y) for x,y in zip(va,vb) if x is not None and y is not None]
        assert len(pairs)>=100
        geo[i,j]=sum(x!=y for x,y in pairs)/len(pairs);sd[i,j]=float(a[0]['scope_harmonized']!=b[0]['scope_harmonized'])
        if i<j:pairrows.append(dict(group_a=';'.join(x['program_id'] for x in a),group_b=';'.join(x['program_id'] for x in b),shared_country_units=len(pairs),geography_distance=geo[i,j],scope_distance=sd[i,j],combined_distance=.5*geo[i,j]+.5*sd[i,j]))
D=.5*geo+.5*sd; tri=np.triu_indices(n,1);target=D[tri]
def fit(dist):
    t=dist[tri]; rng=np.random.default_rng(20261015); best=None
    for _ in range(12):
        initial=rng.normal(0,.4,(n,2))
        result=least_squares(lambda x:pdist(x.reshape(n,2))-t,initial.ravel(),max_nfev=1500)
        if best is None or result.cost<best.cost:best=result
    xy=best.x.reshape(n,2);xy-=xy.mean(axis=0)
    stress=float(np.sqrt(np.sum((pdist(xy)-t)**2)/np.sum(t*t)))
    return xy,stress
xy,stress=fit(D)
coord=[]
for i,g in enumerate(groupvals):
    for v in g:coord.append(dict(program_id=v['program_id'],program=v['program'],group=i+1,x=xy[i,0],y=xy[i,1],known_country_entries=v['known'],scope=v['scope_harmonized'],operational_evidence=lookup[v['program_id']]['operational_evidence']))
write('similarity_coordinates_v15',coord);write('similarity_pair_distances_v15',pairrows)
sensitivity=[]
for w in [.25,.5,.75]:
    dw=w*geo+(1-w)*sd; _,ss=fit(dw)
    sensitivity.append(dict(geography_weight=w,scope_weight=1-w,stress_2d=ss,distance_rank_correlation_to_equal_weights=float(spearmanr(dw[tri],D[tri]).statistic)))
write('similarity_sensitivity_v15',sensitivity)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','savefig.facecolor':'#fbfcfe','figure.facecolor':'#fbfcfe','axes.facecolor':'#fbfcfe','text.color':'#192c42','axes.labelcolor':'#192c42'})
colors={'D':'#158477','I':'#617db2','C':'#316bb0','A':'#73a6c7','B':'#d99531','G':'#d99531','N':'#d99531','P':'#d99531','S':'#d99531','T':'#d99531','H':'#a2a6ad','X':'#ad5961','U':'#edf0f4'}
def title(fig,t,sub):
    fig.text(.055,.955,t,fontsize=20,weight='bold');fig.text(.055,.915,sub,fontsize=10,color='#526276')
def footer(fig,text='Sources: retained agency records, dated through 15 October 2026. Unknown is not zero activity.'):
    fig.text(.055,.035,text,fontsize=8,color='#526276')
def save(fig,name,pdf):
    fig.savefig(FIG/(name+'.png'),dpi=170);fig.savefig(FIG/(name+'.svg'));pdf.savefig(fig);plt.close(fig)

with PdfPages(OUT/'Trade_Program_Evidence_Atlas_v0_15.pdf') as pdf:
    # Geographic observation coverage; geometry does not assert sovereignty.
    fig,ax=plt.subplots(figsize=(12,8));fig.subplots_adjust(left=.04,right=.96,bottom=.19,top=.84)
    counts={r['country_code']:sum(r[p]!='U' for p in ids) for r in activity}; bins=[0,1,3,6,100];pal=['#e5e9ee','#b4d5e3','#71b3ce','#377eaa','#164b74']
    geometry=json.loads((ROOT/'research_v13/world_110m.geojson').read_text());mapped=set()
    for f in geometry['features']:
        prop=f['properties'];cc=prop.get('ISO_A2_EH',prop.get('ISO_A2'));cc='XK' if prop.get('ADMIN')=='Kosovo' else cc
        if prop.get('ADMIN')=='Antarctica':continue
        k=counts.get(cc,0);c=pal[0 if k==0 else 1 if k<=2 else 2 if k<=5 else 3 if k<=8 else 4]
        if cc=='US':c='white'
        geom=f['geometry'];polys=[geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates']
        for poly in polys:ax.add_patch(Polygon(poly[0],facecolor=c,edgecolor='white',linewidth=.35))
        if cc in counts:mapped.add(cc)
    ax.set_xlim(-180,180);ax.set_ylim(-58,85);ax.set_aspect('equal');ax.axis('off')
    title(fig,'Where country-level evidence is recorded','286 country–program pairs across 124 country/territory units and 21 inventory records')
    ax.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(pal,['No qualifying observation','1–2 records','3–5 records','6–8 records','9+ records'])],loc='lower center',bbox_to_anchor=(.5,-.13),ncol=5,frameon=False,fontsize=9)
    fig.text(.055,.105,'Counts combine authorizations, commitments, reported delivery and MCC implementation. They do not measure deals, spending or impact.',fontsize=9)
    footer(fig,'US excluded (white). Not an official participant map. Small territories omitted at this scale; all 249 units remain in data. Natural Earth geometry.')
    save(fig,'01_country_evidence_map',pdf)
    # Full country atlas, including all 249 units and all 18 observed programs.
    # All other 92 program columns are U in the activity matrix and retained in CSV.
    for page,start in enumerate(range(0,len(activity),42),1):
        rows=activity[start:start+42];fig,ax=plt.subplots(figsize=(12,10));fig.subplots_adjust(left=.24,right=.97,top=.81,bottom=.15)
        for i,r in enumerate(rows):
            for j,p in enumerate(observed):
                code=r[p];ax.add_patch(plt.Rectangle((j-.5,i-.5),1,1,facecolor=colors[code],edgecolor='white',linewidth=.5))
                if code!='U':ax.text(j,i,code,ha='center',va='center',fontsize=8,color='white' if code in ['D','I','C'] else '#192c42')
        ax.set_xlim(-.5,len(observed)-.5);ax.set_ylim(len(rows)-.5,-.5)
        ax.set_xticks(range(len(observed)),observed,rotation=45,ha='left',fontsize=8);ax.xaxis.tick_top()
        ax.set_yticks(range(len(rows)),['South Georgia & S. Sandwich Is.' if r['country_code']=='GS' else r['country'] for r in rows],fontsize=8)
        ax.tick_params(length=0);[s.set_visible(False) for s in ax.spines.values()]
        title(fig,f'Country evidence matrix  {page}/6','All country/territory units • 21 columns with observations; 89 additional columns remain unresolved in the full CSV')
        fig.text(.055,.105,'D  reported delivery      I  MCC implementation roster      C  commitment / signed financing      A  EXIM authorization',fontsize=9)
        fig.text(.055,.075,'Light cells: no qualifying observation. Source dates vary; observed financing is not proof of ongoing service delivery.',fontsize=9)
        footer(fig,'Program names and sources are in the key and country_program_status_v15.csv. Full stage history is retained separately.')
        save(fig,f'02_country_matrix_{page}',pdf)
    # Program-level evidence status, not active program totals.
    count=collections.Counter(r['operational_evidence'] for r in inventory)
    labels={'recent_delivery_reported':'Recent delivery reported','current_portfolio_or_authorizations':'Portfolio / authorization evidence','funding_intake_or_approval_action':'Funding, intake or approval action','current_official_offer_only':'Official offer only','current_operation_unresolved':'Current operation unresolved','boundary_or_alias':'Exclusion or alias'}
    fig,ax=plt.subplots(figsize=(12,8));fig.subplots_adjust(left=.34,right=.93,top=.81,bottom=.17)
    keys=list(labels);vals=[count[k] for k in keys];ax.barh(range(6),vals,color=['#158477','#316bb0','#d99531','#8aacc0','#b76b42','#a2a6ad']);ax.invert_yaxis();ax.set_yticks(range(6),[labels[k] for k in keys]);ax.set_xlabel('Inventory records');ax.set_xlim(0,70)
    for i,v in enumerate(vals):ax.text(v+1,i,str(v),va='center',weight='bold')
    title(fig,'What the program-level evidence establishes','124 screened records; evidence categories are not a count of independently verified active programs')
    footer(fig,'Source: program_census.csv operational_evidence. An official offer, financing action and reported delivery are distinct claims.')
    save(fig,'03_inventory_evidence',pdf)
    # Qualified 2-D similarity, duplicates grouped to avoid false point separation.
    fig,ax=plt.subplots(figsize=(12,8));fig.subplots_adjust(left=.07,right=.67,top=.82,bottom=.20)
    for i,g in enumerate(groupvals):
        col='#316bb0' if g[0]['program_id'].startswith('EXIM') else '#158477' if g[0]['program_id'].startswith('DFC') else '#bb853c'
        ax.scatter(*xy[i],s=170,facecolor=col,edgecolor='white',linewidth=1.5,zorder=3);ax.annotate(str(i+1),xy[i],color='white',ha='center',va='center',weight='bold',fontsize=9)
    ax.axhline(0,color='#dfe5eb',lw=.7);ax.axvline(0,color='#dfe5eb',lw=.7);ax.set_xlabel('Similarity dimension 1 (arbitrary orientation)');ax.set_ylabel('Similarity dimension 2');ax.margins(.17);ax.set_aspect('equal',adjustable='datalim')
    title(fig,'Exploratory similarity: geographic routes and scope',f'13 of 62 direct instruments; {n} distinct profiles • equal geography/scope weights • normalized stress {stress:.3f}')
    for i,g in enumerate(groupvals):
        name=', '.join(x['program_id'] for x in g); desc=g[0]['scope_harmonized'].replace('_',' ')
        wrapped='\n    '.join(textwrap.wrap(name,34))
        fig.text(.70,.81-i*.085,f'{i+1}  {wrapped}\n    {desc}',fontsize=8.5,va='top')
    fig.text(.055,.12,'Distances describe documented eligibility routes and broad scope, not actual operations, budgets, performance or substitution.',fontsize=9)
    fig.text(.055,.085,'Approximate projection (stress 0.215): use the distance matrix for exact comparisons. 49 excluded tools remain in the scope chart.',fontsize=9)
    footer(fig,'Model: 70% country-coverage threshold; categorical mismatch distance; deterministic multi-start 2-D fit. Full pair distances and weight sensitivity in data/.')
    save(fig,'04_qualified_similarity',pdf)
    fig,ax=plt.subplots(figsize=(12,8));fig.subplots_adjust(left=.25,right=.85,top=.82,bottom=.18)
    im=ax.imshow(D,cmap='Blues',vmin=0,vmax=1)
    names=[f"{i+1}: "+('/'.join(v['program_id'] for v in g) if len(g)<3 else 'DFC01–DFC06') for i,g in enumerate(groupvals)]
    ax.set_yticks(range(n),names);ax.set_xticks(range(n),[str(i+1) for i in range(n)])
    for i in range(n):
        for j in range(n):ax.text(j,i,f'{D[i,j]:.2f}',ha='center',va='center',color='white' if D[i,j]>.65 else '#192c42')
    fig.colorbar(im,ax=ax,label='Dissimilarity (0 = identical coded profile; 1 = maximally different)')
    title(fig,'Exact dissimilarities behind the projection','Equal-weight geographic-route and scope mismatch; omitted countries are not coded as zero')
    footer(fig,'These profiles are coarse: identical DFC geography/scope does not mean identical financial products, activity or sector portfolios.')
    save(fig,'04b_exact_distances',pdf)
    # All 62 tools: non-metric 2-D layout preserves incompletely normalized profiles.
    geos=sorted(set(v['display_geography'] for v in visual));scopes=sorted(set(v['display_scope'].replace('\n',' ') for v in visual))
    fig,ax=plt.subplots(figsize=(15,10));fig.subplots_adjust(left=.23,right=.98,top=.78,bottom=.12)
    buckets=collections.defaultdict(list)
    for v in visual:buckets[(geos.index(v['display_geography']),scopes.index(v['display_scope'].replace('\n',' ')))].append(v['program_id'])
    for (j,i),ps in buckets.items():
        ax.add_patch(plt.Rectangle((j-.48,i-.46),.96,.92,facecolor='#e4edf4',edgecolor='white'))
        text='\n'.join(', '.join(ps[k:k+2]) for k in range(0,len(ps),2));ax.text(j,i,text,ha='center',va='center',fontsize=8)
    ax.set_xlim(-.5,len(geos)-.5);ax.set_ylim(len(scopes)-.5,-.5);ax.set_yticks(range(len(scopes)),scopes,fontsize=9);ax.set_xticks(range(len(geos)),['\n'.join(textwrap.wrap(g,19)) for g in geos],fontsize=9);ax.xaxis.tick_top();ax.tick_params(length=0);[s.set_visible(False) for s in ax.spines.values()]
    title(fig,'Geographic rule and scope: all 62 direct instruments','Categorical comparison retains tools excluded from the numerical projection; position is not a measured distance')
    footer(fig,'Source: program_visual_crosswalk.csv. Broad scope does not imply universal sector eligibility; full names and sources accompany each program ID.')
    save(fig,'05_full_scope_geography',pdf)
    # Legacy awards explicitly visible and not certified active.
    fig,ax=plt.subplots(figsize=(14,11));ax.axis('off');title(fig,'Legacy awards and agreement leads remain visible','25 selected awards plus 2 IAA leads • current continuation unresolved; this is not proof that none survive')
    cell=[]
    for r in legacy:
        disp=r['survival_disposition'].replace('_',' ')
        cell.append([r['award_id'],r['recipient'][:33], '\n'.join(textwrap.wrap(disp,42)), 'Unresolved'])
    cell.extend([['72067424T00001','Commerce CLDP','Mirrored roster lead; signed agreement missing','Unresolved'],['72067420T00001','DFC','Mirrored PAPA lead; signed agreement missing','Unresolved']])
    t=ax.table(cellText=cell,colLabels=['Award ID','Recipient / counterparty','Strongest retained disposition','Current continuation'],colWidths=[.20,.27,.40,.13],cellLoc='left',bbox=[.025,.06,.95,.79]);t.auto_set_font_size(False);t.set_fontsize(8)
    for (i,j),c in t.get_celld().items():c.set_edgecolor('white');c.set_facecolor('#192c42' if i==0 else '#f2e6da' if i%2 else '#f7f1eb');c.get_text().set_color('white' if i==0 else '#192c42')
    footer(fig,'Historical termination, scheduled end date and current survival are separate. Exact IDs and provenance: legacy_award_survival_v11.csv.')
    save(fig,'06_legacy_awards',pdf)
    network={}
    for r in read('country_program_evidence'):
        key=(r['country_code'],r['network']);val=(r['presence'],r['embassy'])
        assert key not in network or network[key]==val
        network[key]=val
    netrows=[]
    for net in ['CS','FAS','DFC','USTDA','EXIM','SBA','DOD']:
        vs=[v for (cc,nn),v in network.items() if nn==net]
        netrows.append(dict(network=net,in_country_address=sum(p=='P' for p,e in vs),explicit_embassy_affiliation=sum(e=='E' for p,e in vs),partner_channel=sum(p=='T' for p,e in vs),cross_border_service=sum(p=='R' for p,e in vs),unresolved=sum(p=='U' for p,e in vs)))
    write('network_evidence_summary_v15',netrows)
    fig,ax=plt.subplots(figsize=(12,8));fig.subplots_adjust(left=.15,right=.93,top=.82,bottom=.2)
    yy=np.arange(len(netrows));ax.barh(yy-.16,[r['in_country_address'] for r in netrows],height=.30,label='Published in-country network address',color='#316bb0');ax.barh(yy+.16,[r['explicit_embassy_affiliation'] for r in netrows],height=.30,label='Explicit embassy / mission affiliation',color='#158477');ax.set_yticks(yy,[r['network'] for r in netrows]);ax.invert_yaxis();ax.set_xlabel('Country/territory units in retained directory evidence');ax.legend(frameon=False,loc='lower right')
    title(fig,'Overseas networks and embassy affiliation','Agency-network evidence is separate from program availability, current staffing and delivery')
    fig.text(.055,.115,'CS = Commercial Service; FAS = Foreign Agricultural Service. Categories overlap and must not be added.',fontsize=9)
    fig.text(.055,.08,'Zero means no qualifying directory evidence in this collection, not no overseas presence. DFC and USTDA leads retain weaker codes.',fontsize=9)
    footer(fig,'Source: country_program_evidence.csv, deduplicated by country/network; directory snapshots are not an agency-certified current staffing roster.')
    save(fig,'06b_network_presence',pdf)
    # Human-readable program key + source guide (all full names in inventory).
    fig,ax=plt.subplots(figsize=(12,10));ax.axis('off');title(fig,'Country matrix key and evidence guide','IDs identify inventory records, which may include overlapping instruments or initiatives')
    y=.85
    for pid in observed:
        fig.text(.06,y,pid,fontsize=10,weight='bold');fig.text(.17,y,lookup[pid]['name'][:90],fontsize=10);y-=.0245
    for line in ['A: EXIM FY2026 Q3 authorization data; credit-risk geography.', 'C: DFC June 30, 2026 active portfolio and cited financing announcements; project geography.', 'D: dated agency/implementer/recipient reports; delivery venue or specifically supported destination.', 'I: MCC Where We Work implementation label; not independently verified construction.', 'Country evidence rows retain source URL, record ID, date, geographic role and inclusion decision.', 'The full status CSV also shows conditional eligibility, historical/terminated projects, pipeline and unresolved cells.', 'No source establishes a universal official “Trade over Aid participant” country roster.', 'Legacy awards and unresolved current ownership are tracked independently of country activity.', 'Numerical similarity compares geographic rules and scope only. Identical profiles are grouped, not jittered.']:
        fig.text(.06,y,line,fontsize=9);y-=.032
    footer(fig,'Primary data: data/country_activity_ledger.csv; source_registry_v11.csv; post_notice_review_v12/research/evidence; research_v13/uploaded_records.')
    save(fig,'07_evidence_key',pdf)

summary=dict(inventory_records=len(inventory),country_units=len(activity),matrix_programs=len(ids),observed_country_program_pairs=286,observed_programs=len(observed),country_units_with_observations=sum(any(r[p]!='U' for p in ids) for r in activity),similarity_programs=len(selected),similarity_profiles=n,similarity_excluded=len(excluded),similarity_stress=stress,minimum_pairwise_shared_countries=min(r['shared_country_units'] for r in pairrows),legacy_awards=len(legacy),uploaded_prime_transactions=len(txs),uploaded_subaward_rows=len(subs),evidence_categories=dict(count),country_status_counts=dict(collections.Counter(r['evidence_status'] for r in country_rows)))
(DATA/'visualization_summary_v15.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
