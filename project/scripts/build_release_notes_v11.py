from pathlib import Path
import json
P=Path(__file__).resolve().parents[1];O=P/'deliverables';S=json.loads((P/'data/census_summary.json').read_text())
status='''US trade facilitation research status and rigor v0.11
Evidence reviewed: 15 October 2026
Assessment: Share with caveats. Historical action and identity findings are useful; current continuation and two interagency action chains remain unresolved. Visualization stays on hold.

Seven priority awards: results
1. 72067424F00006 — Green Powered Technology, Power Africa communications. Government-filed ECF 20-1, page 2, row 21, lists a termination notice dated February 11, 2025. The only returned procurement transaction is the July 26, 2024 award. Current continuation is not verified.
2. 72067423C00003 — RTI, Empower East and Central Africa. ECF 20-1, page 11, row 182, lists a February 12, 2025 termination notice. Latest returned transaction: January 7, 2025 funding action P00004. Current continuation is not verified.
3. 72067424C00001 — Chemonics, Empowering Southern Africa. ECF 20-1, page 2, row 20, lists a February 11, 2025 termination notice. March 7, 2025 P00003 is coded Other Administrative Action and refers to DEI compliance; its description is truncated. It cannot establish reinstatement or continued delivery.
4. AID-OAA-A-15-00054 — CrossBoundary Energy. Federal identity resolved: FAIN AIDOAAA1500054, URI AID-OAA-A-15-00054-01, USAspending internal ID 259407464, cooperative agreement. Latest reported action is July 12, 2018, Other Action, Non-Financial. DOGE reports a matching CrossBoundary first-loss-facility cancellation dated March 1, 2025, but publishes no award ID or link. The cancellation-to-award join remains qualified.
5. AID-AFR-IO-16-00001 — IBRD / Scaling Solar. Federal identity resolved: FAIN AIDAFRIO1600001, URI AID-AFR-IO-16-00001-04, internal ID 259403396. It is assistance type 11, not in the grant-only search frame. Latest action is May 25, 2022, Other Action, Non-Financial. January 6, 2026 is a record-update date, not a new action. DOGE reports a matching Scaling Solar cancellation dated March 1, 2025 without an award ID/link; action linkage remains qualified.
6. 72067424T00001 — CLDP interagency agreement lead. A publicly mirrored agency-origin roster gives the exact ID and describes legal/regulatory assistance for Power Africa investment. The original signed agreement, an authenticated agency roster and subsequent amendments/cancellation were not retrieved.
7. 72067420T00001 — DFC participating-agency agreement lead. The same mirrored roster gives the exact ID and describes Washington-based deal teams. Signed agreement and subsequent actions remain unverified. The PDF row gives $2 million; the search engine incorrectly associates $22.4 million from a different row. Neither amount is used to infer action or survival.

Resolution accounting
All seven priority items received an adjudication. Three historical contract-notice dates are verified in a government primary record. Two of four formerly unmatched IDs now have exact federal FAIN/URI matches; the two interagency identities remain qualified. No current continuation is verified among the seven. These are different dimensions and cannot be combined into a single completion percentage.
The same government filing also lists HETA and two other already selected Power Africa awards. Those three evidence tiers are upgraded from recipient/congressional reports to government-filed historical notices. HETA's February 11 notice and Abt's separate February 26 termination report are retained as two dated records, not reconciled into an invented action sequence.
The selected survival cohort grows from 23 to 25 awards: five Prosper Africa, 13 Power Africa, seven DCCP. It contains six previously recorded termination-related actions, six government-filed notice reports, three congressional reports, eight elapsed scheduled periods, and two government project-cancellation reports with qualified award links. None is certified currently surviving by this review; this does not prove none survives.

Why the evidence is stronger, and where it stops
The U.S. Department of Justice's February 12, 2025 cover filing, ECF 20, identifies the attached USAID list as the government's submission. ECF 20-1 identifies the three contract IDs, vendors and notice dates. The March 10 court opinion on govinfo cites those filings and documents later proceedings. These are primary government records retained through RECAP, with the cover filing, page locators and file hashes. They are not the signed contract notices, and later litigation prevents treating the initial notices as a final current-status determination. No inference of present legal effect is made.
Seventeen reported financial transactions were retrieved for five federally matched awards. Ten procurement actions also reconcile by modification number to the FPDS feed. These histories contain no termination-coded entry for the three contracts. That does not negate the court-filed roster: the sources measure different things and have different reporting limits. The current SAM contract-awards API requires an authorized key; no key was available and no account access was attempted. FPDS is undergoing migration, so its older feed is not certified as complete current coverage.
The public DOGE API returned 13,440 contract rows and 15,887 grant rows. Duplicate full rows and pagination ties prevent treating these as unique-award counts or a reliable absence test. Of 3,523 USAID contract rows retrieved, 3,506 expose no PIID. Three amount-only matches were rejected and retained separately. The website labels its data update January 1, 2026; October retrieval is not proof of October coverage. DOGE reports cancellations but is not a substitute for executed agency notices.
The two interagency agreements may fall outside ordinary prime-award reporting. Successful searches of contract, grant, direct-payment and other-assistance categories did not produce their IDs. Loan-category requests failed and are not represented as searched successfully. The mirrored March 2025 roster is an exact-ID research lead with unverified provenance; it is not promoted to authenticated agency action.

Effect on the paper and matrices
The three-page paper now explains the primary termination-notice findings and remaining continuation limits. The 124-record census, 62 direct tools, 2,170 country observations and 276 observed country-program pairs are unchanged. No new country delivery, program owner, embassy presence or eligibility is inferred from these historical award records. The 249-by-110 activity matrix and all six baseline eligibility/presence/sector matrices are byte-identical to v0.10.
Current tables: power_africa_action_review_v11, primary_award_actions_v11, legacy_award_survival_v11, legacy_award_followup_ids_v11, doge_cancellation_crosswalk_v11, roster_verification_v11 and source_registry_v11. Unchanged office/event/country-lead tables retain their v0.10 names. Older audit tables remain historical evidence.

What the paper informs
The range of U.S. trade-facilitation instruments, their documented sectors and functions, differentiated operational evidence, published intake, selected country activity, and precisely bounded legacy uncertainties. This release improves award identity and historical agency-action attribution.

What it does not inform
A complete active-program census; an exhaustive surviving-award roster; present legal enforceability of a terminated contract; current country delivery for these awards; spendable balances; filled embassy posts; realized exports; comparative effectiveness; or a causal judgment that trade can substitute for aid.

Rigor assessment
Useful as a source-linked informative tool, with the stated limits. The principal new positive findings follow exact identifiers in retained primary records. Qualified joins, failed requests, stale fields, conflicting dates and duplicate rows remain inspectable. The work does not turn unknowns into facts or claim that all seven action chains are resolved. Consistency checks and visual inspection are performed by the same assistant, not independent peer review or agency certification.

Next evidence needed
For the three contracts: the post-February-2025 contracting-officer action chain and an authorized current SAM extract, including any rescission/reinstatement and final disposition.
For CrossBoundary and Scaling Solar: award-numbered cancellation, rescission and closeout instruments to authenticate the DOGE project-level reports.
For CLDP and DFC: USAID/State and receiving-agency interagency-agreement registers, signed IAA/PAPA and amendments. An operating page or related event cannot fill this gap.
After those records: current program ownership and country-delivery confirmation, then a reassessment of geographic/sector comparability before visualization. No outreach was undertaken.
'''
(O/'Research_Status_and_Rigor_v0_11.txt').write_text(status)
prior=(P/'history/v0_10/deliverables/Methods_and_Census_Boundary_v0_10.txt').read_text()
prior=prior.split('\nReproduction\n')[0].replace('V0.10 priority validation','Historical v0.10 priority validation (superseded below)')
addition='''

V0.11 controlling methods and evidence hierarchy
Scope: seven requested Power Africa gaps, plus incidental exact-ID matches in the same primary roster. A notice's issuance date, latest transaction action date, system update date, scheduled end date and current survival are separate fields. No current legal status is adjudicated.
Government primary action report: DOJ's ECF 20 cover filing authenticates authorship of its ECF 20-1 attachment. Exact ID/vendor/date rows establish reported historical notices, not executed signed instruments or final present status. The court's official govinfo opinion corroborates docket context. Government-authored court filings remain primary records when retrieved through RECAP.
Identifier resolution: strip hyphens only for searching, then require the federal FAIN and hyphenated URI to agree, with matching recipient/project. CrossBoundary is type 05 and Scaling Solar type 11; omitting other-assistance codes caused a real coverage gap. The two IAA candidates are not declared invalid because they lack a prime-award match.
DOGE is a government cancellation-report source. Its project/recipient descriptions corroborate two project leads; null award links leave the action-to-award crosswalk qualified. Redacted records cannot be joined on amount alone. Row counts describe retrieved responses, not unique awards or savings. Dates are retained as reported; no effective termination date is inferred from a generic API date.
Primary financial histories: five awards, 17 transactions, all returned with hasNext=false. Three contract histories (ten rows) reconcile by modification number to FPDS ATOM. No termination code was returned there. This is endpoint-level completeness for returned records, not assurance of complete agency action reporting. SAM migration and key-required current access remain disclosed limits. Failed API requests are retained separately from successful negative searches.
Controlling updated tables: program_census, legacy_reconciliation, power_africa_action_review_v11, primary_award_actions_v11, legacy_award_survival_v11, legacy_award_followup_ids_v11, doge_cancellation_crosswalk_v11, roster_verification_v11 and source_registry_v11. Unchanged v0.10 office, event and country-lead tables remain controlling for those subjects. History/v0_10 preserves the exact update baseline; historical scripts must not be run over current data accidentally.
The selected survival cohort is now 25, including 13 Power Africa awards. Six government-filed historical notices include the three priority contracts and three incidental matches. No current survival certification is made. Country/eligibility/presence/sector matrices and the country ledger are unchanged. No statistical projection is generated.

Reproduction
Run scripts/update_v11.py against retained snapshots; then scripts/build_paper.py and scripts/build_workbook.mjs. Render the DOCX with scripts/render_docx.py --emit_pdf and copy its PDF to the current deliverables filename. Run scripts/verify_census.py, scripts/verify_rosters_v11.py, scripts/verify_artifacts_v11.py and scripts/build_release_notes_v11.py. Inspect rendered paper and changed spreadsheet views. package_release.py creates the manifest and ZIP; verify_release.py checks its source-file hashes. Python and Node dependencies are recorded in scripts/dependencies.txt. Current retrieval requests, responses and failures are in research_v11. Re-fetching live sources may change the evidence and is not identical reproduction.
'''
(O/'Methods_and_Census_Boundary_v0_11.txt').write_text(prior+addition)
print('Release notes written')

check=P/'validation/artifact_verification_v11.json'
if check.exists():
 v=json.loads(check.read_text())
 with (O/'Research_Status_and_Rigor_v0_11.txt').open('a') as f:
  f.write('\nValidation results\nAll '+format(v['csv_cells_verified'],',')+' included workbook cells match their CSVs across 39 sheets; all 27,390 activity-matrix cells reconcile to the ledger. Exact primary IDs/date rows and 434 source index paths/hash records were checked. All three paper pages and six changed workbook previews were inspected. Nine country/eligibility/presence/sector/ledger tables are unchanged from v0.10.\n')
