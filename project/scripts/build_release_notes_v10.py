from pathlib import Path
import json
P=Path(__file__).resolve().parents[1];O=P/'deliverables'
S=json.loads((P/'data/census_summary.json').read_text())
status='''US trade facilitation research status and rigor v0.10
Evidence snapshot: 15 October 2026
Disposition: Useful with stated caveats. Priority evidence review completed; substantive resolution remains partial. Visualization remains on hold.

What changed
Eight unresolved program-to-office assignments received a focused review. Across the full 15-program legacy subset, ownership assessments now comprise four verified agency/published-contact assignments, four qualified component or role assignments, and seven unresolved program assignments. These are not certifications of filled staff posts. DCCP moves from candidate to overlay because one explicitly program-linked 2026 event is now documented. The 124-record register comprises 62 direct tools, 20 supporting services, 17 overlays, 11 unresolved candidates, three adjacent routes, ten exclusions and one alias.

Office findings
Commerce identifies State's Bureau of Cyberspace and Digital Policy (CDP) as convenor of the June 2026 Skopje accelerator; CRDF explicitly identifies DCCP funding. Indexed 1 FAM 495 identifies CDP/SPC management of bureau assistance including DCCP, with a 2024 functional provision and an office-code listing in the 2026 manual index. The full FAM page could not be retrieved. Bureau responsibility for the observed event is supported; the program-wide suboffice assignment remains qualified.
Indexed AF/ERA liaison responsibilities for Prosper Africa and Power Africa predate an AF/CE code effective September 2025. The records do not establish that AF/CE inherited either program. The existing August 2026 EEB/CBA vacancy verifies commercial-affairs functions but does not name ownership of Deal Teams, Direct Line, BIDS or BFIF. TAF remains without a verified current program-specific office assignment.

Legacy award audit
Twenty-three selected legacy award details were refreshed: five Prosper Africa, eleven Power Africa and seven DCCP records. Two Power Africa awards omitted from the prior nine-record selection were added: EECA 72067423C00003 (RTI) and ESA 72067424C00001 (Chemonics). EECA attribution uses RTI's 2023 primary announcement plus matching award title and recipient. ESA uses indexed USAID COP28 text plus the matching award title; the original URL returned an administrative-leave landing page, so this crosswalk remains qualified. These are selected records, not an exhaustive agency roster.
Survival dispositions: six have previously recorded termination-related actions; one has recipient-reported termination; five have congressional-reported termination; eight have elapsed scheduled periods; three have future end dates without verified survival. Zero have affirmative current survival confirmation in this review. Zero confirmed does not mean that no awards survive.
Abt's March 18, 2025 Nebraska procurement disclosure reports HETA award 72067422CA00003 terminated for government convenience on February 26, 2025. PDF page 15, printed page 7, was visually checked. USAspending still returns a 2027 end date and a January 2025 last-modified date. The recipient disclosure defeats any inference of survival from that future date. It is not an executed federal notice or proof that no rescission followed.
The July 2025 Senate Foreign Relations Committee minority report names ten award IDs in its Power Africa termination discussion (footnote 365). Six match the prior selection, including HETA. Five other matches are coded congressional-reported, because the report relies on reported underlying award lists; it is not a contracting officer's action record. Four additional IDs remain explicit follow-up leads. The audit does not adopt the report's causal claims or aggregate loss estimates.
The old award_evidence table is preserved as the historical transaction audit; its False termination flags mean no qualifying text/action was returned in that audit, not survival. The new legacy_award_survival_v10 table supplies the current adjudication. Administrative reporting offices are not treated as current program managers. Detail refreshes do not constitute a new exhaustive transaction pull.

Country-delivery findings
One new DCCP/North Macedonia observation is admitted: the June 10–11, 2026 Skopje accelerator. CRDF's participant account names DCCP funding; Commerce independently supplies dates, venue and State/CDP's role. The CLDP and DCCP observations share one event identifier, preventing their interpretation as two independent deals. No other Western Balkan country, embassy office or award identifier is inferred.
The ledger now has 2,170 observations. The 249-by-110 country/program matrix contains 276 observed pairs across 18 program records and 121 country/territory units. These figures measure evidence coverage, not intensity or a full global footprint. Only MK/STATE09 changed in each activity/stage matrix. The six baseline eligibility, presence and sector matrices are unchanged.
Pakistan Direct Line remains quarantined: the official embassy social-post URL was recovered, but embed metadata exposes only author/date and a shortened link, without the event content. Costa Rica DCCP remains quarantined: FCC index evidence was not upgraded because full text retrieval remains blocked. NIST language translations and webpage update dates were not converted into country-delivery observations.

What the paper informs
The major instrument types, agency structure, sector interests, differentiated evidence of operation, published intake status, documented country observations and identified legacy uncertainties. The paper and companion data make positive observations and their limitations inspectable.

What it does not inform
A complete current federal-program census, every embassy's staffing or program office, exhaustive country delivery, all surviving legacy awards, currently spendable balances, realized exports, comparative effectiveness, or whether trade substitutes for aid. Current intake acceptance is not established by a published application link. An event report establishes reported delivery, not impact.

Rigor assessment
The work is useful as a bounded informative evidence map. Its positive additions rest on identified primary agency, participant or recipient records. Secondary termination evidence is explicitly separated from primary administrative action. Indexed-only sources, failed retrievals, stale date fields and qualified crosswalks remain visible. Unknown cells are never zero activity. Automated checks reconcile the matrix to its ledger, ownership fields across tables, source paths/hashes, and all included workbook cells to CSVs. The same assistant selected sources and adjudicated claims; these are consistency checks, not independent peer review or agency certification.
Calling this an exhaustive active-program census, a roster of confirmed surviving awards, or an effectiveness ranking would exceed the evidence. The release does not make those claims. The demonstrated HETA date conflict and DCCP shared-event link reduce concrete risks of false survival and double counting.

What to explore next
1. Obtain current program-specific operating and award-management rosters for the seven unresolved assignments; treat AF liaison/code changes as leads, not transfers.
2. Resolve the three future-date-only Power Africa awards and four unmatched congressional award IDs with executed continuation, termination or rescission records. Link the verified DCCP event to its funding award.
3. Recover full Pakistan and Costa Rica primary event records; then broaden non-finance agency delivery coverage using consistent geography roles and periods.
4. Reassess similarity visualization only after defining comparable geography and scope measures, documenting missing-data treatment and preventing umbrella/product/event double counting.

No outreach was undertaken. No new visualization was produced. Previous releases remain superseded provenance.
'''
(O/'Research_Status_and_Rigor_v0_10.txt').write_text(status)
old=(P/'history/v0_9/deliverables/Methods_and_Census_Boundary_v0_9.txt').read_text()
old=old.replace('V0.9 roster validation (15 October 2026)','Historical v0.9 roster validation (superseded where updated below)')
old=old.replace('Current files are program_census','The v0.9 current files were program_census')
methods=old+'''

V0.10 priority validation
Current controlling tables: program_census, legacy_reconciliation, roster_verification_v10, program_office_assignments_v10, legacy_award_survival_v10, country_activity_ledger, country_evidence_leads_v10, event_program_links_v10 and source_registry_v10. The qualified ATI/PATI crosswalk remains program_award_crosswalk_v09. Other versioned audit tables are historical unless expressly retained. History/v0_9 contains the complete pre-update data and deliverables used by update_v10.py.
One new DCCP delivery observation is admitted only after an explicit program name in a participant's primary report and official corroboration of the event date and bureau. A common event ID connects CLDP and DCCP; program-country evidence counts may overlap. Event location is not an office footprint, participant origin or regional eligibility rule.
The legacy survival audit covers 23 selected award IDs, not a complete operating roster. The same 21 earlier selected legacy records were refreshed, plus two discovered Power Africa awards. Other rows in the historical 23-row award_evidence table concern ITSI and an unconfirmed TAF match, so the two tables have different membership despite equal row counts. New detail responses do not replace the earlier transaction audit. Termination fields, recipient statements, legislative reporting, scheduled expiry and current continuation evidence remain separate. Future dates do not verify survival; no new continuation was verified. Three Power Africa future-date-only records and four congressional award-ID leads remain unresolved.
The HETA recipient disclosure is a primary first-party statement, not an executed government modification. The Senate report is an official publication but secondary evidence of the underlying termination actions. These evidentiary distinctions are preserved in survival_disposition and evidence_basis. No program-wide closure is inferred from a component's termination.
Full foreign-assistance operating-manual pages were inaccessible; indexed functional assignments are marked qualified. A current office code plus an older liaison function does not prove transfer of a program. A 200 HTTP response can be an unrelated landing page: the USAID COP28 URL returned an administrative notice, so the indexed project link is not labeled a full primary retrieval.
Third-party participant/recipient sources are retained as short attributed evidence notes with original retrieval hashes, URLs and exact page locators where relevant. Federal source snapshots are retained when available. Receipt status records transport success or failure, not claim verification. New retrieval attempts total 46, not 46 validated findings; baseline retrieval counts in census_summary remain labeled by release.
Current ownership dispositions among the 15 legacy records: four agency/contact verifications, four qualified roles and seven unresolved assignments. The new priority office table presents the eight formerly unresolved records; only DCCP moved to a qualified component role. All six baseline eligibility/presence/sector tables remain unchanged. No statistical projection was added.

Reproduction
Use the retained snapshots to reproduce this evidence cutoff; live refetches may change results. Run scripts/update_v10.py, scripts/build_paper.py, scripts/build_workbook.mjs, the packaged DOCX renderer with --emit_pdf, scripts/verify_census.py, scripts/verify_rosters_v10.py and scripts/verify_artifacts_v10.py. Copy the rendered PDF into deliverables before artifact verification. The Node workbook requires @oai/artifact-tool; Python packages are listed in scripts/dependencies.txt. build_release_notes_v10.py generates these explanatory notes. package_release.py regenerates the hash manifest and ZIP after all verification. verify_release.py checks packaged hashes. Source requests and failed attempts are retained under research_v10; indexed notes are analyst adjudications, not reconstructed original pages.
'''
(O/'Methods_and_Census_Boundary_v0_10.txt').write_text(methods)
(P/'START_HERE.txt').write_text('''US trade facilitation research package v0.10 — 15 October 2026
Start with deliverables/US_Trade_Facilitation_Informative_Paper_v0_10.pdf (3 pages).
Read Research_Status_and_Rigor_v0_10.txt for findings, qualifications and next work.
The workbook has 35 tabs, including new office assignments, selected award survival and shared event links.
Current master: data/program_census.csv. Current sources: data/source_registry_v10.csv.
Current legacy survival audit: data/legacy_award_survival_v10.csv; it is not an exhaustive agency roster.
One DCCP/North Macedonia activity pair added. Eligibility and office/network matrices retain the earlier 62-tool scope.
No new visualization. Historical figures and releases are superseded provenance and should not be treated as current projections.
History/v0_9 preserves the pre-update data, scripts and deliverables. Versioned v09 tables are historical except the qualified ATI/PATI crosswalk.
Use current verifier entrypoints; historical scripts are retained for provenance.
''')
print('Wrote status, methods and package guide')
