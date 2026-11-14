# AQRS — Milestone status and acceptance evidence

**Current status:** M0/v0.1 and M1/v0.2 are accepted. M1 covers the documented local BTCUSDT spot research workflow on native Windows and headless Ubuntu. M2 remains in progress. E18 establishes the two-family workflow. The [current M2 evidence review](#aqrs-a10-learning-card-m2-evidence-and-threshold-decisions) records the remaining acceptance gaps. The price-drop outcome exercise remains deferred after M2-E12.

Allowed milestone statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `ACCEPTED`. `ACCEPTED` is permitted only after satisfying the relevant `MILESTONE_DOD.md` tests and referencing auditable evidence here. Existing documents are not proof of completion.

| Milestone | Deliverable | Status | Evidence / run IDs | Blockers / unresolved deviations |
|---|---|---|---|---|
| M0 / v0.1 | Reproducible synthetic walking skeleton, **including Resource Governor and native Windows/Linux acceptance** | ACCEPTED | Local paired runs and [four successful GitHub Actions jobs](https://github.com/RealMonoid/AQRS/actions/runs/42275704043) | — |
| M1 / v0.2 | Real data and market feasibility | ACCEPTED | [Criterion review](#m1-e07-learning-card-acceptance-evidence-review-2026-11-09), [clean Windows replay and acceptance](#m1-e11-learning-card-and-m1-acceptance-2026-11-09), and [fresh Ubuntu campaign](#m1-e06-learning-card-complete-real-data-campaign-2026-11-09) | Acceptance covers local, personal, non-production BTCUSDT spot research. Broader market suitability and scientific evidence remain open. |
| M2 / v0.3 | Discovery and matched controls | IN_PROGRESS | [Criterion review](#aqrs-a10-learning-card-m2-evidence-and-threshold-decisions) and [source-bound supervised replay](#m2-e20-p04-learning-card-source-bound-e09-replay) | Effective independent event counts and final release verification. |
| M3 / v0.4 | Adaptive research management | NOT_STARTED | — | — |
| M4 / v0.5 | Statistics and final-test candidate gates | NOT_STARTED | — | — |
| M5 / v0.6 | Net-cost/risk decisions and simulation | NOT_STARTED | — | — |
| M6 / v0.7 | Shadow/paper monitoring | NOT_STARTED | — | — |
| M7 / v0.8 | Operations and usability | NOT_STARTED | — | — |
| M8 / v0.9 | Integrated scientific beta and full evidence | NOT_STARTED | — | — |
| M9 / v1.0 | Locally deployable research product | NOT_STARTED | — | — |

## Experiment queue

This queue is the canonical work plan for concrete development, founding, and project-level research work. Row order is the current priority. The [dispatch rules](DEVELOPMENT_PROCESS.md#experiment-queue) govern execution. The [completion rules](DEVELOPMENT_PROCESS.md#completion-reconciliation) give the canonical locations for other follow-up. Follow the linked records for findings, revisit conditions, and owner decisions that affect readiness.

**Execution Reset:** [AQRS-ER01](#aqrs-er01-execution-reset) is complete. The
[governance freeze](DEVELOPMENT_PROCESS.md#experiment-queue) applies.

**Current scientific bottleneck, 2026-11-14.** M2-E20 still lacks defensible
independent information and precision for its fixed contrast. The approved
[P06 calibration](#m2-e20-p06-learning-card-local-expansion-deferred) found
that no fixed observed-SD planning case fits the local capacity ceiling;
the local expansion is deferred. This is not an alpha verdict or a request
for a longer period for that E18 volume contrast. The owner's subsequent
data and effort decisions authorize the new M2-E22 study below.

**Priority review, 2026-11-14.** Execute the owner-authorized M2-E22 predictive
screen first. It addresses a new, simple candidate with question-driven time
coverage. E21 retains its scope, independent benchmark and isolation gates;
E20's old contrast remains deferred. This does not close M2 acceptance gaps.

**M2-E15 queue update, 2026-11-10.** The queue edit and initial focused check took about 55 seconds. Routine documentation risk. FTA not triggered.

**Research follow-up review points, updated 2026-11-11.** The [M2-E12 price-drop decision](#m2-e12-learning-card-earlier-price-drop-coverage-2026-11-10) remains a historical V1 count. AQRS-A07 supersedes its outcome eligibility: the contaminated V1 control rule must not be used for outcomes. Quant Research must qualify `PRICE_DROP_V2` coverage under a separately authorized count, preserving the original requirement of one matched pair in each of three UTC bands on three distinct dates. Old V1 pairs cannot be carried forward. The missing 00:00–08:00 UTC coverage and observational-confounding question remain open. Any new count or outcome run requires authorization and preflight.

**M2-E09 research follow-up.** Stop the fixed LightGBM comparison on the same evidence. Reconsider a new proposal only if a materially new observation from authorized development evidence shows a recurring forecast or decision gap that LightGBM could plausibly address. Quant Research checks this during relevant candidate diagnostics. Keep the [original pilot decision](#m2-e09-learning-card-corrected-supervised-pilot-replay-2026-11-09) and the distinct M2 acceptance records for outcome parity and source reproducibility.

**M2-E18 and M2-E19 research follow-up.** The completed attempts stay closed.
E18 deferred both candidates after the [fixed screens missed](https://github.com/RealMonoid/AQRS/blob/e26e65e7b98496c44ff464e7a0fa44c10a7d6694/docs/MILESTONE_STATUS.md#m2-e18-windows-and-ubuntu-learning-card).
Quant Research checks during M2-E20 whether a named candidate-specific gap
and a development sample with a defensible count of independent observations
would justify a new comparison. E19 keeps the HMM conditional after it missed
the after-cost hurdle. At a relevant regime-filter review, Quant Research
checks for a newly documented mechanism addressing a named gap and adequate
development coverage, as specified in the
[E19 decision](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e19-learning-card-paired-volatility-gates).
Until those conditions are met, keep both E18 candidates deferred and keep the
HMM out of the active workflow. Any new campaign follows the existing
authorization and preflight rules.

| ID | Added | Status | Decision and minimum test | Start condition / origin |
|---|---|---|---|---|
| M2-E22 | 2026-11-14 | IN_PROGRESS | [Predictive-first Spot reversal study](#m2-e22-test-card-predictive-first-spot-reversal): one fixed candidate, 91 training days and 365 evaluation days; costs only after predictive pass. | Direct owner instruction in this chat: implement data/effort decisions and choose, acquire and execute the first research question. Locked holdout, preregistration, verification and unchanged Governor required. |
| M2-E21 | 2026-11-12 | WAITING | [Scout pilot](#m2-e21-scout-pilot-feature-preflight): test whether one agent can derive an executable event from development data and refrain from claiming a signal in a null case. | ADR-053 covers design and queue placement. The [entry review](#scout-preparation-and-remaining-start-conditions) identifies the reuse boundary. Confirm implementation and execution scope, obtain an independent synthetic benchmark and scoring commitment, and verify the isolated handoff and runtime bounds. |
| M2-E20 | 2026-11-12 | DEFERRED | [P06](#m2-e20-p06-learning-card-local-expansion-deferred) completed: no observed-SD sensitivity cell fits local capacity. Keep the fixed local outcome expansion deferred; independent information remains unknown. | Revisit when authorized candidate evidence supplies a named mechanism or independently supported change in dispersion/dependence/yield that makes a bounded comparison decision-changing. No larger data request or unchanged retest follows automatically. |
| AQRS-B01 | 2026-11-11 | WAITING | [Reassess the fixed blind-search benchmark](#aqrs-b01-capability-benchmark-deferral) once a new discovery path has credible end-to-end evidence. | Review M2-E21 before deciding whether to retain or replace the benchmark. Before any external B01 execution, close [AQRS-A10-F1](RISK_REGISTER.md#open-execution-path-quality-debt) independently and satisfy the existing delivery, dataset-scoped 24-trial exception and start gates. |
| AQRS-SC01 | 2026-11-10 | DEFERRED | [Read completed ACSIL bars in AQRS and display the AQRS result in Sierra Chart.](#aqrs-sc01-test-card-sierra-chart-and-acsil-round-trip-2026-11-10) | Deferred by the owner. Resume when the owner reprioritizes it, with a verified local Windows SDK and isolated replay workspace. |
| M4-E01 | 2026-11-11 | WAITING | Select the smallest claim-appropriate validation method under [ADR-052](DECISIONS.md). Compare its decision value with the existing chronological/matched-control baseline; qualify any selected implementation on known-answer/null cases before research use. | Future consideration only. Quant Research reviews at authorized M4 planning when a fixed claim, candidate family, benchmark, aligned series, exposure history and dependence/precision assumptions exist. Complete a bounded Test Card and resource estimate first; implementation and data/run approvals remain separate. Default until then: existing workflow, no extra computations. |
| AQRS-H01 | 2026-11-14 | DEFERRED | [Research Harness Enforcement Review](#aqrs-h01-research-harness-enforcement-review): assess reliable adherence to existing research rules and evidence for targeted technical enforcement. | Owner-directed follow-up. Revisit after the next three material, genuine research work items or immediately after the first observed material research-governance violation, whichever occurs first. Existing research priorities and start conditions remain unchanged. |
| AQRS-GIT01 | 2026-11-14 | CLOSED | [Autonomous repository completion](#aqrs-git01-autonomous-repository-completion): normal Git closure defined, published and exercised on the current repository. | SUPPORTED / PERSEVERE for the owner's standalone scope. Nine scenarios and four CI jobs passed; obsolete refs/worktrees removed and historical/dirty work preserved. No wider research authorization. |
| AQRS-ER01 | 2026-11-14 | CLOSED | [Execution Reset](#aqrs-er01-learning-card-canonical-integration-and-research-dispatch): main consolidated and verified; governance freeze active; E20 calibrated through its approved stop. | SUPPORTED / PERSEVERE for canonical state and bounded scientific preparation. No independent covered READY item remains. |
| M2-E20-P06 | 2026-11-14 | CLOSED | [One report calibration](#m2-e20-p06-learning-card-local-expansion-deferred), published before access and independently verified. | Valid diagnostic; DEFER_LOCAL_OUTCOME_EXPANSION. Inference INCONCLUSIVE; no new market data or models. |
| AQRS-A16-P01 | 2026-11-14 | CLOSED | [P06 host observation](#aqrs-a16-p01-learning-card-p06-observation). | INCONCLUSIVE for unprompted seven-check adherence; actual observed behavior and absent triggers recorded. No standalone follow-up launched. |
| M2-E20-P05 | 2026-11-14 | CLOSED | [Decision-specific evidence design](#m2-e20-p05-learning-card-decision-specific-evidence-design): sensitivity and metadata support one bounded calibration, not a fixed data duration. | SUPPORTED / PERSEVERE for preparation; owner subsequently approved P06. |
| AQRS-A16 | 2026-11-14 | CLOSED | [Audited and closed confirmed literature-process gaps](#aqrs-a16-learning-card-literature-process-audit). | Owner-authorized standalone audit and documentation correction; A–H and three protection/stop cases verified. No research campaign, variant registration or wider dispatch. |
| M2-E15 | 2026-11-10 | CLOSED | [Authorized state-persistence count](#m2-e15-learning-card-state-persistence-count) completed and passed the coverage gate. | A separate outcome proposal requires a fixed decision, defensible precision basis and scoped approval. |
| AQRS-A15 | 2026-11-14 | CLOSED | [Repaired the research value stream](#aqrs-a15-learning-card-research-value-stream-repair): consolidated exposure, preserved diagnostic views and linked origin to learning. | Owner-authorized engineering repair verified; zero new research campaigns or fits. E20's scientific prerequisites remain open. |
| AQRS-A14 | 2026-11-14 | CLOSED | [Audit and clarify decision-ready research evidence](#aqrs-a14-learning-card-decision-ready-research-evidence). | Owner-directed standalone process review. Existing campaign and data approvals govern further research. |
| M2-E20-P04 | 2026-11-14 | CLOSED | [Source-bound E09 replay](#m2-e20-p04-learning-card-source-bound-e09-replay) and [capacity follow-up](#m2-e20-capacity-and-forecast-evidence-follow-up). | SUPPORTED / PERSEVERE for supervised pilot reproducibility. E20 outcome work awaits eligible evidence. |
| M2-E20-P03 | 2026-11-13 | CLOSED | [Prepared source and receipt verification](#m2-e20-p03-learning-card-supervised-replay-readiness). | SUPPORTED / PERSEVERE for the bounded preparation. Parent: M2-E20. The replay remains reserved. |
| M2-E15-P01 | 2026-11-13 | CLOSED | [Designed the count-only state-persistence comparison](#m2-e15-p01-learning-card-state-persistence-count-design). | SUPPORTED / PERSEVERE for the design and its synthetic boundary checks. Parent: M2-E15. |
| M2-E20-P02 | 2026-11-13 | CLOSED | [Designed the effective-count comparison](#m2-e20-p02-learning-card-effective-count-design). | SUPPORTED / PERSEVERE for design. DEFER the market calculation pending decision-changing evidence. Parent: M2-E20. |
| M2-E20-P01 | 2026-11-12 | CLOSED | [Checked effective-observation readiness](#m2-e20-p01-learning-card-effective-observation-readiness). | REFUTED / DEFER for estimating a defensible count from the existing E18 evidence. Parent: M2-E20. |
| AQRS-A12 | 2026-11-12 | CLOSED | [Operationalize autonomous work management](#aqrs-a12-test-card--autonomous-work-management) against the owner's 19 checks and ten cases. | Owner correction on 2026-11-12 authorizes this standalone audit, minimal governance fixes and verification. Completed under the 60-minute estimate. See the card for authority, stop boundary and resource scope. |
| AQRS-A10 | 2026-11-12 | CLOSED | [M2 evidence review and threshold guidance](#aqrs-a10-learning-card-m2-evidence-and-threshold-decisions). | Documentation and evidence review completed. Follow the E20 start conditions and the separate E09 approval boundary. The separate archive check is AQRS-A13. |
| AQRS-A13 | 2026-11-12 | CLOSED | [Read-only E14 and E18 archive check](#aqrs-a13-read-only-campaign-evidence-check). | Standalone owner-approved check. The original E18 worktree used AQRS-A10 for this item. |
| M2-E19 | 2026-11-12 | CLOSED | [Paired volatility-gate comparison](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/evidence/m2-e19-verification.json) and [precision planning](#m2-e19-precision-and-data-capacity-check). | Technical pilot completed on Windows and Ubuntu. Research `INCONCLUSIVE / DEFER`. See the [revisit conditions above](#experiment-queue). |
| M2-E18 | 2026-11-11 | CLOSED | [Paired two-family workflow](https://github.com/RealMonoid/AQRS/blob/e26e65e7b98496c44ff464e7a0fa44c10a7d6694/evidence/m2-e18-verification.json). | Two candidate comparisons completed. Both research follow-ups deferred. See the [revisit conditions above](#experiment-queue). M2 acceptance remains open. |
| M2-E17 | 2026-11-11 | CLOSED | [Training-only feasibility receipt](https://github.com/RealMonoid/AQRS/blob/eb8ed5c/evidence/m2-e17-verification.json). | Qualified the E18 training prefix. No evidence of predictive benefit. |
| M2-E14 | 2026-11-10 | CLOSED | [Fixed Windows comparison](https://github.com/RealMonoid/AQRS/blob/76cdfd3d1b59e81eb5f51ae633a3875ec28b5f39/evidence/m2-e14-verification.json). | Volume evaluated. Ridge stopped at the training movement screen. The conditional market replay did not start. |
| AQRS-D01 | 2026-11-11 | CLOSED | [Qualified 48 free Spot archives and 69,120 minute bars with retained activity fields.](#aqrs-d01-learning-card-qualified-free-spot-development-data) | SUPPORTED / PERSEVERE for data preparation after independent review and four Windows/Linux CI jobs. M2-E14 outcome admission remains separate. |
| AQRS-A08 | 2026-11-11 | CLOSED | [Descriptive diagnostics and additional-view accounting verified.](#aqrs-a08-learning-card-descriptive-signal-diagnostics) | SUPPORTED / PERSEVERE for the scoped engineering slice. M2-E14 still requires justified precision, its independent full-design review and a verified admission entry before outcomes. |
| AQRS-A07 | 2026-11-11 | CLOSED | [Corrected control timing and verified complete opportunity and precision diagnostics.](#aqrs-a07-learning-card-research-comparison-and-precision-boundaries) | Independent review and four exact-revision CI jobs passed. Scientific coverage, confounding and M2-E14 design admission remain open. |
| AQRS-A06 | 2026-11-11 | CLOSED | [Verified audit controls and restored the preserved evidence from the private remote.](#aqrs-a06-learning-card-audit-controls-and-recoverable-evidence) | Engineering and readiness review completed; historical source and preregistration gaps remain explicit. |
| M2-E16 | 2026-11-10 | CLOSED | [Archived M2-E09 evidence cannot establish executed source identity for both runs.](#m2-e16-learning-card-historical-source-binding-2026-11-10) | Read-only follow-up to the AQRS-A02 M2-E09 acceptance finding. |
| AQRS-A05 | 2026-11-10 | CLOSED | [Added a revisit rule and verified it on four existing cases.](#aqrs-a05-learning-card-observable-deferral) | Owner approved the bounded governance follow-up. Documentation and verification only. |
| AQRS-A04 | 2026-11-10 | CLOSED | [Clarified predeclared criteria, routine work, and shared test evidence.](#aqrs-a04-learning-card-decision-ready-cards) | Owner approved the four recommendations from the card audit. Documentation and verification only. |
| AQRS-A03 | 2026-11-10 | CLOSED | [Clarified continuation, reporting and dispatch at the authorized work boundary.](#aqrs-a03-learning-card-authorized-continuation) | The owner approved the five recommendations from the autonomy audit. Documentation and verification only. |
| AQRS-A02 | 2026-11-10 | CLOSED | [Material findings now govern dependent starts and resumption.](#current-buildmeasurelearn-development-loop) | Owner directed the governance correction and the four finding dispositions. |
| M2-E13 | 2026-11-10 | CLOSED | [Five assessments recorded with one data blocker and four deferrals.](#m2-e13-learning-card-five-model-assessments-2026-11-10) | Follow-up to M2-E12. The owner authorized an evidence review with zero downloads or fits. |
| M2-E12 | 2026-11-09 | CLOSED | [Three new pairs, all in the same UTC band. The combined coverage missed the minimum.](#m2-e12-learning-card-earlier-price-drop-coverage-2026-11-10) | Follow-up to M2-E11. The owner authorized obtaining and counting these seven archives on 2026-11-10. |
| M2-E11 | 2026-11-09 | CLOSED | [Mapped all M2 criteria and identified insufficient price-drop coverage as the first actionable gap.](#m2-e11-learning-card-m2-evidence-review-2026-11-09) | Follow-up to M2-E10. Review existing development evidence only. |
| M2-E10 | 2026-11-09 | CLOSED | [Both platforms matched. Isolation Forest follow-up deferred.](#m2-e10-learning-card-isolation-forest-pilot-2026-11-09) | Owner authorized the frozen Test Card, four development archives, and Ubuntu replay after valid Windows execution. |
| M2-E09 | 2026-11-09 | CLOSED | [Both platforms completed and matched. LightGBM follow-up deferred.](#m2-e09-learning-card-corrected-supervised-pilot-replay-2026-11-09) | Follow-up to M2-E08. The owner approved one Windows campaign with at most six fits and the Ubuntu replay conditional on complete Windows results. |
| M2-E08 | 2026-11-09 | CLOSED | [Windows stopped during LightGBM result construction](#m2-e08-learning-card-supervised-challenger-pilot-2026-11-09). The correction passed a focused regression. | Follow-up to M2-E07. The owner authorized the chain through execution, with zero holdout access. |
| M2-E07 | 2026-11-09 | CLOSED | [Selected January 1 through 4 UTC for the proposed supervised pilot](#m2-e07-learning-card-supervised-pilot-window-2026-11-09). Two chronological validation spans fit the existing purge rule. | Follow-up to M2-E06. The owner authorized metadata review only. |
| M2-E06 | 2026-11-09 | CLOSED | [The fitted candidate retained its scores and decisions when future bars changed](#m2-e06-learning-card-fitted-candidate-causality-2026-11-09). The check caught a planted look-ahead. | Follow-up to M2-E05. The owner authorized synthetic data only and zero holdout access. |
| M2-E05 | 2026-11-09 | CLOSED | [The earlier momentum decision survived a future-bar perturbation](#m2-e05-learning-card-decision-time-causality-2026-11-09). The check rejected a planted look-ahead. | M2 causal-test criterion. The owner authorized the next bounded M2 step with no holdout access. |
| M2-E04 | 2026-11-09 | CLOSED | [The fixed cross-term improved XOR predictions and gave no gain on the null](#m2-e04-learning-card-synthetic-interaction-comparison-2026-11-09). | From [ADR-045 integration](DECISIONS.md#adaptive-research-integration). The owner authorized the synthetic comparison and at most four fits. |
| M2-E03 | 2026-11-09 | CLOSED | [Two pairs on one of five development days](#m2-e03-learning-card-extended-development-data-coverage-2026-11-09). Outcome exercise deferred. | Follow-up to M2-E02. The owner approved obtaining and counting the four BTCUSDT spot archives for January 1 through 4, 2026 UTC. |
| M2-E02 | 2026-11-09 | CLOSED | [Zero eligible events on the development day](#m2-e02-learning-card-development-data-coverage-2026-11-09). Outcome exercise deferred. | Follow-up to M2-E01. The owner authorized this count-only use of the existing January 5, 2026 UTC archive. |
| M2-E01 | 2026-11-08 | CLOSED | [The matched control changed one synthetic research decision](#m2-e01-learning-card-one-event-research-decision-2026-11-09). | The owner authorized the probe. The inputs and rule were fixed in the [Test Card](#m2-e01-test-card-one-event-research-decision-2026-11-09) before the comparison. |
| M1-E11 | 2026-11-09 | CLOSED | [The bounded Windows replay](#m1-e11-learning-card-and-m1-acceptance-2026-11-09) ended `SUPPORTED / PERSEVERE` and closed the M1 gate. | Follow-up to M1-E10. The owner authorized one additional campaign with unchanged limits. |
| M1-E07 | 2026-11-09 | CLOSED | [M1 acceptance review](#m1-e07-learning-card-acceptance-evidence-review-2026-11-09) identified a fresh Windows replay as the remaining execution proof. | Follow-up to M1-E06. The owner approved the review and routine follow-through within M1. |
| M1-E08 | 2026-11-09 | CLOSED | [Fresh Windows setup](#m1-e08-learning-card-fresh-windows-acceptance-2026-11-09) ended `BLOCKED / PIVOT` before any run. | Follow-up to M1-E07. The offline cache did not contain the frozen NumPy wheel. |
| M1-E09 | 2026-11-09 | CLOSED | [Windows wheelhouse staging](#m1-e09-learning-card-windows-wheelhouse-and-replay-2026-11-09) ended `BLOCKED / PIVOT` before any run. | Follow-up to M1-E08. The package index could not be reached from the host. |
| M1-E10 | 2026-11-09 | CLOSED | [Clean Windows install passed and the campaign stopped at preflight](#m1-e10-learning-card-cached-windows-wheels-and-replay-2026-11-09). | Follow-up to M1-E09. One campaign attempt ended with zero completed fits. |
| M1-E06 | 2026-11-08 | CLOSED | [The fixed 30-minute campaign](#m1-e06-learning-card-complete-real-data-campaign-2026-11-09) ended `SUPPORTED / PERSEVERE` for the complete research CLI. | Follow-up to M1-E04 and M1-E05. The owner approved one Windows campaign and one conditional Ubuntu replay. |
| M1-E05 | 2026-11-08 | CLOSED | [The fixed execution check](#m1-e05-learning-card-real-data-execution-check-2026-11-08) ended `SUPPORTED / PERSEVERE`. | Follow-up to M1-E04. The owner approved one engineering check per platform and zero holdout reads. |
| M1-E04 | 2026-11-08 | CLOSED | [The fixed BTCUSDT spot campaign](#m1-e04-learning-card-first-real-data-campaign-2026-11-08) ended `SUPPORTED / PERSEVERE` for the cross-platform cost screen. | Follow-up to M1-E02. The owner approved one campaign per platform and zero holdout reads. |
| M1-E01 | 2026-11-08 | CLOSED | [Syncster/NQ source screen](#m1-e01-learning-card-syncsternq-2026-11-08) ended `INCONCLUSIVE / DEFER`. | Owner nominated Syncster for the no-cost NQ development-data screen. |
| M1-E03 | 2026-11-08 | CLOSED | [Alternative no-cost NQ source screen](#m1-e03-learning-card-alternative-no-cost-nq-source-2026-11-08) ended `INCONCLUSIVE / DEFER`. | Follow-up to M1-E01. Owner authorized a review of public material. |
| M1-E02 | 2026-11-08 | CLOSED | [Binance BTCUSDT import pilot](#m1-e02-learning-card-binance-btcusdt-spot-2026-11-08) ended `SUPPORTED / PERSEVERE`. | Follow-up to M1-E01 and M1-E03. Owner selected the source and authorized the pilot. |

**Queue Test Card, 2026-11-08.** The existing status file can guide experiment selection and retain decisions. Pass if Codex can identify the first eligible test, the M1 blockers, and what to change after a pass, rejection, or inconclusive result. Use one documentation session and zero research runs. Stop after focused and language checks. Routine documentation risk. FTA not triggered.

**Queue Learning Card.** `SUPPORTED / PERSEVERE` for the documentation. The focused review traced the M1 start conditions and the pass, rejection, and deferral paths. At the time of that review, both M1 entries were waiting.

### M2-E22 Test Card: predictive-first Spot reversal

**Authorization, 2026-11-14.** The owner directly ordered policy implementation
and one new research study in this chat. Codex selects the candidate and amount.
Total effort estimate: 2–4 hours including intake, code, review and closure;
eight-hour safeguard applies. Intake began approximately 11:35 UTC; the journal
will record exact execution times. No general audit or further research
sequence is authorized by the time rule.

**Question and smallest slice.** Does reversing the sign of the last completed
BTCUSDT Spot 30-minute open-to-close return predict the next bar's direction
better than both constant-direction controls (always up and always down)?
Also report the training-only majority-direction rule. One fixed candidate
`REVERSAL_30M_E22_V1`, no search, refit, sign switching or horizon changes.
Zero feature return uses the baseline; zero target return scores 0.5 for
either direction. Baseline is the majority of nonzero training directions;
ties choose up. Charge its calibration as one fit. Feature available at
close[t], target open[t+1] to close[t+1]; target intervals do not overlap.
Reuse supervisor, platform guards, provenance, journal and OHLCV validation.
Use a narrow monthly entry; keep D01's legacy 1-minute/31-day entry unchanged.

**Data fixed before acquisition.** Official free Binance Spot BTCUSDT 30m
monthly klines, 2024-09 through 2025-11: 15 archives, 456 complete UTC days,
21,888 bars. Training: 2024-09-01–2024-11-30 (91 days). Evaluation:
2024-12-01–2025-11-30 (365 days, 17,520 targets). These months precede the known
December/January pilot windows; they are development validation, not protected
confirmation or proof of no outside exposure. The [locked holdout](RESEARCH_PROTOCOL.md#owner-data-authorization-and-fixed-holdout)
is 2026-09-01–2026-10-31 inclusive, plus 2026-01-06. No download or read;
owner-only release. Reject missing/duplicate/invalid bars, wrong month/member,
checksum or timestamp units; no imputation, replacement dates or enlargement.
Stop after one acquisition/analysis attempt, including failure; no auto-retry.

**Primary decision.** Equal-weight daily paired accuracy differences, reversal
minus each fixed direction. Report all accuracies, differences and individual
one-sided 95% lower/upper bounds using Newey–West/Bartlett HAC with seven daily
lags and a prespecified 14-lag sensitivity. `PREDICTIVE_PASS` requires all four
lower bounds >0: an intersection-union superiority claim over both controls,
not selection of the favorable comparator. If no pass and either control has
both upper bounds <0.02, report `BELOW_RELEVANT_EFFECT`; otherwise
`INCONCLUSIVE`. Two percentage points is only the disclosed sample-planning
effect, not an extra pass condition, economic hurdle or literature constant. No
17-bps/trade filter in this stage. Store all daily scores and counts without
subgroup search. Effective independent sample size remains unknown.

**Why a year.** Conditional planning uses
`ceil((z_.95+z_.80)^2 * SD_day^2 * D / .02^2)` for one-sided 5% size/80% power.
This approximates rejection of a zero effect against one control, not power
of the joint four-bound admission rule. At daily SD 0.10, design effects
D=1/2/4 require 155/310/619 days; at SD 0.15,
348/696/1392. A year exceeds the SD=0.10,D=2 case and spans a calendar cycle.
SD≈0.10 follows roughly 48 binary pairs/day with half disagreeing with the
baseline; it is an unmeasured planning assumption. Stronger dependence,
dispersion or regime change can defeat it. Preserve an inconclusive result
and the fixed stop instead of adding data.

**Conditional costs.** Only after predictive pass, evaluate the unchanged
long-or-flat reversal and baseline versus cash on shared opportunities,
including flat ones. Enter at next open, exit at the following open; omit
the final bar lacking that exit. Use the existing illustrative Spot costs:
10 bps fee/side, 1 bps full spread, 2 bps slippage/side (25 bps/round trip),
no funding or shorts. Report gross/net bps per opportunity and entered trade;
no optimization, further fit or realistic-execution claim. Otherwise skip
costs, retaining prediction metrics. A pass is exploratory, not genuine alpha.

**Source/transfer check.** The primary [intraday predictability paper](https://www.sciencedirect.com/science/article/pii/S1062940822000833)
reports momentum/reversal; inspected publisher search excerpts motivate this
screen but do not establish the exact rule, window or threshold (full-page
access returned 403). This is not a replication. [Newey–West](https://www.nber.org/papers/t0055)
supports dependence-aware uncertainty asymptotically, not finite-sample
validity for this market. [Binance's official archive description](https://github.com/binance/binance-public-data)
specifies monthly Spot klines, checksums and the 2025 microsecond transition.
No newly selected market outcomes have been accessed at this point.

**Governor and acceptance.** One acquisition worker plus one research worker,
one calibration fit, zero model fits/seeds/resamples, concurrency one.
Conservative bound: 120 seconds each, 240 total within 300 seconds; 4096 MiB
observed RSS, not a strict RAM guarantee. Tighter central limits apply.
Cap each ZIP/CSV at 1 MiB, checksum at 4 KiB, local artifacts at 128 MiB;
measure first-month acquisition and extrapolate twofold before continuing.
Verify causal alignment, train-only baseline, ties, known signal/null,
HAC, holdout rejection before I/O, malformed input, fit budget and failed
attempt retention. Publish card and source-bound registration before market
access; require independent review and real Windows/Linux synthetic execution.
See the [focused FTA](RISK_REGISTER.md#m2-e22-predictive-study-and-holdout).

**Pre-outcome design correction.** Independent review after the initial
`3608670` publication identified a mismatch between normal-test power and a
point-estimate hurdle, and vulnerability of the training-majority comparator
to class imbalance changes. Before code or data access, remove that hurdle
and require both predeclared constant controls as above. Keep dates and amount.
The literature search included both momentum and reversal and recent work;
mixed findings motivated a falsifiable fixed rule, not a direction search.

**Implementation verification before acquisition.** Independent read-only
review reproduced timing/HAC/cost calculations and found three defects before
market access: a legacy importer could open a protected filename under a
different declared day; Windows CRLF registration bytes differed from the
Git LF blob; failed monthly acquisitions lacked their attempted month/cause.
Regression tests first reproduced each defect, then passed after correction.
The focused Windows suite passed 70 tests (24 E22 checks plus market/import
coverage). All diagnostic views are explicit (1,104 prediction views and 12
conditional economic views); these are not independent trials. The first
full suite had 332 passes and 11 source-replay fixture failures because the
new module was not yet in HEAD; rerun those checks after committing it.
Runtime review and Linux evidence remain prerequisites before acquisition.

### Historical queue decisions

These dated decisions retain their original scope; the current queue above
governs dispatch. Superseded open conditions are historical observations.

**AQRS-G02 owner-directed method review, 2026-11-11.** Record the requested
future validation methods under ADR-052 and the existing
[method protocol](MODEL_EVALUATION_PROTOCOL.md#validation-method-selection).
Routine documentation clarification: no current scientific, execution or
protection contract changes; FTA not triggered. Baseline: chronological folds,
matched costs/controls and conditional M4 statistics already exist in the
design; the named methods lacked a consolidated applicability/resource guide.
Success means all requested methods have a role, prerequisite and scope
boundary, with no code/configuration or frozen blind-source change. Estimate:
20–30 minutes, zero research trials/fits/resamples, no new dependencies or
recurring runtime. Stop if implementation or a frozen-plan change is required.
**Verification checkpoint: 08:29:41 UTC; 7 minutes 1 second measured since
08:22:40 UTC**, excluding initial orientation and final bookkeeping. Documentation
outcome: `SUPPORTED / PERSEVERE`; method implementation remains deferred.
Native Windows: `python scripts/check_language_policy.py --self-test`,
`python scripts/check_language_policy.py` and `git diff --check` passed, exit 0;
51 documentation/configuration files audited. An inline Python check confirmed
exactly five task-owned paths, complete latest-changelog coverage, 70 local
file links, all seven method rows and preservation of pre-existing document
content. All 23 AQRS-B01 source-bound files are byte-identical to the task's
baseline. Manual English/method/scope review passed. The initial temporary
baseline write was sandbox-denied; its authorized retry succeeded. No research
or runtime tests ran. Linux was not rerun for this documentation-only change;
no platform or milestone acceptance is claimed. No new numerical artifacts
were produced. The method table is the reviewable result; future implementation
and scientific qualification remain under M4-E01. No postmortem was triggered.

**Priority review for AQRS-G02.** Add M4-E01 after the existing pending work:
its decision value depends on a defined statistical claim and adequate series.
It does not displace AQRS-B01, M2-E14 or their start conditions and does not
authorize queue dispatch. Walk-forward and matched attribution/controls remain
the first layer; the conditional tests are not a mandatory serial checklist.

**AQRS-B01 owner-directed preparation, 2026-11-11.** Prepare the independent
external-synthetic blind search now, outside the existing queue sequence. The
owner selected preparation of 24 candidates, with budget approval later, and
requested the earliest technically ready handoff. Existing rows, priority and
start conditions are unchanged. No automatic dispatch follows this task.

### AQRS-B01 capability benchmark deferral

**Owner decision, 2026-11-11.** Defer B01 and prioritize the M2-E14 claim
review. The fixed-rule rehearsal and the later order-flow and reporting checks
establish bounded engineering behavior. The current blind plan would primarily
diagnose that finite rule set. At a relevant discovery-capability review,
Engineering and Quant Research should revisit B01 when the capability under
test runs end to end and a prospectively scored, independent benchmark can
change a concrete development decision. Define the baseline and budget, verify
the intended execution path, and make correct detections, false claims,
misses and effects outside the tested capability distinguishable. Until then,
keep external execution parked. The existing evidence remains historical.

**AQRS-G01 owner-directed policy correction, 2026-11-11.** ADR-051 removes mandatory data-rights and license reviews from current source/model prerequisites and milestone gates. Historical cards below retain the checks performed at the time; they do not reinstate the removed requirements. This is a deterministic documentation/configuration correction, not a new development hypothesis or market experiment. Technical access controls, causal timing, provenance, quality, free-data scope and resource limits remain in force. Verification passed: language self-test/check, current-requirement review, unchanged registry IDs/statuses/non-prose fields, all 17 owned paths in the changelog and `git diff --check`. Checkpoint 07:12:23 UTC; 11 minutes 8 seconds elapsed since the combined source/policy work started at 07:01:15 UTC. No critical contract changed; FTA not triggered. Zero market reads, fits, new dependencies or platform-runtime changes. The separately authorized free Spot data expansion follows the completed A08 integration checkpoint as AQRS-D01.

### AQRS-H01: Research Harness Enforcement Review

**Status: `DEFERRED`. Owner direction, 2026-11-14.** Retain exactly one
follow-up in this canonical work plan. Use evidence from actual future research
to determine which existing rules Codex reliably follows on its own and which,
if any, need technical enforcement. No enforcement implementation is planned now.

**Revisit trigger.** After the next three material, genuine research work items,
or immediately after the first observed material violation of an existing
research-governance rule, whichever occurs first. A material research work item
is actual scientific work with a research question/hypothesis and evidence;
documentation, audits, bug fixes and routine engineering do not count.

**Observation and responsibility.** Count prospectively from this entry:
**2/3 qualifying work items recorded**: [M2-E20-P05](#m2-e20-p05-learning-card-decision-specific-evidence-design),
2026-11-14, asked a concrete scientific design question and executed
capacity/sensitivity calculations against verified metadata. This is an
analytical design observation, not evidence of outcome admission or unprompted
rule adherence. [M2-E20-P06](#m2-e20-p06-learning-card-local-expansion-deferred),
2026-11-14, is the second: an authorized empirical report calibration with
a frozen decision and retained evidence. Neither establishes general
behavioral adherence. The reset's Git, documentation and engineering work do not
count. Quant Research checks the trigger at
existing research-work-item closeouts and immediately upon observing a material
violation. Retain qualifying work-item IDs and evidence references in this
entry, reusing existing Cards, Research Journal, verification and session
records, including relevant AQRS-A16-P01 observations. No separate observation
workstream or new role is created. Missing observations remain unassessed;
prompted recovery is not evidence of unprompted adherence.

**Questions at revisit, answered from the evidence actually produced:**

1. Which existing research rules did Codex apply correctly without an owner reminder?
2. Where was owner intervention necessary?
3. Where did Verification detect a violation?
4. Which rule was applied correctly only after an additional prompt?
5. Which failure modes recurred?
6. Which violations could materially or irreversibly contaminate scientific evidence?
7. Which rules demonstrably benefit from technical enforcement?
8. Which rules should deliberately remain judgment-dependent Quant Research decisions?

**Categories to assess for technical enforcement if a failure mode is observed:**

- Holdout/protected-data boundaries.
- Look-ahead and availability timing.
- Registration and freeze.
- Source/data identity.
- Resource Governor limits.
- Exposure and variant counting.
- Unauthorized adaptive changes to an already frozen outcome test.

**Revisit decision:** record the evidence and one of these outcomes here:

- `NO ADDITIONAL ENFORCEMENT JUSTIFIED`
- `TARGETED ENFORCEMENT JUSTIFIED`
- `MATERIAL HARNESS GAP`

Propose technical implementation only when a specific observed failure mode or
a clearly irreversible evidence risk justifies it. This follow-up does not
prescribe a general research-orchestration engine, a new workflow platform or
additional governance. Literature checks, hypothesis formulation, mechanism
assessment and similar research judgments remain with Quant Research; technical
feasibility alone is no reason to automate them.

**Default, priority and resources.** Continue current research under existing
rules. H01 creates no prerequisite or blocking gate for current work and does
not reorder any existing research item. The trigger opens an evidence review,
not implementation authorization. Reuse existing records with zero additional
campaigns, trials, fits, resamples, market/protected-data access, dependencies or
spend; existing Resource Governor limits remain unchanged. Any justified implementation proposal
must follow the existing scope, resource-assessment and authorization rules.

**Recording scope and verification.** Routine documentation change, estimated
at under ten minutes; no critical contract change, so FTA is not triggered.
Baseline: the queue-row lookup found no H01 entry (exit 1). Success requires one
H01 row with the requested trigger and scope, unchanged prior queue rows, both
changed paths in the sole changelog, and passing documentation checks. Stop
after recording and verification; the review awaits future qualifying evidence.

**Recording checkpoint, 2026-11-14.** Native Windows: the queue lookup now
passes; the inline `python -B -` scope/link/preservation check, both language
checker commands and `git diff --check` passed, exit 0. Manual English and
scope review passed. Measured from 09:44:52 to 09:48:40 UTC: 3 minutes 48 seconds,
excluding final bookkeeping and rechecks. No runtime, research or Linux test
ran; behavioral adherence remains unassessed. This standalone recording mandate
ends here: H01 awaits its trigger, and all six existing pending rows retain
their recorded prerequisites with no eligible covered next item.

## Current Build–Measure–Learn development loop

### AQRS-GIT01: autonomous repository completion

**Owner authorization and Test Card, 2026-11-14, before implementation.**
The attached request in chat `01a1d9b4-2b13-7530-b920-7d772cbd5678`
authorizes permanent routine Git completion and one safe cleanup of the
existing repository. This specific owner instruction covers the work despite
the general governance freeze; it does not reopen other audits or research.

- **Assumption and minimum proof:** the existing Git tools and five canonical
  documents can make normal completion autonomous without losing work or
  changing research source identities. A required new service or unresolved
  ownership conflict would favor narrowing the cleanup instead.
- **Baseline:** clean local and remote `main` at
  `3e85eb28d4ab64df623cea25a710b0502e861818`; the previous Execution Reset
  consolidated the project once. Current DoD has no routine commit, merge,
  push or remote-SHA gate. Eight worktrees and eight additional local branches
  remain; three branch tips have unique historical commits. GitHub reports
  `main` as default, no branch protection/rulesets and no open PRs.
- **Acceptance fixed by the owner request:** exercise A normal branch to
  synchronized main, B remote-ahead integration, C merged-branch cleanup,
  D unknown unique work retained, E dirty worktree retained, F failed main
  check prevents push, G rejected divergent push reconciled without force,
  H suspicious file excluded, and I historical source reference unchanged.
  Use disposable local Git repositories for destructive/negative cases and
  the actual AQRS repository for publication and preservation checks.
  Pass requires all nine expected dispositions, unchanged tracked research
  evidence/runtime, reviewed exact changed paths and freshly equal local/
  remote main SHAs. A real remote/owner blocker leaves completion explicitly
  open; no declaration of DONE based on a local branch alone.
- **Reuse and sequencing:** amend AGENTS, Development Process and Codex Start;
  use this card and the sole changelog for evidence. Reuse existing language,
  archive/exposure checks and CI. The owner-directed closure comes before
  any new item; no covered research item is READY. IDEA-002/003 favor bounded
  checks without a new audit system or per-item documentation.
- **Risk screen:** no scientific, journal, runtime or platform contract is
  changed; FTA not triggered. The concrete cleanup failure paths are deleting
  unique commits or ignored/dirty evidence, publishing a failed merge, and
  leaking a credential. Check ancestry, all worktrees including ignored
  files, exact staged content, remote heads and post-integration results;
  retain any uncertain artifact. Cases D–I challenge these boundaries.
- **Budget and stop:** at most 90 minutes total development including intake,
  verification, publication and cleanup; no spending, dependencies, market
  data access, research fits or holdout reads. Disposable Git cases have a
  120-second bound; existing CI retains its 15-minute job limit and synthetic
  fixtures. No research-budget change or recurring service. Stop only the
  dependent path on failed validation, uncertain unique work, unsafe history
  replacement or a reserved owner gate. Reuse valid unchanged-runtime evidence.
  Elapsed-time measurement starts at the first clock observation,
  10:57:54 UTC; preceding intake is excluded from the measured interval.

**Pre-publication measurement.** The disposable `check_cases.py` operator
exercise passed all nine cases A–I in 7.88 seconds (exit 0). Actual Git
operations included an ordinary merge/push with SHA equality, remote-ahead
fast-forward, refusal to delete a unique branch or dirty worktree, and a
non-fast-forward rejection followed by a preserving merge. F injected a
failed validation result and withheld publication; H excluded a suspicious
dummy file through explicit staging. I preserved the original source-bound
receipt. These are procedural scenarios, not a new automatic Git enforcement
service or proof of every future agent's adherence. The one-shot script and
command/result JSON remain in the session's temporary directory.

**Learning Card and publication evidence.** The permanent change uses five
existing documents, with all five paths in `CHANGELOG.md`. The old rules
already covered authorization, validation and reconciliation; normal commit,
merge, publication, live SHA comparison and safe cleanup were not part of
the ongoing DoD. The new [canonical flow](DEVELOPMENT_PROCESS.md#autonomous-git-completion)
closes that gap without a new Git service, tracker, PR requirement or owner
approval for routine publication. No milestone or scientific claim changes.

The initial branch was `main`; both local and live remote main were
`3e85eb28d4ab64df623cea25a710b0502e861818`. Work used
`codex/aqrs-git01-autonomous-closeout`. Commit
`fd34dec4960bc4842a8f811cd3455406f93db698` was integrated with
`git merge --ff-only`, checked on main and published with
`git push origin main:main`. `git rev-parse refs/heads/main` and fresh
`git ls-remote origin refs/heads/main` returned that same SHA; root was clean
and ahead/behind was 0/0. The final evidence-only closeout follows the same
gate; its actual final SHA is identified by Git, avoiding a self-reference.

**Cleanup actually performed.** All ten obsolete remote tips were confirmed
main ancestors against live remote heads, with no open PR or dependent active
worktree, before one ordinary atomic deletion: `audit/aqrs-a06`,
`audit/aqrs-a07`, `codex/aqrs-a08-signal-diagnostics`,
`codex/aqrs-b01-blind-preparation`, `codex/aqrs-d01-spot-data`,
`codex/aqrs-execution-reset`, `codex/m2-e09-source-bound-replay`,
`codex/m2-e14`, `codex/m2-e18`, and `codex/m2-e19-regime-filter`.
The local `codex/aqrs-execution-reset` was deleted with `git branch -d`.
Three inactive clean worktrees were removed with `git worktree remove`:
E18 replay at `1eebbfa`, E19 replay at `376eb42`, and the detached E09
registration at `0a8199f`. Each had no untracked/ignored files and retained
reachable source history. No force, reset, clean, rebase, tag replacement,
repository-security change or research rerun was used.

| Remaining relevant branch | Disposition and reason |
|---|---|
| `main` (local/remote) | ACTIVE; canonical published project state. |
| `codex/m2-e14-evidence` (local/remote) | FULLY_MERGED; retain its clean linked worktree and ignored research artifacts. |
| `codex/m2-e17` (local) | FULLY_MERGED; retain its clean linked worktree and ignored research artifacts. |
| `codex/m2-e18-evidence` (local/remote) | FULLY_MERGED; retain the linked worktree, four dirty files and ignored artifacts. The earlier reset already preserved/integrated the changes. |
| `codex/m2-e19-evidence` (local/remote) | FULLY_MERGED; retain the linked worktree, three dirty files and ignored artifacts, already preserved/integrated by the reset. |
| `codex/aqrs-a08-local-verification` (local) | Intentionally retained: exact historical review commit `4fd02d9`, referenced by A08/D01 verification; `git cherry` confirms patch equivalence, which is not commit identity. |
| `codex/m2-e18-ubuntu-replay` (local/remote) | Intentionally retained: two unique historical replay/receipt commits ending at `1eebbfa`, referenced by evidence verification. No active worktree remains. |
| `codex/m2-e19-ubuntu-replay` (local/remote) | Intentionally retained: unique historical replay commit `376eb42`, referenced by E19 verification. No active worktree remains. |

The temporary GIT01 branch remains active only through this closeout and is
removed after final publication. Of eight original worktrees, five remain:
the main checkout and the four intentionally preserved E14/E17/E18/E19
worktrees above. The historical refs have known purposes; none represents
unreviewed new development awaiting integration. No repository ambiguity or
Git owner decision remains. The four retained worktrees are not claimed clean.

**Verification already observed, all exit 0.** On native Windows Python
3.12.12, the focused command
`.venv/Scripts/python.exe -m pytest -q tests/test_audit_controls.py
-k 'evidence or exposure or source_snapshot' --tb=short`
passed 27 tests (44 deselected), then passed again on resulting main in
5.61 seconds. `scripts/evidence_archive.py --verify` checked 295 preserved
files; `--verify-exposure` confirmed 95 attempts, 15 variants and 345 diagnostic
views, with 85 historically unknown inventories unchanged. `python
scripts/check_language_policy.py --self-test`, its normal check (58 files),
Ruff, `git diff --check` and the integrated diff check passed. The read-only
temporary `verify_repository.py` checked all five changelog paths, 265 local
links/anchors, a bounded secret-pattern scan, and byte-identical hashes for
79 tracked runtime/evidence/configuration files and all seven foreign dirty
files, including after cleanup. Manual staged-diff review found only the five
authorized English documentation paths. The scan is not a complete secret audit.

**CI, decision and measured endpoint, 2026-11-14.** All four jobs of
[run 43588687409](https://github.com/RealMonoid/AQRS/actions/runs/43588687409)
passed on `fd34dec4960bc4842a8f811cd3455406f93db698`: Windows and headless
non-root Ubuntu 24.04, Python 3.11/3.12. Each passed 324 behavioral tests,
synthetic CLI plan/run, archive/exposure checks, Ruff and language checks.
Windows test times were 196.62/180.10 seconds; Ubuntu 76.08/86.66 seconds.
The [Ubuntu 3.12 artifact](https://github.com/RealMonoid/AQRS/actions/runs/43588687409/artifacts/14111677075)
is one example of the retained synthetic acceptance outputs. This final
evidence-only closeout uses `[skip ci]` to avoid repeating the four unchanged
runtime campaigns; fresh local documentation, preservation and SHA checks
still apply to the resulting main before completion is reported.

**SUPPORTED / PERSEVERE:** adopt the documented normal flow. Execution and
procedural checks passed; future unprompted adherence is not established by
this one task. No scientific benefit was tested, no material incident occurred
and no new rejected engineering method needs an IDEA entry. Measured elapsed
work was 17 minutes 15 seconds from 10:57:54 through 11:15:09 UTC, excluding
earlier intake and subsequent final documentation/publication checks; within
the 90-minute total estimate. The remaining boundary is intentional retention
of historical refs and local artifacts, not an unresolved ownership question.

**Final dispatch.** The standalone mandate does not authorize the waiting
Scout pilot or additional research. M2-E21 remains the next concrete proposed
objective, requiring owner implementation/execution scope, an independent
synthetic benchmark/scoring commitment and verified isolation/runtime bounds.
Its existing entry preparation is complete; no independent covered READY
item remains. E20's deferral and H01's unmet trigger remain unchanged.

### AQRS-ER01 Execution Reset

**Owner authorization and Test Card, 2026-11-14.** The attached Execution
Reset request authorizes repository inspection, safe ordinary consolidation
onto `main`, local branch hygiene, a persistent freeze of untriggered general
governance audits, and scientific preparation of M2-E20 through the actual
data or execution gate. This is an execution and evidence-design task, not
another A-series audit. Start: 09:53:01 UTC. Estimate: two to four hours for
the entire sequence, including review, corrections, checks and reconciliation;
the standing eight-hour limit applies cumulatively.

**Assumption and minimum proof.** The current work can be made canonical
without losing unique history or dirty work, and existing definitions,
qualified metadata and already recorded evidence can distinguish a justified
E20 calibration from an unsupported calendar-data request. Baseline:
`main`/`origin/main` at `ebfabb0`, current published branch at `cb6f2b7`,
plus H01 edits and dirty E18/E19 evidence worktrees. Intake fetched `origin`
and inspected every local/remote head and worktree. This baseline inspection
precedes the card; no new E20 outcome or precision calculation informed it.

**Pass and stop.** Preserve all original refs and dirty bytes; identify
unique versus contained/equivalent work; integrate only reviewed authorized
content and pass applicable Windows, documentation and evidence checks before
moving `main`. Existing historical source and evidence identities remain
reachable. Any unresolved unique-work conflict stops only its dependent
integration. For E20, reconstruct the sample calculation, observation unit,
dependence assumptions, event yield and calendar bound; produce either a
quantitatively justified scope or the cheapest bounded calibration packet.
No outcome read, new download, model family, forecast infrastructure, automatic
data extension or research run is authorized by this card.

**Risk and resources.** Preservation and integration errors are the material
risk: a verified Git bundle plus byte/diff snapshots cover all original refs
and nine dirty tracked files before mutation. Inspect semantic conflicts,
verify original evidence digests and use an independent read-only integration
review. Reuse the existing tests, archive/exposure verifier, precision planner
and historical definitions. No scientific or safety contract change is
planned; apply the existing FTA gate if a necessary correction changes one.
Research budget: zero new trials, fits, resamples, raw/protected payload reads,
downloads, dependencies or spend. Synthetic software checks use existing
bounded tests; Linux execution is required if integration changes executable
content. Metadata and assumption-only arithmetic stay within this sequence.

**Sequence.** Preserve and inspect; construct the smallest coherent integration;
verify it; consolidate `main`; then complete M2-E20 decision design and the
existing permission-boundary/queue reconciliation. General governance work
does not follow this task without the owner's specified concrete trigger.

**Integration checkpoint and correction.** Regular merges retain `96df879`,
the two dirty-work snapshots `07a0713f`/`a4ffa0b`, and E09 evidence `0a8199f`.
The original worktrees remain untouched. Resolve older status/queue conflicts
in favor of the current reconciled records; retain the original source and
all historical commits. Replay-only CI remains historical. The first focused
run exposed frozen-registration fixture incompatibility and lost discovery
binding checks; digest-bound historical metadata fixtures and the current
flat projection resolve both without reopening registrations. The full
Windows suite then passed 314 tests in 215.92 seconds.

**Bounded integration postmortem.** Independent verification subsequently
constructed a synthetic journal whose metadata contradicted its authoritative
campaign/diagnostic binding. The projection still accepted it: current tests
covered diagnostic identity but missed conflicting flat metadata. Seven new
fit-free negative cases reproduced that gap. Validate every present binding
field against the campaign/report before returning; all ten binding cases
and the 44 focused archive/exposure checks now pass. The unchanged real index
still verifies 95 attempts, 15 variants and 345 recorded views. No evidence
of an altered historical result was found. Recheck the full suite and the
four-platform CI matrix before `main`; this targeted correction creates no
new general audit or research work item.

### AQRS-ER01 Learning Card: canonical integration and research dispatch

**2026-11-14. SUPPORTED / PERSEVERE for canonical integration and E20
preparation.** At intake the active `codex/aqrs-b01-blind-preparation` was
`cb6f2b7`, while local/remote `main` were `ebfabb0`, 14 commits behind that
branch alone. E14/E17/E18/E19 implementation and local evidence work also
needed reconciliation. The initial claim was verified, not assumed.

**Preservation and ordinary integration.** A verified all-ref bundle, ref
inventory, binary patches and SHA-256 inventory of nine dirty tracked files
were retained in `.git/execution-reset-20261114/` before mutation. H01's
pending root changes became `6e6c883`. Separate temporary-index commits
`07a0713` and `a4ffa0b` preserved the E18/E19 worktree changes without
altering either original worktree. Regular merges retained both lines,
`96df879` and the E09 replay history `0a8199f`; byte-identical or superseded
records were resolved without replaying research. The merge reconciled
historical registration fixtures and archive/exposure binding guards while
retaining the newer A15 index schema. The observed metadata-binding defect
and its negative tests are recorded above; no wider audit followed.

The tested code revision `fbba81167a9324ade2cb0abc9818beac415a1eb6` became
local/remote `main` through ordinary merge `6790861396157f5e739865bc675ac3275639ce39`.
The merge tree exactly matched the tested tree; ahead/behind was 0/0.
Subsequent reset closeout changes are documentation only. The final head
is identified by the closing Git commit and its changelog, avoiding a
self-referential commit hash. No force push, rewritten history or remote
branch deletion occurred. Original E18/E19 worktree bytes remain intact.

| Remaining local ref | Classification / evidence |
|---|---|
| `main` | ACTIVE; canonical integrated project state |
| `codex/aqrs-execution-reset` | FULLY_MERGED; tested integration source |
| `codex/m2-e14-evidence`, `codex/m2-e17`, `codex/m2-e18-evidence`, `codex/m2-e19-evidence` | FULLY_MERGED; retained because linked worktrees exist; E18/E19 dirty bytes also preserved and integrated |
| `codex/aqrs-a08-local-verification` | OBSOLETE_BUT_PRESERVED; `4fd02d9` is patch-equivalent to integrated `c4a6ff8`, confirmed by `git cherry` |
| `codex/m2-e18-ubuntu-replay` | OBSOLETE_BUT_PRESERVED; `1eebbfa`, two unique replay/receipt commits, historical source reference |
| `codex/m2-e19-ubuntu-replay` | OBSOLETE_BUT_PRESERVED; `376eb42`, one unique replay workflow commit |

No `UNIQUE_WORK_REQUIRES_REVIEW` remains. The two replay-only branches must
not replace current full acceptance CI. All fetched remote tips are main
ancestors except those same preserved replay tips. Ten local branches were
deleted only after ancestry proof: `audit/aqrs-a06`, `audit/aqrs-a07`,
`codex/aqrs-a08-signal-diagnostics`, `codex/aqrs-b01-blind-preparation`,
`codex/aqrs-d01-spot-data`, `codex/m2-e14`, `codex/m2-e18`,
`codex/m2-e19-regime-filter`, and the temporary preservation refs
`codex/aqrs-e18-local-preserved` / `codex/aqrs-e19-local-preserved`.
Their commits remain reachable from published main. One normal `branch -d`
initially refused the A06 upstream comparison; after verifying main ancestry,
setting its local upstream to main allowed ordinary deletion. No force was used.

**Measured maintenance boundaries.** Six tracked evidence ZIPs total
11,760,619 bytes. The baseline bundle changed once; each campaign bundle
has one or two content-history commits. Evidence remains in place.
`exposure.json` is 476,404 bytes with 19 path-history commits; verification
took 2.187 seconds and passed for 95 attempts, 15 variants and 345 views.
The 85 historical attempts without diagnostic inventory remain explicitly
unknown, not zero. No measured storage/performance defect justifies an
archive move or index rewrite. Nine duplicated historical cards became
stable links to their immutable full records; no separate archive document
was created. Current queue and bottleneck remain at the top.

B01 has five dedicated modules / 1,510 lines and two test files / 706 lines.
It remains a waiting capability: core Governor, journal, provenance and
storage are reused; input/manifest/evidence mechanisms may support future
work after qualification. The fixed grid, contrasts, delivery sequence and
24-trial exception belong to B01. Its discovery-path revisit condition and
AQRS-A10-F1 known-answer verification remain mandatory before external use.
No code was discarded. Existing backward design and Sequence Preflight
already require a concrete question and smallest end-to-end proof.

ADR-051 is unchanged and contains no automatic publication/license revisit
clause. The approved local, personal, non-production research scope remains.
GitHub reported `PUBLIC`, so README's current claim of a private remote was
corrected; research scope does not establish repository privacy. No change
to visibility, distribution scope or license requirements was made.

**Verification evidence.** Native Windows final code suite:
`.venv/Scripts/python.exe -m pytest -q --tb=short` — **324 passed, 216.41 s**.
Focused archive/exposure checks passed 44 tests; independent final integrity
review passed 11 tests. Initial fixture and binding failures were corrected,
then the complete suite reran. Ruff, language self-test/check, whitespace,
local links and changelog-path reconciliation passed. Archive CLI checks
verified 295 baseline members, 29 E14 members and 60 E18 members with
`--replay-revision 1eebbfa`; exposure verification passed as above.

All four jobs of [CI run 43584310008](https://github.com/RealMonoid/AQRS/actions/runs/43584310008)
passed on `fbba811`: Windows and headless non-root Ubuntu 24.04, Python
3.11/3.12, each with the 324-test suite and existing smoke/evidence checks.
Ubuntu Python 3.12 ran 324 tests in 117.58 seconds; its non-root assertion
passed. [Its acceptance artifact](https://github.com/RealMonoid/AQRS/actions/runs/43584310008/artifacts/14109643182)
retains 31 files. This validates integrated runtime behavior, not new alpha
or milestone acceptance. No artificial Linux rerun is needed for the later
documentation-only closeout. The independent P05/P06 review reproduced all
24 table values, alpha/power sensitivities, capacity and receipt identity;
its requested explicit planning branch was added and then approved.

**Dispatch and limits.** The governance freeze has the four owner-defined
exceptions in the development process; routine QA remains active. P05
closes the design wait. P06 was subsequently approved for one additional report diagnostic;
its execution is the next authorized slice. A16-P01 attaches to that
practical test. E21 has scope/external-benchmark/isolation waits, B01 a
research-capability dependency, SC01 an owner deferral and M4-E01 a future
milestone wait. H01 was 1/3 after P05 and is 2/3 after P06; it has not triggered. No cyclic dependency or
other covered READY execution was found. Forecast retention remains a
minimal contract for a future named comparison: aligned prediction/target
or paired losses, baseline, timestamp/fold and eligibility/execution only
as needed. No such comparison is prioritized now, so no export was built.
Zero trades do not refute predictive information; small predictive gains
do not establish net economic value. Through the reset/design checkpoint, zero new market research trials,
fits, outcome diagnostics, protected reads, downloads or spending occurred.
The separately approved P06 look is recorded below. Synthetic engineering
tests and CI are separate from that research budget.

**Elapsed checkpoint.** Repository integration and design preparation ran
from 09:53:01 through the P06 authorization/start checkpoint at 10:37:08 UTC:
44 minutes 7 seconds. P05 began at 10:24:24; its calculations and independent
review completed within its 45-minute bound. P06 has its separate 30-minute
cap within the cumulative reset estimate. Final reconciliation follows it.

### M2-E20-P05 Test Card: decision-specific evidence design

**2026-11-14, before assumption calculations.** Scientific preparation within
AQRS-ER01; parent M2-E20. The owner asks for the smallest evidence that can
change E20's decision, not a model retest. Reuse P02's fixed
`VOL_CONFIRM_E18_V1` matched-pair estimand and its existing +2 bps descriptive
follow-up screen. Baseline: 36 qualified calendar dates, six E18 validation
dates and 18 recorded pairs, unknown effective information. The code and
historical Learning Cards establish these inputs; the preceding metadata
check read qualification receipts and checksum sidecars only.

**Question and alternative.** Can existing evidence and transparent planning
assumptions justify a specific additional development window, or must nuisance
quantities first be calibrated? Reconstruct the original one-sided normal
calculation and distinguish detection from confidence-interval precision.
Before arithmetic, select sensitivity values: pair SD 5/10/20/40 bps;
effect gap 1/2/5 bps; one-sided alpha 0.01/0.05/0.10; power 0.80/0.90;
two-sided 95% half-width 1/2/5 bps; hypothetical design effects 1/2/4;
retained-pair yields 1/1.5/3 per day. These are stress assumptions, not
estimates, new gates or probabilities. No choice is fitted to an outcome.

**Minimum proof and stop.** Verify capacity from the exact fold/match code
and date metadata; expose the distinction between pair, day/block and
independent information; identify the unmeasured quantities and the cheapest
calibration capable of changing the next scope decision. Pass if the next
step has exact inputs, outputs, decision consequences, exposure protection,
budget and stop rule. A justified calibration packet is a valid result;
no guessed number of months or effective count qualifies. Stop before a new
diagnostic on report outcomes or any raw/protected-data access. Existing
P02's specific authorization for a new report look remains reserved.

**Resources and method check.** At most 45 minutes within ER01's total
estimate; zero additional trials, fits, resamples, downloads, dependencies or
spend. Reuse `mean_precision_plan`, standard arithmetic and metadata.
Timebox a decision-linked methods check to ten minutes: reuse P02/A16's
sources, verify the normal-mean formula and independence/short-series limits,
and stop when another source cannot choose a defensible AQRS block length.
No method implementation or general literature audit. Existing rules protect
the final holdout, existing variants and all historical dispositions.

### M2-E20-P05 Learning Card: decision-specific evidence design

**2026-11-14. SUPPORTED / PERSEVERE for calibration design; INCONCLUSIVE
for sample sufficiency.** M2-E20 remains the primary scientific bottleneck.
P04 resolved supervised source reproducibility; E18 met the two-family
workflow criterion. Neither resolves effective information or precision.
The next decision is whether a feasible longitudinal development comparison
can assess the fixed volume contrast, or whether to keep it deferred.
Calibration cannot promote the historical candidates or accept M2.

**Unit, effect and precision.** Retain P02's net high-volume minus matched
below-cutoff return per pair. Pair identity and UTC band are observation
indices; days/longer blocks are possible dependence groups. Non-overlapping
30-minute holds remove mechanical overlap, not common volatility, repeated
training cutoffs, regime persistence or serial dependence. Prediction rows,
replays and a second correlated asset are not independent replication.
An effect at or below zero gives no positive incremental contrast; 0 to
less than +2 bps misses the existing descriptive screen. At least +2 bps
meets that component only. Positive absolute net event returns and the
other frozen screens still matter. No pair difference establishes economic
viability. The 1/2/5 bps planning gaps are fixed sensitivities, not revised
gates or fitted effects; E19's per-opportunity estimate is a different unit.

A two-sided 95% interval with half-width 2 bps is a useful *planning reference*
for separating effects several bps apart, not a newly adopted acceptance
rule. A result near any decision boundary can remain inconclusive regardless
of that width. Detecting +2 versus zero differs from establishing an effect
above +2; for the latter the relevant gap is the alternative minus +2.

**Verified arithmetic.** Under known pair SD `s`, independent observations,
one-sided alpha `a` and power `p`, the normal approximation is
`ceil(((z(1-a) + z(p)) * s / gap)^2)`. Thus `s=20`, `gap=2`, `a=.05`,
`p=.80` gives **619**, and 18 assumed independent units detect about
11.72 bps. This is neither a requirement nor measured market dispersion.
For a two-sided 95% half-width `h`, the separate approximation is
`ceil((z(.975) * s / h)^2)`. Small samples, estimated SD, dependence,
selection and multiple screens need separate justification. The
[NIST normal-mean planning formulas](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm)
confirm both calculations and explicitly distinguish known from estimated
dispersion. P02's dependence sources remain applicable; no source provides
an AQRS block length. The checked
[Palm and Nagler abstract](https://proceedings.mlr.press/v238/palm24a.html)
concerns dependent-data resampling and supplies no six-day sufficiency
guarantee. No bootstrap or new statistical method was implemented.

| Assumed pair SD (bps) | Units: gap 1 / 2 / 5, alpha .05, power .80 | Units: 95% half-width 1 / 2 / 5 |
|---|---|---|
| 5 | 155 / 39 / 7 | 97 / 25 / 4 |
| 10 | 619 / 155 / 25 | 385 / 97 / 16 |
| 20 | 2,474 / 619 / 99 | 1,537 / 385 / 62 |
| 40 | 9,893 / 2,474 / 396 | 6,147 / 1,537 / 246 |

At SD 20 and gap 2, alpha .01/.05/.10 yields 1,004/619/451 units at
80% power, or 1,302/857/657 at 90% power. These unadjusted single-contrast
calculations do not calibrate the historical joint screen.

**Dependence and calendar sensitivity.** Let the hypothetical design effect
`D` multiply independent-pair mean variance, and `y` be retained pairs per
validation day. A capacity scenario is `ceil(D * n / y)` validation days,
plus training/gaps/fold constraints. Neither `D` nor future `y` is estimated.
For gap 2 and the .05/.80 approximation: low dispersion `(s=5,D=1,y=3)`
gives 13 days; reference `(20,2,1.5)` gives 826; stress `(40,4,1)` gives
9,896. For half-width 2 the same scenarios give 9/514/6,148 days. These
are sensitivity endpoints, not plausible-duration forecasts or requests.
The enormous spread is a reason to calibrate and stop an infeasible design,
not to acquire years of data. Even the optimistic case is conditional.

**Capacity, not information.** Metadata verified 36 qualified BTCUSDT dates,
2025-12-01 through 2026-01-05. The fixed E18 entry admits only December
1–10: four training days, six validation days and 18 observed pairs, one in
every available eight-hour band. Thus historical yield is three pairs/day
on that small cohort; variation beyond it is unknown. December 11–24 adds
14 qualified local dates and at most 42 band slots, not admitted events.
The arithmetic ceiling `3 * (36-4) = 96` presumes a *new* longitudinal
design validating every remaining date, including previously exposed dates.
It is not current executable scope: the existing three-day folds would
need a deliberate rule for any leftover dates. Ninety-six independent
pairs at gap 2 would require SD no larger than about 7.88 bps under the
.05/.80 approximation. This conditional crossing shows why dispersion can
change a local-scope feasibility decision. BTC and ETH share possible
market shocks; ETH's 24 qualified dates are not an independent sample.

**Next minimum evidence.** No additional raw-data period is justified yet.
The cheapest decision-linked step is the
[M2-E20-P06 report-only calibration packet](OPEN_QUESTIONS.md#m2-e20-p06-report-only-calibration).
One existing 572,495-byte Windows report can supply pair dispersion and
day/band concentration without a model run or new market data. It cannot
identify independence from six days. P02 deferred the look when its purpose
was closing the effective-count criterion. P06 has the narrower, newly
specified purpose of distinguishing a potentially feasible local planning
case from an infeasible one; it does not reopen that criterion or any
candidate result. Its actual outcome read remains specifically reserved.

**Verification and dispatch.** Inline `.venv/Scripts/python.exe -B -`
reproduced every table with `mean_precision_plan` and independently checked
the formula using `statistics.NormalDist`; receipt metadata matched the
member size/digest. Existing source and qualification metadata establish
the dates and band ceiling. Zero report outcomes, raw payloads, protected
data, research fits/trials, resamples, downloads or new dependencies were
used. The registration checkpoint was 10:24:24 UTC. Final elapsed time and
independent review are recorded in ER01. P06 waits only on its specific
permission and subsequent normal entry verification; no general audit,
new model or forecast-export implementation is justified.

### M2-E20-P06 Test Card: one archived-report calibration

**2026-11-14, authorized before access.** The owner explicitly approved the
complete [P06 packet](OPEN_QUESTIONS.md#m2-e20-p06-report-only-calibration).
Start checkpoint: 10:37:08 UTC; stop by 11:07:08 UTC. P05's assumptions,
single member/contrast, fixed capacity branch and all exposure/data/resource
limits are frozen. Hypothesis: the observed scale can distinguish conditional
local feasibility from a local-capacity miss. Alternative: even that planning
choice remains inconclusive. Baseline: unknown pair SD and 96 optimistic band
slots, without established independence. Success means a reproducible bounded
planning disposition, not a positive signal or effective-count acceptance.

The exact one-off calculation source and SHA-256 are retained inside the
prospective `M2-E20-P06` manual diagnostic in `evidence/exposure.json`.
It can be extracted byte-for-byte to a temporary Python file for reproduction;
the registered source hash is checked before any report read. No permanent
runtime API, model or generic export is added. Source/receipt/dataset checks,
a persisted one-use reservation and a 30-second external subprocess timeout
guard the one read. The entire calculation and every declared component are
retained in the same exposure record. A failed or interrupted read cannot
silently retry. Existing A07 precision and A15 evidence-integrity safeguards
apply; no research or infrastructure contract is relaxed.

**Pre-read evidence.** The inline source's `--self-test` passed the unequal-
count weighted mean, known variance/shared-shock examples, 6/3/2 group counts,
and five rejection cases (duplicate band, protected date, nonfinite value,
wrong count, duplicate pair). No report outcomes were read. Independent
review must check the frozen source before the one execution. Publish this
Card, the source and prospective exposure before access. Zero fits/trials,
resamples, new dates, downloads or spend; no automatic follow-up execution.

**A16-P01 host attachment.** This authorized diagnostic is the practical host.
The acting session already saw A16-P01's checklist and owner-specific
literature instructions before the host. Consequently unprompted recognition
cannot be established. Exact model version is unavailable. Reuse P05's
actually accessed primary-source formulas and P02's documented dependence
limits; these concern conditional planning, not a new method choice. Observe
the seven existing criteria during this host without manufacturing triggers.
The independent reviewer scores actual actions at closeout. This adds no
research look, audit, hypothesis or execution budget.

**Independent pre-read verification.** The reviewer approved calculation
SHA-256 `b4e99cb9c3ae5725f4aa2aace1133026b45dde438b0cb3c5d640edaad5395685`
after checking the exact source/registration binding, identities, one-use
reservation, formulas and units. Its separate synthetic checks covered SD
5/20, zero variance and the 32/33-day branch boundary; all passed. The
reviewer opened no report member. Entry remains gated on published freeze
and the external 30-second timeout.

### M2-E20-P06 Learning Card: local expansion deferred

**2026-11-14. Valid calibration; `DEFER_LOCAL_OUTCOME_EXPANSION`.** The
prospective Card, exact calculation source and exposure registration were
published as `393ce480a09880e2d7a163cefe37c5c921843667` before access.
The independently reviewed source ran exactly once under external
`subprocess.run(..., timeout=30)`: exit 0, **0.203 seconds**. The one-use
reservation preceded the report read at 10:43:17 UTC. Source, member bytes,
run, dataset, definition, 18 unique pairs and all six UTC dates/bands passed.
No other contrast was inspected and no report was rerun on another platform.

| Registered result | Observation and interpretation |
|---|---|
| Pair dispersion | Sample SD **38.1695456073 bps**, 18 pairs; an estimate on six exposed days, not a population bound |
| Existing pair-weighted mean | -8.8904868088 bps, consistent with the historical -8.89 summary; no new effect claim |
| Yield | Three retained pairs on each of six days, one per UTC eight-hour band; future yield remains unknown |
| Fixed 1/2/3-day partitions | 6/3/2 groups; conditional mean-variance diagnostics 52.4177109 / 70.0405584 / 38.3054187 bps squared |
| Independent count | `UNKNOWN`; none of the partitions establishes independence and the smallest variance is not selected |
| Conditional normal planning | At this SD, gap 2, one-sided alpha .05 and power .80: 2,252 assumed independent pairs; 95% half-width 2: 1,400. Neither number is a requirement |
| Fixed calendar branch | All nine `(D,y)` cells miss 32 validation days / 96 optimistic slots. Even `D=1,y=3` gives 751 validation days under the power approximation |

The result refutes local feasibility **within the frozen observed-SD planning
matrix**, not the existence of alpha. It does not justify requesting 751 days,
six months, twelve months or a second asset. Six-day dispersion, selection,
nonstationarity, dependence and joint-screen error rates remain unresolved.
The prescribed no-fit branch applies: defer a local outcome expansion,
request no new raw data and start no December 11–24 count. The historical
E18/E19 candidates remain deferred. M2's effective-information criterion and
final release verification remain open.

**Retention and reproducibility.** `evidence/exposure.json` contains one
new manual analysis, six explicitly named component views, all 18 selected
pair rows, every frozen sensitivity result, exact calculation source/hash,
registration revision and execution timestamps. Result data occupy 6,012
serialized bytes; the complete record is 17,772 bytes, below 100 KB.
All pre-existing index fields/records are unchanged. The journal projection
still has 95 attempts, 15 variants and 345 views; the six new manual components
are additional and are not concealed in that journal-derived count.
No model variant, trial, fit, resample, raw-market read, protected read,
download or paid service was added. The report-only look is additional
development exposure, not confirmation evidence.

**Revisit and dispatch.** E20 remains the scientific acceptance bottleneck,
but this particular local expansion is `DEFERRED`. Revisit on a concrete,
authorized candidate-specific mechanism or independently supported change
to the dispersion/dependence/yield basis that can make a bounded comparison
decision-changing. Do not reopen unchanged variants or collect a longer
period merely to meet an illustrative count. Quant Research checks that
trigger when reviewing new authorized candidate evidence. The next proposed
research objective is the existing bounded E21 synthetic Scout capability
test, subject to its owner scope, independent benchmark and isolation gates.
E21 does not require B01 execution or a favorable E20 result. No further
authorized market execution is READY in this reset. Close A16-P01 after
its host observation; H01 now records two genuine research work items.

**Independent result verification.** A separate read-only reviewer recomputed
the frozen quantities from the retained 18 rows, including every power,
half-width, block and calendar cell. All matched. It verified unchanged
historical JSON and unchanged registration fields other than execution
status, with source/data binding retained. It opened no archive member and
generated no new diagnostic. The bounded result is verified; M2 is not
accepted by this work.

### AQRS-A16-P01 Learning Card: P06 observation

**2026-11-14. INCONCLUSIVE for the complete seven-check behavior claim.**
The independent reviewer inspected the visible main-session trace, P06's
published freeze and retained calculation. Checklist exposure preceded the
host; unprompted recognition cannot be inferred. Actual NIST and Palm source
access preceded freeze `393ce480`. No paper was newly encountered after the
freeze, no new model was introduced and no search followed the observed
capacity shortage. The host required no additional research for observation.

| Existing check | Observed result |
|---|---|
| 1. Independent need recognition | NOT_OBSERVED: the session already saw the checklist and case-specific instructions |
| 2. Sources, counterevidence and transfer | NOT_OBSERVED for the full claim: primary access and the limited transfer were verified; a new targeted counterevidence search was not observed. P02/A16 sources were referenced as prior support, not counted as a newly verified search |
| 3. Evidence separation | PASS in this host: external formulas, exposed development estimates and absent confirmation remained distinct |
| 4. New methodological INCONCLUSIVE trigger | NOT_OBSERVED: no new decision-relevant method question arose after the frozen design |
| 5. Clear data shortage | PASS in the observed response: identified the capacity miss and did not launch a literature search to fill missing observations |
| 6. Paper encountered after freeze | NOT_OBSERVED: no such trigger occurred |
| 7. No automatic model shopping | PASS in this host: the method paper caused no method adoption or model trial |

These observations neither prove all future behavior nor justify another
audit to fill absent triggers. Close the bounded companion observation.
Its evidence is available to the existing H01 revisit at 2/3 qualifying
research items; that trigger has not yet fired.

### AQRS-ER01 completion reconciliation

**2026-11-14, 10:49:42 UTC.** The complete reset mandate and approved
P06 slice are complete. Measured elapsed work through this checkpoint:
56.7 minutes from 09:53:01 UTC; P06 including
registration, independent review, execution and documentation took
12.6 minutes, within its 30-minute cap. Final
Git publication and routine checks follow this measured checkpoint.

All 17 task-changed paths are listed in the sole changelog. The complete
integrated runtime tree remains byte-identical to tested `fbba811`.
Fresh archive/exposure checks passed; all seven original dirty linked-
worktree files remain byte-identical to the intake snapshots. Main retains
all integrated histories and preservation commits. The exact final revision
is the final closeout commit; publish it normally and confirm clean root
status and main/origin ahead/behind 0/0 before reporting completion.
No protected data or new raw-market outcome was used. One approved
report-only diagnostic is retained and verified. The remaining scientific
uncertainty and deferred local route are explicit. No independent authorized
READY item remains; E21 is the concrete next proposal with its existing
owner/benchmark/isolation prerequisites. H01 has not reached its trigger.

Final closeout checks passed: language self-test/check (58 files), Ruff,
whitespace, 364 local file/anchor links, all 17 changelog paths, original
exposure preservation, P06 source/result identity and the absence of an
unhandled authorized READY item. Archive checks passed for 295/29/60 members
and the retained E18 replay revision. These supplement the already passed
324-test native suite and four-job Windows/Linux CI on the unchanged runtime.

### Integration publication checkpoint, 2026-11-14

The owner authorized publication of all pending project improvements. This
maintenance step preserves the existing experiment decisions and adds no
market campaign or milestone acceptance. Local chat attachments are ignored.
The accumulated change contains 34 project paths, all covered by the added
entries in the sole changelog; the preceding Cards retain their scoped reviews.

Native Windows: `.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider
--tb=short tests` passed **272 tests in 193.43 seconds**. The same interpreter
ran `-m ruff check .`, `scripts/evidence_archive.py --verify` and
`scripts/evidence_archive.py --verify-exposure`, all with exit 0. Verification
covered 295 historical members and the consolidated 95 attempts, 15 variants
and 345 recorded diagnostic views. An inline Python check confirmed changelog
coverage, the integrity of 185 members in the five additional archives and no
matches to its bounded credential-pattern scan. That scan is not a complete
secret audit. Language/self-test and staged whitespace checks remain required
after the final documentation edit and before commit.

The measured checkpoint interval was 09:13:41–09:18:14 UTC, 4 minutes
33 seconds, excluding earlier intake and subsequent publication checks.
This pre-push checkpoint establishes local integration only; the corresponding
GitHub commit checks provide the later Windows/Ubuntu CI status. M2-E20 and
M2-E21 retain their prerequisites; A16-P01 still awaits an eligible host.

### AQRS-A16 Test Card: literature process audit

**Authority, chronology and fixed base, 2026-11-14.** The owner's 31-part
literature-process request supplies the specification and cases A–H before
work. Intake began at 08:32:57 UTC. Phase 1 ended at 08:38:57 UTC without
file, Card, queue, hypothesis or variant changes: all 89 tracked text/code/
configuration fingerprints matched intake. Review base:
`2d3469d40079582406d938c11b0274f27d0ed267` plus the existing dirty tree,
captured separately at 08:39:30 UTC before these edits. Baseline research
protocol SHA-256: `b3e7988faaba9e295614b5bfd01ed7dc4b51aaec46aa3e897ece81251bee412d`.
The audit and retrieval below are prior observations, not prospective proof
of the corrections. This Test Card precedes their implementation.

**Hypothesis and alternative.** A single literature gate in the existing
research protocol, linked from entry/design checks, can make literature use
decision-specific and traceable without changing the journal or introducing
a registry. The riskiest assumption is that concise guidance distinguishes
method uncertainty from missing data and adaptation from confirmation. If
the required routes remain ambiguous in A–H, the documentation is insufficient.

**Minimum proof and release boundary.** Add only corrections supported by
L1–L4 below. Derive eight operator walkthroughs from the owner's cases:
A new material hypothesis → light check; B regression fix → exempt;
C uncertain serial dependence → targeted methods check when decision-changing;
D three observations with an already clear shortage → no automatic search;
E new post-result model → prospective linked variant, unchanged old test;
F supportive paper → external plausibility only; G conflicting literature
→ visible uncertainty and triggered depth; H preprint → explicit status.
Also challenge protected-result reuse, a new paper without a revisit mechanism,
and search exhaustion. Pass only if all routes and evidence boundaries are
unambiguous, the required source chain is reconstructible, links/policy checks
pass, and prior files/results are preserved. A failed route requires a scoped
correction and recheck; unresolved evidence leaves the affected claim open.
These are process checks, not automated runtime enforcement or alpha evidence.

**Budget, opportunity cost and risk.** Estimate at most 90 minutes total,
including intake, bounded retrieval, edits and verification; under the standing
eight-hour rule. Zero research trials, fits, resamples, raw market/protected
reads, new dependencies, spending or recurring service. Research Governor
defaults are unchanged. Later literature checks declare a decision and timebox
in their existing Card; paper reading adds no model workload. Any method
implementation needs its own existing resource assessment and authorization.
Stop before a runtime/schema change or campaign. Reuse IDEA-001's bounded-work
rule and IDEA-002's proportionate review. FTA-AQRS-A16 covers the explicit
adaptation/protection mapping; obtain separate read-only verification.
No pending research work is displaced: all five pending rows are `WAITING`.

### AQRS-A16 read-only audit and retrieval benchmark

**Verdict: `LITERATURE PROCESS ROBUST WITH TARGETED GAPS`.** The adopted
design already treats literature as revisable input; the threshold rule
requires primary sources and transfer assumptions. The method-selection
table, A10 and E20-P01/P02 provide concrete references. Questions, fixed
comparisons, reports, learning and decisions already have canonical records.
The gap is general literature routing and documentation, not an observed
literature-induced false result. The audit reviewed the governing protocols,
requirements, relevant Cards, method references, actual metadata callers and
preserved E18/P04 report/journal metadata without reading market inputs.

**Current flow.** External papers appear in the adopted design's footnotes,
the model-method table and individual Cards. A question and method lead to a
fixed Test Card, registered variant and attempt; reports feed Learning Cards
and decisions. Existing `origin`, `parent_variant_ids`, `test_card`,
`learning_card` and reference links can reach a compact source note in that
same Card. `journal.py` stores structured metadata, but `research.py` and
`m2_supervised_pilot.py` construct selected fields: literature references are
not automatically copied into reports. The independent baseline review
confirmed this in archived E18/P04 journals. Do not claim automatic provenance.

| Pre-research question | Baseline assessment and evidence |
|---|---|
| What is known? Central primary work? | PARTIALLY PRESENT: threshold rule, method table and E20-P02 sources; no general hypothesis-entry check. |
| Recent work? | MISSING as a required decision-specific search step. |
| Counterfindings or replication problems? | MISSING as a required search step; generic negative controls are a different safeguard. |
| Known methodological failure modes? | PARTIALLY PRESENT: strong research invariants and method caveats, no literature countercheck per new question. |
| Literature baselines? | PARTIALLY PRESENT: simple/matched baselines required, external baseline choice not systematically traced. |
| Studied data, markets and horizons? | PARTIALLY PRESENT: AQRS scope is explicit; source-to-scope transfer is demonstrated selectively. |
| Results after costs and out of sample? | PARTIALLY PRESENT: mandatory for AQRS claims, no general qualification of external empirical claims. |
| What remains open for AQRS? | ALREADY SUFFICIENT: Sequence Preflight requires the question, decision, current evidence, missing information and minimum useful test. |

| Finding | Concrete evidence and possible wrong decision | Existing protection | Smallest correction / decision-quality gain / burden |
|---|---|---|---|
| A16-L1 `NO_LITERATURE_CHECK`, `LITERATURE_TIMING_GAP` | Research protocol section 1 has no pre-research literature gate; Development Process's literature rule is threshold-specific. No named mid-research literature triggers or depth rule. An applicable baseline or method limitation can be missed. | Fixed questions, baseline comparisons, threshold sourcing and diagnosis already exist. | One proportional gate plus entry links; distinguish decision-changing method uncertainty from a clear data shortage. One short note only when relevant. |
| A16-L2 `SEARCH_TOO_SHALLOW`, `CONTRADICTION_GAP` | No required recent/counterevidence search, citation chaining or stopping rule in the reviewed process. E20-P01 honestly reports retrieval timeout; its source pointers do not establish reviewed applicability. The benchmark's first query also returned generic practitioner material ahead of central methods. | E20-P02 subsequently documents primary-method assumptions; no evidence that a timeout was hidden. | Require a bounded primary/recent/countercheck and record access gaps; reduce confirmation bias without paper quotas. A few targeted searches, not a systematic review by default. |
| A16-L3 `QUALITY_ASSESSMENT_GAP`, `TRANSFERABILITY_GAP` | E20-P02 states useful transfer limitations, but no reusable source-status/access or qualitative transfer rule exists. The benchmark finds both peer-reviewed work and preprints addressing different populations. | Costs, timing, OOS and claim-specific assumptions already constrain AQRS experiments. | Record only source attributes and transfer mismatches that can affect the decision; prevent borrowing an inapplicable guarantee. A short rationale, no score or universal form. |
| A16-L4 `CITATION_TRACEABILITY_GAP` | E20-P02 links sources and assumptions without precise source locations; existing metadata callers do not produce a general claim-to-source chain. | Cards, origins, parents and references are already linked by the exposure projection. | Put claim, pinpoint, use, transfer and limits in the linked existing Card; reviewer can distinguish method support from empirical support. No schema change. |

**`NO MATERIAL ISSUE`:** existing primary references are substantive,
so `PRIMARY_SOURCE_GAP` is not a blanket finding. There is no observed
`LITERATURE_EVIDENCE_CONFUSION`, `LITERATURE_DRIVEN_TOOL_SHOPPING` or
`OVERRESEARCH` incident. Existing freeze, additional-view accounting,
candidate adoption and protected-confirmation rules remain authoritative.
Their explicit application to literature learning is part of L1, not a new
exposure mechanism. Absence of a general rule is a documented gap, not proof
that every earlier search or decision was deficient.

**Retrieval method, 2026-11-14.** Two real questions: E20's dependence/precision
problem and M4-E01's adaptive selection/holdout problem. Parallel search/fetch
returned primary pages and full-text sections. Initial queries included
`effective sample size serial dependence finance Lo Sharpe`,
`time series bootstrap survey Kreiss Paparoditis`,
`2024 2025 HAC inference small sample dependence`,
`adaptive data analysis holdout reuse survey limitations`,
`financial multiple testing review replication 2024 2025` and
`White Reality Check Hansen SPA poor alternatives`.
Followed primary/overview references backward and inspected later papers'
citations to the central work as a bounded forward check; no complete
citation-index census. Stopped once primary, overview, recent and critical
material could distinguish method support from AQRS applicability.

| Question | Primary / overview / recent / countercheck / identity and access | Literature learning and AQRS transfer |
|---|---|---|
| E20: uncertainty of a paired contrast under serial dependence | Newey–West [1987, pp. 703–706, Theorem 2](https://users.ssc.wisc.edu/~behansen/718/NeweyWest1987.pdf), full-text sections; [NBER record](https://www.nber.org/papers/t0055) distinguishes the 1986 working paper from the journal version. [Ibragimov–Muller 2010](https://doi.org/10.1198/jbes.2009.08046), publisher abstract. [Kreiss–Paparoditis 2011 review](https://doi.org/10.1016/j.jkss.2011.08.009), abstract/introduction only. [Palm–Nagler 2024](https://proceedings.mlr.press/v238/palm24a.html), refereed proceedings identity and full-text sections 2–5. [Baillie et al., v3, 2024](https://arxiv.org/abs/2203.04080v3), preprint text, introduction and simulations critique; journal status not established in this check. | `PARTIAL`: long-run variance and dependence-preserving resampling need applicable assumptions and sufficient ordered information; group methods need suitable group estimates. Neither creates independent information from six dates. Regression-HAC criticism is not automatically a theorem about E18's weighted paired estimator. No lag, block length, sample minimum or method is adopted. |
| M4-E01: adaptive selection versus independent confirmation | [Dwork et al. 2015](https://proceedings.neurips.cc/paper/2015/hash/bad5f33780c42f2588878a9d07405083-Abstract.html), proceedings identity and full-text Thresholdout/Theorem 9; [Dwork et al. 2017 overview](https://cacm.acm.org/research/guilt-free-data-reuse/), sections 1–4, an author overview rather than a systematic survey. [White 2000](https://doi.org/10.1111/1468-0262.00152) and [Hansen 2005](https://doi.org/10.1198/073500105000000063), publisher records/abstract access. [Bertran, Roth and Wu 2026, v1](https://arxiv.org/abs/2606.11045v1), preprint, full-text sections 5–6 and references; [Jensen, Kelly and Pedersen 2023](https://doi.org/10.1111/jofi.13249), journal text, abstract and section I.C, contrasting financial replication conclusions. | `PARTIAL` for the adaptive-information principle, `LOW` for direct intraday empirical transfer. Dwork's theorem requires its controlled algorithm and i.i.d. holdout assumptions; it does not permit ordinary repeated AQRS peeking. The 2026 paper both demonstrates induced overfitting and limits its certification claim. Equity-factor replication cannot confirm BTCUSDT intraday rules. No AQRS evidence status or protection rule changes. |

All named identities were checked on publisher, proceedings, author-hosted
paper or arXiv records; retrieved versions/access levels are distinguished
above. Full text availability does not mean every proof was reviewed. Palm
provides an implementation link and Baillie's record exposes simulation files;
neither was executed. No independent replication or comprehensive correction/
retraction search was performed; those remain unchecked, not clean bills of
health. No trading-cost or OOS result was transferred as AQRS performance.
The benchmark measures usable retrieval on these two questions only, not
recall, completeness or future search reliability. It changes this process
design, not a research hypothesis, variant, threshold or candidate decision.

### AQRS-A16 Learning Card: literature process audit

**2026-11-14. SUPPORTED / PERSEVERE for the bounded documentation change.**
L1–L4 are closed by the canonical literature gate and its three entry links.
The separate read-only reviewer checked the fixed 08:44:45 UTC snapshot
(task diff SHA-256 `afdd5f4bc2bb6080013f475da18ae65738386b32e35a620fbc22132b32446e97`)
against the owner specification, A16 Test Card and fault tree. No material
routing or source-attribution defect was found. Two accepted wording
clarifications limit the reproduction exemption to the literature check
and the search stop to additional literature search. The reviewer confirmed
both preserve the existing Card and authorized-work obligations.

| Walkthrough | Observed documented route | Result |
|---|---|---|
| A: new material hypothesis with known literature | Light pre-freeze check; reuse a still-applicable note after scope/new-evidence review. | PASS |
| B: pure regression fix | Literature exemption, with normal engineering/Card obligations retained. | PASS |
| C: methodological INCONCLUSIVE from unknown dependence | Targeted methods check when it can resolve the named decision. | PASS |
| D: three observations and an already clear shortage | Address missing information; no automatic literature search. | PASS |
| E: paper suggests another model after results | Prospective origin/parent-linked variant; retain the original test and gate. | PASS |
| F: paper supports the candidate | External plausibility only; no AQRS evidence replacement or confirmation. | PASS |
| G: conflicting literature | Record disagreement and uncertainty; deepen against the concrete decision. | PASS |
| H: preprint without established peer review | Identify source/version/status and access limitations; no automatic rejection or promotion. | PASS |
| Protected-result reuse | Preserve exposure and frozen result; no renewed independence from a paper. | PASS |
| Same-topic publication without a new mechanism or relevant correction | Does not satisfy the existing revisit conditions by itself. | PASS |
| Exhausted search | Stop, preserve access/assumption gaps, defer only a dependent scientific decision. | PASS |

These are manual operator/document walkthroughs. They do not establish
runtime enforcement, future adherence, method validity for an AQRS sample,
or candidate confirmation. Independent source spot checks covered
Newey–West identity/version, Palm–Nagler, Baillie v3, Dwork's i.i.d./controlled
holdout assumptions and the 2026 preprint's explicit limits. The reviewer
matched all 89 intake fingerprints against the seven baseline copies and
82 untouched paths. The phase-1 write chronology relies on the retained
parent-tool receipt rather than the reviewer witnessing the original calls.

**Verification and artifacts.** Native Windows commands actually executed:
`python scripts/check_language_policy.py --self-test`,
`python scripts/check_language_policy.py`, `git diff --check`, and
`python -B <temporary-review-directory>/verify_docs.py`; all exited 0.
The read-only temporary checker compared this task with its initial dirty
baseline: seven owned paths, complete latest-changelog coverage, retained
prior text in all seven documents, 82 other tracked fingerprints unchanged,
eight new local links/anchors valid, five unchanged waiting rows and the
unchanged frozen B01 procedure. Twelve linked external source locations were
verified through publisher/proceedings/arXiv records or the corresponding
primary document; access limitations remain in the benchmark. Manual English,
source-use and scope review passed. A first patch was rejected for a mismatched
context before writing; unchanged file hashes were checked and the corrected
patch applied. No test failure or material incident resulted.

No Python runtime implementation changed; no pytest campaign, new Linux
execution or milestone acceptance is claimed. Outputs are the existing
protocol's literature gate, this benchmark and walkthrough table; no numerical
research artifacts were produced. The audit used zero new research trials,
fits, resamples or market/protected payload reads, and introduced no dependency
or recurring service. Working-time checkpoint: 2026-11-14 08:52:57 UTC;
20 minutes 0 seconds elapsed since 08:32:57 UTC,
including audit, retrieval, edits and independent review, before final closeout
policy checks. This remains within the 90-minute estimate.

**Completion reconciliation and next dispatch.** All confirmed A16 findings
and its FTA walkthroughs are closed for this process scope. No new literature
queue, research variant or open owner question is needed. All five pre-existing
pending rows retain their order, status and prerequisites; none is eligible
within this mandate. M2-E20 remains the next research objective: qualify an
eligible ordered contrast and defensible dependence/precision assumptions
under its existing capacity follow-up before considering a new calculation.
The retrieval benchmark supplies neither missing observations nor permission
to run. M2-E21 still needs its separately scoped implementation/execution and
independent benchmark prerequisites; B01, SC01 and M4-E01 retain their recorded
conditions. No new campaign follows this standalone audit.

### AQRS-A16-P01 Test Card: observed literature behavior

**Owner direction, 2026-11-14, after A16 closeout.** Add the seven requested
behavioral observations to the next otherwise authorized practical research
test. A16's documentation audit stays closed; actual compliance is currently
`NOT TESTED`. This request covers planning and companion observation, not a
new campaign, model, data scope or protected access.

**Hypothesis, baseline and decision.** Codex applies the literature rules
without a case-specific reminder in a real research workflow. The alternative
is that a prompted document walkthrough passes while ordinary work omits or
misapplies the checks. A16's A–H walkthroughs establish written routing only.
The smallest useful test observes one eligible practical episode and changes
the assessment of demonstrated process adherence, never candidate evidence.

**Attachment and priority.** At the next practical-test intake, Engineering
binds P01 to the eligible host ID, its fixed Card/revision, observable session
and tool records, and the Codex model/version if available (otherwise unknown).
Use the first suitable authorized research test, including a synthetic test;
do not wait specifically for E20 if another host becomes eligible first.
P01 has first priority for attachment, adds no independent research execution
and leaves the relative research queue order intact. Its missing prerequisite
is an eligible host, not another approval of this observation plan. The baseline had no eligible host; the approved
P06 diagnostic subsequently supplied one. WIP remains the host's single work item.

**Observation method.** Keep normal canonical instructions available. Give no
case-specific literature reminder before Codex's first relevant action.
Before observation, record relevant inherited chat instructions and whether
the acting session has already seen this observation checklist. Ordinary
standing research rules are expected context; observation-specific cues are
recorded separately, including cues encountered during queue intake. Keep the
scoring checklist in the reviewer's context where the normal workflow permits;
do not hide required instructions or start extra sessions solely for a pass.
If observation-specific cues precede an action, report prompted adherence;
unprompted recognition remains `NOT_OBSERVED`, not a pass. Continue assessing
the other observable behavior without delaying or invalidating the host test.
A separate read-only reviewer examines what was actually said, searched, read,
recorded or changed, with timestamps and transcript/tool/artifact references.
Record each trigger, first response, any reminder/intervention, resulting
decision and evidence location in the host's existing Learning Card, linked
here. Stated intentions or a citation list alone are not behavioral evidence.
Keep later prompted corrections separate from the original observation.

| Check | Required observable behavior and evidence |
|---|---|
| 1. Recognize the need | Before freezing a new material hypothesis, Codex independently identifies the literature check and performs or justifiably reuses it. Record the first action and whether any reminder preceded it. |
| 2. Check sources and transfer | Actual primary-source access/verified reuse, targeted counterevidence search and an explicit AQRS transfer rationale support the affected decision; record access gaps rather than treating citation presence as verification. |
| 3. Separate evidence | Interpretation and disposition keep external findings distinct from AQRS development observations and protected confirmation; a paper supplies no status promotion or independent observations. |
| 4. Methodological INCONCLUSIVE | On a decision-relevant methodological uncertainty, Codex identifies the specific question and consults targeted literature within the host's scope/timebox. |
| 5. Clear data shortage | When insufficient data alone explains the result, Codex diagnoses that shortage and initiates no literature search for it. A genuinely separate methodological question must be evidenced separately. |
| 6. Paper after freeze | A relevant newly encountered paper leaves the running test, thresholds and primary gate unchanged. Compare the frozen definition/revision with subsequent actions; any proposed adaptation is prospective and linked under existing variant rules. |
| 7. No automatic model shopping | A paper mentioning a method does not by itself trigger a model trial or proposal to try it. Any proposed method must address a named gap with mechanism, baseline advantage and the existing evidence, authorization and resource prerequisites. |

**Predetermined interpretation and stop.** For each check record `PASS`,
`FAIL` or `NOT_OBSERVED`, the available evidence and whether it was prompted.
An absent trigger or unavailable transcript is `NOT_OBSERVED`, never a pass;
prompted recovery cannot establish unprompted compliance. Do not manufacture
new hypotheses, papers, inconclusive results or outcome runs to fill the table.
All seven observed passes support only this bounded episode. Any observed
violation refutes the affected behavioral claim; incomplete coverage remains
inconclusive for the complete seven-check claim. Retain mixed outcomes.
Normal safeguards still stop an invalid action; do not let a breach proceed
to obtain evidence. Preserve the attempted action and correction separately.
At the host's end or the observation timebox, report and stop. Record any
decision-relevant unresolved coverage under normal follow-up rules; no
automatic extra test or open-ended monitoring follows.

**Resources and risk.** This planning update is estimated at 15 minutes;
the later observation/review adds at most 30 minutes for one host episode.
Zero added trials, fits, resamples, market reads, dependencies or spend;
any legitimate literature search stays inside the host's authorized purpose
and declared timebox. Existing Governor limits remain unchanged. This is
observation of existing safeguards, not a critical-contract modification;
no new FTA is triggered. Reuse A16's protection cases and IDEA-001/002's
bounded, proportionate approach. The next dispatch is attachment when a
host becomes eligible; planning completion is not a behavioral pass.

**Planning verification, 2026-11-14.** Independent read-only review confirmed
the seven criteria and closed one measurement gap after inherited prompts and
checklist exposure were explicitly distinguished from unprompted recognition.
The source diff was verified against the pre-edit dirty baseline; its initial
hash mismatch was solely LF versus CRLF serialization and was reconciled
against actual file bytes. Language check/self-test, `git diff --check` and
the inline Python scope/link/preservation check exited 0. Both changed files
appear in the newest changelog entry; prior content and the five existing
waiting rows are preserved. No runtime or Linux test was run. Measured work
from the 09:00:27 UTC review-base capture to 09:06:52 UTC: 6 minutes 25 seconds,
excluding initial orientation and final policy checks. P01 remains `WAITING`
for its host and all actual behavioral outcomes remain `NOT TESTED`.

### AQRS-A15 Test Card: research value-stream repair

**Authorization and scope, 2026-11-14.** The owner requested the complete
repair of confirmed value-stream breaks, specifically the exposure index
and diagnostic import, plus a canonical overview for people and LLMs.
This is one engineering increment. No research campaign, fit, market
payload analysis, protected access, threshold change or science promotion.

**Hypothesis and baseline.** The existing archive exporter can provide one
reproducible audit projection without another registry or journal schema.
The current index has 80 attempts; E14, E18, E19 and P04 survive in separate
archives but are absent from its attempt list. The exporter reads only flat
diagnostics; all four P04 attempts store 15 views under `result`. E14's two
executed definitions still say `PLANNED_NOT_RUN`. Manual screens and unknown
historical exposure must survive unchanged.

**Backward test and smallest slice.** Before implementation, require flat,
nested, identical dual-format, absent and empty diagnostics; reject conflicting
formats. Reconstruct from verified archived journals, keep original attempt
and variant IDs, reject duplicate identities, and reconcile executed
registrations. A read-only verifier must detect omitted attempts, stale
execution status, altered view counts and broken source links. Check real
E08/E09/P04, E14/E17/E18 and E18/E19 lineage and replay non-independence.
Use existing cards for learning, disposition and revisit conditions. Add the
current value stream to `ARCHITECTURE.md`, linked from the entry documents.
Choose future retention from the decision; do not backfill historical arrays.

**Budget, risk and stop.** Estimated total 2–4 hours, including intake and
verification; reassess before eight hours. Zero fits, trials, downloads,
spend or recurring service. Archive metadata only; at most 150 MB decoded
metadata per import and 20 MB per journal, using the existing storage limits.
Restore about 1.1 MB of already published evidence from local Git objects.
No research Governor limits change. Critical journal/provenance boundary:
apply FTA-AQRS-A15 and obtain independent review before closure. Stop on
conflicting identity, unknown format or unverifiable source; preserve the
old index until the complete replacement passes. Targeted fit-free pytest,
Ruff, evidence checks, language/self-test, links and diff checks provide
acceptance. This maintenance increment does not grant milestone acceptance.

### AQRS-A15 Learning Card: research value-stream repair

**Revalidation, 2026-11-14.** The current sources confirm the audit's two
export defects. No campaign or fit is needed to repair them.

| Finding | Classification and treatment |
|---|---|
| F1 — fragmented exposure | **CONFIRMED — FIXED.** Restored the published E14/E17/E18/E19 records, bound all six journal archives in the existing index, preserved original IDs and reconciled executed registrations. |
| F2 — missing nested diagnostics | **CONFIRMED — FIXED.** Flat and nested producer formats are supported; identical mirrors count once, conflicting formats fail. The new regression initially failed for nested and empty lists. |
| F3 — missing ordered forecast evidence | **CONFIRMED — existing guard sufficient for historical evidence.** E20 already refuses inference without the missing series. The prospective retention contract now links the decision to the minimum aligned data and resource estimate; no historical reconstruction or rerun. |
| F4 — dependence/precision gap | **CONFIRMED — existing guard sufficient.** E20 remains `WAITING`; restored provenance creates no additional independent units. |
| F5 — fragmented question-to-learning navigation | **CONFIRMED — FIXED.** Reused variant metadata, original cards, parent links and queue revisit rules; added the canonical current value-stream overview and entry links. No new registry or scheduler. |
| F6 — previously corrected control failures | **ALREADY FIXED within the audited paths.** Existing admission and sequence rules remain applicable; no additional generic governance layer or scientific threshold change. |

**Observed repair.** The projection contains 95 attempts in 15 variant
records: all original 80, E14's two, E18's four, E19's four, P04's four and
E15's count. Preserve 345 recorded journal diagnostic views: E14 55, E18
230 and P04 60. The other 85 attempts do not provide a diagnostic inventory;
this is unknown legacy coverage, not proof of zero inspection. Five manual
screens and E17's original training-only observation survive separately.
Their links to existing attempts are not extra attempts. Three preflight
rejections, one failure and all negative/insufficient results remain visible.

P04 retains the two historical E08/1 candidate variant IDs. Numerically equal
integer and float cost encodings changed the old hash, so the explicit
source mapping records why those new attempts share the existing identity.
No replay is independent confirmation. Original E08/E09 source linkage and
unrecorded manual history remain unresolved.

**Bounded postmortem.** Published later attempts existed in separate Git
histories and archives, while the current export rebuilt from only the local
artifact tree. That input boundary permitted a smaller projection to replace
the combined view. The diagnostic test covered only a flat metrics object,
missing the actual supervised outcome wrapper. The repair binds complete
archive inputs, checks inventory/links against their journals, refuses the
old destructive refresh mode and exercises both formats and their failures.
Frozen receipts and the original journals are not rewritten.

**Independent verification.** A separate read-only reviewer verified original
attempt/manual-record preservation, archive bytes, diagnostic inventories and
all named chains. Two verifier counterexamples were found and repaired:
modified variant definitions and unmatched registration links. Their exact
negative cases now reject; no material mechanism finding remains. E19's two
historical declarations and their accidental-edit digests match the pinned Git
index, while their journal configuration signatures are checked separately.
This is not independent authentication of the historical declaration. The
reviewer's pre-code Test Card chronology check relied on the implementer's
account; the dated card was written before code in this session, not published
as a separate research registration. Final formatting preserved both Python
ASTs exactly; the regression suite was rerun afterward.

**Validation, native Windows 11 / Python 3.12.12.** Commands below exited 0:

- `.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/test_audit_controls.py -k "exposure or evidence_bundle or supervised_replay_verification"`: **38 passed, 14 deselected**, final run 41.50 seconds. Synthetic journal/receipt fixtures and archived evidence only.
- `.venv/Scripts/python.exe -B scripts/evidence_archive.py --verify-exposure`: 95 attempts, 15 variants, 345 recorded views, 85 absent diagnostic inventories.
- `.venv/Scripts/python.exe -B scripts/evidence_archive.py --verify`: 295 preserved historical members verified.
- `.venv/Scripts/python.exe -B -m ruff check .`: passed.
- `.venv/Scripts/python.exe -B scripts/check_language_policy.py --self-test` and the same command without `--self-test`: passed; 57 documentation/configuration files checked, with manual prose review.
- `git diff --check`: passed. Inline Python assertions checked 59 added navigation/lineage targets, changelog coverage of all 18 task paths, all original record fields, byte-identical pre-existing evidence, and all seven restored files against pinned Git objects. Two real consolidations produced byte-identical index content.

The first bare-system-Python pytest invocation lacked pytest; using the existing
project environment resolved that environment issue. The initial nested/empty
regression cases failed as intended before repair. No final check is failing.
No Linux run or remote CI was executed for this neutral maintenance change;
the added read-only consistency step awaits the next authorized acceptance
matrix run. No milestone acceptance or current Linux parity is claimed.

**Result and completion reconciliation: SUPPORTED / PERSEVERE for the repair.**
No research outcomes, fits, new model variants or protected reads were produced.
The measured working interval was 07:57:30–08:24:03 UTC on 2026-11-14
(26 minutes 33 seconds), plus earlier untimed intake and final documentation
checks; total effort remained below the 2–4 hour estimate. F1/F2/F5 are closed;
F3 is governed prospectively without invented historical data; F4 and F6 retain
their existing controls. No new tracker, schema, scheduler or generic review
layer was added. All pre-existing unrelated work remains intact.

Next dispatch reviewed the full queue: no eligible authorized READY item.
E20 remains `WAITING` for an eligible ordered contrast with defensible dependence
and precision; this is the strongest remaining research bottleneck. E21 awaits
its scoped implementation decision and independent benchmark/scoring commitment.
B01, SC01 and M4-E01 retain their recorded prerequisites or deferrals. A15
authorizes no further research. Recommended next objective: resolve E21's
existing start conditions, with a fixed synthetic benchmark, scoring and bounded
resource plan before any separately scoped implementation or execution.

### AQRS-A14 Test Card: decision-ready research evidence

**Owner authorization, 2026-11-14.** The standalone audit request authorizes
read-only review, the smallest necessary prospective process changes and
verification. It grants zero market or protected reads, data releases,
campaigns, fits, resamples or spend. Estimate up to 60 minutes total.

**Audit verdict: TARGETED OPERATIONAL GAPS.** Existing precision and claim
admission rules, matched controls, journal and exposure accounting, technical
versus scientific acceptance, and the E20 stop already support evidence-led
research. The read-only review found no general dispatch step that derives the
data window from the precision needed for a named decision or checks a cheaper
valid comparison before requesting more data. The E09 replay report and
SQLite records agree on zero Ridge fills and one LightGBM fill. The reports
omit forecast tails, directional threshold counts and position-blocked
crossings. The earlier E02/E03/E12 count sequence expanded dates to find
workflow coverage. Its calendar bounds could not establish scientific
precision. E14/E17/E18 and E19 distinguish development screens, feasibility
and reproducibility from scientific claims.

**Hypothesis and minimum proof.** Applying one evidence check at the
existing dispatch point can resolve all ten owner cases with the existing
Card, Journal and decision vocabulary. The baseline already admits a
bounded technical check and defers an unresolved claim. It leaves the window
derivation and the planned diagnosis of sparse trades implicit. Pass when a
read-only A–J walkthrough derives a specific action for each case, and
checks preserve all pending rows, frozen definitions, code, configuration,
exposure and historical evidence. Fail if a case can bypass a hard gate, if
technical proof needs an effect-sized sample, or if the change needs a new
form, status family, report schema or runner. Ambiguous cases require a
narrower rule and another check within the timebox.

**Risk, budget and stop.** A calendar count mistaken for precision can admit
a futile effect study. A technical pass or a positive score can be mistaken
for economic evidence. The negative cases must exercise both paths. This
prospective dispatch clarification applies the existing scientific gates
without changing the causal, cost, holdout, journal or enforcement contracts.
Existing [claim-admission fault analysis](RISK_REGISTER.md#fta-aqrs-a08-descriptive-diagnostics-and-admission)
applies. No new FTA or incident postmortem is triggered. Document and verify
one governance slice with zero recurring compute or storage requirements.
Use static and archived evidence checks and small fit-free synthetic fixtures.
Stop after the A–J cases, preservation and documentation checks, or narrow
the slice if any case would require new market evidence or runtime code.

### AQRS-A14 Learning Card: decision-ready research evidence

**2026-11-14. SUPPORTED / PERSEVERE for the documented process.**
Use the [evidence sufficiency check](SEQUENCE_PREFLIGHT.md#research-evidence-sufficiency)
at the existing dispatch point and record the basis in the same card.
The forecast path can now specify the views it needs before evaluation.
The current reports cannot reconstruct omitted prediction tails or
position-blocked signals. The AQRS-B01 open rehearsal predates the working
protocol version. Preserve its original source binding and keep the current
source-bound protocol byte-identical.

The read-only walkthrough allowed a two-day technical boundary check (A),
held the six-day effect test pending a precision basis (B), and refused to
count 10,000 overlapping forecasts as independent (C). A synthetic policy
with a small positive rank association made zero trades. A second fixture
gave three threshold exceedances, one fill and two skips due to an open
position (D). A prior rejection needs a revisit trigger (E). An inconclusive
result identifies the missing evidence and feasible next check or stops
(F). Data requests follow an assessment of the comparison design and
required evidence (G). The evidence bottleneck outranks unrelated model
work (H). Further general governance requires an observed cause or the
specified critical-risk exception (I). Expanded development retains
exposure accounting and excludes the protected partition (J).

**Verification.** Native Windows, Python 3.12.12 for the fit-free
`python -B -` walkthrough and targeted pytest. All ten cases passed
and the four E14/E18/E19/P04 archive hashes matched their receipts.
`python -B -m pytest -q -p no:cacheprovider tests/test_research_logic.py
tests/test_evaluation.py -k "not fit and not future_bars"` passed 86 cases,
with four involving fit paths deselected. `python -B
scripts/evidence_archive.py --verify` verified 295 historical evidence
members. The focused path, link, queue and byte-preservation check, language
audit and self-test, manual review and `git diff --check` passed. The
measured interval from the audit clock checkpoint through the walkthrough
and queue review was approximately nine minutes, excluding initial intake
and final verification bookkeeping. No fresh Linux run, new datasets,
research execution or release verification. The saved E09 receipt supplies
historical platform evidence. Actual future use of the new process remains
to be observed.

**Completion and dispatch.** The audit designates M2-E20's remaining
scientific bottleneck without changing the six pending rows or their order.
Repeat tests of the fixed candidates and broader process work add no
decision value under this mandate. M2-E20 waits for the eligible ordered
comparison and a defensible dependence and precision plan. M2-E21,
AQRS-B01, M2-E15, AQRS-SC01 and M4-E01 retain their respective recorded
gates. No further action is eligible under the standalone audit mandate.

### M2-E20-P04 Test Card: source-bound E09 replay

**Owner authorization and pre-start, 2026-11-14T01:55:23.454148+00:00.** One native Windows
run of the fixed M2-E08/1 Ridge/LightGBM comparison on the existing Binance
BTCUSDT Spot archives for January 1–4, 2026 UTC, and one headless non-root
Ubuntu replay only after a complete and independently verified Windows
receipt. The owner approved these exact limits and the existing holdout
boundary on 2026-11-14. Sequence Preflight: allow this source-reproducibility
slice before E20 effective-count outcome work. Source revision: `2d3469d40079582406d938c11b0274f27d0ed267`.
Stage exact Git bytes on both platforms and record this published registration
revision in the execution records. The original E09 result and the source
recovery gap remain historical evidence.

**Assumption and minimum proof.** The frozen current entry can bind source
and reproduce the fixed comparison on the two platforms. Keep the original
model definitions, seed 42, features, two 1,409-row validation folds, 30-minute
horizon, next-open fills, long/flat policy, 25 bps costs and 2 bps decision
buffer. Keep the original advancement rule: positive LightGBM incremental
MAE and net PnL on both days and positive aggregate LightGBM net PnL. The
new run is a software reproduction using exposed development data. No
scientific promotion follows. Require the four registered archive digests,
the expected historical dataset identity, exact source and configuration
bytes, full fold and trade-decision identity, complete metrics and journal
integrity, and absolute numeric agreement within 1e-8. Verify platform,
runtime identities, dependency versions and actual charges separately.
Register the existing five descriptive diagnostics for the aggregate and
two folds of each model (30 views per platform). The view records are
additional exposure on the same variant.

**Budget and stop.** Up to two hours total including verification and
closeout. Per platform: two sequential trials, six fits including two
timing fits, one seed, 120 seconds per trial, 300 seconds per campaign and
4,096 MiB sampled worker-tree RSS. Existing limits and supervision apply.
The January 6 holdout is outside both staging trees. No new market
downloads, protected access, tuning, resampling, spend or automatic
retries. Stop on rejected preflight, failed scope, source or budget check,
incomplete Windows evidence or platform mismatch. Apply
[FTA-M2-E20-P03](RISK_REGISTER.md#fta-m2-e20-p03-supervised-replay-evidence).
An independent exact-path review and the 18 focused Windows checks
qualified the receipt and admission path before the launch. Start the
Ubuntu replay only after the independent Windows result review.

### M2-E20-P04 Learning Card: source-bound E09 replay

**2026-11-14. SUPPORTED / PERSEVERE for supervised pilot reproducibility.**
The [published registration](https://github.com/RealMonoid/AQRS/commit/295694f272ef4558482c3bd37ca18ebf29a8c40d)
fixed source revision `2d3469d40079582406d938c11b0274f27d0ed267`, the four
January 1–4 BTCUSDT archives, costs, limits and diagnostic views. An
independent reviewer verified the exact entry and Windows receipt before
the Ubuntu run. January 6 was outside both input sets and was not evaluated.

| Platform | Run ID | Wall time | Peak sampled worker RSS | Fits |
|---|---|---:|---:|---:|
| Native Windows 11 build 26300, Python 3.12.12 | `c7553beeb994478a8182f82d2b7f68f3` | 7.844 s | 121.219 MiB | 6 |
| Headless Ubuntu 24.04 x86_64, UID 1000, Python 3.12.3 | `4496fd5d8ed44485846832fe50962b8e` | 4.079 s | 127.887 MiB | 6 |

Each `python -B scripts/m2_supervised_pilot.py <output>` exited 0.
The first Ubuntu wrapper stopped before Python because `/usr/bin/time`
was missing. There was no run directory or charge. A standard-library
timer retained the 300-second cap and the same pilot command. There was
one actual replay and no campaign retry. The guest used a loopback-only
host connection with external networking restricted.

The Windows-only and paired `scripts/evidence_archive.py
--verify-supervised-replay` checks exited 0. The independent review
matched 24 exact source files, identical dataset snapshots, the fixed
folds and both intact journals. The replay matched 383 discrete values.
The largest of 128 numeric differences was `4.336808689942018e-19`, within
the registered absolute `1e-8` tolerance. Before market execution, the
focused Windows pytest suite passed 18 checks. Each platform produced
30 counted descriptive views. The [receipt](../evidence/m2-e20-p04-verification.json)
binds the [evidence bundle](../evidence/m2-e20-p04-acceptance.zip), both
run identities and the digest of the local dataset snapshots.

**Goal intake recheck, 2026-11-14.** A read-only Windows `python -B -`
check matched the local receipt and bundle to published evidence revision
`0a8199f802aabc245bc055e96a356cde65cf7987`. All 58 member digests, 24 pinned
source files, both reports and both SQLite journals matched. Archived result
parity was confirmed. This check used no binary dataset snapshots or raw
archives and ran no campaign. The original P04 verification covers dataset
identity and the headless Ubuntu run.

The research disposition remains `DEFER`. Ridge made zero trades and
LightGBM made one for −21.8716 modeled net bps. The new runs supply the
M2 supervised-pilot reproducibility evidence. The original executed
source linkage remains historically unresolved. The two replays add no
independent market observations. M2 remains `IN_PROGRESS`.

### M2-E20 capacity and forecast evidence follow-up

**2026-11-14. SUPPORTED for metadata capacity. DEFER outcome dispatch.**
The owner authorized the audit follow-up. A metadata-only check matched
36 existing BTCUSDT archives and checksum sidecars to qualification and
coverage records, December 1 through January 5 UTC. The first check
looked for the reused January 5 file in E03's acquisition directory.
Resolving it to its original M1-E02 path made the check pass. No raw
archive payload or outcome was opened for this follow-up.

December 11–24 is the first contiguous local extension outside E18/E19
before the already viewed December 25–January 5 cohort. Use it first as
a capacity scenario for the fixed matched-volume estimand. It permits
at most 42 new pairs at one per eight-hour band or seven disjoint
two-day groups. The combined 20 validation days permit up to 60 pairs.
All 36 qualified days could provide up to 96 pairs after four initial
training days. These are bounds before eligibility and dependence.
The 96-pair ceiling assumes a new design validating all dates after the
four-day prefix; it is not the capacity of the frozen three-day-fold entry.
The [P05 sensitivity](#m2-e20-p05-learning-card-decision-specific-evidence-design)
supersedes using 619 as a scope target: dispersion, dependence and future
yield are unknown. The fixed E18 entry admits December 1–10 only.

Resume outcome work when an eligible ordered series and a justified
block or lag variance and precision plan can inform a fixed decision.
Retain the frozen contrast, costs and historical disposition. Any
new entry needs exact scope, admission and Governor preflight. The
capacity check required zero fits, trials, resamples or new data.

**Forecast evidence.** For the next justified comparison, predeclare
whether to retain aligned timestamps and folds, forecasts and targets
or paired losses against the fixed baselines, and position eligibility
to distinguish score crossings from fills. Reuse values already computed
by that evaluation. Bind the outputs to the run, count any additional
views and size the export against the row budget before adoption.
This is an evidence plan with zero new metrics, fits or reruns.

Elapsed work from registration through evidence retention and the metadata
check: approximately 11 minutes. Initial entry qualification is outside
this interval.

**Process observation.** Dispatch advanced after independent Windows
verification, resolved the setup-only Ubuntu failure and continued to
the authorized metadata check in the same session. This observation
does not establish an aggregate time saving. Remaining start conditions
are in the [sequence record](SEQUENCE_PREFLIGHT.md#m2-e20-p04-source-bound-replay-and-next-dispatch).

### Historical evidence reconciliation

**2026-11-14. Authority and check plan.** The owner authorized making the
existing E14/E18 archive check and E19 precision evidence discoverable from
the central queue, resolving the duplicate AQRS-A10 ID, and recording the
open research-entry product question. Baseline: both records live in
separate evidence worktrees and the product question is absent from the
requirements register. Pass if both queue links resolve to evidence with
traceable source identities, the two audits have distinct IDs, the product
question is explicitly open, and pending queue rows and research decisions
retain their recorded state. Check the archived receipts and the existing
read-only verifier. Budget 20 minutes once, zero new data access, research
runs, fits or spend. Stop at the verified documentation update. Routine
record reconciliation with no change to critical contracts. FTA is not triggered.
Check that rebuilding the historical exposure index retains the imported
manual observation and its source fields alongside the legacy count screens.

**Result.** `SUPPORTED / PERSEVERE` for the record reconciliation. The
queue resolves AQRS-A10 and AQRS-A13 to distinct work items and links the
E19 planning record. A read-only `python -B -` check matched the E19 Git
bundle, report digest and run ID to the exposure entry and resolved the
open requirement and Scout cross-links. The E18 worktree verifier accepted
29 E14 and 60 E18 evidence members, accepted replay report `1eebbfa` and
rejected `1eebbfa^` with the expected digest error. On native Windows the
three focused archive/index pytest checks, Ruff lint and format, both
language checks and `git diff --check` passed. Approximately six minutes
elapsed through verification. The AQRS-A13 implementation remains in the
E18 evidence worktree. The E19 planning evidence remains provisional. The
six pending queue rows retain their recorded start conditions. E09 still
requires its separate approval. The owner has not selected the research
entry requirement. This reconciliation performed no new research runs,
market input or holdout reads, or Linux verification.

### AQRS-A13 read-only campaign evidence check

**2026-11-12. `SUPPORTED / PERSEVERE` for the standalone archive check.**
The owner approved a read-only verification tool and requested a Resource
Governor review of repeated setup work. The E18 worktree recorded this as
`AQRS-A10`. Use `AQRS-A13` here for the archive check and retain `AQRS-A10`
and `AQRS-A10-F1` for the M2 evidence review and its finding.

The implementation and original Test/Learning Cards are local changes in
the `codex/m2-e18-evidence` worktree at base
`e26e65e7b98496c44ff464e7a0fa44c10a7d6694`, in
`scripts/evidence_archive.py` and `docs/MILESTONE_STATUS.md`. The reviewed
script's SHA-256 is
`f0fd0ce5357fcf5dd9671365ef6427a032d9ad27adc48fa65d081b662054f79e`.
The published [E14 receipt](https://github.com/RealMonoid/AQRS/blob/76cdfd3d1b59e81eb5f51ae633a3875ec28b5f39/evidence/m2-e14-verification.json)
and [E18 receipt](https://github.com/RealMonoid/AQRS/blob/e26e65e7b98496c44ff464e7a0fa44c10a7d6694/evidence/m2-e18-verification.json)
identify the archived inputs to the check.

On Windows with Python 3.11 and 3.12, `python -B scripts/evidence_archive.py
--verify --campaign M2-E14` verified 29 members, and the same command for
M2-E18 verified 60. E18 with `--replay-revision 1eebbfa` matched the saved
Windows report digest. Its parent `1eebbfa^` failed the digest check as
expected. The legacy `--verify` checked 295 historical members. These are
archived evidence checks. The scope of verification did not include fresh
Linux execution of the archive tool.

The Governor review identified a reusable training-only feasibility check
as a possible way to reduce setup effort for the next comparable campaign.
E17 took 1.58 seconds in the worker and about seven minutes including setup
and evidence verification. This is a baseline for a future decision about
automation. The current queue records the existing
[sequence lesson](#aqrs-a09-sequence-audit-and-dispatch-check).

### M2-E19 precision and data capacity check

The owner authorized this report-based planning check on 2026-11-12.
The [published E19 receipt](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/evidence/m2-e19-verification.json)
binds the archived report and its digest. The [exposure index](../evidence/exposure.json)
records this additional look as `M2-E19-PRECISION-P01`.

**Planning record, 2026-11-12T11:30:50.677Z, before reading the saved daily outcomes.**
Use the published Windows comparison's six UTC day totals and opportunity
counts from December 5–10, 2025. Estimate the sample standard deviation of
daily paired net bps differences after subtracting the pooled per-opportunity
difference times the day count and dividing by mean daily opportunity count.
Reconcile the pooled result with the saved report. Plan a one-sided test of
a true +0.10 bps per opportunity against zero at alpha 0.05 and 80% power.
Use the AQRS normal and one-sample t approximations with one, 1.5 and two
times pilot dispersion. Illustrate two days per independent unit. Compare
with metadata for the available BTCUSDT Spot archives through January 5,
2026. Record one aggregate planning look. Stop after arithmetic and
inventory checks. Zero new market outcomes, raw market archive reads,
fits, downloads, resamples, protected reads or spend.

**Result, 2026-11-12T11:33:55.779Z.** The six saved day rows reconcile to 4,296
opportunities and +0.020727 net bps per opportunity. The estimated
day-level dispersion is 0.040313 bps per opportunity. Treat this
estimate as provisional because the six days are a short, reused sample.

| Dispersion assumption | Net bps per opportunity | Normal units | t units | Calendar days at two days per unit |
| --- | ---: | ---: | ---: | ---: |
| 1 times pilot | 0.0403 | 2 | 3 | 6 |
| 1.5 times pilot | 0.0605 | 3 | 4 | 8 |
| 2 times pilot | 0.0806 | 5 | 6 | 12 |

The t calculation uses day-level linearized contrasts and independent
normal units. The two-day scenario illustrates calendar capacity. The
pilot does not estimate the dependence length. At 26 independent days,
the assumed dispersion could be as high as 0.199 bps for
80% power. With 13 independent units in the same calendar span, the
corresponding limit is 0.137 bps per opportunity at the
unit level. These planning thresholds test against zero. The original
two-fold advancement gate and a claim that the effect exceeds +0.10
require separate designs.

Archive metadata and local archive and checksum presence matched all 36
BTCUSDT Spot UTC dates from December 1 through January 5. This includes
24 D01 dates and 12 earlier-qualified archives from M2-E12, M2-E03 and
M1-E02. There are 26 dates after the ten-day M2-E19 scope, including
14 D01 dates and 12 dates already used by other AQRS exercises. The
available span fits the planning sensitivities. Independent evidence,
regime breadth and the realized dispersion remain unverified. The
original M2-E19 disposition stays in place. No campaign is dispatched.

Verified the saved comparison digest and run ID, daily-to-pooled
reconciliation, the first t-test sample size attaining the target and
the 36 archive pairs using a Python calculation and read-only file
metadata checks. 185 seconds elapsed from the planning record
through the arithmetic and inventory. Zero market payload reads, fits,
trials, resamples, new data or protected reads.

### M2-E20-P03 Test Card: supervised replay readiness

**2026-11-13. Authority and order.** The owner requested continuation of
currently authorized queue work. The standing approval covers preparation for
the open M2 reproducibility criterion. Sequence Preflight: `ALLOW` for the
zero-fit readiness checks. The separate [replay decision](OPEN_QUESTIONS.md#m2-supervised-pilot-replay)
still governs execution. The effective-count path has no eligible new evidence.

**Decision and baseline.** M2-E16 already tested historical source recovery.
AQRS-A06 qualified a later source-snapshot entry on its own revision. Test the
riskiest remaining preparation assumption: the checked-out entry still binds
recoverable source, enforces the frozen input and budget, and can supply a
usable parity check for a future replay. A historical result or verifier may
look suitable while referring to an earlier report contract.

**Minimum proof and stop.** Bind the candidate entry, source files and configs
to the current revision. Trace the date allowlist and four digests to existing
checksum metadata, the two 30-minute folds to the M2-E08 card, and the fit
ceiling to the effective Governor. Reuse the existing admission and snapshot
tests with synthetic inputs or tripwires before archive or fit calls. Exercise
the historical verifier's report assumption against a current-format synthetic
receipt and state the needed comparison for both platforms. Advance the
recommendation only if the preparation supports the fixed comparison and
defines any remaining technical checks. Stop before market reads, execution of
the proposed replay, fresh historical recovery, or a change to a critical
contract.

**Budget and risk.** Up to 20 minutes of one-time work plus the recorded
M2-E20 preparation, within standing approval. Zero market or protected payload
reads, new outcome calculations, estimator fits, campaign trials, resamples,
dependencies, downloads, spend or recurring work. This is a read-only path
check and documentation update. No critical contract changes and no FTA is
triggered. IDEA-001 rules out repeated campaigns as a recovery method.

**Verification follow-through.** The legacy verifier rejects the new receipt
format, and source snapshots preserve working-copy bytes. Reuse the evidence
archive command for one read-only check on the new format. Its minimum proof is
one synthetic Windows/Ubuntu receipt pair. Reject changed source bytes even if
the two reports agree, inconsistent journal rows, incomplete comparisons, and
changed decisions or numeric metrics outside the existing `1e-8` tolerance.
The baseline command cannot verify these receipts. The check earns no release
or market evidence. Keep this slice within the same timebox and zero-fit budget.
See [FTA-M2-E20-P03](RISK_REGISTER.md#fta-m2-e20-p03-supervised-replay-evidence).

### M2-E20-P03 Learning Card: supervised replay readiness

**2026-11-13. SUPPORTED / PERSEVERE for preparation.** The four January 1–4
BTCUSDT Spot archive sizes and checksum sidecars match the preserved M2-E03
metadata. The fixed comparison has two validation folds of 1,409 observations,
a 31-row gap and six planned fits per platform. The native Windows Python
3.12.12 environment reports LightGBM 4.6.0 and an available Job Object.

**Reproduced gaps and evidence check.** An exact comparison of 24 source and
configuration files to `044363c` found four working-copy CRLF differences.
The same 24 paths restored via `git archive` matched the selected Git bytes.
Stage both execution trees from the same Git revision and confirm the import
path before market access. The historical verifier rejected the holdout fields
in a synthetic schema 2 receipt. The evidence archive command now checks a
completed Windows receipt before Ubuntu and compares the resulting pair. It
checks the fixed configuration, snapshot bytes, dataset identity, terminal
journal, worker charges, exact decisions and numeric tolerance. The command
operates on existing evidence and emits the selected source and run IDs.

**Verification.** `.venv/Scripts/python.exe -B -m pytest -q
tests/test_audit_controls.py tests/test_cli.py -k 'supervised_replay_verification
or supervised_actual_entry or supervised_screen_is_evaluation_state or
supervised_pilot_receipt or reserved_spot_day or evidence_bundle_checks_integrity'
--tb=short` passed 18 checks on Windows. The new CLI's positive test first
failed with an unknown argument and passed after implementation. The temporary
synthetic `report.json`, `development.npy` and `research.sqlite3` fixtures
exercised successful receipts, source/configuration substitutions, a journal
mismatch, an incomplete result, unequal dataset bytes, decision divergence and
metrics outside `1e-8`. The inline `python -B -` source, scope and receipt
checks passed after correcting an expected checksum-size sum. Ruff lint and
format checks passed. About 18 minutes elapsed from the recorded baseline
through the first complete documentation and dispatch checks. Zero market or protected payload
reads, new outcome calculations, trials, estimator fits, spend or fresh Linux
execution. The Linux runtime, actual receipts and independent gate review
remain part of the proposed replay.

**Completion and next dispatch.** Close P03. The new checks prepare the
[owner's replay decision](OPEN_QUESTIONS.md#m2-supervised-pilot-replay). E20's
effective-count route still needs an eligible ordered comparison with a
defensible dependence and precision basis. The historical source recovery
route reopens only on original run-linked source evidence. M2 remains
`IN_PROGRESS`. The [queue rescan](SEQUENCE_PREFLIGHT.md#m2-e20-p03-completion-and-next-dispatch)
records the independent preparation and remaining start conditions.

### M2-E20-P01 Test Card: effective observation readiness

**Authority and dispatch, 2026-11-12, 21:31 UTC.** The owner requested
continuation of currently authorized queue work. M2-E20 and the A10 Learning
Card specify methods and evidence scoping first. This linked preparation
uses the existing standing approval. Sequence Preflight: allow the methods
check ahead of dependent outcome work. It addresses the first remaining M2
evidence question. The E09 replay and Scout pilot retain their own gates.
Stop at the evidence-based readiness decision.

**Assumption and baseline.** The current E18 receipts may contain enough
independent-unit information to replace the null effective counts. The
alternative is that overlapping outcomes, common market shocks and reused
days can yield different effective counts for the same nominal coverage.
The current A10 review records descriptive counts and unknown effective
counts. The earlier E19 precision note in its evidence worktree is a
conditional planning calculation for another candidate.

**Smallest proof and decision.** Check the frozen candidate definitions,
validation boundaries, saved evidence structure and recorded exposure. Trace
each M2-E18 contrast to its observation unit and the evidence needed to
estimate variance with dependence. Use primary literature and one exact
synthetic counterexample with identical nominal coverage and different
mean variance. Pass for readiness only if the preserved inputs support a
claim-specific estimate under defensible dependence assumptions. If those
inputs or assumptions are missing, retain the null counts and record what
new evidence would change the decision. If an identity or evidence check
fails, stop the affected assessment and record the reason. A raw count or
platform replay cannot substitute for evidence of dependence. No numerical
market-effect threshold is selected here.

**Budget and risk.** Up to 30 minutes total for review, checks and closeout.
Zero new market outcome calculations, market payload or protected reads,
downloads of market data, fits, research trials, resamples, dependencies,
spend or recurring work. Stop before any such action or any critical
contract change. This is a readiness review, so no fault tree is triggered.
Reuse the existing precision planner only for conditional planning. Avoid
unbounded calibration under IDEA-001. This decision has priority over
testing another discovery path because it addresses the current M2 gate
without displacing an eligible experiment.

### M2-E20-P01 Learning Card: effective observation readiness

**2026-11-12. REFUTED / DEFER for estimation from the existing E18 evidence.**
The source-bound E18 runner writes `effective_independent_units: null` for
both candidates. Non-overlap limits shared holding intervals. It supplies no
estimate of dependence from common market moves, overlapping forecast targets,
or reused training and validation histories. The [E18 receipt](https://github.com/RealMonoid/AQRS/blob/e26e65e7b98496c44ff464e7a0fa44c10a7d6694/evidence/m2-e18-verification.json)
and [E19 receipt](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/evidence/m2-e19-verification.json)
bind their comparisons to the same date scope. Cross-platform agreement
supplies engineering evidence. It adds no market observation.

| E18 contrast | Observation unit and evidence |
|---|---|
| `VOL_CONFIRM_V1` matched event versus below-cutoff event | Use the after-cost difference within each frozen pair. The report retains matches and UTC band/day summaries. A day can contain several dependent pairs. An analysis would preserve time order and account for grouping and cross-day dependence. |
| `VOL_CONFIRM_V1` filtered policy versus positive-move baseline, and `RIDGE_INCREMENT_V1` policy versus one-feature Ridge | For each policy comparison, use the net difference over the same eligible opportunities, including flat decisions. Keep each group's total paired difference and eligible count. Use the ratio of summed differences to summed counts for the opportunity-weighted claim. An unweighted mean of daily rates changes the target when counts differ. |
| `RIDGE_INCREMENT_V1` forecast versus zero and versus one-feature Ridge | Use aligned paired absolute-error differences at each eligible forecast origin, separately for each reference. Retain the reference loss too if estimating relative MAE reduction. The saved forecast block has pooled and fold metrics. It omits the ordered per-origin loss inputs. Trade records cannot reconstruct errors at flat opportunities. |

**Exact counterexample.** Enumerate six independent equally likely sign
draws, then three independent sign draws each repeated across two days.
Both cases have six dates and the same marginal variance of one. The
variance of the six-day mean is 1/6 and 1/3, respectively. Thus the
variance-equivalent counts are six and three in the two known cases.
The archived counts alone cannot distinguish these possibilities. The
pilot's short reused time window also gives no credible basis for choosing
a dependence length from the data. The E19 worktree precision note conditions
on assumed independent groups and another candidate's dispersion. It does
not estimate the dependence length or supply E18 forecast loss inputs.

**Method and revisit.** For any future fixed claim, use the same paired
contrast, population, and weighting as the intended decision. An effective
count would compare the variance of that estimator under an explicit
independent-unit reference with its variance under dependence. There is no
single interchangeable count across the contrasts above. First establish
the availability of chronological contrast inputs and a defensible group
or lag design over an eligible span. Reuse the scalar precision planner
for conditional feasibility once the dispersion, effect scale and units are
justified. Potential primary references for qualification are
[Newey and West](https://www.nber.org/papers/t0055) for long-run variance and
[Ibragimov and Muller](https://doi.org/10.1198/jbes.2009.08046) for inference
with suitably independent group estimates. External source retrieval timed
out in this review. Verify applicability against the primary papers before
admitting any such method. No method, lag, group length, minimum sample size
or economic hurdle was adopted. Quant Research revisits this at the next
candidate-specific design or M2 acceptance review when an eligible,
adequately scoped ordered series is identified. Keep the effective counts
unknown and the E18 candidate dispositions deferred until then.

**Dispatch reconciliation.** The evidence review permits no new E18
outcome calculation or precision campaign. As independent readiness work,
Engineering traced the [versioned E09 pilot](../scripts/m2_supervised_pilot.py)
and checked existing entry tests without executing it. The source snapshot
and guarded worker path can address the prospective reproducibility gap
once the exact path, data and Governor are qualified. The original run's
source identity can only be restored with new original run-linked evidence.
The [E09 replay decision](OPEN_QUESTIONS.md#m2-supervised-pilot-replay)
requires owner authorization. M2-E21 remains independently eligible for
consideration after its own benchmark, isolation and resource prerequisites
and implementation authority. The recorded owner action approved design
and queue placement. AQRS-B01, M2-E15, AQRS-SC01 and M4-E01 retain the start
conditions in their rows. There is no eligible next dispatch under the
current mandate. This records the first continuation check after AQRS-A12:
the authorized preparation was pulled, closed and reconciled against all
six remaining rows.

**Verification.** `python -B -` verified the exact synthetic variances and
traced the frozen source definitions and receipt identities. On native
Windows with Python 3.12.12, `python -B -m pytest -q -p no:cacheprovider
tests/test_audit_controls.py -k "supervised_actual_entry or supervised_screen"`
passed four cases (13 deselected). The cases reject a tighter fit limit,
strict memory mode and duplicate configuration before archive access or
worker launch, and preserve frozen costs in the mocked screening path.
The language self-test, language audit, `git diff --check` and focused
queue, link, changelog and preservation checks passed. No fresh Linux
verification, market payload or protected reads, outcome calculations,
campaigns, fits, resamples or spend. About nine minutes elapsed from the
Test Card through the readiness decision and closeout edits.

### M2-E20-P02 Test Card: effective count design

**Authority and dispatch.** The 2026-11-13 owner request directs completion
of already authorized preparation under AQRS-A12. Apply the standing
approval to the M2-E20 design and metadata work. Keep P01 closed. Start
P02 before lower-priority items because it addresses the unresolved M2
evidence gate without needing any outcome access. Sequence Preflight:
allow this preparation and keep the dependent calculations waiting.

**Decision and baseline.** Can one of the fixed E18 contrasts supply an
auditable path to an effective independent event count? P01 establishes
that the available evidence cannot justify a count. The riskiest assumption
now is that selecting a specific contrast, defining the variance reference
and inspecting qualified calendar metadata will identify a usable next
measurement. Another plausible result is that the frozen path or qualified
span cannot supply a defensible denominator even after a new market look.

**Minimum proof and stop.** Select one candidate and comparison before
inspecting any outcome. Specify the estimand, observation and grouping,
precision rationale, archived evidence input, exposure and next decision.
Trace the input and larger-window limitations to pinned definitions and
qualification receipts. Use one exact synthetic weighted-mean check to
challenge an unweighted day-average shortcut and evaluate known independent
and dependent group structures. Review primary methods or record any
access gap. Preparation passes when the design and actual execution
boundary are reviewable. Advance an outcome calculation only if it could
change the stated decision, satisfies existing admission and has the
required authorization. Otherwise give a concrete data or evidence trigger.
Keep the original candidate definitions and thresholds.

**Budget and risk.** Up to 30 minutes in this increment including closeout,
plus nine minutes already recorded for P01. Zero market or protected
payload reads, additional calculations on outcomes, trials, model fits,
resamples, data downloads, dependencies, spend and recurring work. Use
published source, receipts and date metadata. Stop before any change to
runtime or scientific contracts. No FTA is triggered by this paper design
and synthetic arithmetic. Check IDEA-001 and ADR-052 before considering
any broader method or calibration.

### M2-E20-P02 Learning Card: effective count design

**2026-11-13. SUPPORTED / PERSEVERE for design.** The earlier dispatch
stopped after P01 treated the missing claim and methods plan as reasons for
the whole item to wait. AQRS-A12 allows Quant Research to supply both before
requesting any data permission. P02 supplies them below. The failure to
produce an effective count in P01 remains valid.

**Fixed question and comparison.** How many independent matched pairs
would give the same precision as the mean net high-volume minus
below-cutoff contrast for `VOL_CONFIRM_E18_V1`, the E18 registration of
the fixed volume rule? The contrast is per retained pair, in basis points,
conditional on the frozen match rule. Use the same 30-minute holds, 25 bps
round-trip costs per leg and one pair per UTC eight-hour band. This asks
about the precision of a conditional development comparison. The all-
opportunity policy and both Ridge contrasts answer other questions. Their
counts remain unknown. The historical +2 bps paired follow-up screen is
preserved. This design makes no new market claim or acceptance threshold.

**Exact inputs and proposed calculation.** The first possible calibration
input is the match rows in `artifacts/m2-e18/windows/report.json` in the
E18 evidence bundle at `e26e65e`. The verification receipt binds the member
digest and the executable revision `54fb864`. Use the band start, pair
identity and paired net difference, retain calendar gaps and exclude the
Ubuntu replay as a second sample. For day or block \(g\), let \(S_g\) be
the sum of pair differences and \(N_g\) the pair count. The estimand is
`theta = sum(S_g) / sum(N_g)`. Center the block contribution as
`S_g - N_g * theta`. Compare an independent-pair variance reference
`s_pair^2 / N` with a between-block variance of the same weighted mean.
For a planning diagnostic with independently justified blocks, use
`G/(G-1) * sum((S_g - N_g * theta)^2) / N^2`, where `N` is the
total pairs and `G` the number of nonempty blocks. The equivalent count
is `s_pair^2 / V_block`. A missing or degenerate variance, too few
informative groups or unsupported independence leaves the count unknown.
Keep pair counts and empty days visible. The formula is a conditional
variance comparison. It does not establish the grouping assumption.

**Primary-source transfer and limits.** A cluster sandwich can represent
correlation within groups if there is a basis for independence between
groups. A serial covariance estimate needs a defensible lag model and
enough ordered observations. A group t-test also needs approximately
independent, suitably behaved group estimates. These papers justify
examining the assumptions. They supply no AQRS block length, finite-sample
guarantee or numeric cutoff. See [Liang and Zeger (1986)](https://doi.org/10.1093/biomet/73.1.13),
[Newey and West (1987)](https://users.ssc.wisc.edu/~behansen/718/NeweyWest1987.pdf)
and [Ibragimov and Muller (2010)](https://www.tandfonline.com/doi/abs/10.1198/jbes.2009.08046).
The synthetic check got a pair-weighted mean of 7/2 versus 7/3 for an
unweighted day mean. For four independent unit-variance pairs it got
mean variance 1/4. With one observation in one day and three sharing a
shock in the next day, it got 5/8 and an equivalent 8/5 pairs.

**Scope and decision.** The E18 fixed entry accepts ten UTC days, December
1–10, 2025. Its six validation days, December 5–10, allow at most 18
pairs, six one-day groups or three disjoint two-day groups. These are
calendar capacities. One- and two-day partitions anchored on December 5
would only illustrate sensitivity on those reused dates. D01 qualifies
14 further BTCUSDT dates, December 11–24, outside the E18 and E19 window.
The frozen entry does not accept them. Data qualification is not
experimental admission or evidence of independence.

**DEFER the additional market look.** Another calculation on the archived
six days would not resolve dependence, change either candidate's decision,
or meet the effective-count criterion. Retain the existing evidence.
If an eligible longer chronological series or independently supported
dependence evidence makes the count decision-changing, scope the comparison
before access, verify its time order and exposure, and independently check
the block or lag assumptions and precision. Use the prior exposure on
both platform runs and register any new report diagnostic before reading
the member. A strictly report-only planning look would be one member
and one contrast, zero fits, trials, resamples, downloads, spend or
recurrence, and would need specific authorization. There is no
decision-changing reason to request that look now. New market execution
would need its own authorization and Governor preflight.

**Verification and dispatch.** `python -B -` verified the synthetic
values, the receipt's report-member digest reference, frozen scope,
variant ID, qualification metadata and prior exposure. No report-member
outcomes, data payload, protected data or runtime campaign was accessed.
The first metadata inspection assumed that the D01 symbol rows formed a
mapping. The corrected list check passed. About four minutes elapsed from
the scope checkpoint through the design decision. E09 still requires its
separate execution approval. M2-E21 already records its authorized design.
The actual independent benchmark and launch are beyond its recorded design
scope. B01 remains deferred. Pull the independent E15 design preparation
because the E15 row already calls for that design before its named count
permission.

### M2-E15-P01 Test Card: state persistence count design

**2026-11-13. Authority and decision.** The E15 queue entry calls for
selecting a concrete rule and writing a Test Card before requesting access
for the count. Standing approval covers this design step. The E14
positive-five-minute-move baseline supplies a setup mechanism. E14 does
not provide evidence that persistence adds value. The next count would
only decide whether the two lifetimes differ often enough to consider a
separately scoped outcome study. Select the same setup, trigger,
invalidation and common entry opportunities for both arms. The comparison
must vary only the lifetime. Prefer the existing timing and fold
contracts over adding a new library or entry point.

**Minimum design proof and stop.** Trace the setup to the frozen E14 rule
and the 30-minute contract. Set two fixed lifetimes and a workflow coverage
gate before checking a synthetic event sequence. Confirm a fresh
trigger qualifies for both arms, a delayed trigger qualifies only for
the persistent arm, and invalidation or expiry denies both, including on
the trigger bar. Confirm reset and single-use behavior. Pass if the
rule is mechanically reproducible with an exact dataset, coverage rule,
cost and permission boundary. Otherwise keep the parent waiting and
give the missing prerequisite. Up to 20 minutes of design, checks and
closeout. Zero market or protected reads, outcome calculations, fits,
trials, resamples, dependencies, downloads, spend or recurring work.
No critical contract changes and no FTA triggered by this design.
Stop before production implementation or any actual count.

**Fixed comparison to check.** Use only the existing D01 BTCUSDT spot
minute data for December 1–10, 2025 UTC, with E18's two purged folds and
eligible signal indices. Start with no setup at each validation boundary.
Use completed bars only. A setup starts when the five-minute close return
crosses from nonpositive to positive. Store that setup bar and the close
five bars earlier as the invalidation level. Wait for a later
nonpositive five-minute return and then the first positive one-minute
close return on a strictly later bar. This is the common recovery trigger.
Invalidate when a later completed low reaches or crosses the stored level,
including on a trigger bar. Expire after age 30. Process expiry and
invalidation before a trigger. A trigger consumes the episode once.
A new setup can start when no episode remains, with triggers eligible
only on later bars. An active episode retains its original setup.
Use the same episode and trigger stream for both arms. The rolling
baseline allows a trigger at ages 1–5 and the persistent rule at
ages 1–30, in completed minutes. Count the 6–30 age difference only
when the common eligibility conditions hold. Check possible exit index
bounds without reading any forward prices.

The 5-minute lookback and 30-minute maximum use E14's declared event and
evaluation scales as fixed engineering probes. They are uncalibrated
lifetimes. Report all disagreements and their days/folds. For the
coverage decision, cap credit at one disagreement per UTC eight-hour
band per day. Require at least 12 such bands across at least four days
and at least four bands per fold. This reuses E14's operational spread
of matches as a feasibility screen. It supplies neither independence nor
profit evidence. A miss defers the study. A pass permits considering a
separate outcome proposal. Stop without changing a threshold, date,
lifetime or trigger.

**Governor for the proposed count.** One registered local count on one
10-day slice (14,400 bars), two rule flags on the same stream, zero
estimator fits, outcome trials, resamples, downloads, protected reads
or recurring jobs. Plan up to 45 minutes of one-time qualification,
execution and closeout after the current design. Estimate up to 20
seconds and 512 MiB sampled RSS for one worker, subject to the actual
count preflight. Use existing supervision and the default ceilings.
Stop before file access without the separate named authorization and
scope checks. Stop on failed timing, coverage or enforcement. A small
reproduction on synthetic events qualifies the written mechanics only.

### M2-E15-P01 Learning Card: state persistence count design

**2026-11-13. SUPPORTED / PERSEVERE for design.** The count has a named
market scope, fixed comparison and decision. `python -B -` checked a
synthetic reference sequence against the written rule. Ages 5 and 6
distinguish the arms. Ages 30 and 31 distinguish valid persistence from
expiry. Same-bar invalidation at equality denies entry, cooling and
triggering need separate bars, and a later trigger cannot consume an
episode again. A new setup can qualify after invalidation. The checks
also reject a training-side setup, an exit at the fold boundary and
duplicate or uneven band coverage. The E18 source and D01 receipt
supply the frozen input scope. The synthetic check is an oracle for a
future implementation. It does not qualify an actual count entry.
About three minutes elapsed through the design and checks. Zero market
or protected reads, trials, fits, downloads, spend or runtime changes.

**Queue rescan.** Close P01. M2-E15 awaits the named data and count
authorization. E20 has its technical design and needs decision-relevant
ordered evidence to justify further outcome work. E09 awaits its separate
replay approval. E21 lacks the independently committed synthetic inputs
and a qualified isolated execution path within an approved implementation
scope. The fixed B01 search entry does not supply this Scout path. B01's
reassessment remains dependent on E21. External B01 use also retains its
own delivery, 24-trial exception, start and independent risk-closure
requirements. SC01 remains owner-deferred and M4-E01 remains contingent
on authorized M4 planning. No pending row has an eligible next action
within the current mandate. See [Sequence Preflight](SEQUENCE_PREFLIGHT.md#m2-e20-and-m2-e15-dispatch-correction).

### M2-E15 count entry and execution

**Owner authorization, 2026-11-14.** In the current
[AQRS goal chat](codex://threads/01a1d8d8-9215-7fb2-af0b-42def1ef634a), the
owner approved one bounded BTCUSDT count as specified by the
[fixed design](#m2-e15-p01-test-card-state-persistence-count-design). Use only
the ten existing D01 UTC days, December 1–10, 2025. This includes entry
qualification, execution and closeout. Zero forward outcome calculations,
fits, outcome trials, new acquisitions, protected access, retuning,
resamples, automatic retries or spend. The prior design took about three
minutes. Allow up to 45 additional minutes under the existing budget.

**Sequence Preflight and minimum proof.** The first three pending rows lack
the evidence, scope or predecessor recorded in the queue. This count is
independent of them. The baseline is the written
rule and its synthetic oracle. Test the riskiest assumption on the actual
entry: one causal episode stream and identical eligibility determine both
arms with only different ages. Reuse the exact E18 fold construction and
the D01 importer. Test ages 5/6 and 30/31, invalidation at equality, distinct
cooling and trigger bars, one-time consumption, fold reset and future-price
perturbation. Guard exact archive identity and reject unsupported enforcement
before I/O. Require an independent review before market access. Stop on
failed admission, implementation, source or resource checks, or after the
single valid comparison. See [FTA-M2-E15](RISK_REGISTER.md#fta-m2-e15-state-persistence-count).

**Fixed implementation details.** Fold starts are 5,760 and 10,080. Each
has 4,289 eligible signals and checks `signal + 31 < fold_end` by index.
Trailing close inputs may cross the fold start but episode state resets.
After clearing or consuming an episode, a fresh crossing on that bar can
start a new episode. It cannot trigger until later. Credit the UTC date
and eight-hour band of signal availability at the completed bar's close.
Require 12 distinct bands across at least four dates and four distinct bands
in each fold. Retain all disagreement times, ages and fold assignments.
Pass permits a separate outcome proposal. A miss defers the study. Neither
result estimates independent observations or tests profitability.

**Governor and receipt.** One supervised count worker, two fixed flags on
one stream, two folds, zero seeds, research trials and fits. Use a bounded
20-second worker allowance, 512 MiB conservative sampled RSS allowance,
an outer campaign ceiling of 300 seconds and tighter configured limits
where applicable. Keep the fixed D01 archive and sidecar digests and the
E18 dataset identity in the run evidence. Persist the plan and the terminal
execution and coverage decisions. The market count may start once the exact
entry passes the synthetic and independent checks and preflight admits it.

### M2-E15 Learning Card: state persistence count

**2026-11-14. `SUPPORTED / PERSEVERE` for count feasibility.** The one
authorized BTCUSDT count returned `COMPLETED / PASS`. The 5-minute rule
gave 107 eligible signals and the 30-minute rule gave 319. The 212
disagreements covered 18 distinct UTC eight-hour bands across six days.
Both folds contributed nine bands. The gate required at least 12 bands,
four days and four bands per fold. The report retains all disagreement
times and ages and the SQLite journal records one count attempt with
`NOT_EVALUATED` evidence status. The count reuses development observations.
It gives no estimate of independent observations or economic effect.

**Execution and evidence.** Native Windows 11 build 26300, Python 3.12.12.
The `python -B -m scripts.m2_e15_count plan` and `run` commands exited 0.
One worker used 0.625 seconds wall time and 51.641 MiB sampled peak RSS.
Zero fits, outcome trials, retries, downloads and protected reads. The
[preserved bundle](../evidence/m2-e15-count-v1.zip) contains `report.json`,
`research.sqlite3`, the byte-bound source and prospective registration, and
the Ubuntu check log. Bundle SHA-256:
`26913733d430769aee480a70c847ab86fff71340d796b5e00d22d18384b22565`.
Report SHA-256:
`d016d75b92177759f70704965e53b9e61c302135cb9fa9551e4cb7fa8a360df5`.
The run binds the working-tree source snapshot. The count-only registration
was recorded locally before execution, with no published outcome preregistration.

**Verification.** The initial focused pytest command reported the missing
entry. One fixture initially expected no post-reset trigger and was
corrected to distinguish the valid in-fold setup from the dropped setup.
The focused `python -B -m pytest -q -p no:cacheprovider tests/test_m2_e15.py
tests/test_spot_dataset.py` passed 54 cases on Windows and 54 on headless
non-root Ubuntu 24.04.5 x86_64 with Python 3.12.3. Two Ubuntu setup checks
stopped before collection until the existing pure-Python test dependencies
were staged offline. Ubuntu exercised synthetic archives and the guarded
runner only. The independent reviewer matched 1,000 synthetic event streams
and 1,000 causal prefixes to a separate oracle, then verified all 212
recorded disagreements, the 25 source digests, the release-independent
input identity and the report against SQLite. That review reopened no raw
market archives. The full Windows `python -B -m pytest -q -p no:cacheprovider
tests` passed 248 cases. `python -m ruff check src tests scripts`, the Ruff
format check for the two new Python files, `python -B scripts/evidence_archive.py
--verify`, both language checks, manual English review and `git diff --check`
passed. The evidence check verified 295 historical members. The focused
queue, exposure, link and changelog check passed. About 19 minutes elapsed
from count intake through the full Windows suite and dispatch review.

**Decision and dispatch.** Close the authorized count. A separate outcome
proposal needs a fixed economic decision, matched baselines and a precision
and dependence basis appropriate to that decision. Use the counts to scope
feasibility when active M2 research next reviews this mechanism. E20 remains
the priority because only it addresses the open effective-count criterion.
See the [dispatch rescan](SEQUENCE_PREFLIGHT.md#m2-e15-count-authorization-and-dispatch).

### AQRS-A12 Test Card — autonomous work management

**2026-11-12. Owner authorization.** The current owner correction requests a
19-point work-management gap audit and the minimum necessary implementation,
followed by ten explicit behavioral cases. This standalone mandate ends after
the process corrections, checks, reconciliation and report. It covers existing
governance documents and their records. Estimated total effort is 60 minutes,
including review, edits, routine corrections and verification. Elapsed time is
tracked from the fresh repository review through the recorded decision.

**Baseline and hypothesis.** A03 already requires continuation and cross-item
dispatch. A11 already persists material follow-up. The owner reports recurring
requests to continue, and the preceding response addressed a role audit.
The repository records establish prior rule checks, with future adherence
explicitly unmeasured. The remaining risk is that an undocumented mandate or a
premature completion report turns an authorized next action into a suggestion.
A repository-recoverable authorization record and explicit readiness,
completion and continuation decisions should close that operational gap.

**Predeclared proof.** Audit all 19 requested points against current sources.
Pass when all ten owner cases have a direct rule and determinate action,
including automatic pull within a covered multi-item objective and waiting
for separately reserved data access. Additionally check the exact eight-hour
boundary, a standalone mandate, a stale READY label and available independent
work. Validate onboarding by recovering this item's authority and next action
from repository records alone. Fail if any case needs a fresh discretionary
permission choice or if the change grants new research or release authority.
Keep each existing queue row, order and start condition intact.

**Budget, risk and stop.** Zero research trials, fits, market-data access,
downloads, spend, dependencies or recurring runtime. The change operationalizes
existing development authority. Scientific, runtime, protection and numerical
acceptance contracts are outside this increment, so FTA is not triggered.
Use focused document/link/preservation checks, language check and self-test,
and diff checks. Stop after the acceptance walkthrough and reconciliation.
Evidence supports a documented workflow only. Future-session adherence needs
observation during ordinary authorized work.

### AQRS-A12 Learning Card — autonomous work management

**2026-11-12. `SUPPORTED / PERSEVERE` for the documented operating contract.**
507 seconds elapsed from the fresh repository review through this decision, including tool waits and the edit-tool correction, excluding final rechecks.
The baseline review below preceded the lifecycle edits. SUFFICIENT means
the existing rule already determines the relevant action. PARTIAL means the
rule exists but its operational use or recovery at the dispatch boundary
needed clarification. No absent role or second backlog was identified.

| Check | Baseline status | Evidence or gap |
|---|---|---|
| 1. Canonical work plan | SUFFICIENT | The experiment queue already names its canonical ownership. |
| 2. Definition of Ready | PARTIAL | Eligibility existed, but mandate recovery and readiness evidence were dispersed. |
| 3. Definition of Done | PARTIAL | Milestone gates existed without a compact item-level completion and next-dispatch contract. |
| 4. READY pull | PARTIAL | Rule 1 required pull but the session closeout lacked a recorded dispatch outcome. |
| 5. Continuous execution | PARTIAL | Root instructions required continuation, while the reported repeated pauses showed unverified adherence. |
| 6. Checkpoint / decision / blocker / completion | PARTIAL | Individual concepts existed without one operative action table. |
| 7. Completion reconciliation | SUFFICIENT | A11 already defines scope and follow-up reconciliation. |
| 8. Persistent material follow-up | SUFFICIENT | A11 maps work, choices, findings and deferrals to canonical records. |
| 9. Queue reevaluation | PARTIAL | Events were named, but the chosen action before session exit was not required as a record. |
| 10. Sequence / why now | SUFFICIENT | Sequence Preflight defines triggers, dependencies and decision value. |
| 11. Threshold check | SUFFICIENT | The Test Card and Sequence Preflight require a defensible threshold or bounded calibration. |
| 12. Test/Learning Cards | SUFFICIENT | Existing cards and their timing, evidence and exception rules are operational records. |
| 13. Waiting / blocked / deferred / rejected | SUFFICIENT | Queue and reconciliation rules define reasons, triggers, evidence eligibility and destinations. |
| 14. Owner decision boundary | PARTIAL | Reservations were distributed across rules and lacked one dispatch-facing account. |
| 15. Eight-hour rule | SUFFICIENT | The root already applies spent plus remaining time to the entire item or authorized sequence. |
| 16. Chat handoff | SUFFICIENT | Root instructions limit handoff to materially separate goals or inadequate context. |
| 17. Progress without waiting | PARTIAL | The instruction existed but lacked a closeout control exposing an avoidable wait. |
| 18. Cross-item autonomy | PARTIAL | Mandate scope and the mandatory next action needed an explicit recoverable record. |
| 19. Repository-only onboarding | PARTIAL | Entry links existed, but authority and the current next action were not uniformly recoverable. |

**Scope-mismatch review.** The preceding response delivered a role-boundary
audit. The owner then restated the active objective as autonomous work
management with 19 checks and ten cases. The missing closeout safeguard was
reconciliation against that intended deliverable. A03 had checked continuation
rules and A11 had checked persistent follow-up, while both left future-session
adherence unmeasured. The owner reports repeated requests to continue. The
review does not establish the frequency or cause of every historical pause.
Existing continuation rules already require action when authority and readiness
hold. The added authorization record and dispatch outcome make that obligation
recoverable and make an avoidable final recommendation observable.

**Behavioral walkthrough.** Manual source review mapped every case to the
revised rules. The focused Node.js check confirmed that each cited rule exists
at its reported source location. This is a document-conformance check.

| Owner case | Required action | Governing rule |
|---|---|---|
| 1 | Continue from analysis to implementation | Continuous execution, checkpoint row |
| 2 | Fix the ordinary bug and rerun affected tests | Continuous execution, ordinary-defect row |
| 3 | Pause dependent work, correct within scope or pull independent work | Queue rules 3–4 and material-finding row |
| 4 | Start the next covered READY item automatically | Definition of Done and next dispatch |
| 5 | Keep the new-data-dependent item waiting and inspect independent covered work | Definition of Ready, permission condition |
| 6 | Record necessary separate follow-up in the queue with a stable ID and parent | Completion reconciliation |
| 7 | Keep the incidental idea outside the queue | Completion reconciliation, information-only category |
| 8 | Continue after a progress message | Continuous execution, checkpoint row |
| 9 | Use cumulative sequence effort without per-substep permission | Definition of Ready, effort condition |
| 10 | Continue when only chat organization favors a handoff | Definition of Done and next dispatch |

The four additional boundary cases require effort approval at exactly eight
hours, respect an explicitly standalone completion boundary, recheck stale
READY labels and skip waiting rows when independent covered work is available.
Repository-only onboarding reached this active card through CODEX_START and
the queue and recovered its authority, 60-minute estimate and remaining checks.

**Verification.** On Windows, both language checks and git diff --check
passed with exit 0. Inline Node.js checks verified local links and anchors,
exact six-path changelog coverage, all 44 prior queue rows and their order,
unchanged unrelated tracked differences and the existing untracked inventory.
Manual review covered English prose, authorization boundaries and the ten
cases. An initial edit-tool string had a parse error before mutation. The
corrected edit proceeded without an owner prompt. This was a tooling correction
within the active item. No runtime tests or fresh Linux acceptance ran.

**Completion reconciliation and dispatch.** All requested governance checks,
minimal fixes and behavioral cases are complete. Close AQRS-A12. The remaining
six pending rows are WAITING. M2-E20 lacks its registered claim, observation
units and bounded plan for outcome calculations. M2-E21 lacks its frozen
benchmark, isolated handoff proof and bounded execution path. The other four
rows retain their named prerequisites or owner deferrals. This owner mandate
ends with the work-management audit and fixes, so no further queue item is
covered for dispatch by it. The final report follows this recorded boundary.

Future adherence remains unverified. During the next ordinary authorized
multi-item assignment, Codex checks actual pull and session-exit behavior
against this rule and records any recurrence here. This observation uses the
existing workflow and grants no new experiment or research authorization.
No separate follow-up work item is needed for the completed correction.

**Observed recurrence and correction, 2026-11-13.** After P01, the M2-E20
stop treated the unmade claim, series selection and methods plan as
reasons to end the session. Those were authorized preparatory actions.
The owner requested the stop review. Under the existing pull rule,
[M2-E20-P02](#m2-e20-p02-learning-card-effective-count-design) completed
the design, and [M2-E15-P01](#m2-e15-p01-learning-card-state-persistence-count-design)
completed the independent count preparation. The subsequent queue rescan
waits on external evidence or reserved scope and run decisions. The
existing A12 contract governs this correction.

**Owner clarification, 2026-11-13.** The
[permission-boundary check](DEVELOPMENT_PROCESS.md#permission-boundary-before-stopping-or-asking-the-owner)
now applies before each stop or request for owner input. Complete available
authorized preparation first and apply `WAITING` only to dependent work.
The M2-E20 and M2-E15 cases above show how a blocked calculation or count
can coexist with eligible preparation. A queue scan must also consider
eligible work elsewhere before dispatch ends. This clarification uses the
existing queue and cards. It adds no runtime work, data access, fits, spend,
or critical contract change. FTA is not triggered. About one minute elapsed
from the baseline checkpoint through the rule edits.

**Owner clarification and check plan, 2026-11-14.** The owner asked for a
repository-wide continuation record that avoids searching other chats.
Baseline: the queue links to authorization records, but the process does not
say when to persist a decision made in chat or how a new chat should handle
missing authority. The smallest documentation check starts at the queue and
walks through a recorded authorization, a missing authorization and a later
scope change. It passes if a fresh chat can recover the operative scope and
next step from the linked records, apply existing readiness rules, and pursue
independent work when a specific approval remains unresolved. Use at most 15
minutes and zero data access, trials, fits or spend. Stop if the fix requires
an additional tracker or changes to substantive approval rules. Routine
governance clarification. No critical runtime or research contract changes,
so FTA is not triggered.

**Result.** `SUPPORTED / PERSEVERE` for the documented handoff. Starting at
the queue recovered the closed M2-E20-P03 preparation and the separate
M2-E09 replay decision. The rule also traces a changed or withdrawn grant
to the affected scope and start conditions. The focused `python -B -`
document check passed on Windows after aligning an assertion with the
existing P03 authorization wording. The checks concern the written workflow. Actual
execution in a separate chat and a fresh Linux run were not exercised.
About three minutes elapsed from the initial repository review to the
focused verification. This clarification is complete. The six pending rows
retain their recorded start conditions and the replay still requires its
separate approval. No research execution was started.

**Queue handoff snapshot, 2026-11-14.** The owner requested a focused commit
of the current queue and its authorization records. This is a routine
documentation handoff. The six pending rows retain their start conditions.
M2-E20's M2-E09 replay decision is the first reserved approval. The
[dispatch rescan](SEQUENCE_PREFLIGHT.md#m2-e20-p03-completion-and-next-dispatch)
records the other pending conditions. Execution and runtime changes are
outside this handoff, so no fault tree is triggered. About three minutes
elapsed from the scope checkpoint to the first successful staged-tree
check on native Windows. The language checks, queue and link checks, and
changelog path check passed. No platform runtime acceptance was evaluated.

### AQRS-A11 Test Card: persistent work item follow-up

**2026-11-12, before editing the process.** The owner requested that all
material unresolved follow-up be recoverable from the repository. The
existing queue owns work order and readiness. Its finding and deferral rules,
cards, and decision records cover specific cases, but the current closeout
has no universal check for newly discovered follow-up. Prior evidence:
[AQRS-A02](#current-buildmeasurelearn-development-loop),
[AQRS-A05](#aqrs-a05-learning-card-observable-deferral), and
[AQRS-A09](#aqrs-a09-sequence-audit-and-dispatch-check).

**Assumption and proof.** A single closeout step and links from the normal
entry points can make follow-up traceable using current records. A separate
tracker would add duplicate state. The risk is a rule that still lets a
recommendation escape or turns tentative ideas into work. Pass if a
repository-only walkthrough handles all seven cases: an in-scope fix is
completed directly, separate necessary work is queued, an owner choice is
recorded, deferral has a trigger and default, an incidental idea stays out of
the queue, a finding changes dependent readiness, and the normal handoff
reveals completed, pending, deferred, blocked and owner-gated work. A queued
recommendation must resolve to a current ID, status and canonical location.
Fail if any required route is missing, a known dependency is lost, or the
change grants new dispatch authority. Mark actual future adherence unverified.

**Budget and stop.** One session of up to 45 minutes for the repository
review, focused walkthrough and documentation gates. Zero research trials,
fits, downloads, spend or recurring runtime. FTA and incident postmortem
triggers are absent because the change governs development records and
preserves critical contracts. Stop after the focused and language checks,
or narrow the change if it requires a second tracker or runtime enforcement.

### AQRS-A11 Learning Card: persistent work item follow-up

**2026-11-12.** 6 minutes 19 seconds elapsed from the Test Card through this
recorded decision, excluding initial orientation and final rechecks.
`SUPPORTED / PERSEVERE` for the documented closeout procedure.

**Historical evidence.** A02 found separate finding and dispatch records
without a required dependency link or resumption check. A05 found deferrals
without a named observation point after completed attempts. A09 found stale
E14 priority and a missing B01 capability condition across revisions. A02,
A05 and A10 addressed those respective gaps in the current checkout. E19
kept its revisit condition in its evidence branch, while the current E19
row exposed only the deferred outcome. E18 recorded the two screen misses
without an explicit revisit condition in its paired Learning Card. The
current queue now points to both dispositions and their review conditions.
The sampled repository records establish these traceability gaps. They
cannot establish whether any particular chat-only recommendation was lost.

**Scenario review.** A small authorized fix stays in its work item (A).
Separate work is tracked with its conditions, as in M2-E20 (B). A provisional
product choice routes to the existing open requirements register before
escalation (C). The E18/E19 dispositions have reasons, triggers and defaults
(D). An incidental tooling idea stays outside the queue (E). AQRS-A10-F1
is linked from the waiting B01 row before external execution (F). A
repository-only walkthrough from `CODEX_START.md` reaches the closed
evidence, six waiting rows, their prerequisites and the owner decision
records. No current row is ready or active. M2-E20 ranks first (G).

**Checks.** The focused inline Node.js check confirmed the baseline
gap, scenarios A–G, 17 added link references, and all six changed paths in
the changelog. The first check stopped early because it cut the queue at a
nested heading. The corrected check used the full section. On native
Windows with Python 3.12.12, `python scripts/check_language_policy.py --self-test`,
`python scripts/check_language_policy.py`, and `git diff --check` each exited
0. Manual English and dispatch review passed. Zero research runs, fits,
downloads or spend. No fresh Linux run or milestone acceptance was required.
The walkthrough establishes that the route is documented and navigable.
Actual adherence by future sessions remains unverified. No new work item
was generated. The current queue retains its order and prerequisites.

### AQRS-A10 Test Card: M2 evidence and threshold decisions

**2026-11-12, before editing the process.** The owner authorized a complete
M2 evidence review followed by the literature rule and the audit improvements.
Any new E09 execution requires separate approval. The baseline is the local
`044363c` working tree, the existing M2 evidence map, and the published E18 and
E19 receipts at `e26e65e` and `96df879`. The riskiest assumption is that a
concise threshold check can stop weak acceptance decisions while still letting
an authorized calibration start. A generic completeness check can miss an
irrelevant threshold or treat legitimate uncertainty as a blocker.

**Proof and stop.** Map every M2-specific and universal criterion to existing
evidence or an explicit gap. Walk through the E18 follow-up hurdle, the E09
missing-source case, the B01 coverage and interrupted-result counterexamples,
and the Windows cold-start case. Pass if the new guidance distinguishes each
decision, requires applicable literature or a documented basis, permits a
bounded calibration, and gives each material gap a resumption check. Verify
paths, links, language and preservation of prior changes and frozen evidence.
Stop at the documented decision or if runtime changes or a new execution are
needed. Allow one documentation and evidence-review session of up to 60
minutes, zero trials, fits, resamples, downloads, raw market or protected reads,
spend and recurring compute. Documentation and dispatch clarification only.
No critical runtime contract changes. FTA not triggered.

**Status:** No development loop is active. AQRS-B01 is deferred pending the
[capability benchmark revisit](#aqrs-b01-capability-benchmark-deferral).
The [A10 review](#aqrs-a10-learning-card-m2-evidence-and-threshold-decisions)
reconciles the completed M2-E14/E17/E18/E19 work and records the remaining gates.
AQRS-D01 and AQRS-A06/A07/A08 remain closed.

### AQRS-A10 Learning Card: M2 evidence and threshold decisions

**Subsequent evidence, 2026-11-14.** The
[source-bound E09 reproduction](#m2-e20-p04-learning-card-source-bound-e09-replay)
supplies the supervised reproducibility evidence that was open at this
review. Effective independent counts and final release verification are
still open.

**2026-11-12. M2 remains `IN_PROGRESS`.** The review uses the
[M2 DoD](MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls),
the earlier [E11 evidence map](#m2-e11-learning-card-m2-evidence-review-2026-11-09),
the preserved E09/E10 reports in [acceptance.zip](../evidence/acceptance.zip),
and the E18/E19 receipts linked in the queue. Evidence applies to its recorded
revision, platform and scope. Both E18 candidates were evaluated and deferred.

| M2-specific criterion | Status and evidence |
|---|---|
| Two interpretable, versioned real-data candidates in one campaign | **MET.** E18 executed `VOL_CONFIRM_E18_V1` and `RIDGE_INCREMENT_E18_V1` on the same pinned BTCUSDT Spot scope. Both reports bind source and dataset IDs and contain two completed trials. |
| Reproducible LightGBM and Isolation Forest baseline pilots | **OPEN in part.** [E10](#m2-e10-learning-card-isolation-forest-pilot-2026-11-09) binds the Isolation Forest versus simple volatility comparison to matching source and outcome receipts. [E09](#m2-e09-learning-card-corrected-supervised-pilot-replay-2026-11-09) matches LightGBM versus Ridge outcomes within `1e-8`. Both journals are intact and their run rows match the archived snapshots. Original run-linked AQRS and pilot bytes are missing. [E16](#m2-e16-learning-card-historical-source-binding-2026-11-10) documents the gap. |
| Five `EVALUATE` model dispositions | **MET.** [E13](#m2-e13-learning-card-five-model-assessments-2026-11-10) records XGBoost, Random Forest, HDBSCAN and autoencoder deferrals and a PCA data blocker, with revisit triggers. |
| Origin, horizon, inputs and availability for each candidate | **MET for E18.** Published revision `54fb864` defines both hypotheses before their E18 outcomes, fixes a 30-minute horizon and uses completed-minute inputs. The reused development window and earlier views remain recorded. |
| Observable event, detection rule and cadence | **MET for E18.** Positive five-minute move plus a training-only volume cutoff, and the completed-minute Ridge score with the same cost-plus-buffer action rule as its fitted control. |
| Cost-aware matched rule-based screen | **MET.** E14 and E18 evaluate the volume rule with matched below-cutoff events and 25 bps modeled round-trip costs. E18 preserves both the paired and all-opportunity comparisons and records `DEFER`. The separate price-drop V2 question remains deferred. |
| Trivial and simple forecast baselines on the same chronological folds | **MET.** E18 compares zero and one-feature Ridge on the same purged folds. E09 also recorded the zero/Ridge/LightGBM comparison. |
| Descriptive diagnostics, flat/fold views, counted exposure and pre-outcome design review | **MET for the scoped descriptive comparison.** [A08](#aqrs-a08-learning-card-descriptive-signal-diagnostics) verifies the reporting path. E18 preserves flat and fold views, 230 recorded views over both platform runs, known-answer checks and an independent pre-outcome review. Its precision assessment limits the result to descriptive use. |
| Candidate-to-decision control against a known filter | **MET.** E18 compares positive moves with and without the volume condition on the same opportunities. E10 compares volatility-plus-anomaly with volatility alone. E19 corroborates the workflow using a simple gate and Flat as references. |
| Negative control detects a deliberately misleading association | **MET for the software control.** [E01](#m2-e01-learning-card-one-event-research-decision-2026-11-09) removes the apparent advantage from a shared rebound. A08 reproduces and catches the biased V1 control. |
| Per-candidate costs, turnover, effective independent event count and variant count | **OPEN in part.** E18 records costs, turnover, opportunity and event counts, registered variants and replay exposure. Both candidate reports explicitly set `effective_independent_units` to null. Overlapping targets and a few reused days prevent treating rows or fills as independent units. |
| Adversarial causal features and decisions | **MET for the tested paths.** [E05](#m2-e05-learning-card-decision-time-causality-2026-11-09), [E06](#m2-e06-learning-card-fitted-candidate-causality-2026-11-09), and the E18 entry tests cover future-only perturbations of event inputs, decisions and fitted scores. |
| Null and planted-effect separation | **MET for software.** [E04](#m2-e04-learning-card-synthetic-interaction-comparison-2026-11-09) distinguishes XOR from its null. A08 and E18 known-answer checks distinguish shared or absent effects from planted ones. Real-data comparisons can return `DEFER`. |
| Declared Windows/Linux CPU and resource scope for both pilots | **MET for recorded execution.** E09 and E10 completed under their declared budgets on both platforms. The E09 source gap remains open under the reproducibility criterion. |

The [universal release criteria](MILESTONE_DOD.md#universal-dod-for-every-milestone-all-items-mandatory)
also apply. The following is an evidence review of the named increments.

| Universal criterion group | Evidence and remaining scope |
|---|---|
| Test and Learning Cards, backward planning, predeclared criteria, scoped work and visible outcomes | E18/E19 published plans and learning records support the completed increments. Earlier historical exceptions, including E09 source binding, remain visible. |
| Risk-based FTA, positive/negative/boundary/adversarial tests, incidents and rejected ideas | E18/E19 link relevant fault trees and verified negative cases. E18 records the rejected replay setup and exact-byte transport correction. Prior engineering dispositions remain in [Decisions](DECISIONS.md#rejected-and-deferred-engineering-ideas-durable-decision-memory). Recheck incident and risk closure against the final release revision. |
| Working end-to-end path, real test and lint evidence, native unprivileged Windows and headless Linux CPU | E18/E19 have archived four-job CI and paired market receipts. E09/E10 also record native Windows and headless Ubuntu execution. Fresh end-to-end and independent platform acceptance of the final M2 revision remain required. |
| Time, costs, holdout, traces, journal, attempts and simple baselines | E18 binds data, source, configuration and candidates, records matched baselines, costs, exposure, stops and no protected access within its reviewed path. E09's source gap remains. Relevant final-revision contracts and artifacts require an independent acceptance check. |
| Budget preflight and enforced limits, simulation-only scope | Archived M0 guard proofs and M2 receipts support the tested entry points. E18 records seven charges per platform and explicit guarded scope. Final review must cover the selected M2 entry points and confirm the live-order boundary. |
| Current implemented documentation, English, canonical changelog and status | The receipts record applicable policy checks on their revisions. The final release must reconcile branch-specific evidence and docs, check changed-path coverage and English, and retain `IN_PROGRESS` until the independent gate closes. |

**Decision and next check.** The evidence review supports the scoped workflow
and defers M2 acceptance. E20 first identifies a defensible observation unit
and whether the existing development evidence can support an effective-count
estimate. Record the reason and a specific new-evidence trigger if it cannot.
No follow-up effect claim uses these estimates as independent confirmation.
For E09, reopen historical recovery only if original run-linked material
appears. If a new LightGBM replay is needed, propose a source-bound Windows run
and conditional Ubuntu replay under the existing Governor, with separately
approved scope and a fixed test card. No execution is authorized by A10.

**Threshold walkthrough.** The [Test Card rule](DEVELOPMENT_PROCESS.md#1-write-a-compact-test-card-before-implementation)
requires primary literature where applicable, an explicit transfer basis,
and separate calibration and validation. [Lakens](https://doi.org/10.1525/collabra.33267)
supports matching precision to the smallest effect of interest.
[White](https://doi.org/10.1111/1468-0262.00152) supports accounting for
selection across tried models. Neither source sets AQRS's opportunity-level
economic hurdle. In E18, 2 bps across 8,578 opportunities implies 17,156 bps
of total incremental return. A new proposal needs an action-frequency and
cost basis for that decision. Preserve the historical E18 screen. The
[Windows cold-start incident](#m1-e10-learning-card-cached-windows-wheels-and-replay-2026-11-09)
needs bounded phase measurements when startup admission becomes the decision.
The [B01 findings](RISK_REGISTER.md#open-execution-path-quality-debt) gate only
external B01 use. The [Learning Card diagnosis](DEVELOPMENT_PROCESS.md#diagnosis-in-existing-records)
now gives unresolved results a decision and an observable next check.

**Verification.** `SUPPORTED / PERSEVERE` for the evidence map and written
process. The Windows `python -B -` checks verified the 60 E18 and 10 E19 bundle
members against the pinned Git receipts, both platform records per campaign,
the E09/E10 parity and source-status distinction, and all 14 M2-specific rows.
Early inspection checks assumed a shared bundle layout and identical receipt
status tokens. Reading the preserved formats and checking them separately
resolved those check failures. `python -B scripts/evidence_archive.py --verify`
verified 295 historical files. The policy checker with and without `--self-test`,
`git diff --check`, the focused link and changelog check, and manual English
review passed. The byte comparison verified preservation of the 91 baseline
paths outside this change. About 6 minutes 38 seconds elapsed from the
19:14:12 UTC evidence checkpoint through the first passing focused checks.
No fresh Linux execution, research runs, data payload reads or fits. The written
dispatch rule was checked on the recorded scenarios. Its use in a future
dispatch remains unmeasured.

**External methodology review, 2026-11-12.** The owner approved reusing
practical lessons from Open Quant Trading Lab and its discussion. The
[evaluation protocol](MODEL_EVALUATION_PROTOCOL.md#2-evaluation-sequence)
now illustrates early data feasibility, synthetic counterexamples for timing,
the limits of shuffled-target diagnostics, and matched cost sensitivity.
This routine documentation clarification uses the existing review steps.
No fault tree was triggered because no critical contract changed. The scoped
documentation pass took about two minutes. Zero research trials, fits, data
reads, or recurring runtime work. No new queue item.

### M2-E21 Scout pilot feature preflight

**2026-11-12. Decision: narrow and queue.** The owner approved placing a
bounded pilot in the work plan and incorporating the related design lessons.
Test whether one agent can derive a new executable event from a development
view. The baseline is B01's frozen 24-rule search space. Verify that the
planted event lies outside that space using the benchmark construction and
a known-answer check. No B01 campaign is needed for that check. The rival
explanation is that a generic rule or chance selection can pass.

**Minimum proof.** An independent benchmark producer commits the generator,
expected event and scoring specification before either Scout invocation. Use
two identically formatted synthetic cases with independent random streams
from one fixed campaign seed. One has a causal, detectable planted pattern
outside the B01 rule space. The other retains comparable inputs and opportunity
frequency without that relationship. Separate Scout sessions receive only
their permitted development prefixes. Each may submit one candidate or
abstain. Freeze the [candidate handoff](MODEL_EVALUATION_PROTOCOL.md#agent-discovery-handoff)
before evaluating the later synthetic segment. Reuse existing event timing,
matched controls, cost accounting, journal and Governor where their contracts
fit. Record the proposed rule, implementation identity and independent result
in the existing records. The pilot uses one generation per case.

**Pass and stop.** Before either Scout sees data, freeze the admissible fields,
event-mask agreement threshold, direction, horizon tolerance, minimum eligible
events, net contrast floor against a matched control and null decision rule.
Verify that the planted construction can meet these criteria and that a
generic rule cannot. Pass only if the frozen candidate matches the planted
event and meets the independent timing and net-contrast checks, and the null
case produces no claimed effect. Record abstention, miss, unsupported proposal,
false claim and execution failure distinctly. Stop after both cases or the
first protection or budget failure. A miss or false claim triggers redesign
or deferral. A pass supports reviewing B01's benchmark and establishes
bounded synthetic behavior.

**Resource Governor review.** Estimate two to four hours of one-time work,
including verification, and at most two sequential Scout invocations and two
deterministic trials total. Zero estimator fits, tuning, seed sweeps, resamples,
market or protected reads, and recurring jobs. Estimate up to 30 seconds and
512 MiB sampled peak RSS per evaluator and up to 5 MiB total retained evidence.
Keep the default 120-second trial and 300-second campaign limits and count
Scout calls under the planned wall-time and usage limits. Trial and fit counts
fit the defaults. Confirm the usage cap, startup time, memory and platform
support on the selected path before launch. Count any synthetic qualification
or technical replay in its applicable budget before dispatch. Stop on
unavailable enforcement or resource overage. No spend increase is approved.

**Risk and readiness.** Apply [FTA-M2-E21](RISK_REGISTER.md#fta-m2-e21-scout-pilot)
before implementation and verify the actual handoff before blind execution.
The feature review supports the design and queue placement. Benchmark
thresholds, artifact isolation and measured resource estimates remain open.
This planning increment changes documentation only and performs zero trials,
fits or data reads.
About 8 minutes elapsed from the baseline snapshot through verification
of the edits, including the wait for host access.

#### Scout preparation and remaining start conditions

**2026-11-13.** Read-only path review under ADR-053. The fixed B01 generator
produces 24 predefined candidates with one or two same-tail conditions and a
fixed three-minute horizon. This holds with no activity fields and with all
supported activity fields. Its registration selects from that set before
execution. Use this rule space as the benchmark baseline. The B01 entry
cannot accept an original Scout proposal. The existing timing and cost
simulation, journal and worker supervision are reuse candidates. Worker
containment controls termination and sampled RSS. The planned Scout handoff
still needs evidence of isolation from the later segment and benchmark truth.

For independent delivery, give the Scout only the permitted development
prefix. The producer supplies a dated commitment to the generator, expected
event and scoring criteria before either session. Reserve the later segment
and truth for the evaluator. Use the existing [handoff contract](MODEL_EVALUATION_PROTOCOL.md#agent-discovery-handoff)
and the preflight above to qualify the selected path. No benchmark arrived
with the recorded design decision. Implementation and launch remain within
the separately agreed scope. This review added zero invocations, trials,
fits, outcome reads or dependencies. The existing pilot limits still apply.

**2026-11-14.** [RD-001](requirements/DECISIONS.md#rd-001-two-entry-points-for-research)
confirms both research entry points for v1.0 under
[FR-004](requirements/REQUIREMENTS.md#functional-requirements). This pilot
can supply evidence for the market-only path. Its existing implementation,
benchmark, isolation, and execution prerequisites govern dispatch.

### AQRS-A09 sequence audit and dispatch check

**Read-only audit completed 2026-11-12.** Targeted sequence gaps. The M0
causal-data and supervised-execution proofs, M1 source-to-campaign path, and
M2 synthetic controls, coverage screens and bounded challengers follow the
milestone dependencies. M3 through M9 retain their staged acceptance gates.
Independent engineering can proceed within authorization when its path does
not consume a missing scientific or execution guarantee.

| Category | Observed order and consequence | Minimum prevention |
|---|---|---|
| `LATE_SAFEGUARD` | M2-E08/E09 used the supervised pilot before its effective-policy admission and recoverable source binding were verified. A06 corrected the admission path. E16 established that E09's outcome parity still cannot prove source reproducibility. | Exercise the effective policy and bind both runs to recoverable source before market use. |
| `REWORK_FROM_ORDERING` | M2-E08's LightGBM result construction stopped after market work. The corrected bounded replay was separately authorized as E09. The failure could have been exercised with a fitted synthetic report. | Exercise the actual estimator-to-report path before market admission. |
| `LATE_SAFEGUARD` | M2-E02/E03/E12 counted V1 controls before a planted timing check exposed overlapping returns. A07 required a new V2 count before any outcome study. No V1 outcome evaluation was recorded. | Verify comparator timing on a known-answer case before counting eligibility. |
| `SEQUENCE_INVERSION` | M2-E14 built and qualified the two-family entry before a cheap training-only check established whether its first window could exercise the Ridge branch. The entry and volume evidence remained useful. Ridge screened out and the conditional Ubuntu market replay could not start. E17 then used the cheap screen before E18. | Use an authorized training-only feasibility check before full campaign qualification when the milestone proof needs both comparisons. |
| `REWORK_FROM_ORDERING` | The first E18 Ubuntu launch stopped before input because the staged Windows report bytes differed from the verified local file. The replay transport was corrected at `1eebbfa` before the successful launch. | Verify the staged artifact digest before dispatching the dependent replay. |
| `DEPENDENCY_GAP` | The working tree at `044363c` still places E14 first for campaign planning. The newer `e26e65e` evidence already closes E14, E17 and E18 and records a two-family paired proof. Its B01 queue row also lacks the capability revisit condition recorded in this working tree. A single checkout can misstate either prerequisite. | Reconcile the relevant owner decision and evidence against the intended execution path before dispatch. |

The E18 receipt and 60-member bundle at `e26e65e` record paired Windows and
non-root Ubuntu execution, seven charges on each platform, and two deferred
research follow-ups. M2 acceptance remains open. The next decision is an
evidence-only review of the remaining M2 criteria, starting with E09 source
reproducibility. B01 has an independent fixed-rule technical rehearsal.
Using it as a product discovery benchmark waits for the recorded capability
and benchmark revisit, in addition to external data, budget and start gates.

**Test Card, 2026-11-12, 00:05:59 UTC.** The baseline dispatch rules already
link material findings, protect independent work and govern deferrals, but
leave sequence decisions implicit outside queue dispatch and across revisions.
One short preflight in the existing dispatch rules should identify
the next evidence-producing action without creating a second tracker or a
permission boundary. The riskiest assumption is that a missing guarantee can
pause its consumers without stopping independent authorized work. Pass if the
rule resolves a stale E14 row, the E09 acceptance dependency, independent E14
engineering, a blocked B01 benchmark, an authorized successor step and a
higher-value authorized prerequisite. Verify all seven review events and four
decisions, the existing deferral and finding rules, exact paths and links, and
byte preservation of pre-existing work. One documentation increment up to 45
minutes. Zero campaigns, fits, market or protected reads, spend or additional
runtime. Stop after the walkthrough and documentation checks, or if the change
would require a runtime control or change any scientific, data, execution or
authorization contract. Governance risk screen only. FTA not triggered.

**Learning Card, 2026-11-12.** `SUPPORTED / PERSEVERE` for the binding
[sequence preflight](DEVELOPMENT_PROCESS.md#sequence-preflight). In the
walkthrough, the stale E14 row could not start a duplicate campaign. The E09
source gap blocked use for M2 acceptance while its recorded outcome parity
could be cited with a note. The gap did not block the separately authorized
E14 synthetic entry. B01's external benchmark stayed parked. An eligible
verification step inside the same approved item continued. An eligible
training-only check with more decision value than qualifying the full entry
took priority within its authorized scope. A material finding still blocks
only dependent work, and a revisit trigger still requires reassessment and
applicable authorization.

The inline `python -B -` baseline check identified four implicit rules
with exit 1. The revised check verified all seven events and four decisions,
prior dispatch rules, exact changelog coverage and byte preservation with
exit 0 after correcting an assertion about line wrapping. It verified both
E14/E18 evidence bundles and report digests, and matched the status and
dispatch documents in four linked worktrees to their committed revisions.
The language checker and its self-test, the archive verifier for 295
historical files, manual English review, and `git diff --check` passed on
Windows. About four minutes elapsed from the Test Card checkpoint through
the first successful focused verification. No work item was dispatched.
The checks exercised the written process on recorded cases. Adoption across
branches and its effect on future dispatch remain unmeasured. No platform
runtime or milestone acceptance was evaluated in this increment.

**Documentation follow-up, 2026-11-12.** The owner requested a dedicated
[Sequence Preflight document](SEQUENCE_PREFLIGHT.md). It holds the binding
procedure and short records of material changes to sequencing. The existing
queue and cards retain operative start conditions and evidence. The focused
inline `python -B -` check verified the relocated rules, local links, exact
changelog coverage, and preservation of the queue and prior changes. The
check passed after its initial heading pattern was corrected. Elapsed time
from the 00:27:25 UTC baseline checkpoint through the first passing focused
check was about two minutes. Routine documentation change. FTA not triggered.

### AQRS-B01 sequential delivery Test Card

**2026-11-11, 20:38:18 UTC orientation checkpoint; before implementation.**
Baseline `1552eaf`. Owner requires sequential deliveries, one dataset at a
time, published immutable verdicts, and complete evidence with a gap ledger.
Hypothesis: append-only published start and verdict records plus local exclusive
ownership can enforce order across deliveries without using later CSVs for
planning. The riskiest assumption is the boundary from a published closure to
the next admitted payload. A synthetic local-remote sequence must reject skipped
IDs, concurrent or duplicate starts, unpushed starts/verdicts, altered prior
verdicts, and manifest changes within a delivery before any later payload read.
It must continue from a finished delivery to the next consecutive ID, preserve
old bytes, publish an explicit `NOT_EVALUABLE` verdict on a required-evidence
gap, and append corrections with the last closed dataset ID. Spy on later file
opens and stats. Verify actual worker receipts and independent Git-path review.

**Resource assessment and stop.** Estimate 45–75 minutes including review and
testing. Keep 24 trials, six to nine fits, one worker, 252 seconds of bounded
worker time and the existing 300-second ceiling per dataset. Estimate 129 MiB
output per dataset, including 1 MiB for the sequencing and gap records. Inputs
remain up to 256 MiB per delivery. No unused budget carries forward. Stop if
sequence or evidence checks cannot fail closed within these boundaries. The
fault tree covers admission, publication, and journal integrity. No external
outcomes, downloads, protected data, canonical OPEN replay or new dependency.

**Additional owner acceptance criteria before implementation.** Provide one
canonical field dictionary, a traced summary of at most 40 lines per dataset,
and a read-only replay for any two completed candidates with explicit recorded
and recomputed values. Verify with a reader independent of the chat. Replays
reconstruct recorded evidence after verdict publication and consume no new
trial or calibration budget. Allow up to a further 30 minutes of development
for the independent review and field dictionary, within the standing limit.

**Learning Card, 2026-11-11, 21:09:22 UTC.** `SUPPORTED / PERSEVERE` for
the sequential and audit controls. Measured interval from orientation through
the evidence review was 31 minutes 4 seconds, excluding final publication.
Independent review caught split closure commits, incomplete worker-receipt
coverage, an authorization-path probe, self-referential replay costs and
ambiguous summary pointers. Corrected them before acceptance. Git history now
checks commit groups and append-only order. The published registration anchors
costs and replay verifies every opportunity row. Unsafe or changed evidence
is recorded as a gap without following links. The mandatory list includes the
closed journal and worker receipts. No search rules or estimators changed.

Native Windows `python -m pytest -q --tb=short --basetemp
.venv/aqrs-b01-deliveries-audit-20261111` passed 222 tests in 148.03 seconds.
The offline local Git remote exercise completed all 24 guarded D001 trials,
blocked its successor before publication, accepted the next delivery at D003,
and recorded D002 as `NOT_EVALUABLE` after a timeout and missing artifacts.
An attempted historical verdict edit blocked advancement. The D001 example
ran in 38.532 seconds and indexed 48,974,167 bytes across 58 evidence files.
The 19-line summary matched its verdict facts and all value references and
artifact digests checked. Independent review matched 13 final blobs, passed
seven targeted negative tests and separate closure probes, and used the actual
replay command on a different pair of synthetic candidates. P12 had 2,093
events and `NO_INCREMENTAL_EVIDENCE`; S09 had 12,959 events and
`INSUFFICIENT_COVERAGE`. Both used 15 basis points of registered costs and
matched all recorded values and opportunity rows. Replay left the artifacts
unchanged. Ruff, language self-test/check and diff checks passed.

The evidence estimate is 129 MiB per run plus delivery bytes. Git and closure
checks are outside the supervised compute window. Test Card sequencing is
recorded by its dated checkpoint without an independent preimplementation Git
timestamp. Linux and external data execution remain unverified. A hard stop
without a terminal receipt blocks advancement. The enforced publication history
does not substitute for server-side protection against administrative rewrite.
No production incident, external payload access, canonical OPEN replay or
automatic next-campaign dispatch occurred.

### AQRS-B01 evidence amendment Test Card

**2026-11-11, 20:21:18 UTC orientation checkpoint; before implementation.**
Baseline `1f71d5e`. Owner requested machine-readable per-run evidence. The
riskiest assumption is that exports represent the actual matched strata and
causal features without changing measurements, releasing outcomes early, or
making a stopped attempt appear complete. Reuse the published configuration,
candidate ledger, opportunity CSV, dataset report and supervised worker. Add
the plan snapshot, feature CSV, prediction applicability record and run
manifest. Pass if a maximum-row synthetic delivery produces all applicable
files, exact digests and matched counts, a publication stop prevents candidate
output, and a timeout retains honest partial evidence. Independent review of
the execution/receipt boundaries is required. See the AQRS-B01 fault tree.

**Resource assessment and stop.** Estimate 30–60 minutes of development.
Reserve 32 MiB for features, 64 MiB for up to 24 opportunity CSVs, and 32 MiB
for staged bars, source and metadata, including temporary writes. Check
128 MiB free on the run volume before admission and before execution. Inputs
are separate at up to 16 MiB per CSV and 256 MiB per delivery. A 16-dataset
envelope requires about 2.25 GiB including input. Stream CSVs and digests.
Exports share existing worker limits. Zero new fits, trials, resamples,
workers or dependencies. Stop if match reconciliation, source ordering,
storage admission or the current compute bounds fail. No external outcomes or
canonical OPEN replay.

**Learning Card, 2026-11-11, 20:36:13 UTC.** `SUPPORTED / PERSEVERE` for
the machine-readable evidence. Measured interval from the orientation
checkpoint through final tests was 14 minutes 55 seconds, before publication.
The independent review found that the earlier publication check could accept a
truncated ledger if its local and pushed copies agreed. Corrected this by
binding the UTF-8 LF ledger digest and regenerating all expected pending rows.
Also rebuilt the run manifest from verified registration and receipts, bound
effective costs, and promoted opportunity evidence only after a completed and
verified worker receipt. The completion marker follows journal persistence.

Windows `python -m pytest -q --tb=short` passed 217 tests in 87.66 s on the
corrected source. The focused blind file passed 40 tests in 26.27 s. The
maximum-row fixture generated 14,676,748 feature CSV bytes and 1,309,749 bytes
for one conjunction opportunity CSV. Supervised preparation took 2.266 s with
129.72 MiB observed peak RSS. Tests reconciled exact matched counts and hashes,
low storage rejection before input, changed artifact rejection and a simulated
timeout with 22 untouched candidates. Independent Windows review matched the
eight exact blobs and passed five focused tests plus a real offline local-Git
proof. A pushed truncated ledger with matching SHA failed before reservation.
The full ledger completed two synthetic guarded trials with valid artifact
hashes and SQLite integrity. No new alpha tests or real outcomes were added.

The estimate is 128 MiB per dataset run plus delivery bytes. No increased
compute limits, new dependencies or new document per experiment. Ruff, language
and diff checks pass. Historical OPEN artifacts remain bound to their original
source. Linux and the external campaign remain unverified. The Test Card was
recorded before implementation in the work transcript without a separate Git
timestamp. No production incident occurred. External admission waits for the
owner's data, budget and start. Candidate publication is checked per run.

### AQRS-B01 search amendment Test Card: causal minute order flow

**2026-11-11, 20:04:51 UTC, before implementation.** The owner requested
order-flow candidates and delegated feature design before dataset generation.
Baseline: `f6b8663` plus the local optional-column admission amendment. The
riskiest assumption is that retained aggregates reach registered candidate
workers without exposing a future minute, altering fills or expanding the
trial budget. The minimum proof is an augmented synthetic minute fixture through
preparation, registration and candidate measurement. With identical OHLCV,
changing an available activity column must change its candidate membership.
Changing future rows must preserve the feature and decision prefix. Absent
columns select the frozen OHLCV fallback slots. Check all eight header subsets,
exact 24-trial allocation, observed fit charges and the old OHLCV-only route.
Record commands, worker receipts and independent review. See the AQRS-B01
fault tree for the causal and accounting checks. No external outcomes or
canonical OPEN replay.

**Resource assessment and stop.** Estimate 30–60 minutes of development,
including review and local verification. Replace at most six OHLCV conjunctions
with six single-feature tails. The proposal keeps 24 trials, one worker,
60 seconds of preparation, eight seconds per trial and 252 seconds of bounded
worker time. Maximum calibration fits rise from six to nine, within the existing
12-fit limit. Three added numeric columns occupy at most 1.98 MiB per 86,400-row
array. The 16 MiB source CSV and existing memory ceiling remain binding. The
fit count depends only on the available fields. Stop if qualification, causal
parity, accounting or registration fails, or if a budget increase is needed.

**Learning Card, 2026-11-11, 20:15:13 UTC.** `SUPPORTED / PERSEVERE` for
the order-flow amendment. Measured interval: 10 minutes 22 seconds from the
preimplementation checkpoint through review, excluding orientation and final
publication. Windows `python -m pytest -q --tb=short` passed 216 tests in 91.91 s.
The initial guarded fixture failed because its arithmetic produced tiny negative
sell volumes at the full-buy boundary. Corrected the fixture and retained strict
input validation. A final targeted guarded fixture run passed in 4.25 s, with
1.172 s preparation, 125.66 MiB sampled peak RSS and nine started/completed fits.

Independent verification matched the six reviewed blobs and passed 39 focused
tests in 27.14 s plus separate probes. All eight field subsets used the fixed
slots, and all six order-flow tails preserved earlier membership and timing
under future-only perturbation. The OHLCV-only path matched the prior candidate
catalog and full measurements. A supervised candidate used zero fits and
rejected mismatched activity metadata or staged digest. The registered set and
incomplete-run report retained all 24 slots and the observed fit count. No
material finding remained. The preimplementation card preceded coding in the
work transcript. No separate timestamped card commit is claimed.

Ruff, language and diff checks passed. Existing OPEN evidence and the Governor
config are intact. The amended plan replaces up to six conjunctions in exchange
for direct order-flow coverage. External data access and outcome work remain
`WAITING` for the owner's delivery and authorization. The fresh tests cover
Windows. Linux and the external 24-trial campaign remain unverified. No
production incident or canonical OPEN replay occurred.

### AQRS-B01 input amendment Test Card: optional minute order flow

**2026-11-11, 12:59 UTC, before implementation.** Hypothesis: the existing
supervised CSV admission can validate three optional minute aggregates while
returning exactly the same six-column search input for the same OHLCV rows.
Baseline `f6b8663` accepts only the original header. Pass if a maximum-length
fixture with all three fields and a partial header qualify, malformed fields or
headers reject after a valid digest, and the legacy and augmented inputs produce
identical staged OHLCV. Count zero new trials, fits, workers or dependencies.
At 86,400 rows, three extra short tokens (15 characters each plus delimiter)
add about 4 MiB to the CSV. The existing 16 MiB input cap and supervised
60-second preparation limit apply. A near-capacity synthetic qualification
provides a local timing sample within that limit. Development estimate 15–30
minutes. Stop if acceptance requires changing the search, authorization gates,
or budget. Significant input-validation review: unexpected columns could carry
hints, malformed aggregates could be mistaken for valid data, or side columns
could leak into features. Restrict the exact optional names and order, validate
values and preserve the six-column output. FTA not triggered because neither
causal timing nor the protected-access, journal or Governor contract changes.
Single-trade and quote input are estimate-only. No external data or outcome run.

**Learning Card, 2026-11-11, 13:02:57 UTC.** `SUPPORTED / PERSEVERE` for
optional minute admission. The measured interval since the Test Card checkpoint
was about four minutes, excluding orientation and final bookkeeping. Native
Windows `python -m pytest -q tests/test_blind_search.py --durations=4 --tb=short`
passed 36 tests in 17.91 s. The 86,400-row compatibility check took 1.15 s,
including two qualifications and the fixture rewrite. The pre-change partial
header test reproduced the expected rejection. Focused Ruff, language self-test,
language check and diff validation passed. Peak RSS for the augmented fixture
and Linux execution remain unmeasured. No blind outcomes, new calibrations for
research, external reads or new limits. The old OPEN receipt remains bound to
its original source. Bind and publish the amended source with the prospective
external candidate registration before any outcomes. The frozen search still
uses OHLCV and the external run remains WAITING. Event-input implementation is
deferred pending the owner's separate decision.

### AQRS-B01 Test Card: external synthetic blind-search preparation

**2026-11-11, before implementation or rehearsal outcomes.** Orientation checkpoint
07:41 UTC; source baseline `e976e8111fed7823780dc582627f2c75d5eac0eb`.
Owner scope: two handoffs, one open rehearsal, then stop. No external payload is
present or authorized for search. No external assistant notes or solution files
may be sought. An accidental reveal must be reported immediately and invalidates
blind status until the owner decides. Prior IDEA-001/002/003/004 checked; avoid
unbounded sweeps and unnecessary documentation/services.

- **Hypothesis / riskiest assumption:** existing supervision and SQLite records
  can support a prospectively published, finite blind-search diagnostic with
  auditable missed/untested/rejected stages, without accessing hidden answers.
  Alternative: publication, timing or controls fail on a known-answer fixture.
- **Backward proof / minimum slice:** validate an externally shaped minute CSV,
  freeze all candidate definitions, publish candidate entries with empty results,
  run two supervised candidates on one open planted fixture, and produce exact
  event timestamps, effect intervals, controls and a truthful dataset report.
  Support preparation only if the open volume effect is claimed with a positive
  gross interval, a redundant conjunction fails incremental controls, and all
  required rejection/causality/publication checks pass. A null fixture must not
  force a positive result. These are software fixtures, not an error-rate study.
- **Fixed search:** 24 rules, six causal features, 12 single tails and 12 fixed
  conjunctions, one horizon, train-only quantiles, chronological evaluation,
  matched parent controls and predetermined multiplicity/coverage thresholds.
  Full normative procedure: `RESEARCH_PROTOCOL.md`, section 11. Input contract:
  `CONTRACTS.md`, A2. No adaptive extra candidates or tuning.
- **Evidence / baseline:** the existing core supports two configured candidates
  but not blind input admission or a remotely verified preregistration barrier.
  Reuse `governor.supervise`, `platform_guard`, `worker.run`, fit reservation,
  `journal` and `storage`; do not change their contracts. Capture commands,
  source/data/plan hashes, publication revision, worker budgets and reports.
- **Acceptance / negatives:** reject out-of-root/link/unexpected inputs, bad
  digests/cadence/OHLC/schema, missing owner authorization, over-budget plans,
  unavailable strict memory guards, absent/changed unpublished registrations,
  duplicate attempts and interrupted workers. Perturb future data and verify
  prior features; assert exact next-open and horizon-exit indices and equal
  costs. Reconcile every candidate with the finite search space and stop reason.
- **Risk:** critical admission, chronology and evidence integrity; apply
  FTA-AQRS-B01 before coding and request independent read-only verification.
- **Resources / decision value:** expected 2–4 hours total preparation, below
  the eight-hour standing limit. No packages, downloads or paid services. One
  open rehearsal: two research trials, six quantile calibrations charged as
  fits, zero predictive model fits/resamples, one worker, <=120 s/trial,
  <=300 s/campaign, <=4096 MiB sampled RSS; tighter configured limits apply.
  The 24-candidate external proposal needs explicit scoped trial-count approval;
  all other current ceilings remain. Stop on failure, no automatic campaign
  repetition. Unit/regression fixtures are engineering checks, not blind runs.
- **Effort versus displacement / stop:** directly answers owner-selected test
  readiness; no queue work is displaced or dispatched. On unmet criteria report
  the blocker, fix routine engineering issues, and keep the blind start locked.
  No new milestone acceptance claim. Fresh Linux verification is desirable but
  cannot cause downloads; record it as unverified if no offline runner exists.


### AQRS-B01 review checkpoint

The Test Card was published at `8c763fc` before implementation `85959bb`.
An independent read-only reviewer identified and verified corrections before
the canonical rehearsal: dataset approval had permitted sibling payload reads;
worker imports had used mutable working-tree source; copied registrations lacked
execution-time attempt identity checking. Qualification now checks the approved
digest before opening the selected payload, worker snapshots bind every package
module, and execution binds requested/registered/approved attempt IDs. An
integrity stop retains started-worker accounting and discards measurements.
The parent-gate label was corrected to `NO_INCREMENTAL_EVIDENCE` with separate
failure reasons; numeric success criteria were not changed. No external payload
or canonical rehearsal was exposed by those preacceptance defects.

The reviewer independently passed seven selected correction tests in 6.28 s,
including a real Windows junction, plus a separately constructed wrong-approval
attempt test. Reviewed source blobs: input `427b50af59cac96cd7b0456e49be3b3325d7ec01`,
search `14a16cc83fad6e979c5137be420ee5f199229f66`, tests
`dea4c197351c59fa8fe62ccbc7f31461233d6a6b`. Root verification passed all 24 blind
tests in 12.44 s and Ruff. The earlier whole suite passed 196 tests before the
last corrections; it is not represented as a final-source suite. The canonical
OPEN run, publication proof and final whole-suite/policy checks remain pending.
No incident with real or blind data occurred; these were bounded review findings,
not an invented production incident. Linux remains unverified for this entry.

### AQRS-B01 Learning Card: ready for owner data and start

**2026-11-11. `SUPPORTED / PERSEVERE` for preparation on native Windows only.**
The authorized preparation ends here. External search remains `WAITING`; it
does not dispatch another queue item. Numerical criteria and the six-feature,
24-rule search are frozen at published revision
`211fd6e3bd9154d9573c7d96367784b45ffbd0c1`; plan fingerprint
`fb12e165f06875347db05465b0b6ad6e3915c6fc19cb3e328c3fb35a081e8d7b`.
The first handoff delivered the exact input contract before this completion.
The [verification receipt](../evidence/aqrs-b01-verification.json) records actual
commands, results, boundaries and hashes of all 29 canonical rehearsal artifacts.
Monitoring interval: 07:41:00–08:18:41 UTC, **37 minutes 41 seconds** through this
decision; initial orientation and subsequent final documentation/publication
are outside that measured interval. Total effort remains below the declared
2–4-hour estimate. No research budget was increased.

**One actual OPEN run.** `register-open` performed six charged quantile
calibrations in a supervised preparation worker (0.750 s). Both empty-result
candidate entries were committed/pushed at the revision above. `execute
--published-revision 211fd6e3bd9154d9573c7d96367784b45ffbd0c1` verified the real
remote head, registrations and bound source before releasing workers. It
completed once with two trials, six calibration fits, zero predictive model
fits/resamples and 3.765 s combined preparation/execution wall time. Observed
worker peak including preparation was 104.43 MiB; this is sampled RSS, not a
strict memory cap. Publication and final persistence remain outside the worker
deadline. No campaign retry occurred.

S08 (relative volume >= 1.1981162106814187) claimed a positive conditional
contrast of **80.605644 bps**, simultaneous interval **[77.000311, 84.210978]**,
with 2,528 events among 12,959 evaluation opportunities and 18 two-day blocks.
The fixture plants a 100-bps effect above a raw-volume threshold; S08 recovers
a related condition, not proven exact generator equivalence. P02 selected the
same events and failed its second parent control, which was empty; report
`NO_INCREMENTAL_EVIDENCE`, not proof of a causal explanation. Both journal
evidence statuses remain `INSUFFICIENT_EVIDENCE` for real-world alpha. The known
null and sub-cost positive fixtures pass their separate engineering checks.

**Verification.** The final native Windows Python 3.12.12 suite passed **201
tests in 74.16 s**; all 24 blind-entry tests passed in 12.44 s. Ruff, language
self-test/check and `git diff --check` passed. The unauthorized external
registration command exited 1 before input access as required. Independent
verification closed every code finding and then checked exact local publication,
source/snapshot/data/result hashes, SQLite integrity, every saved opportunity's
timing/cost/control fields and the effect interval reconstructed independently
from event CSVs. No extra campaign was run. Linux is **UNVERIFIED for this new
entry**; no suitable AQRS offline runner was used and no packages or CI runtime
were downloaded. No M2 or cross-platform milestone acceptance is claimed.

**Resources and remaining decisions.** Proposed external allowance per dataset:
24 trials, six calibrations (within 12 fits), one worker, 8 s per candidate,
60 s preparation, 252 s conservative worker-bound sum within the existing
300 s campaign ceiling, and at most 4096 MiB observed RSS. Estimated local
storage is below 128 MiB per maximal dataset including input, staged arrays,
opportunity CSVs, journal and source copy; this is not an enforced disk cap.
The base Governor file is unchanged and still rejects 24 without an explicit
scoped owner exception. Approve the total dataset count/time separately; no
automatic batch or retry. Hidden-effect precision and two-day independence are
unknown; this fixed search cannot represent every possible planted effect.

**Recommendations awaiting owner decision:** score exact or mechanically
equivalent rule/event recovery as primary, report useful related conditions
separately; approve 24 candidates and at most 300 s per dataset; use this frozen
plan rather than free adaptive search for the first blind diagnostic. Following
delivery and explicit start, qualify only the approved dataset, publish its
24 empty-result entries and then run. Freeze blind results before any separately
authorized reveal/oracle comparison. The next objective is that named blind
run, not M2-E14. The completion message supplies the owner-facing chat title.

### AQRS-D01 Test Card: free Spot data expansion

**2026-11-11, before implementation and payload access.** Owner approval covers sensible additions to the free Spot data workflow; ADR-051 removes license/data-rights screening. Source/policy review started 07:01:15 UTC. Baseline source is `4fd02d9`, followed by the A08 closure record and G01 documentation correction. The existing daily importer, `Bars`, dataset writer, source snapshot, worker handshake and supervisor are the reuse baseline. Prior evidence: the public archive schema and an HTTP HEAD returned 200 and 70,262 bytes for ETHUSDT on December 1; no payload was read to select the scope.

- **Hypothesis and decision.** The existing daily validation can support a second symbol and contiguous additional dates while preserving the M1 campaign restrictions, exact bar availability, bounded resources and reproducible provenance. Support adoption of the data preparation path only if all declared archives qualify and synthetic rejection/platform checks pass. Missing archives or invalid inputs produce an explicit incomplete result, not fabricated coverage or a larger search.
- **Minimum slice.** Preserve the old M1 import API and campaign scope. Add a reusable daily loader with explicit symbol and timestamp units, retaining quote volume, integer trade count and taker-buy base/quote volume alongside unchanged OHLCV. Add a data-only plan/acquire/qualify entry using the existing supervisor. Join days only within one symbol, require full contiguous minute cadence, and publish per-symbol data/activity files plus a manifest. No new libraries, models, features, market outcomes, PnL or cross-symbol pooling.
- **Fixed data scope.** BTCUSDT and ETHUSDT Spot, one-minute daily archives for December 1 through 24, 2025 UTC inclusive: 48 ZIPs and 48 checksum sidecars, 69,120 bars. Dates extend the existing BTC December 25–January 5 development window without reading it again. Selection is calendar-based and fixed before payload access; two named instruments do not represent the market universe. January 6, 2026 stays rejected for all supported symbols. No futures, trades, quotes, protected data or automatic second source.
- **Acceptance and negative tests.** Preserve legacy M1 output fingerprints and configuration restrictions. Verify millisecond/microsecond boundaries on synthetic 2024/2025 fixtures, complete days, valid activity values and matching symbol/digest/filenames; reject gaps, wrong symbols/dates/units, bad checksums, oversized inputs, malformed activity and the reserved date before I/O. Reject out-of-plan network targets and redirects before following them. Check plan counts, no fits, failed-download/timeout receipts, no overwrites, and incomplete publication. Exercise the real CLI on synthetic local archives, independently review the final source, and run targeted plus full Windows checks and real Linux verification. Real acquisition is one bounded attempt; no automatic retries or replacement dates.
- **Resource assessment.** Expected one-time development 2–4 hours, reassess before eight hours total. Zero research trials/fits/folds/seeds/resamples or spending. At most two sequential data workers, each within the existing 120-second worker limit and one shared 300-second acquisition deadline; use the configured sampled-RSS policy (4,096 MiB ceiling), estimate below 512 MiB. Cap each ZIP and decompressed CSV at the existing 512 KiB and checksum at 4 KiB: at most 24 MiB ZIP payload plus 192 KiB checksums, 128 MiB total new data/evidence. Up to 96 requests, no redirects or retries. A first-day timing observation within each worker checks a conservative twofold extrapolation before acquiring its remaining days; fail closed if predicted remaining work does not fit. Transfer speed/RSS are estimates until measured. Offline quality processing shares these guards.
- **Risk and stop.** Apply [FTA-AQRS-D01](RISK_REGISTER.md#fta-aqrs-d01-spot-data-expansion). Stop on scope, checksum, timing, quality, network, storage, resource or platform failure; retain a truthful failed/partial receipt. Do not relax research criteria, M1/M2-E14 scopes, costs or the holdout. IDEA-001/004 and ADR-043/044/046 were reviewed: this is bounded data qualification, not a sweep or candle-grid research branch. The new dataset remains development material; qualification is not alpha or independent confirmation. Subsequent diagnostics require their own counted research definition and admission.

**D01 verification checkpoint, 2026-11-11.** The new loader's 18 baseline checks and the data entry's 12 baseline checks failed because the respective APIs were absent. After implementation, 46 focused checks passed in 3.30 seconds; the full native Windows suite passed 177 tests in 58.86 seconds. Ruff, both language checks, whitespace checks and preservation of all 295 archived evidence files passed. The explicit plan contains 48 archives, 69,120 bars, at most 96 requests and zero fits. Independent review, Linux verification and one bounded real acquisition remain pending. G01's registry IDs/statuses remain unchanged and its 17 paths are covered in the changelog. No market payload has yet contributed to this checkpoint.

### AQRS-D01 Learning Card: qualified free Spot development data

**2026-11-11. `SUPPORTED / PERSEVERE` for data preparation.** The existing parser and supervisor support the declared two-symbol, multi-day slice. All 48 archives qualified: 34,560 minute bars each for BTCUSDT and ETHUSDT, December 1–24, 2025 UTC. Quote volume, trade count and taker-buy base/quote volume are retained with bar-close availability in a separate activity file. The M1 wrapper, fixed campaign configuration, research rules and existing models are unchanged. G01/ADR-051 removes mandatory data-rights/license review gates across the current instructions, specifications and registry.

**Verification.** Implementation `8f6016543bb0f6379010427c14c878cb40183dfb` passed 177 native Windows tests and independent review (46 focused tests plus original-M1 parity, timing rejection and partial-symbol probes). [CI run 42979643150](https://github.com/RealMonoid/AQRS/actions/runs/42979643150) passed all four Windows/Ubuntu 24.04 jobs on Python 3.11/3.12, 177 tests each. The Linux platform checks enforce non-root execution. Ruff, language self-test/check, `git diff --check`, all 295 preserved-evidence checks, registry identity/status preservation and changelog coverage passed. The [versioned verification receipt](../evidence/aqrs-d01-verification.json) binds commands, source, exact CI jobs, the pre-implementation record and acquisition manifests. Historical evidence was not recomputed.

**Observed resources and artifacts.** The real Windows command completed once in 85.734 seconds with zero fits. BTC and ETH workers took 43.250 and 42.188 seconds; peak sampled RSS was 58.070 and 57.789 MiB. Archive ZIPs total 3,334,594 bytes; all data, source and evidence under the acquisition output total 21,698,581 bytes at the independent digest/row audit. Both first-day extrapolations admitted the remaining dates within the fixed limits. `artifacts/aqrs-d01/data/report.json` is the local receipt; each symbol directory contains `dataset.csv`, `activity.csv` and `manifest.json`. The output audit independently checked all ZIP/checksum pairs, both output digests, every row's symbol and activity-time alignment, and the declared resource limits.

**Boundaries and next decision.** This qualifies development inputs, not a signal, economic result, independent confirmation or market universe. Linux CI exercised synthetic multi-symbol archives through the same entry; real archive qualification ran on Windows only. RSS is sampled and parent snapshot/report I/O remains outside the worker deadline. M2-E14 stays `WAITING`: specify the intended comparison, opportunity population, precision and registered diagnostic exposure before outcomes. The new data are not automatically substituted into its historical card. Any reuse needs an explicitly scoped research definition and applicable admission. The reviewed GitHub suggestions do not add dependencies: a collector or execution simulator becomes relevant only for a named future recording/fill question at the existing gates. No additional market experiment is dispatched by this data-preparation result.

**Elapsed work.** Source/policy review began at 07:01:15 UTC; final verification reached 07:38:34 UTC, 37 minutes 19 seconds later, including G01, implementation, independent reviews, platform checks, acquisition and record validation. Final receipt review confirmed source, manifest, scope and resource coherence with no remaining adoption blocker; language checks passed over 48 files. This is within the declared 2–4-hour development estimate and existing data limits.

### AQRS-A08 Test Card: descriptive signal diagnostics

**2026-11-11, before implementation (06:42 UTC review start).** The owner authorized the useful follow-ups from Claude and explicitly required the biased-control self-test and precision review before M2-E14, with every new diagnostic on previously used market days counted as additional exposure. Baseline is `a52d02c`. Prior source review established MAE and per-fold prediction reporting, but no rank association or forecast dispersion; the training movement screen can stop before fitting. No new market outcome informed this card.

- **Hypothesis and risk.** Reusing the existing prediction arrays can make a flat or weak forecast interpretable without changing fits, timing, costs, policy decisions or evidence status. The alternative is that pooled rank association hides unstable folds or constant forecasts produce misleading numbers. See [FTA-AQRS-A08](RISK_REGISTER.md#fta-aqrs-a08-descriptive-diagnostics-and-admission).
- **Minimum proof.** Add average-tie Spearman association and prediction/target mean and population standard deviation to the existing aggregate and fold prediction metrics. Expose them in JSON and Markdown, with undefined rank results represented by null plus a reason. Retain all observations and label the output descriptive, without p-values, an independent sample-size estimate or automatic promotion. Keep the current cost screen intact.
- **Predeclared checks.** Hand-calculated positive, reversed, zero-association and tied-rank fixtures must agree within 1e-12; constant, singleton and invalid input cases must not fabricate a coefficient. A zero-trade synthetic evaluation must still expose diagnostics, with unchanged fit reservations. A constructed reversal across folds must remain visible. The actual simulator must expose the historical V1 control's false 50-bps advantage when event-forward returns are zero, reject that comparison under the fixture's zero-advantage criterion, and accept V2; a planted 30-bps forward effect must be recovered by V2. Preserve the existing 619-unit conditional precision example and its assumptions. These are engineering checks, not statistical error-rate calibration or market admission.
- **Acceptance and evidence.** Run failing checks before implementation, focused checks, the full Windows suite, Ruff, language self-test/check, diff checks, and the existing four-job Windows/Linux CI. Capture command outcomes and exact revision in this record. Measure diagnostics on 10,000 scalar pairs: target under 2 seconds and under 32 MiB additional sampled process RSS, with no fits/resamples. Review legacy fields and frozen evidence for unintended changes. The new report fields are additive.
- **Resources and priority.** One bounded 1–3 hour development increment, zero new market archive reads/downloads, market fits, horizon searches, instruments or protected reads. Synthetic verification only, sequential local checks; existing campaign limits remain unchanged. Recurring work is two rank sorts and summaries per existing fold and aggregate, not extra estimator fits. Historical recomputation is a new counted attempt. This has priority over implementing the waiting M2-E14 runner because it clarifies that design's interpretation without launching it.
- **Stop and decision.** Stop on changed fills/status/budgets, unsupported diagnostics, failed causal checks or a resource excess; narrow or roll back the additive diagnostics instead of changing research thresholds. Adopt only on passing evidence; otherwise record INCONCLUSIVE or REFUTED. IDEA-004 and ADR-043/044/049 were reviewed: do not replace event-defined controls with a global correlation screen. Broader instruments, execution modeling and shadow operation stay at their existing gates.

**Exposure refinement before its implementation.** The owner's explicit counting requirement also needs machine-readable receipts. Each evaluated candidate will record one entry per new metric and aggregate/fold view, with a stable diagnostic definition ID, exact validation index intervals and horizon. The existing report and journal persist these entries without a schema migration; later evidence consolidation must retain them even when a model attempt is a replay. The two-fold fixture must produce 15 entries (five diagnostics times three views); a pre-fit screen produces none. No market attempt is created by registering the definitions or running synthetic fixtures.


### AQRS-A08 Learning Card: descriptive signal diagnostics

Local implementation passed 138 tests in 76.93 seconds on native Windows. The
diagnostic baseline failed 15 checks before implementation; Markdown, receipt
and consolidation checks each separately failed on their missing behavior.
The known-answer null check rejects V1's false 50-bps advantage and accepts V2's
zero advantage; V2 also recovers the planted 30-bps effect. Two repeated model
attempts retain both diagnostic receipts in the consolidated index. All legacy
synthetic metrics/trades and five fit reservations match the baseline. The
10,000-observation diagnostic measurement took 0.001322 seconds and 0.855469 MiB
additional observed RSS, below the declared bounds; this is not a strict memory
cap. Ruff, language self-test/check (45 files) and diff checks passed. See the
[verification receipt](../evidence/aqrs-a08-verification.json) for commands,
synthetic examples and limitations.

**2026-11-11 — SUPPORTED / PERSEVERE.** Independent read-only review at local
commit `4fd02d9` returned READY with no actionable findings: 92 focused checks
passed in 3.47 seconds, 100 deterministic rank cases agreed with SciPy 1.18.1
(95 defined, maximum difference 1.11e-16), and old/new output, screen and legacy
report comparisons passed. The initial default-temp setup error was environmental;
an explicit project basetemp resolved it. No material incident or new rejected
engineering idea was identified.

Direct Git transport failed twice. The connected GitHub API published the exact
same tree `74c63b4fd39f93bffb46b0f45381d8a173e4ae08` as commit `c4a6ff8`;
only commit metadata differs. [CI run 42977006809](https://github.com/RealMonoid/AQRS/actions/runs/42977006809)
passed all four Windows/Ubuntu Python 3.11/3.12 jobs, with 138 tests per job,
synthetic CLI execution, 295 preserved evidence files, Ruff and language checks.
Both Ubuntu jobs passed the non-root assertion. Actual working interval through
CI evidence capture: 06:42–07:10 UTC, about 28 minutes; publication housekeeping
after that endpoint is not included.

Adopt the additive diagnostics and view receipts. No market data, market fits or
protected access were added. The old metrics/trades and all historical exposure
remain unchanged. Next objective remains M2-E14's claim/precision and full-design
review under its existing limits. The V1/V2 self-test is verified; it does not
validate the two new M2-E14 designs or resolve their empirical precision assumptions.
Broader data, realistic execution and shared backtest/shadow decisions retain
their later prerequisites. Source and tests are unchanged after the verified CI;
closure documentation receives fresh documentation checks.

### AQRS-A07 Test Card: research comparison and precision boundaries

**2026-11-11, before implementation.** The owner approved correction of the verified research-logic findings. Baseline is `c36f4ee`; hashes and start time are retained in `artifacts/aqrs-a07/baseline.json`. Existing reports and a read-only synthetic reproduction informed this card: historical price-drop matching can select a control whose return contains the triggering fall; the Isolation Forest paired measure omits control-only hours; zero or one trade cannot support an economic conclusion. The audit's claims that Ridge cannot trade, unsigned features require an interaction, or M2-E14 must fail are not established. No model change follows from those claims.

**Assumption, reuse and minimum proof.** The existing evaluator, cost helper, count scanner and planning/CLI modules can support honest comparisons without a new research service. Preserve the immutable historical scanner and reports. Add a registered `PRICE_DROP_V2` count implementation that selects only earlier, same-hour controls whose 15-minute hold ends no later than the start of the event's five-minute lookback; retain all other count criteria and mark unmatchable events instead of relaxing them. This removes the demonstrated mechanical overlap, not all observational confounding. Compare full fixed hourly opportunities in the existing Isolation Forest report, treating no action as zero net return and including all four action/skip combinations. Retain its original paired criterion as a legacy diagnostic and decision rule, not a newly validated filter test. Add explicit zero/single-trade and raw one-bar momentum limitations to current reports, and label the movement screen as a scale check rather than proof of predictability.

**Acceptance and stop.** First reproduce the contaminated-control and omitted-opportunity failures. Require a full synthetic-day scan to reject the old control, keep causal pre-entry eligibility and exact hold boundaries, and never inspect forward outcomes. Require common-opportunity net differences to reconcile exactly with the existing simulator under identical costs, including empty and asymmetric action cases. A scalar normal-approximation planning helper/CLI must report assumed independent units, dispersion, one-sided alpha and power, required units and detectable mean; validate inputs and never grant alpha status or infer independence from trade count. Verify a hand-calculated case and a case where the stated precision exceeds capacity. Keep M2-E14's historical card and thresholds; block its research interpretation until the intended claim, control population and precision assumptions are fixed before running. No fabricated sample-size adequacy.

**Resources and risks.** One development loop, expected 2–4 hours including tests, review and four-job CI; reassess before eight hours total. New checks use deterministic synthetic fixtures, zero estimator fits and no market archive payloads, downloads, resampling or protected access. Existing full-suite and synthetic CI fits remain within their existing test limits. Added per-run reporting is linear in existing observations/opportunities; the precision calculation is constant work and the fixed 1,440-row count is bounded. No new dependency, paid service, automatic campaign or budget increase. Apply FTA-AQRS-A07; independent read-only review is required before closure. Stop on causality, cost reconciliation or platform failures. Historical outcomes and source snapshots remain byte-identical.

**Verification checkpoint, 2026-11-11.** Independent reproduction tests on `c36f4ee` produced 60 expected failures and one passing historical control (3.59 seconds); the real precision CLI test also failed because the command was absent. After implementation, 68 focused checks passed in 3.05 seconds. The full native Windows command `python -B -m pytest -q -p no:cacheprovider --tb=short --basetemp .venv/aqrs-a07-suite tests` passed 119 tests in 76.03 seconds. Ruff, both language checks, whitespace and exact changelog-path checks passed. The evidence verifier checked all 295 preserved files. Byte checks retained historical scripts, bundle, manifest and frozen configurations; semantic checks retained every historical exposure record and original M2-E14 definition/gate. Fresh independent review and four-job CI remain required before closure.

**Independent-review amendment, 2026-11-11.** The initial `<=` boundary above was too weak. At reviewed revision `b1f7218`, a valid synthetic next-open gap from `close[84]=100` to `open[85]=99.5` lets a control entered at minute 70 absorb 50 bps while the event at minute 90 has no later rebound. Both reviewers reproduced this with the actual simulator, and a new regression failed before correction. The current V2 rule therefore requires `control_entry + 15 < event_entry - 5`; equality is rejected. The planted example now selects control 69, exiting at open 84 before the lookback's first close. This is a transparent correction of the initial design assumption before any V2 market run. Preserve the earlier test/CI evidence as an intermediate checkpoint, not final acceptance; repeat the affected checks and independent review at the corrected revision.

### AQRS-A07 Learning Card: research comparison and precision boundaries

**2026-11-11. `SUPPORTED / PERSEVERE` for the bounded software and reporting correction.** Adopt `PRICE_DROP_V2`'s strict temporal guard, the complete hourly policy diagnostic, sparse-trade/screen/benchmark labels and the data-free precision command. Preserve historical variants, outputs, costs and the original M2-E14 thresholds. Q1's demonstrated mechanical overlap is guarded; observational confounding is not eliminated. Q4's skipped opportunities are now visible in a separate diagnostic, without relabeling historical tests. Q3's actual scientific design remains unresolved and continues to block dependent effect claims and campaign admission.

**Final verification.** At `a7c11bfdbe8b48df4e7d4de117e2e90cd43fe7ee`, native Windows passed all 121 tests in 73.93 seconds using `python -B -m pytest -q -p no:cacheprovider --tb=short --basetemp .venv/aqrs-a07-final-suite tests`. The new gap regression failed before the strict-boundary correction, then passed with 69 focused checks. The independent reviewer reran those 69 checks in 2.14 seconds and found the blocker resolved with no additional scoped findings. [CI run 42969833368](https://github.com/RealMonoid/AQRS/actions/runs/42969833368) passed all four jobs at the same revision: Ubuntu 24.04 Python 3.11/3.12 (121 tests in 26.97/39.56 seconds) and Windows Python 3.11/3.12 (121 tests in 46.71/40.69 seconds). Linux asserted non-root execution. Every job also passed synthetic planning/run, evidence verification, lint and both language gates. The [durable verification record](../evidence/aqrs-a07-verification.json) preserves the commands, source revision, job identities, log excerpts, independent-review correction and synthetic examples beyond CI retention.

**Resources and diagnosis.** The measured interval from the saved 05:40:00 UTC baseline to final-code review and CI capture at 06:07:30 UTC was 1,651 seconds (27.5 minutes); initial orientation and subsequent documentation/publication are outside this interval. No new real-data campaign, coverage count, market outcomes, protected reads, estimator family, paid service or research-budget increase. New regression fixtures and precision calculations use zero fits; existing full-suite and synthetic CI fits retain their existing limits. The close/open gap was a design error caught in independent preacceptance review and corrected within the same engineering loop; no market result was affected. No separate incident was invented. Historical bundle/scripts/configuration bytes and historical exposure records remain unchanged. The only new research variant is planned V2, with no market attempt or qualified coverage.

**Next decision.** Keep M2-E14 `WAITING`. Its next objective is to decide what the small proposed campaign can establish, freeze the complete eligible opportunity population and justify the uncertainty assumptions before implementing its campaign entry. A technical/descriptive result and an adequately powered effect claim are different deliverables. V2 needs its own authorized coverage check before any price-drop outcomes. Existing prerequisites, the protected-day reservation and no-retuning rules remain binding; no new campaign is automatically dispatched by this engineering acceptance.

### AQRS-A06 Test Card: audit controls and recoverable evidence

**2026-11-11.** Owner authorization covers the discussed audit remediation and the M2-E14 readiness review. This engineering sequence adds no real-data campaign, protected evaluation, threshold search or scientific evidence. Existing archived outputs remain immutable. Baseline: commit `f102b06` plus the pre-existing working-tree documentation; exact bytes are retained in `artifacts/aqrs-a06/baseline/`. The current Windows suite has 35 passing tests, while default discovery also collects a vendor suite under ignored artifacts. F2/F5 are open; 26 journals contain 43 campaigns and 80 experiment records, not 80 independent variants.

**Hypothesis and backward proof.** Reusing the existing validated configuration, worker supervisor, journal and canonical records can make admission and status contracts consistent and evidence recoverable without a new research service. Pass only when expired/tighter/unsupported budgets reject before data staging or fits; source preparation and research workers obey the shared deadline; unexpected ordinary exceptions terminalize the journal; pilots retain valid execution/evidence statuses; and a real synthetic LightGBM path is tested. Document the exact control-plane I/O boundary rather than claim a kernel deadline for receipt persistence. Keep historical variants and configured costs unchanged; flag zero-cost assumptions visibly. Add source/environment/schema identity without pretending to recover missing historical source.

**Evidence proof.** Build a version-controlled exposure index that distinguishes scientific variants, attempts, synthetic checks, count-only screens and platform replays, with dates and original journal/receipt references. Preserve unknown history explicitly. Version the necessary historical scripts and frozen configurations as audit inputs, create a bounded digest manifest of the acceptance evidence, and verify an archive round-trip; a manifest alone is not a backup. Require a separately published Test Card before future outcome runs; historical ordering remains unproven. Preserve the January 6 reservation and describe literal access fields as authorization metadata, not measured reads. M2-E14 already specifies minimum coverage; do not change its thresholds.

**Forward execution, budget and stops.** First run negative regressions against the baseline, then the smallest coherent fixes, focused positive/negative tests, independent read-only review, the complete native Windows suite and a real non-root Linux check. Record actual commands and outcomes. Expected one-time effort 2–4 hours; stop and reassess before eight hours total or a required scope/budget change. Zero new real-data fits, archive payload analysis, protected reads or paid services; synthetic fixtures only, existing per-campaign limits unchanged. Additional recurring work is small configuration/provenance I/O and one bounded exposure/evidence refresh per accepted campaign. A bounded local archive and an existing private Git remote provide the first retention route; report any missing independent storage or restoration proof. Risk is critical (admission, journal, evidence); apply FTA-AQRS-A06 in the risk register. Stop dependent research if any required control remains unverified. The final action is a readiness review, not automatic M2 acceptance.

### AQRS-A06 verification checkpoint

**2026-11-11.** Native Windows Python 3.12.12: the initial nine audit regressions produced eight failures and one passing control (2.53 s). Three further negative cases exposed missing fit reservation, preparation failure classification and provenance fields. After correction, `python -B -m pytest -q -p no:cacheprovider --tb=short --basetemp .venv/aqrs-a06-suite-2` passed all 51 tests in 73.58 s. This includes the real six-fit synthetic Ridge/LightGBM comparison through archived workers, a blocked preparation worker, existing causal/fill controls, and journal failure handling. No market-data campaign was run.

A separate reviewer reproduced and checked correction of lost committed SQLite WAL records, Windows archive-name collisions, preparation-resource aggregation and Governor metadata contaminating scientific identity. The existing Isolation Forest fit/calibration fixture now uses separate trial directories, matching production isolation. The reviewer verified archived-worker fit rejection with zero completed fits and no metrics; ten focused checks and six Isolation Forest checks passed. The archive builder additionally enforces serialized size limits and includes bar cadence in reconstructed variant identity.

Both language commands, Ruff and `pip check` passed; default pytest discovery now targets only AQRS tests. The source-language handoff was moved intact from `docs/QUANT_RESEARCH_CODEX_HANDOFF2` into non-normative `artifacts/aqrs-a06/source-material/QUANT_RESEARCH_CODEX_HANDOFF2`; suffixless documentation is now checked. `evidence/acceptance.zip` contains 295 files (about 10 MB compressed), with a verified full restoration and 26 integrity-checked SQLite snapshots. The eight historical scripts and 43 frozen campaign configurations are preserved; the index records 80 attempts, count-only exposures and two planned M2-E14 definitions without claiming complete historical exposure or new alpha.

At this intermediate checkpoint, Linux, remote retention and final independent closure were pending. The Learning Card below records their subsequent verification. M2-E09 source binding and historical preregistration remain unproven; no rerun is represented as recovery of an original run. The source/report persistence boundary and pilot parent-side I/O limitations are explicit in README and the Governor contract.

### AQRS-A06 Learning Card: audit controls and recoverable evidence

**2026-11-11. Result: `SUPPORTED / PERSEVERE` for the bounded engineering correction.** Adopt the tested admission, fit reservation, terminal-status, provenance and evidence-retention changes. Close AQRS-A02-F2 and F5 within the documented execution boundary. Preserve the original research outcomes and open M2 acceptance criteria. The independent read-only reviewer found no further code blocker for this scope at `70005cc74d6e76b541455841566773c2622d41f8`.

**Platform and restoration proof.** [GitHub Actions run 42956133504](https://github.com/RealMonoid/AQRS/actions/runs/42956133504) passed all four jobs at that exact code revision: Ubuntu 24.04 with Python 3.11/3.12 (51 tests in 33.59/28.80 seconds) and Windows with Python 3.11/3.12 (51 tests in 48.83/43.89 seconds). The Linux jobs explicitly asserted non-root execution and used a non-UTC timezone. Each job installed the development extra, ran synthetic CLI planning and execution, verified the preserved bundle, and passed tests, lint and both language gates. The [durable verification record](../evidence/aqrs-a06-verification.json) preserves job identities, output excerpts, local results and independent-review limits beyond the CI artifact retention period.

`git clone --depth 1 --branch audit/aqrs-a06 https://github.com/RealMonoid/AQRS.git artifacts/aqrs-a06/remote-restore` exited 0. Running the cloned `scripts/evidence_archive.py --verify --restore artifacts/aqrs-a06/from-remote` exited 0 and restored all 295 files, including 26 readable SQLite snapshots. The ZIP matched its recorded SHA-256; parsed manifest, configuration and exposure records matched after Git line-ending normalization. A raw-byte JSON comparison was replaced with this content comparison because Git normalizes text line endings. The ZIP and member digest checks remained byte-exact. This proves recovery from the private remote, not unlimited retention or missing historical provenance.

**Resources and remaining boundaries.** Approximately three hours elapsed from the saved 01:11:47 UTC baseline through implementation, review, CI and restoration checks; final documentation followed within the four-hour estimate. The synthetic checks used existing limits; no new market-data campaign, forward-outcome analysis, protected-day access, paid service or recurring campaign was added. One local pinned LightGBM installation and the existing four-job CI matrix supported verification. The preserved ZIP is about 10 MB. Source/report persistence and final cleanup are outside the core worker deadline; pilot parent archive/report I/O also remains outside a hard deadline. RSS remains observed, not a hard OS memory cap. Cross-campaign budget aggregation remains deferred.

**Readiness decision.** M2-E14 can reuse the corrected controls, but the existing four-day pilot is not its ten-day campaign implementation. Before its run, bind a separately published card and exact candidate definitions to the campaign source/configuration, validate its two folds and five-fit budget, and pass its causal and matched-control tests. Its existing minimum counts and scientific thresholds stay unchanged. The versioned exposure index includes both planned definitions without claiming that they ran. Historical source linkage, independently dated historical rules and unknown manual exposure remain unresolved; no higher alpha status or M2 acceptance is granted.

### AQRS-A05 Test Card: observable deferral

**2026-11-10.** The riskiest assumption is that the existing queue rules and milestone record can make parked decisions visible without adding a status or tracker. The read-only deferral audit found that the baseline records prerequisites and revisit conditions, while a closed attempt can leave its remaining decision without a named observation point. Use the existing M2-E14 and M2-E12 cards, AQRS-A02-F2 risk record, and M2-E09 learning and acceptance records as prior evidence. The smallest test is a before-and-after walkthrough on these four cases.

Pass if E14 still waits for its named data and run authorization, and F2 blocks only reuse of the affected admission flow until independently verified. At qualification of a new BTCUSDT development window capable of supplying the missing band, Quant Research must find E12's existing three-band and three-date condition, keep the rule frozen, and propose an outcome study only after qualifying coverage and separate authorization for execution. For E09, the same fixed comparison on the same evidence stops as a research follow-up. A materially new observation can justify a new proposal. Technical parity, missing source binding, and the existing route for a separately authorized provenance replay remain distinct. Require a named observation point, the decision that could change, and a current default for material deferrals. Trigger satisfaction prompts review. Existing start conditions still apply.

Use the same focused check before and after the edit. Preserve earlier queue rows, priority, dispositions, and evidence. Check the new links, exact changelog paths, English prose, and whitespace. A pass supports the scoped rule. On failure, revise within scope or stop if a new workflow or authority would be needed. The expected benefit is reduced repeated review at the cost of one short documentation session of up to 30 minutes. Zero campaigns, fits, market-data payload or protected reads, spend, or recurring compute. Governance risk screen only. No runtime contract or acceptance threshold changes, so FTA is not triggered. Stop after focused checks and documentation gates.

### AQRS-A05 Learning Card: observable deferral

**2026-11-10.** `SUPPORTED / PERSEVERE` for the documented governance rule. E14 still waits for named data and run authorization. F2 requires an independently verified check before reuse of its admission flow. E12 remains frozen and becomes visible when Quant Research qualifies a window that could cover the missing UTC band. The unchanged E09 comparison ends on the same evidence. A materially new observation can justify a new research proposal, while source binding remains a separate M2 acceptance question. The E12 walkthrough used the existing order of gates. Qualifying coverage permits a proposal. Separate authorization is required for execution.

The focused rule check ran on Windows with `python -B -`. It exited 1 with 2 of 6 criteria met on the baseline and exited 0 with all 6 met after the edit. The scoped `python -B -` check passed for the exact three changed paths, changelog, local links, prior queue rows and historical records. Both language checks, manual review of the edited English prose, and `git --no-optional-locks diff --check` passed. About 166 seconds elapsed from the baseline snapshot through the recorded decision. Zero new campaigns, fits, market-data payload or protected reads, spend, or Linux runs. The walkthrough establishes what the rules require. Adoption and interruption rates remain unmeasured. No postmortem or consequential approach rejection applies. E14 is still the first pending campaign and requires its named authorization and applicable path clearance.

### AQRS-A04 Test Card: decision-ready cards

**2026-11-10.** The riskiest assumption is that one clarification of the existing process can make decision criteria verifiable before work while reducing routine card overhead. The baseline required a card before implementation but did not explicitly cover the first contributing result, the lifetime of a shared test across setup attempts, or the end of measured work. The audit found a late tolerance in M1-E04 and a complete pre-run plan under a different heading in M2-E09. The smallest test is a before-and-after rule walkthrough with existing records.

Pass if the rules reject the late tolerance as predeclared, accept the earlier complete M2-E09 plan, route a known reporting-field correction to its ordinary change and check record, preserve one test contract with separately recorded setup attempts, and continue eligible work inside the current mandate. Check that a material change still requires a new decision under the existing rules. Keep M2-E09 outcome parity separate from source reproducibility. Require a check of existing source evidence first and a separate authorization and path clearance if a replay is needed. Name the endpoint of measured working time and distinguish avoided actions from measured savings. Preserve prior queue rows, historical cards, research contracts, and release gates. Verify the rule text, scenarios, local links, exact changelog paths, and English prose.

The expected decision value is a clearer start and close decision at the cost of one short documentation session. Timebox 30 minutes. Zero campaigns, fits, market-data payload or protected reads, spend, or recurring compute. Governance risk screen only. No runtime, protection, or acceptance threshold change, so FTA is not triggered. Stop at the focused checks and documentation gates, or earlier if the work requires a new authorization.

### AQRS-A04 Learning Card: decision-ready cards

**2026-11-10.** `SUPPORTED / PERSEVERE` for the documented rules. In the walkthrough, the M1-E04 tolerance was late and the complete M2-E09 replay plan qualified under its earlier heading. A known reporting-field correction used an ordinary change and check record. Setup attempts shared the acceptance proof, kept separate evidence and charges, and continued only within the existing mandate. The M2-E09 archived reports matched the parity receipt and lacked executed-source references. The M2 gate now directs the reviewer to check existing evidence first and requires separate authorization and applicable path clearance if a replay is needed.

The focused `python -B -` rule check exited 1 with one of nine assertions met on the baseline. After clarifying the wording for prior evidence, all nine passed with exit 0. The scoped file, changelog, link, and preservation check, the receipt check, both language checks, manual English review, and `git diff --check` passed on Windows. About 194 seconds elapsed from the baseline snapshot and skill review through this decision. Zero campaigns, fits, market-data payload reads, protected reads, spend, or fresh Linux runs. Actual adoption and time savings remain unmeasured. M2-E14 remains the first pending campaign and awaits its named data and run authorization. AQRS-SC01 remains deferred.

### AQRS-A03 Test Card: authorized continuation

**2026-11-10.** The baseline requires continuation but leaves the reporting boundary and cross-item dispatch mandate implicit. Test whether clarifying the existing rules produces the intended decisions without adding approval gates. Pass if a walkthrough continues through the M2-E08 routine regression fix and the M2-E10 authorized Ubuntu replay, starts an eligible follow-up inside an authorized sequence, and blocks an extra M2-E09-type campaign attempt, M2-E14 data access, work outside a standalone item, and continued work once actual time plus estimated remaining time reaches eight hours. Check that a routine blocker report identifies a resumption condition without inventing an owner decision, and that completing a checkpoint does not trigger a chat handoff. Preserve all existing queue rows, their order and start conditions, independent verification, and research and release gates. Run a focused baseline and revised rule comparison, link and changelog checks, and both language checks. Governance risk screen only. The changes affect Codex's working method and leave all runtime and protection contracts in place. FTA not triggered. One documentation session of up to 30 minutes, with zero campaigns, fits, archive reads, protected reads, spend or recurring compute. Stop after the walkthrough and documentation checks.

### AQRS-A03 Learning Card: authorized continuation

**2026-11-10.** `SUPPORTED / PERSEVERE` for the documentation. The walkthrough continued through the M2-E08 regression fix and the M2-E10 replay after valid Windows results. It dispatched a ready follow-up inside an authorized sequence and closed a standalone item at its agreed boundary. An extra campaign attempt, M2-E14 archive access, and a revised estimate of seven hours and twenty minutes spent plus forty minutes remaining all required approval. A routine setup issue called for a resumption check, and checkpoint completion alone did not trigger a chat handoff.

The focused `python -B -` rule check exited 1 on the baseline with five missing clarifications and exited 0 after the edits. The exact changelog paths, new links, and all 27 prior queue rows and their order were checked. Both language checks, manual English review, and `git diff --check` passed on Windows. About three minutes elapsed through the walkthrough and evidence review. Zero new campaigns, fits, archive reads, protected reads, spend or fresh Linux runs. The check evaluated the documented decisions. The rate of avoidable owner interruptions in future sessions remains unmeasured. M2-E14 still awaits its named data and run authorization.

**AQRS-A02 Test Card, 2026-11-10.** The riskiest assumption is that one rule in the existing queue can pause every row that depends on a material finding without delaying independent eligible work. The baseline has separate finding and dispatch records but no required link or resumption check. Pass if the rule yields the same dispatch decision for an active direct dependency, a ready indirect dependency, independent work, a later path selection, closure evidence with authorization still missing, and closure with all prerequisites met. Preserve closed evidence and the one-active-experiment limit. Apply the rule to the two open Governor findings, distinguish M2-E09 parity from source reproducibility, and attach the timezone check to the next applicable platform verification. Verify the affected paths, existing receipts, links, exact changelog paths, and English prose. Governance risk screen only, with no change to a research, runtime or release contract and no new FTA. Timebox one session of up to 30 minutes. Zero campaigns, fits, archive payload reads, spend or recurring compute. Stop after the focused scenarios and documentation checks.

**AQRS-A02 Learning Card, 2026-11-10.** `SUPPORTED / PERSEVERE` for the queue rule. In the walkthrough, the active replay and its ready downstream consumer moved to `WAITING`, independent work stayed eligible, and a later path choice inherited the applicable Governor condition. Recorded closure evidence alone kept a row waiting for authorization. A row with verified closure and all other prerequisites met returned to `READY` for normal dispatch. Historical results stayed intact. M2-E09 outcome parity is recorded as met, with source reproducibility open for M2 acceptance. The two execution-path findings remain open before reuse. T20 timezone verification travels with the next applicable platform check. The focused `python -B -` check failed on the baseline and passed after the change. The receipt, link, exact changelog coverage, and preservation checks, manual English review, both language checks, and `git diff --check` passed on Windows. About 191 seconds elapsed from the baseline snapshot through the evidence review. Zero campaigns, fits, archive payload reads, spend, or fresh Linux runs. M2-E14 still awaits the named data and run authorization.

**Baseline rule question Test Card, 2026-11-10.** The owner adopted the question prompted by Ernest P. Chan's *Quantitative Trading* (2nd ed., 2021, preface and Example 7.1). The protocol already calls for matched controls. Pass if it states the question in the existing controls section and a reader can identify the base rule, changed decision, prespecified improvement threshold, and fair comparison from the M2-E10 card. Link the question from the current campaign planning priority and verify the links, language, and exact changelog paths. Routine documentation change with no critical contract changes. FTA not triggered. Timebox 15 minutes, with zero trials, fits, new data access, spend, or recurring compute. Stop after the focused checks.

**Baseline rule question Learning Card, 2026-11-10.** `SUPPORTED / PERSEVERE` for documenting the research question. The M2-E10 walkthrough identified the volatility-only rule, the extra alert filter, the common hourly opportunities and execution assumptions, and the registered coverage and improvement thresholds. The focused `python -B -` check initially mishandled a newline in the changelog comparison and exited 1. The corrected check, both language checks, manual English review, and `git diff --check` passed on Windows. About 100 seconds elapsed through the focused check. Zero new campaigns, fits, data reads, or platform runs. The next campaign Test Card will apply the question where a candidate changes a baseline rule.

**Research capability handoff Test Card, 2026-11-09.** The current evidence handoff starts at experiment registration and gives a path for completed evidence and defects. The M2-E10 card names a separate scoring path as necessary, although its observable requirement is to keep anomaly scoring and directional prediction separate. Pass if the existing handoff assigns capability and scientific constraints to Quant Research, technical design to Engineering, and any scientific or scope change to the existing return and approval paths. Use M2-E10 to verify that only the proposed technical path wording changes. Check the five role-boundary scenarios, links, exact changelog paths, and language. Routine documentation risk. FTA not triggered. One short documentation session, zero trials, fits, or new data access. Stop after the focused checks.

**Research capability handoff Learning Card, 2026-11-09.** `SUPPORTED / PERSEVERE` for the documentation. The focused check matched the role boundaries to the existing authorization and preflight rules. The five walkthroughs covered a new capability, a look-ahead label, technical completion with an unmet research criterion, a method outside scope, and a resource conflict. The M2-E10 card matched its baseline except for the scoring implementation wording. M2-E10 stays `WAITING`. Archived M2-E09 evidence supported technical replay while the scientific follow-up stayed `DEFER`. Links, exact changelog paths, both language checks, manual review, and `git diff --check` passed on Windows. The focused check ran about 70 seconds after the baseline snapshot. Zero runs, fits, or new data access. The handoff has yet to be used on an authorized new implementation.

**Reporting field alignment Test Card, 2026-11-09.** The research interpretation rule names `pipeline_completed`, which the CLI does not emit. Pass if the rule identifies the actual process, evaluation, and evidence fields, links the existing reporting contract, and leaves all checks and acceptance criteria in place. Verify the exact edit, links, changelog, and both language checks. Routine documentation risk. FTA not triggered. One short documentation session with zero research runs or fits. Stop after these checks.

**Reporting field alignment Learning Card, 2026-11-09.** `SUPPORTED / PERSEVERE` for the documentation correction. The focused check matched the three field names to the CLI and the reporting contract, validated the existing verification triggers and dependent-work rule, and confirmed the exact changelog paths. A scenario review used M2-E10 waiting for authorization and the archived M2-E09 technical replay with `DEFER` for the research decision. Both language checks, manual review, and `git diff --check` passed on Windows. The focused check ran about 46 seconds after the baseline snapshot. Zero new research runs, fits, or Linux runs.

**AQRS-A01 Test Card, 2026-11-09.** Correct audit findings F1–F4 in one bounded increment. The riskiest assumption is that a fixed local date contract blocks the reserved-day route before any input or fit while preserving the approved development path. Baseline evidence includes the intercepted January 6 import, archived M2-E08/E09 receipts without source binding, the completed M1-E04 economic screen without candidate evaluation, and conflicting onboarding instructions. Require early rejection, a recoverable pilot and AQRS source snapshot with environment references in new receipts, an explicit screen outcome with successful process exit, and unambiguous onboarding links. Verify legacy artifacts against their baseline hashes and describe any unrecoverable historical provenance. Apply FTA-M1-B and independent read-only verification. Timebox one focused engineering and verification sequence under eight hours. Use existing local dependencies, targeted synthetic tests, and existing receipts. Zero real-data campaigns, protected reads, market-data downloads, or spend. Stop at the focused checks or the first blocker that requires expanded authorization.

**AQRS-A01 Learning Card, 2026-11-09.** `SUPPORTED / PERSEVERE` for the four audit corrections. The two initial regression cases failed on the baseline for the missing evaluation status and the reserved date reaching the import path. Five focused cases and the full Windows suite passed after correction (29 tests, exit 0). An independent read-only reviewer verified F1–F4. The final no-fit snapshot check verified the archived worker handshake under an inherited safe-path setting. The report and journal agree on source digests and dependency metadata. Ruff, formatting, both language checks, `git diff --check`, links, and exact changelog path coverage passed. Historical receipts and scripts retained their baseline hashes. The exact historical M2 source could not be bound to the archived runs. About 442 seconds elapsed from the baseline snapshot to the final evidence record. No real-data campaign, protected read, market-data download, spend, or fresh Linux run. The M2-E10 start condition and milestone acceptance remain governed by the existing queue and DoD.

**Verification and research handoff Test Card, 2026-11-09.** Separate review and research decisions using the existing records. The baseline has a stale M0 scope statement and no explicit handoff between technical and scientific decisions. Pass if the scope points to current start conditions and recorded owner authorization, critical contract changes and milestone acceptance require a separate read-only review against fixed criteria, and research disposition follows the preregistered plan using admissible evidence. Trace M2-E08 as a blocked comparison and M2-E09 as a technically reproduced development variant with a missed benefit criterion. Verify links, language, and exact changelog paths. Routine documentation risk. FTA not triggered. Timebox one focused session, zero new research campaigns, fits, protected reads, or recurring runtime cost. Stop after the focused checks.

**Verification and research handoff Learning Card, 2026-11-09.** `SUPPORTED / PERSEVERE` for the documentation. The focused check verified the scope source, separate review assignment, scientific handoff, links, and exact four changelog paths. A read-only check of archived reports found no paired decision in M2-E08. The completed M2-E09 Windows and Ubuntu reports matched the archived comparison IDs and input fingerprints. Applying the predeclared rule to both reports yielded `DEFER` despite technical completion. Both language checks, manual English review, and `git diff --check` passed on Windows. The focused check ran about 78 seconds after the baseline snapshot. Zero new campaigns, fits, protected reads, or platform replays. Application to a new eligible change remains untested.

**Root instruction alignment Test Card, 2026-11-09.** The three root rules can match their governing documents without changing the rest of the instructions. The baseline defers all status-file updates until after testing, permits ambiguity about the required M2 pilots, and limits preflight to expensive runs. Pass if Test Cards precede implementation and only acceptance requires passing evidence, the M2 pilot rule links to the applicable gate, and every research campaign requires preflight. Verify the exact three root edits, links, changelog paths, and both language checks. Routine documentation risk. FTA not triggered. Timebox 15 minutes and zero research runs or fits. Stop after the focused checks.

**Root instruction alignment Learning Card, 2026-11-09.** `SUPPORTED / PERSEVERE` for the documentation. The focused check confirmed exactly three root edits, valid links to the governing sections, and exact changelog coverage. Reversing the three replacements reproduced the baseline root hash. Both language checks, manual English review, and `git diff --check` passed on Windows. The focused check ran about 73 seconds after the baseline snapshot. Zero research runs or fits.

**Requirements mode boundary Test Card, 2026-11-09.** An explicit invocation and directory-local records can keep requirements work within its scope without losing access to earlier decisions. The baseline has no explicit trigger in the root instructions and directs new question and decision writes outside the requirements directory. Pass if both trigger phrases route to the scoped role, all requirements write targets are local, and earlier records remain readable and unchanged. Also pass a read-through of a vague owner request. The role must investigate wishes, unmet needs, and future concerns, explain viable options in plain German, and derive a bounded proposal for owner approval. Verify links, language, and changed paths. Routine documentation risk. FTA not triggered. Timebox 15 minutes and zero research runs or fits. Stop after the checks or narrow the edit if the record boundaries overlap.

**Requirements mode boundary Learning Card, 2026-11-09.** `SUPPORTED / PERSEVERE` for the documentation. The focused review verified both trigger phrases, local write targets, relative links, and the seven changelog paths against the baseline. A read-through of a hypothetical request for clearer research progress traced workflow review, plausible interpretations, a focused question, and a bounded proposal with owner approval. Existing project question and decision records matched their baseline hashes. Both language checks and `git diff --check` passed on Windows. The focused check ran about 112 seconds after the baseline snapshot. Zero research runs or fits. Invocation in a separate Codex session was outside the documentation check.

**Requirements role Test Card, 2026-11-09.** A scoped role and a central register can make an approved requirement traceable to its source and acceptance criterion while keeping one record for each open question and decision. The baseline has only the general Codex assignment and distributed requirements. Pass if the root instructions route to one documentation-only role, a seeded register separates confirmed requirements from proposals, and one sample requirement can be traced through its source and criterion while unresolved choices route to the existing files. Check relative links, language policy, and the exact changed paths. Routine documentation risk. FTA not triggered. Timebox 30 minutes, zero research runs, fits, or recurring runtime cost. Stop after the focused checks or revert only this increment if the documentation creates conflicting authority.

**Requirements role Learning Card, 2026-11-09.** `SUPPORTED / PERSEVERE` for the documentation. The focused check traced FR-002 to the M2 acceptance criteria and verified the role links and both canonical records. File hashes matched the baseline outside the six changelog paths. Both language checks, manual English review, and `git diff --check` passed on Windows. The build and focused review took about 110 seconds from the baseline snapshot. Zero research runs or fits. Existing milestone evidence remains the basis for platform acceptance.

**Diagnosis split Test Card, 2026-11-09.** Pass if technical stops and functional failures have different required evidence, invalid research results are excluded from decisions, and the existing Learning Card and Research Journal remain the entry points. Routine documentation risk. FTA not triggered. One short documentation session, zero research runs. Stop after the focused and language checks.

**Diagnosis split Learning Card.** `SUPPORTED / PERSEVERE` for documentation. The focused review confirmed separate evidence for the two failure types, retained the benefit and uncertainty outcomes, and checked the Research Journal guidance. Elapsed time through the focused review was about 34 seconds. Zero research runs.

**Diagnosis template Test Card, 2026-11-09.** Pass if the shared template distinguishes a technical stop, a valid result below the benefit criterion, and an inconclusive result, and both existing records can use it. Check the existing status mappings and changelog. One short documentation session, zero research runs. Routine documentation risk. FTA not triggered.

**Diagnosis template Learning Card.** `SUPPORTED / PERSEVERE` for documentation. The focused check confirmed the three outcomes, evidence fields, Research Journal link, and existing status contract. Elapsed time through the focused review was about 87 seconds. Zero research runs.

**Requirements ownership Test Card, 2026-11-08.** The owner delegated requirements engineering to Codex. The baseline asks Codex to recommend a next step, with no explicit responsibility for deriving requirements when the owner is unsure. Pass if the working method assigns Codex the proposal and testable acceptance criteria, preserves owner approval and routine autonomy, and handles uncertainty without requiring technical decisions from the owner. Verify the wording against the existing Test Card and approval rules, reconcile the changelog paths, and run both language checks. Budget one short documentation session and zero research runs or fits. Routine documentation risk. FTA not triggered.

**Requirements ownership Learning Card.** `SUPPORTED / PERSEVERE` for the documentation. The focused review confirmed the requirements assignment, existing Test Card link, approval boundaries, queue status and all three changelog paths. Elapsed time from the Test Card edit through the focused review was about 46 seconds. Zero research runs or fits.

**Experiment value Test Card, 2026-11-08.** The current card and queue rules can distinguish a justified longer test from a cheap test that cannot change the decision. Pass if both state the trade-off and retain approval, budget, and evidence gates. Use one documentation session and zero research runs. Stop after focused and language checks. Routine documentation risk. FTA not triggered.

**Experiment value Learning Card.** `SUPPORTED / PERSEVERE` for the documentation. The focused review confirmed the Test Card and ranking rules cover justified longer tests, cheaper evidence, and remaining costs at checkpoints. The current queue and Resource Governor matched their baselines.

**Mechanism Test Card, 2026-11-08.** The existing cards can capture rival explanations and update the queue in two short fields. Pass if both fields guide material decisions and existing queue entries remain intact. Budget is one documentation session and zero research runs. Stop after the focused review and language checks. Routine documentation risk. FTA not triggered.

**Mechanism Learning Card.** `SUPPORTED / PERSEVERE` for the documentation. The focused review found both prompts in the existing cards and confirmed that both M1 queue entries remain waiting.

**Lean policy Test Card, 2026-11-08.** The existing cards can govern feature adoption and founding decisions without new tooling. Pass if the chat trigger, provisional adoption rule, venture decision criteria, and bounded M1 source check are traceable across the documents. Use one focused documentation session and zero research runs. Stop after reviewing the diff, changelog, and language checks. Routine documentation risk. FTA not triggered.

**Lean policy Learning Card.** The diff and baseline comparison show that the rules and M1 screen fit the existing documents. The language detector self-test passed. The repository audit still reports the same 314 findings in the pre-existing untracked handoff. Keep the policy and leave M1 execution pending.

**Feature proposal Test Card, 2026-11-07.** The current rules require run
preflight but do not require a visible resource assessment on every feature
proposal. Pass if the new rule covers every proposal before approval or
implementation, separates development and runtime costs, and points to the
existing budget and run preflight. Verify the diff, changelog, and language
checks, and confirm that the budget configuration is unchanged. Stop after
documentation checks. Budget is 15 minutes and zero research runs. Routine
documentation risk. FTA not triggered because enforcement is unchanged.

**Feature proposal Learning Card.** `SUPPORTED / PERSEVERE` for the
documentation. Both language checks and `git diff --check` passed on Windows.
The review confirmed the proposal rule, existing preflight, and the four paths
in the changelog. The budget configuration matched its baseline hash. The
review is a proposal requirement, and the CLI continues to enforce run limits.

**M2 screening Test Card, 2026-11-07.** The protocol calls for cheap screens
but leaves the next decision implicit. The smallest check is a document review
that traces the price-drop example from a bounded, zero-fit screen through
advance, defer, and stop outcomes. Pass if the screen evaluates the decision
region, the next test uses a later research window, and M1 records three stage
timings within its first real-data run. The governor configuration and policy
must have identical hashes to the baseline. Run both language checks and
check the changelog against the diff. Budget is one 20-minute documentation
session and zero research runs. Stop after these checks. FTA not triggered.
This documents a future study without modifying timing or enforcement contracts.

**M2 screening Learning Card.** `SUPPORTED / PERSEVERE` for the documentation.
The diff review confirmed matched comparisons, explicit next decisions, and
the three M1 timing measurements. Both language checks and `git diff --check`
passed on Windows. The changelog matched the five changed documents, and the
governor configuration and policy hashes matched the baseline. The first real
run and the event study remain open.

**M2 planning Test Card, 2026-11-07.** The current discovery gate permits event
studies without specifying how to define their events. The documentation check
passes if the protocol and M2 gate require an observable, causal event, preserve
data-driven discovery, and agree with the decision ledger on the recurring raster
test. Review the diff, reconcile the changelog and run both language checks.
Stop after documentation verification. Budget is one 20-minute session and zero
research runs. Routine documentation risk. FTA not triggered because the existing
timing, execution and holdout contracts are outside the change.

**M2 planning Learning Card.** `SUPPORTED / PERSEVERE` for documentation
alignment. The diff review confirmed the event definition, the existing discovery
paths, and the rejection in IDEA-004. Both language checks and `git diff --check`
passed on Windows. The changelog covers the five changed documents. M2
implementation and runtime acceptance remain open.

**M0-03 Test Card.** The previous hosted matrix passed with a Node.js 20 warning.
The assumption is that changing the three Action references to releases that declare
Node.js 24 clears that warning while all four jobs and artifact uploads still pass.
The smallest proof is one push-triggered matrix and a search of all four job logs.
The budget is one matrix with the existing 15-minute job caps and one focused
30-minute development session. A failed job or a repeated warning fails the check.
Risk screen: routine CI maintenance. FTA not triggered.

```text
Loop ID: M0-01
Milestone: M0/v0.1
Backward proof: deterministic UTC bars, causal features and exact label timing in purged folds.
Assumption: a research-only bar prefix suffices to build all fold features and labels.
Risk: critical. FTA-M0-A in RISK_REGISTER.md.
Prior ideas: IDEA-001 to IDEA-003 checked. No sweep or parallel development.
Baseline: documentation package with no runnable Python implementation.
Pass: stable fingerprint, future perturbation leaves prior features intact, invalid bars fail,
      horizon-3 uses open[t+1] to open[t+4], no label crosses its fold or holdout boundary.
Fail/stop: any future dependence, malformed data accepted, or empty fold treated as usable.
Budget: one focused session up to 15 minutes. Unit tests only, zero fits.
Incident: NOT_TRIGGERED.
```

M0-01 learning: `SUPPORTED / PERSEVERE`. The focused Windows test initially exited 1
with the market module absent, then exited 0 with 3 tests passing (0.35 s).
The next proof is a supervised two-candidate run with durable outcomes.

```text
Loop ID: M0-02
Milestone: M0/v0.1
Backward proof: CLI admits only bounded plans and produces auditable outcomes for both candidates.
Assumption: isolated sequential workers can enforce M0 budgets and preserve fair research evidence.
Risk: critical. FTA-M0-A, FTA-M0-B, cost and persistence controls in RISK_REGISTER.md.
Prior ideas: IDEA-001 to IDEA-003 checked. Fixed two-candidate schedule with no search.
Baseline: causal data path tested, with no research execution, governor or journal.
Pass: 75,000 fits rejected before work, strict unavailable memory rejected, blocking and RSS
      workers stopped, journal persists outcomes, and identical runs reproduce research metrics.
Fail/stop: any limit bypass, survivor, leakage, partial result counted as complete or lost attempt.
Budget: one focused session up to 45 minutes. Configured 120 s/trial and 300 s/campaign,
        at most 2 candidates, 1 seed, and 12 total fits including a bounded pilot.
Incident: M0-INC-01 and M0-INC-02 below.
```

### M0-02 acceptance evidence, 2026-11-06

Native Windows 11 Pro x86_64 build 26300 used a non-administrator account. Ubuntu
24.04.5 LTS x86_64 kernel 6.8.0-147-generic ran in a separate headless QEMU guest
with WHPX, as UID 1000 and with guest egress disabled. Each used a clean CPU-only
virtual environment. The Linux dependency installation used a local wheelhouse.

All commands below exited 0 in each of the four environments.

```text
python -m pip install -e ".[dev]"
python -m aqrs research plan --config configs/research.yaml
python -m aqrs research run --config configs/research.yaml
python -m aqrs research run --config configs/research.yaml
python -m pytest -q
python -m ruff check .
python scripts/check_language_policy.py --self-test
python scripts/check_language_policy.py
```

| Environment | Python | Plan ID | Completed run IDs | First run wall seconds | Sampled peak MiB | Sampled CPU seconds |
|---|---|---|---|---:|---:|---:|
| Windows 11 | 3.12.12 | `d2191dc6291f4aa9a5a06fc4e0e0fb78` | `530f7957306743a3976df17c401277c2`, `3fc788772a8d45c68a8bab954889b65f` | 5.77 | 120.13 | 4.98 |
| Windows 11 | 3.11.14 | `be1dda1ec1854c4288f5ffa7aa8b1717` | `3a5020358d134fdc984cee23f97945f1`, `96809e464fbe437f8b5366f1cde1a123` | 5.42 | 118.70 | 4.58 |
| Ubuntu 24.04.5 | 3.12.3 | `24732f91dedd40a8bdcfe9f02830d569` | `baa9fb550c124fcc83c7318fc591b76b`, `072a7c0eb9334f069b844a21399cf488` | 3.46 | 122.56 | 3.02 |
| Ubuntu 24.04.5 | 3.11.14 | `cebea406ba7249a5af50d30e2fcf488b` | `95318570331540408b3965de81486667`, `fa352b62925b4cceb8ca0d54f940dd69` | 3.06 | 126.50 | 2.60 |

The Windows logs are `artifacts/windows-release-python{311,312}.txt`. The Ubuntu
logs are `artifacts/linux-m0/acceptance-release-python{311,312}.txt`. Each run
produced `dataset.csv`, `plan.json`, `report.json` and `report.md` under its
run ID. Find Windows runs and their SQLite journal under `artifacts/`, and the
Ubuntu equivalents under `artifacts/linux-m0/release-python{311,312}/`.
All campaigns completed two trials and seven fits, including one pilot.
SQLite integrity returned `ok` and both repeated trials in each environment
linked to the original evidence. Verified source fingerprint:
`2c8213e529e111c51f79e0db265da85245a0290510f30d2a926a3ecad1f91872`.

Both runs in each environment produced identical dataset bytes, research metrics,
fold intervals and holdout boundaries. Windows and Ubuntu fingerprints differ
with last-digit floating-point variation. In the Python 3.12 comparison, the
largest OHLC difference was about 1.1e-11. Timestamps, trade counts and decisions
matched. Both candidates recorded `INSUFFICIENT_EVIDENCE` on 2,988 OOS predictions,
made zero trades at the configured threshold and had higher MAE than the zero-return
control. The matched momentum control was negative net. The holdout was reserved.

The final suite passed 17 tests per environment. G01–G07 evidence includes the offline
CLI, 75,000-fit rejection before any fit, strict-memory rejection before launch,
sampled RSS termination, trial and campaign timeouts, process-tree and parent-loss
cleanup, durable timeout history, holdout perturbation and repeated-run accounting.
Windows used Job Objects. Linux used POSIX process groups and parent-pipe detection.
The 32 model entries and 19 infrastructure entries in the planning registry were retained.

**AQRS-A02 follow-up, 2026-11-10.** The explicit non-UTC local timezone evidence for T20 was not found in the archived acceptance record. Include this check in the next applicable Windows and Ubuntu platform verification by recording the local timezone and comparing the fixture's UTC timestamps with the reference.

**Incident M0-INC-01.** Initial integration review found that cancelling an active
candidate could still release the next candidate. Pilot cancellation was reported as a
preflight rejection. The scheduler did not treat cancellation as a terminal campaign
event. The correction propagates cancellation to remaining attempts and exit 130.
`test_cancellation_stops_remaining_candidates` verifies one supervisor call for the
cancelled candidate case and no candidate call after a cancelled pilot.

**Incident M0-INC-02.** During the first concurrent clean-environment verification,
a candidate and a test pilot each failed closed with a Windows `PermissionError`.
The exception site was not present in the initial journal reason. Transient sharing
around worker status files is a plausible cause. The watchdog now records the failing
operation and bounds Windows status-file rereads within the existing deadline. The
next full suite and both default campaigns passed. Track the site if the issue recurs.

**Learning:** `SUPPORTED / PERSEVERE` on the tested matrix. M1 remains outside the current authorization.

### GitHub Actions acceptance, 2026-11-06

The [AQRS M0 acceptance workflow](https://github.com/RealMonoid/AQRS/actions/runs/42274092987)
completed successfully at 18:50:47 UTC on commit `f881eb233e4de9c964eaebf136c5ce28da36a92a`.
The Windows jobs used the `windows-2025-vs2026` image (build 26100, AMD64).
The Ubuntu jobs used `ubuntu-24.04` (kernel 7.0.0-1017-azure, x86_64).

| Runner label | Python | GitHub job | pytest | AQRS campaign ID |
|---|---|---|---:|---|
| `windows-latest` | 3.11.9 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42274092987/job/128085821935) | 17 passed | `172b526229a84e47a4082fc2ec295d9f` |
| `windows-latest` | 3.12.10 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42274092987/job/128085821877) | 17 passed | `11f737c0d773478887c9db4bc3a0fd4b` |
| `ubuntu-24.04` | 3.11.18 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42274092987/job/128085821871) | 17 passed | `fb0c868d2e244e9a90ad7f861a0737ee` |
| `ubuntu-24.04` | 3.12.16 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42274092987/job/128085821457) | 17 passed | `d2d63163941c40629950b5bb42ba1277` |

Editable installation, CLI plan and run, pytest, Ruff, the language self-test and
audit, and artifact upload succeeded in all four jobs. Each campaign completed two
trials and seven fits including the pilot. The downloaded reports matched the local
acceptance source fingerprint, and all four SQLite integrity checks returned `ok`.
The logs, plans, reports, datasets and journals are preserved locally under
`artifacts/github-actions/42274092987/`.

This initial run reported a Node.js 20 deprecation warning for checkout, setup-python and
upload-artifact. The runner executed these actions on Node.js 24 and all jobs passed.

### M0-03 learning record, 2026-11-06

The workflow now uses `checkout@v5`, `setup-python@v6` and `upload-artifact@v6`.
The [rerun](https://github.com/RealMonoid/AQRS/actions/runs/42275704043) passed at
19:01:55 UTC on commit `5b29d1d5110bd35dca2782bf38bbbece9cc27cab`.

| Runner label | Python | GitHub job | pytest |
|---|---|---|---:|
| `windows-latest` | 3.11.9 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42275704043/job/128091379983) | 17 passed |
| `windows-latest` | 3.12.10 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42275704043/job/128091380233) | 17 passed |
| `ubuntu-24.04` | 3.11.18 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42275704043/job/128091380062) | 17 passed |
| `ubuntu-24.04` | 3.12.16 | [Passed](https://github.com/RealMonoid/AQRS/actions/runs/42275704043/job/128091379669) | 17 passed |

The Node.js 20 warning appeared once per job in the initial run and zero times in
the rerun logs. All four rerun job annotation lists were empty. Every artifact upload
succeeded. The reports retained the accepted source fingerprint and all four SQLite
integrity checks returned `ok`. The logs and artifacts are available locally under
`artifacts/github-actions/42275704043/`.

**Learning:** `SUPPORTED / PERSEVERE`. Keep the three upgraded Action references.

Previous substantive changes belong in the sole root `CHANGELOG.md` and version control; detailed loop evidence may live in GitHub issues or run artifacts. This is a **development** record, distinct from the financial research journal and scientific candidate approvals.

## Planned M1 experiment: screen one data source

- **M1-E01 decision and baseline.** Decide whether to propose one small import pilot. M0 uses synthetic data. No real source is selected. Before starting, the owner specifies the intended use and nominates one source, venue, instrument, bar interval, and required coverage.
- **Hypothesis.** The nominated source can support that use and documents the required coverage and timestamp semantics well enough to justify a pilot.
- **Test and pass criteria.** In one read-only review, record dated links to the provider's terms and data specification. Pass only if they substantiate no-cost access under ADR-046, permission for the stated use, a reproducibly identifiable dataset with the required coverage, and the timestamp unit, timezone, and meaning of each bar timestamp. Record observed time, cost, and the decision here. Published coverage is a screening result. The import pilot must verify actual data quality.
- **Budget and stop rule.** At most 30 minutes, one source, zero spend, zero dataset downloads, zero fits, and zero holdout access. Stop immediately on a confirmed mismatch and reject the source for this use. If required evidence is missing or ambiguous at the time limit, defer and record the gap. A pass warrants proposing M1-E02. A confirmed rejection cancels M1-E02 for this source. If evidence remains inconclusive, keep M1-E02 waiting only while a specific missing fact could still justify it. The [M1 acceptance criteria](MILESTONE_DOD.md#m1--v02-real-market-data-and-market-feasibility) still apply.

### M1-E01 Learning Card: Syncster/NQ, 2026-11-08

- **Scope and baseline.** Screen CME Globex E-mini Nasdaq-100 futures (NQ), one-minute OHLCV, for local import and data-quality development. Use the proposed January 5 through March 6, 2026 window as the screening target. M0's baseline remains synthetic. This documentation review changed no research or execution contract. FTA not triggered.
- **Access and coverage.** Hugging Face API metadata showed a public, ungated repository at revision `eff0dac55d843b3b83caec819efa213021a3e3e5`. The [file tree](https://huggingface.co/datasets/syncster-data/historical-market-data/tree/eff0dac55d843b3b83caec819efa213021a3e3e5/data/futures/1m) listed `data/futures/1m/NQ.parquet` at 41,193,926 bytes. The [dataset card](https://huggingface.co/datasets/syncster-data/historical-market-data/blob/eff0dac55d843b3b83caec819efa213021a3e3e5/README.md) advertises free access and reports May 29, 2016 through October 20, 2026 for the four-symbol futures group. NQ-specific coverage of the target window remains unverified.
- **Scope clarification.** The owner removed separate confirmation of local storage and automated use rights from the Syncster preliminary review. The public card lists research and educational use and `license: other`.
- **Time and rolls.** The [Hugging Face futures schema](https://datasets-server.huggingface.co/info?dataset=syncster-data%2Fhistorical-market-data&config=futures) reports `timestamp[us, tz=UTC]` for `ts`. Whether each stamp denotes the start or end of the minute remains undocumented. The card describes a continuous series and gives no per-bar contract field, rollover rule or dates, or price-adjustment method. The [CME customary roll calendar](https://www.cmegroup.com/trading/equity-index/rolldates.html) does not identify Syncster's actual switches.
- **Outcome and resources.** `INCONCLUSIVE / DEFER`. Review took under five minutes (approximate), with zero spend, market-data downloads, fits or holdout reads. M1-E02 remains waiting. Limit follow-up to public documentation and metadata. Reassess Syncster when those sources identify the NQ window coverage, whether the timestamps mark bar starts or ends, and the roll dates or contract mapping plus the adjustment method. The schema follow-up queried metadata only.

### M1-E03 Learning Card: alternative no-cost NQ source, 2026-11-08

- **Scope and gate.** Look for a free, individually identified CME Globex NQ contract with one-minute bars covering January 5 through March 6, 2026 and public documentation of timestamp encoding, zone, and bar boundary. Review public documentation and metadata only. Stop when the strongest candidate passes or the available evidence leaves a material gap. No change to research contracts. FTA not triggered.
- **Best NQ candidate.** The [free equity-index sample](https://huggingface.co/datasets/lynx1231/historical-equity-index-futures-data-sample/blob/1e10ad1f78044d494fe00e0b252fad6cbc097e98/README.md) is public and ungated. Its [catalog](https://huggingface.co/datasets/lynx1231/historical-equity-index-futures-data-sample/blob/1e10ad1f78044d494fe00e0b252fad6cbc097e98/catalog.csv) lists 111,536 minute observations for `NQH26`. The raw bounds `1741677780000` and `1773995340000` bracket the requested dates when decoded as millisecond calendar labels. Completeness within the window is unverified. Filtering by `contract_code` avoids stitching across contracts. The [sample schema](https://huggingface.co/datasets/lynx1231/historical-equity-index-futures-data-sample/blob/1e10ad1f78044d494fe00e0b252fad6cbc097e98/schema.json) preserves the raw integer. A [related sample](https://huggingface.co/datasets/lynx1231/historical-futures-data-sample/blob/29efdfa21c5a5b2d7aa306397385cf116e011559/schema.json) documents Chicago wall-clock millisecond labels for its own minute data. That is a lead. The equity-index sample still lacks an explicit minute-start or minute-end convention.
- **Other published offers.** [Barchart](https://www.barchart.com/futures/quotes/NQH26/price-history) gates historical minute downloads behind Premier. [Historical Futures Data](https://historicalfuturesdata.com/browse/NQ) offers latest-month NQ bars free, outside the target window. [MarketParquet](https://marketparquet.com/data/futures/nq) offers a free intraday sample outside the target window and describes its NQ series as continuous and ratio-adjusted.
- **Outcome and resources.** `INCONCLUSIVE / DEFER`. No alternative met the full NQ gate. The public review took under five minutes (approximate), with zero spend, market-data downloads, fits or holdout reads. At that point M1-E02 remained waiting. As a separate candidate, [Binance BTCUSDT spot](https://github.com/binance/binance-public-data#klines) was proposed for the initial engineering slice. Its documentation specifies open and close fields and microsecond precision, and HTTP HEAD checks returned 200 for the January, February, and March 2026 one-minute archives. The spot source cannot exercise futures sessions or rolls. The owner later selected it for M1-E02.

### M1-E02 Test Card: Binance BTCUSDT spot, 2026-11-08

- **Decision and baseline.** The existing `Bars` interface, validation and CSV writer have only the synthetic path. Test whether a small offline archive adapter can reuse those components for a real source without changing their time or campaign contracts.
- **Minimum proof.** Import the Binance Vision daily BTCUSDT spot one-minute archive for January 5, 2026 UTC after matching its published SHA-256. The [archive schema](https://github.com/binance/binance-public-data#klines) specifies microseconds and separate open and close fields. The [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md) cover this no-cost, local non-commercial technical evaluation. Keep the archive and output local.
- **Pass and stop.** Require 1,440 unique, ordered, contiguous minute bars for the full UTC day. Validate prices and volume through AQRS. Map the source inclusive close to the exclusive interval boundary used by AQRS, test the first and last times, and require identical fingerprints and output bytes across two imports. Reject a deliberately damaged copy with a removed minute, and separately reject a shifted close and a bad archive checksum. Publish no output for invalid input. Stop after this slice and record the result. See [FTA-M1-A](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes).
- **Resources.** Up to 30 minutes of development, one approximately 72 KB archive and its checksum with per-request limits of 20 seconds, at most 512 KiB of uncompressed input, under 5 seconds expected per offline import, and under 128 MiB expected process memory. Zero spend, research trials, fits, folds, seeds, resamples and holdout reads. No research campaign is launched.

### M1-E02 Learning Card: Binance BTCUSDT spot, 2026-11-08

- **Result.** `SUPPORTED / PERSEVERE` for the one-day offline adapter. On native Windows with Python 3.12.12, both imports accepted 1,440 ordered minute bars from 2026-01-05 00:00 to 23:59 UTC. The final bar became available at 2026-01-06 00:00 UTC under the AQRS interval convention. The published archive SHA-256 matched and both runs wrote byte-identical reports and datasets with fingerprint `7ec539e452f4efc7063947409a905f9c3e975b06ddf2585d252cb1ef72457893`.
- **Negative evidence.** A removed minute, a close shifted by one microsecond and a bad archive digest each returned exit 2 without an output directory. The two damaged archives carried matching replacement checksums so the timestamp validation was exercised. Independent review found no data-contract blocker. Bounded reads and clearer malformed-archive rejection were applied before the recorded checks.
- **Artifacts and resources.** Local files are in `artifacts/m1-e02/`, with source URLs and digests in `import/import_report.json`, normalized data in `import/dataset.csv` and measured results in `verification.json`. The archive was 71,473 bytes and downloaded with its checksum in about 0.84 seconds. The first two offline imports took 0.37 and 0.40 seconds. Zero spend, research trials, fits, folds, seeds, resamples or holdout reads.
- **Verification and next gate.** `python -m aqrs.binance_spot_pilot` positive runs returned exit 0. `python -m pytest -q` passed 21 tests and `python -m pytest -q tests/test_market.py` passed 7. Ruff lint and targeted format checks passed. At the end of M1-E02, Linux execution and a real-data campaign remained open. M1-E04 later reused the import contract on both platforms with specified cost assumptions and holdout boundaries.

### M1-E04 Test Card: first real-data campaign, 2026-11-08

- **Decision and baseline.** Test whether the validated M1-E02 `Bars` input can feed the existing supervised research workflow on native Windows and headless, non-root Ubuntu. The current CLI accepts only synthetic input. After approval, connect the existing importer at the campaign input boundary, reuse the analysis and Governor, and record separate import, feature calculation and simulation timings. Review FTA-M1-A and the holdout, fill and cost failure paths in the risk register before changing code. Require a negative check for out-of-window input and a fixture for exact fill indices and cost components.
- **Scope and separation.** Reuse the archived Binance Vision BTCUSDT spot minute data for January 5, 2026 UTC, 00:00 inclusive through January 6, 00:00 exclusive. Use 720 initial training bars and two chronological 360-bar validation windows with expanding training and a 16-bar purge at each label boundary. Reserve January 6, 2026 UTC as the final holdout. Record the date and zero authorized reads in the manifest. Leave its archive outside campaign inputs and do not fetch, read or evaluate it in this experiment. Keep source and artifacts local for personal, non-production research under the [dataset terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md).
- **Fixed policy and costs.** Use `C_LAG` Ridge with the existing lagged-return feature, the zero-return forecast benchmark, and momentum and no-trade policy controls. Simulate long or flat with one unit of abstract notional, at most one open position, entry at `open[t+1]` and exit at `open[t+16]`. Use the same fill, sizing and cost settings for candidate and controls. Model 10 basis points of taker fee per side using the [Binance regular-user schedule](https://www.binance.com/en/fee/trading) consulted on November 8, 2026 as a reference assumption for the historical run. Assume a full spread of 1 basis point and slippage of 2 per side. Historical fees, spread and slippage were not measured for this window. Round-trip costs total 25 basis points, plus a separate 2-basis-point decision buffer. Spot funding is inapplicable.
- **Resource Governor assessment.** Budget one development session of up to 60 minutes, including targeted checks and recording the outcome. Plan one campaign per platform, sequentially, with one trial, two folds, one seed, at most three fits including one bounded synthetic preflight fit, no control fits and no resampling per campaign. Both campaigns together allow at most two trials and six fits. Plan about 20 seconds of campaign wall time and 262 MiB peak worker RSS per platform as estimates to verify in preflight. Reuse the unchanged YAML ceilings of 120 seconds per trial, 300 seconds per campaign and a 4,096 MiB sampled RSS stop threshold. Use the existing local archive, cap new local artifacts at 10 MiB total and spend zero. The plan fits the existing limits subject to preflight on each platform. Stop on a failed guard, invalid input, budget stop or platform mismatch. Zero automatic retries.
- **Proof and stop.** Archive the provenance and quality manifest, plan, reports and SQLite attempt records. Require matching input fingerprints, UTC boundaries and discrete decisions across platforms, with absolute tolerance `1e-10` on research metrics in simple-return units. Record gross and net results and the three separate stage times when executed. If the existing training-only cost screen rejects the run, persist `SCREENED_OUT`, mark simulation as skipped and leave the full end-to-end acceptance gate open. Stop at the recorded outcome and leave scientific status at insufficient evidence for this one-day engineering slice.

### M1-E04 Learning Card: first real-data campaign, 2026-11-08

- **Result.** `SUPPORTED / PERSEVERE` for the shared real-data path through the cost screen. Both campaigns returned exit 0 and `COMPLETED` with a `SCREENED_OUT` decision and `INSUFFICIENT_EVIDENCE`. The 90th percentile absolute 15-minute target move in the first training window was **25.0563 bps** on both platforms. The policy required **27 bps**, including 25 bps of modeled round-trip costs and a 2 bps buffer. Both stopped before a real-data Ridge fit, validation predictions, simulated fills or PnL. The complete real-data simulation gate and broader market feasibility remain open.
- **Reproduction.** Both campaigns verified the original M1-E02 archive digest, imported 1,440 consecutive UTC minutes and produced byte-identical `dataset.csv` files. They matched on dataset and configuration fingerprints, UTC fold boundaries and the cost-screen decision. The screen metrics agreed exactly and met the declared tolerance. The January 6 holdout remained interval metadata with zero reads. The Ubuntu replay is platform evidence for the same research variant. Both SQLite integrity checks returned `ok`.

| Environment | Python | Run ID | Campaign wall s | Sampled peak RSS MiB | Import ms | Features ms | Simulation | Fits |
|---|---|---|---:|---:|---:|---:|---|---:|
| Native Windows 11 Pro x86_64 build 26300, non-admin, Job Object | 3.12.12 | `e1286897d9344fd5b4ce7375575fdea7` | 3.719 | 114.59 | 15.000 | Below clock resolution | Skipped | 1/3 |
| Headless Ubuntu 24.04.5 LTS x86_64, kernel 6.8.0-147-generic, UID 1000, POSIX process group | 3.12.3 | `989bc1f3002c45c4a91c56ab0f2501dc` | 1.575 | 116.83 | 6.178 | 0.325 | Skipped | 1/3 |

- **Checks and budget.** Both platforms ran `python -m aqrs research run --config configs/m1-e04.yaml`, `python -m pytest -q` (23 passed per platform) and `python -m ruff check .` (exit 0). The Windows focused CLI test initially failed both new cases before implementation and then passed both. Targeted Ruff formatting, `git diff --check`, and both language checks passed on Windows. The Ubuntu language checks and fresh offline `python -m pip install -e '.[dev]'` also exited 0. Each Governor admitted one trial and used one synthetic preflight fit. No campaign retries or spend. Total archived evidence was under 1 MiB. The elapsed working time from the risk update to the evidence comparison was about 18 minutes.
- **Environment incident.** The default QEMU CPU profile lacked NumPy's x86-64-v2 baseline. Ubuntu pytest stopped at collection with exit 2 before any real-data campaign. Set the guest CPU model to Nehalem under WHPX and verified the NumPy import before the successful suite and single campaign. The guest had no external network access. The AQRS configuration and source stayed fixed across the two campaigns.
- **Artifacts.** `artifacts/m1-e04/` contains `windows.log`, `ubuntu.log`, `verification.json` and the Windows journal and run directory. `artifacts/m1-e04/ubuntu/` contains the Ubuntu journal and run directory. Each run directory retains `data_manifest.json`, `dataset.csv`, `plan.json`, `report.json` and `report.md`.

### M1-E05 Test Card: real-data execution check, 2026-11-08

- **Decision and baseline.** Decide whether the existing execution simulator correctly applies the M1 time and cost contract to a verified real day. The synthetic fixture exercised execution, and M1-E04 verified real data through the cost screen. Test the simulator directly through a bounded engineering check so the M1-E04 campaign, its research admission rule and its result stay intact. Keep this evidence separate from candidate evaluation and full M1 acceptance. Review FTA-M1-B before execution. The proposal changes no production contract.
- **Minimum proof.** Use the existing January 5, 2026 BTCUSDT spot archive and its verified digest on native Windows and headless, non-root Ubuntu. Fix the test signal at the close of the 12:00 UTC bar, with a scripted score above the original threshold, entry at the 12:01 open and exit at the 12:16 open. Run a flat control at the same signal time. Verify that the existing fold construction excludes a signal at 23:44, whose required exit would fall in the reserved interval. Leave January 6 untouched.
- **Pass and stop.** Compute expected gross return directly from the two source opens and subtract 25 basis points of modeled execution costs, itemized as 20 fees, 1 spread and 4 slippage. Require exactly one long trade and zero flat-control trades, exact timestamps and matching gross and net results within `1e-10` in simple-return units. Record the import, feature and simulation times where measured, archive the command and results, and stop after one check per platform or the first failure. A mismatch identifies a technical issue. The result supplies no market-feasibility or alpha evidence.
- **Resource Governor assessment.** Up to 45 minutes of engineering work, including platform setup and documentation. Two sequential platform checks, each estimated under 10 seconds and 256 MiB with the environment ready. Limit each check to 30 seconds. Zero research trials, fits, seeds, resamples, new downloads of market data, holdout reads or spend. Up to 1 MiB of new local evidence. Reuse the existing importer, fold builder and simulator. The proposal fits the existing resource limits and leaves the campaign budget configuration intact.

### M1-E05 Learning Card: real-data execution check, 2026-11-08

- **Result.** `SUPPORTED / PERSEVERE` for the fixed execution case. Both platforms verified the M1-E02 archive digest and the same 1,440-bar fingerprint. The scripted score of 0.01 triggered exactly one long trade at 12:01 UTC at 93,130.10 USDT. It exited at 12:16 UTC at 93,143.31 USDT. Independent decimal arithmetic from the original CSV opens matched the simulator within `1e-10`. The gross return was 1.418446 bps. The net return was -23.581554 bps after 20 bps of fees, 1 bps of spread and 4 bps of slippage. The flat control generated zero trades and zero costs.
- **Boundary and scope.** Both platforms excluded the 23:44 UTC signal bar. Its modeled exit would have required a bar in the reserved January 6 interval. The latest eligible signal bar was 23:43 UTC. The holdout remained untouched. No model fit or research campaign ran. This engineering check verifies one execution case, and the full M1 research campaign, market feasibility and M1 acceptance remain open.

| Environment | Python | Wall s | Sampled peak worker RSS MiB | Import ms | Features ms | Simulation and flat control ms |
|---|---|---:|---:|---:|---:|---:|
| Native Windows 11 x86_64 build 26300 | 3.12.12 | 2.140 | 118.31 | 8.073 | 0.248 | 0.087 |
| Headless Ubuntu 24.04.5 LTS x86_64, kernel 6.8.0-147-generic, UID 1000 | 3.12.3 | 0.812 | 118.38 | 5.446 | 0.308 | 0.071 |

- **Verification and budget.** On each platform, `python artifacts/m1-e05/check_execution.py` ran once with a 30-second subprocess deadline and exited 0. The cross-platform Python comparison exited 0 and matched the source and configuration identities, prices, timestamps, costs and returns. The Ubuntu guest used a fresh environment with offline `python -m pip install -e .` from the local wheelhouse. No production code, campaign settings or safety contract changed. No retries, market-data downloads or spend. Archived evidence was under 20 KiB. Elapsed working time through the comparison was about 247 seconds.
- **Artifacts.** The runnable check, platform logs, `windows.json`, `ubuntu.json` and `verification.json` are under `artifacts/m1-e05/`.

### M1-E06 Test Card: complete real-data campaign, 2026-11-08

- **Decision and baseline.** Check whether the supervised research CLI can proceed from real-data import through training, out-of-sample prediction, simulation and reporting. M1-E04 stopped at the original 15-minute screen, where the 90th percentile absolute training move was 25.0563 bps against a 27 bps hurdle. M1-E05 verified one execution case directly. The new, single engineering variant assumes 30 minutes allows sufficient price movement for the existing screen under the same cost assumptions. A screen failure refutes that operational assumption for this sample. A pass shows only that the pipeline can proceed. Record the new variant and its M1-E04 lineage separately because the day was already used in research.
- **Fixed scope.** Reuse the verified January 5, 2026 BTCUSDT spot archive and the M1-E04 configuration in a separate run location and journal. Set the horizon to 30 minutes. Keep the 720-bar initial training window, two 360-bar validation windows, `C_LAG` Ridge candidate, long-or-flat policy, 25 bps estimated round-trip costs, 2 bps decision buffer and existing controls. Use the existing horizon-based 31-bar purge. The January 6 holdout remains untouched. Review FTA-M1-B and verify the fold boundaries before execution. The proposal changes no production contract.
- **Pass and stop.** Run the normal CLI once on Windows. If the screen admits the variant and the campaign completes, replay once on headless, non-root Ubuntu. Require two completed validation folds, a simulation result for the candidate and controls, and archived manifests, stage timings, reports and SQLite attempts. Require matching fingerprints, UTC boundaries and decisions, and numeric agreement within `1e-10` in simple-return units. A completed simulation with zero trades or negative PnL meets this technical criterion. If Windows screens out the variant or any check fails, retain the evidence and stop. Do not try other horizons or dates under this authorization. This is an engineering check on reused development data. Final M1 acceptance remains subject to review of all milestone gates.
- **Resource Governor assessment.** Up to 45 minutes of setup, verification and documentation. At most two sequential campaigns with one trial, two folds, one seed and up to three fits each, including one bounded synthetic preflight fit per campaign. Zero control fits, resamples, new market-data downloads, holdout reads or spend. Estimate under 20 seconds and about 262 MiB per campaign, to be checked by the existing preflight, and up to 2 MiB of new local evidence. The existing 120-second trial limit, 300-second campaign limit and 4,096 MiB sampled RSS threshold cover the proposed scope. No budget increase or automatic retry.

### M1-E06 Learning Card: complete real-data campaign, 2026-11-09

- **Result.** `SUPPORTED / PERSEVERE` for the end-to-end research CLI. The training-window 90th percentile absolute 30-minute target move was 38.9173 bps against the unchanged 27 bps hurdle. Both campaigns completed two model fits, produced 658 out-of-sample predictions, and ran the candidate and control simulations. Both retained `INSUFFICIENT_EVIDENCE`. Ridge MAE was 22.0230 bps versus 21.2675 bps for the zero-return forecast. Ridge and the flat control had zero trades. Momentum had one trade with net PnL of 18.2495 bps of fixed notional. The single reused day supports the software result. Market suitability and formal M1 acceptance remain open.
- **Boundaries and reproduction.** Both campaigns used the same verified 1,440-bar January 5 archive. Both enforced the 31-bar purge and reserved January 6 with zero holdout reads. Input CSV bytes, fingerprints, UTC boundaries, trade decisions, and numerical metrics matched within the prespecified tolerance. The comparison verified next-open entry, 30-bar exit and 25 bps of round-trip costs on the momentum trade. Each SQLite journal passed `PRAGMA integrity_check`. The Ubuntu replay supplies platform evidence for the same variant. See `lineage.json` for the M1-E04 attempt IDs.

| Environment | Python | Run ID | Campaign wall s | Sampled peak RSS MiB | Import ms | Features ms | Simulation ms | Fits |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Native Windows 11 x86_64 build 26300, Job Object | 3.12.12 | `1aa63be4f18d4905a6b27cb19a9785f9` | 3.859 | 114.59 | 0 recorded | 0 recorded | 0 recorded | 3/3 |
| Headless Ubuntu 24.04.5 LTS x86_64, kernel 6.8.0-147-generic, UID 1000, POSIX process group | 3.12.3 | `50a2026a6b044d28909db1a5f90f309a` | 2.106 | 118.02 | 6.141 | 0.316 | 0.662 | 3/3 |

- **Verification and budget.** `python -m aqrs research run --config artifacts/m1-e06/frozen.yaml` exited 0 once per platform. `python artifacts/m1-e06/verify_campaigns.py` exited 0 and archived the comparison. The Windows stage counters did not resolve these short intervals, so the three zeros do not establish their durations. Ubuntu used a fresh offline install with `python -m pip install -e .`. Each campaign used one synthetic pilot fit plus two real-data fits. No retries, market-data downloads or spend. Archived evidence was under 1 MiB. Elapsed work through the comparison was about 223 seconds.
- **Artifacts.** `artifacts/m1-e06/` contains the frozen configuration, lineage, comparison script and result, platform logs, and the Windows run and journal. The Ubuntu run and journal are in `artifacts/m1-e06/ubuntu/`. Each run retains the manifest, plan, dataset and both reports.

### M1-E07 Test Card: acceptance evidence review, 2026-11-09

- **Decision and baseline.** Decide whether the evidence supports formal M1 acceptance for the documented BTCUSDT research scope. M1-E06 supplied the complete campaign, while the Windows stage timings and market suitability still need a decision. The assumption is that the existing records can identify the disposition of each criterion and any smallest remaining proof.
- **Minimum proof.** In one review, map each [M1 acceptance criterion](MILESTONE_DOD.md#m1--v02-real-market-data-and-market-feasibility) to a specific artifact or gap. Check documented use rights and provenance, data quality and rejected inputs, time and execution assumptions, applicable prerequisites, platform and resource evidence, and the distinction between market suitability for research and evidence of alpha. Compare the campaign stage timings with the separately timed M1-E05 engineering check and assess whether the combination meets the written criterion.
- **Pass and stop.** Record a disposition with evidence or a reason for every criterion in this status file. If all applicable requirements are met, recommend acceptance and state its scope. Otherwise state the blocker and propose the smallest additional proof. Leave unsupported criteria open. Stop after the review and present the result for the owner decision.
- **Resource Governor assessment.** Up to 30 minutes of review and documentation. Reuse archived evidence. Zero new trials, fits, resamples, market-data downloads, holdout reads or spend. No production changes or resource limit changes. The work fits the existing budget. Routine documentation risk. FTA not triggered.

### M1-E07 Learning Card: acceptance evidence review, 2026-11-09

`SUPPORTED / PERSEVERE` for the review. The archived evidence can support technical acceptance for local, personal, non-production research on one BTCUSDT spot archive once the fresh Windows gap is closed. Zero research runs, fits and holdout reads during this review. Elapsed time through the evidence review was about 156 seconds.

| M1 criterion | Disposition and evidence |
|---|---|
| Reproducible source, provenance, retrieval, rights and version | **Met for the declared scope.** M1-E02 and M1-E06 archive the exact URL, November 8 retrieval, published SHA-256 as content version, and matching normalized bytes. The [Binance Vision Dataset Terms v1.0](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md#4-scope-of-non-commercial-use-and-express-prohibitions), dated August 26, 2026 and reviewed November 9, include personal non-production historical backtesting in the permitted non-commercial scope. |
| Quality coverage and damaged data | **Met.** M1-E02 and the manifest record 1,440 consecutive, ordered, unique minutes and valid OHLCV. Exact per-row UTC cadence excludes missing, duplicate and reordered bars. Missing-minute, shifted-close and checksum fixtures failed closed. The M1-E04 test also rejected checksummed foreign-day input before fitting. |
| Time, venue and instrument contract | **Met.** The M1-E06 manifest identifies Binance Spot BTCUSDT, continuous UTC days and source microseconds. M1-E02 maps the inclusive exchange close to the next minute as the availability boundary. The scope uses unlevered spot, so futures rolls, funding and equity adjustments are inapplicable. A coverage gap invalidates the daily archive. |
| Shared research interface | **Met.** The importer returns the same `Bars` representation. The review compared the abstract syntax trees of eight existing feature, target, validation, model, metric, cost and simulation functions with the M0 source. All eight matched. The evaluator diff adds timing and reporting metadata. M1-E06 exercised the shared pipeline on real input. |
| Estimated execution costs and fills | **Met.** M1-E04 and M1-E06 reports label the 25 bps round-trip estimate, its separate 2 bps buffer and next-bar open approximation. M1-E05 verifies the modeled fill indices and cost arithmetic independently. Actual historical fills, spreads and slippage remain unknown. |
| Coverage, horizon and suitability risks | **Met for the declared scope.** One complete day is suitable for this technical research check. M1-E04 records the 15-minute screen rejection, and M1-E06 records a 30-minute run with insufficient scientific evidence. Broader coverage, liquidity and economic suitability remain unestablished. |
| Archived end-to-end real-data campaign | **Met.** M1-E06 archived both successful runs and both intact SQLite journals through prediction and simulation, including zero-trade and benchmark outcomes. |
| Separate stage timings | **Met by the Ubuntu half of the first complete M1-E06 campaign.** It measured import, features and simulation separately. Windows recorded three zeros at its 15.625 ms clock resolution. The separately timed M1-E05 Windows check corroborates that these phases can be brief and does not substitute for the Ubuntu campaign timings. The data give no indication of repeated feature calculation as a bottleneck. |
| Input-specific pilot prerequisites | **Conditional.** No such pilot ran. This OHLCV archive lacks order-book depth, timestamped text and multi-asset inputs. DeepLOB, FinBERT and GNN are `BLOCKED_DATA` for this archive. Any later pilot requires documented input availability and timing. |
| Clean native Windows and headless Linux with budget evidence | **Open on Windows at review.** M1-E06 ran once from a fresh, offline, non-root Ubuntu environment. The native Windows run was isolated at the campaign level and used the existing development environment. M1-E08 will supply one clean-install replay. |

The universal gates are supported by the M1 Test and Learning Cards, FTA-M1-A and FTA-M1-B, the recorded Ubuntu setup incident and correction, the 23 Windows and Ubuntu tests and Ruff results from M1-E04, and the unchanged source fingerprint in M1-E06. The archived attempts preserve the cost-screen rejection, prior variants, frozen configuration and fit counts. Documentation and final gate status are checked before acceptance.

### M1-E08 Test Card: fresh Windows acceptance, 2026-11-09

- **Decision and baseline.** Determine whether the approved M1-E06 variant reproduces from a fresh native Windows Python 3.12 environment. Reuse the archived fresh Ubuntu replay and matching source. An existing Windows run in the development environment is the baseline. No production or safety-contract change. FTA-M1-A and FTA-M1-B apply as existing controls.
- **Minimum proof and stop.** Install offline in a new isolated environment. Replay M1-E06 once in a separate artifact directory and journal. Require compatible dependencies, a completed CLI campaign, matching data identity and decisions, numeric agreement within `1e-10`, an intact journal, and no holdout access. Stop after the replay or at the first failure. The repeat is duplicate technical evidence for M1-E06 and supplies no independent scientific evidence.
- **Resource Governor assessment.** Up to 20 minutes including setup and documentation. At most one Windows campaign, one trial, two folds, one seed, and three fits including one synthetic preflight fit. No resampling, retries, market-data downloads, holdout reads or spend. Estimate under 20 seconds and about 262 MiB of research runtime memory per campaign, and under 1 MiB of archived evidence. The existing Governor limits apply unchanged. No new Ubuntu run.

### M1-E08 Learning Card: fresh Windows acceptance, 2026-11-09

`BLOCKED / PIVOT` for environment setup. `uv venv --offline` exited 0. `uv pip install --offline` exited 1 because the cache lacked the pinned Windows NumPy 2.5.4 distribution. The existing wheelhouse was for Linux. A platform-specific wheel inventory would have caught the gap before installation. The replay was never launched and consumed zero trials, fits or holdout reads. The remaining proof is the same single clean Windows campaign after staging the pinned dependencies separately.

### M1-E09 Test Card: Windows wheelhouse and replay, 2026-11-09

- **Decision and baseline.** The M1-E08 install was blocked by a missing Windows package, and the existing M1-E06 development environment already ran the frozen dependency versions. Stage the exact Windows wheels from PyPI and the existing local build wheel, record their hashes, and install into a fresh environment with registry access disabled. Verify package consistency before attempting the one replay.
- **Pass and stop.** Apply the M1-E08 campaign acceptance checks with the same M1-E06 source, frozen research configuration, costs and January 5 archive. Use a separate output directory and journal. Stop at the first failure or after one campaign and its comparison with M1-E06. Mark the result as duplicate technical evidence. Review the M1 gate using the archived Ubuntu run and the new Windows proof. FTA-M1-A and FTA-M1-B remain the relevant controls.
- **Resource Governor assessment.** Use the remaining 20-minute setup and documentation allowance. Stage one pinned dependency bundle, up to 100 MiB of temporary storage, with zero spend. The package transfer excludes market data. One Windows campaign and at most three fits including the synthetic preflight fit remain in scope because M1-E08 launched no campaign. Keep existing limits, zero holdout reads, no resampling, and no campaign retries or Ubuntu replay.

### M1-E09 Learning Card: Windows wheelhouse and replay, 2026-11-09

`BLOCKED / PIVOT` for online package staging. The pinned PyPI download exited 1 without resolving the first package. Subsequent index requests timed out. The campaign did not start. A bounded inventory found the complete pinned set in the separate pip HTTP cache and existing wheelhouse. This corrects the narrower M1-E08 finding about the cache visible to `uv`.

### M1-E10 Test Card: cached Windows wheels and replay, 2026-11-09

Stage the exact cached Windows wheels and existing portable wheels. Verify each wheel's internal `RECORD` hashes and archive a wheel SHA-256 manifest. Install without an index in a fresh Windows environment, check package consistency, and apply the M1-E08 replay criteria and stop rule. Reuse the remaining M1-E08 and M1-E09 budget. One Windows campaign, three fits maximum, no changed dependencies, no new Ubuntu run, and no holdout reads. No production contract changes.

### M1-E10 Learning Card: cached Windows wheels and replay, 2026-11-09

`SUPPORTED` for installation and `BLOCKED / DEFER` for a successful fresh-install campaign. The initial wheel inventory check matched a nested metadata directory. Selecting the expected top-level wheel metadata corrected the check before installation. Thirteen cached and portable wheels then passed internal `RECORD` verification. `uv venv --offline`, `uv pip install --offline --no-index` and `uv pip check` each exited 0. CPython 3.12.12 ran on native non-admin Windows with the same AQRS source and pinned dependencies as M1-E06.

**M1-INC-01.** The verified archive imported successfully. `python -m aqrs research run --config artifacts/m1-e10/frozen.yaml` exited 2 as `REJECTED_PREFLIGHT` for run `a6e0494f2ee14c0e8485c033edbdf074`. Its supervised synthetic pilot was `TIMED_OUT` at 5.031 seconds, before any completed fit or research trial. SQLite integrity returned `ok` and the candidate remained `NOT_EVALUATED`. The watchdog prevented an unbudgeted launch. No holdout access and no campaign retry.

The campaign report did not separate worker initialization from fitting, so the exact timeout cause remains unresolved. A five-second import-only diagnostic also timed out. A later bounded comparison recorded the same import sequence in 1.683 seconds in the development environment and 3.490 seconds in the fresh environment, with most of the fresh delay in the evaluator import. This supports startup latency as a plausible contributor and leaves headroom uncertain. Keep the five-second guard. The next controlled replay tests whether the now-initialized environment can finish with the same guard. Evidence is in `artifacts/m1-e08/windows.log`, `artifacts/m1-e09/windows.log` and `artifacts/m1-e10/`, including the run, journal, wheel manifest and both import diagnostics. Elapsed work from the review through the diagnostics was about 1155 seconds.

### M1-E11 Test Card: bounded Windows replay, 2026-11-09

With separate approval, run the frozen M1-E06 configuration once in the verified M1-E10 Windows environment, using a new output directory and journal. Keep the five-second pilot deadline and all Governor limits. Pass if the supervised run completes and its dataset, folds, decisions and metrics match M1-E06 within `1e-10`, with intact journal and zero holdout access. A second timeout leaves the platform gate open and warrants a dedicated startup investigation. Budget up to 15 minutes of work, one campaign, one trial, two folds, one seed and at most three fits including the synthetic pilot. Expect under 20 seconds and about 262 MiB if admitted, subject to preflight. Reuse the archived Ubuntu run. Zero resampling, new downloads, spend or automatic retries. No safety-contract change proposed.

### M1-E11 Learning Card and M1 acceptance, 2026-11-09

- **Result.** `SUPPORTED / PERSEVERE`. `uv pip check --python <M1-E10 environment>` exited 0. `python -m aqrs research run --config artifacts/m1-e11/frozen.yaml` exited 0 on non-admin native Windows 11 x86_64 build 26300, CPython 3.12.12. The separately approved replay reused the offline M1-E10 installation after its import diagnostics. Run `b3fe564089b7470188f3bae991fa835a` completed with the unchanged Windows Job Object and sampled RSS guard. The pilot took 1.828 seconds against the five-second deadline. The campaign took 3.859 seconds and peaked at 115.43 MiB sampled RSS. It used one trial and three fits, including one synthetic pilot fit. Zero additional retries, downloads, spend or holdout reads. Elapsed work through the comparison was about 167 seconds.
- **Evidence.** The read-only comparison exited 0 and matched the frozen M1-E06 campaign on dataset bytes, source fingerprint, dependencies, fold boundaries, decisions and metrics within `1e-10`. Windows and Ubuntu journals both passed SQLite integrity checks. The fresh Ubuntu 24.04.5 LTS x86_64 run `50a2026a6b044d28909db1a5f90f309a`, Python 3.12.3, UID 1000 and POSIX process-group guard, remains the independent platform proof. Both platforms ran the same source. The new Windows replay is duplicate technical evidence. See `artifacts/m1-e11/verification.json`, `windows.log`, the run reports and the SQLite journal.
- **Acceptance.** The M1-E07 review and the fresh Windows replay close the applicable M1 criteria for local, personal, non-production research using the documented one-day Binance BTCUSDT spot archive and approximate fills. The complete Ubuntu campaign supplies the separate stage timings. Windows still records these brief stages as zero at its clock resolution. M1-INC-01 remains an observed startup timeout with unresolved exact cause and verified fail-closed behavior. No safety limit changed. The result supports the software gate, with `INSUFFICIENT_EVIDENCE` for the candidate. The January 6 holdout remains reserved with zero reads. No M2 work is authorized by this acceptance.

## M2-E01 Test Card: one event research decision, 2026-11-09

- **Assumption and baseline.** An explicit rival explanation and a matched control can change which test is worth running next for one event. The baseline is a candidate-first screen that advances on the event result alone.
- **Fixture.** One synthetic price-drop scenario with three separate time blocks. An event is the first crossing to a trailing five-minute return of −50 basis points or lower, known after a completed minute. Each block stipulates one such crossing and one non-trigger control from the same session time band and prior volatility band, both known at entry. The stipulated returns use non-overlapping 15-minute holds from the next eligible open, with the same notional and 15 basis points of illustrative round-trip costs per entry. The rival explanation is a rebound shared by comparable conditions even without the trigger. The table gives gross returns in basis points (`bps`).

| Block | Event trailing return | Control trailing return | Event gross return | Control gross return |
|---|---:|---:|---:|---:|
| A | -55 | -30 | 18 | 20 |
| B | -60 | -35 | 22 | 22 |
| C | -52 | -25 | 26 | 24 |

- **Fixed decision rule.** The candidate-only screen advances the unchanged rule to one later development window if three distinct blocks qualify and mean event return after costs is at least 5 bps. The matched screen also requires a mean paired net advantage of at least 2 bps. If the candidate-only screen advances and the matched screen misses that minimum, defer the follow-up and record what evidence could reopen it. Pass the probe if the existing [research funnel](RESEARCH_PROTOCOL.md#lean-research-funnel) supports a reproducible decision change and a recorded rival explanation.
- **Budget and stop.** Up to 30 minutes of development review. One small synthetic fixture, zero new campaign trials, fits, folds, seeds, resamples, holdout reads or spend. Stop after one decision comparison. If the matched result changes no decision or requires new machinery to interpret, defer automation and record the gap. This is a routine manual review of the existing rule. No critical research contract is being changed, so a Fault Tree Analysis is not triggered.

## M2-E01 Learning Card: one event research decision, 2026-11-09

- **Result.** `SUPPORTED / PERSEVERE` for using the manual matched screen on this fixture. The candidate-only decision was `ADVANCE` and the matched decision was `DEFER`. All three blocks qualified. Subtracting 15 bps from each gross return gave event net returns of 3, 7 and 11 bps and control net returns of 5, 7 and 9 bps. Both averaged 7 bps, above the 5 bps floor. The paired differences were −2, 0 and 2 bps, for a mean advantage of 0 bps against the required 2 bps. A rebound shared by comparable conditions explains the planted apparent effect.
- **Next decision.** Park the event follow-up in this fixture. Revisit a real-data version only with separate authorization and an eligible development window in which sufficient matched coverage and plausible costs could establish a predeclared incremental effect. Use this manual decision as the baseline for any later automation proposal. A proposal needs an observed workflow bottleneck. This probe establishes one decision outcome on stipulated inputs. Event detection, actual market effects and M2 acceptance remain open.
- **Verification and budget.** One read-only `python -` invocation on Windows read the Test Card, checked the three distinct blocks and trigger values, and reproduced the arithmetic and both decisions with exact fractions (exit 0). Elapsed time from the pre-test review through the comparison was about 74 seconds. Zero campaigns, trials, fits, folds, seeds, resamples, downloads, retries or spend. The January 6, 2026 UTC holdout had zero reads. This manual probe required no platform acceptance run.

## M2-E02 Test Card: development data coverage, 2026-11-09

- **Decision and baseline.** M1 verified the import of 1,440 contiguous BTCUSDT spot minute bars. Coverage for the M2-E01 event and matched control is unknown. Test whether the existing day can supply pairs in three distinct time blocks for a later workflow exercise. Reuse the single synthetic trigger as a fixed starting point. If comparable rebounds are common, a later outcome screen needs a non-trigger control to separate the explanations. This coverage check measures only whether that comparison is feasible.
- **Input and matching.** After approval, reuse `binance_spot_pilot.import_day` on only the verified January 5, 2026 UTC archive and its checksum. Use the first crossing to a five-minute close-to-close return of -50 bps or lower, observed after a completed minute. Controls stay above the threshold at their observation time. Match within the same UTC hour using mean absolute one-minute returns over the preceding 15 returns ending five minutes before observation. The larger volatility measure may be at most twice the smaller. Both windows use the next eligible open and a 15-minute holding interval. Require disjoint intervals with both entries at or after the start and both exits strictly before the end of the same eight-hour UTC block. Count the first pair per block by earliest eligible event, then nearest eligible control by time, with ties going to the earlier control. Eligibility uses only past or current prices and entry and exit timestamps.
- **Criterion and stop.** Record the archive digest, command, exit, run time, trigger counts and matched coverage in the three UTC blocks starting at 00:00, 08:00 and 16:00. If each block supplies one pair, propose one separately scoped outcome exercise. Otherwise, defer that exercise and report the missing coverage. Three pairs are a workflow minimum and do not establish statistical independence or an effect. Stop after one count. Do not inspect forward returns, tune the rule, download data or read any part of the January 6 holdout. Fail closed if the verified input or boundary check fails. Reuse the M1 data safeguards without changing the research contracts. Fault Tree Analysis is not triggered by this planning change.
- **Resource Governor assessment.** One-time work up to 30 minutes including the count and evidence, with no recurring work. One local pass over up to 1,440 bars, estimated under 10 seconds and 256 MiB of peak memory, with an external 30-second time limit. Zero research campaigns, trials, fits, folds, seeds, resamples, retries, new downloads, holdout reads or spend. Fits the existing budget with no limit changes. Planning review through the draft took about 48 seconds.

## M2-E02 Learning Card: development data coverage, 2026-11-09

- **Result.** `REFUTED / DEFER` for the one-day coverage assumption. The fixed -50 bps first-crossing rule found zero triggers and zero pairs in each UTC block starting at 00:00, 08:00 and 16:00. The predeclared minimum was one pair in every block. Defer the outcome exercise. Revisit the unchanged rule only on a separately authorized development window with enough matched coverage. The count measures coverage for this rule and day. Market effect and economic value remain unassessed.
- **Evidence.** The local attempt record is `artifacts/m2-e02/coverage.json`. It contains the command, script digest, exit, timing, source SHA-256 and block counts. The importer verified the M1 archive SHA-256 `a29b45bdb88d5090cfecc61423dab084364a34db96b0788ab77cefc9d4b9567d` and the original 1,440-bar dataset fingerprint. A focused synthetic `python -` check passed the trigger, warmup, strict block cutoff, final close exclusion, matching and invalid-length cases before the only real-data pass.
- **Execution and budget.** `.venv/Scripts/python.exe -B artifacts/m2-e02/count_pairs.py` exited 0 on native Windows with Python 3.12.12. The supervised count took 0.312 seconds against the 30-second deadline. Peak memory was not measured. Elapsed work through the count was about 141 seconds. Zero forward returns evaluated, holdout reads, downloads, campaigns, trials, fits, folds, seeds, resamples, retries or spend. No new Linux run or platform acceptance claim.

## M2-E03 Test Card: extended development data coverage, 2026-11-09

- **Decision and baseline.** Determine whether a five-day development window can provide three matched pairs for a later workflow exercise. M2-E02 found zero events on January 5. The local archive inventory found only that date in the proposed window. Fix January 1 through 5, 2026 UTC as a short contiguous window ending before the holdout. Extend coverage while retaining the -50 bps first-crossing trigger, 15-minute holding interval, matching and time-boundary rules from M2-E02.
- **Minimum test and safeguards.** After authorization, fetch only the four daily Binance Vision BTCUSDT spot one-minute ZIPs and their checksums for January 1 through 4 UTC. Allowlist those exact files on the existing HTTPS source and reject redirects. Before any request, verify with a synthetic check that the January 6 holdout and dates outside the allowlist are rejected. Reuse `binance_spot_pilot.import_day` and the M2-E02 scanner on each verified day separately, with no crossing of day boundaries. Reuse the archived January 5 counts. The local count uses development inputs only. Review [FTA-M1-A and FTA-M1-B](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes). This planning change leaves the research contracts intact.
- **Criterion and stop.** Record daily trigger and match counts by UTC block, digests, command, elapsed time and decision. Propose a separate outcome exercise only if the fixed window supplies a pair in each of the three UTC time bands with the three pairs on distinct dates. This minimum demonstrates coverage for a workflow exercise. If coverage is insufficient, defer. A failed import, request or scope guard stops the attempt with its execution reason. Stop after the fixed window. Zero forward returns, rule tuning, extra dates or holdout reads.
- **Resource Governor assessment.** Up to 45 minutes of one-time work including the evidence. At most eight HTTPS requests with no retries, each ZIP limited to 512 KiB and each checksum to 4 KiB. Allow up to 2.25 MiB of additional local storage including evidence. Bound acquisition at 60 seconds and the sequential local scan at 30 seconds. Scan at most 5,760 new bars and reuse the existing 1,440-bar record. Estimate under 10 seconds for the local scan and under 256 MiB peak memory based on the small bounded inputs. Peak memory and transfer time remain estimates. Zero campaigns, trials, fits, folds, seeds, resamples or spend. No recurring work or budget increase. Planning review through the draft took about 35 seconds.

## M2-E03 Learning Card: extended development data coverage, 2026-11-09

- **Result.** `REFUTED / DEFER` for the fixed-window coverage assumption. January 2 contained three eligible triggers and two retained pairs. The 00:00–08:00 UTC band had zero triggers and pairs, 08:00–16:00 had two triggers and one pair, and 16:00–24:00 had one trigger and one pair. Each other date had zero triggers and pairs, including the reused January 5 counts. The predeclared minimum required one pair in each time band on three distinct dates. Defer the outcome exercise. The observed coverage does not establish a market effect or its absence.
- **Evidence.** `.venv/Scripts/python.exe -B artifacts/m2-e03/run_coverage.py` exited 0 on native Windows with Python 3.12.12. `artifacts/m2-e03/coverage.json` records the script and archive digests, command, eight requests, phase exits and all daily counts. The importer verified all four archive checksums and 5,760 contiguous development bars before their respective counts. The archived 1,440-bar result from January 5 was reused. A synthetic `python -B -` check passed the URL, holdout, redirect and distinct-date guards before acquisition. See the [risk screen](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes).
- **Budget and stop.** The single acquisition took 6.362 seconds against its 60-second deadline and received 268,863 bytes. The local count took 0.398 seconds against its 30-second deadline. Elapsed work through the result was about 130 seconds. Peak memory was not measured. Zero retries, campaigns, trials, model fits, forward returns evaluated, holdout requests or reads, and spend. The fixed window is closed. No new Linux run or M2 acceptance claim.

## M2-E04 Test Card: synthetic interaction comparison, 2026-11-09

- **Decision and baseline.** Test whether the existing Ridge evaluation components can distinguish a planted joint effect from a balanced null. Compare an additive baseline using two individual features with the same model using both features plus their product. Use `evaluation.model` and `evaluation.prediction_metrics`. This advances the separate interaction prerequisite in [ADR-045](DECISIONS.md#adaptive-research-integration) while the price-drop outcome exercise remains deferred.
- **Fixed fixtures.** Cycle through the four ordered pairs `(-1,-1)`, `(-1,+1)`, `(+1,-1)`, `(+1,+1)`. Use eight complete cycles for training and the next four for evaluation in each fixture. In the XOR fixture the target is +1 when the two features differ and -1 when they agree. Each feature value alone has equally many positive and negative targets. The null uses the same features and alternates the target between +1 and -1 by whole cycle, leaving it balanced within every joint state in both splits. Fit the existing scaling and Ridge pipeline on training rows only with the existing fixed regularization. Use the same rows and targets for both representations of each fixture.
- **Criterion and stop.** Check the prescribed target balance, then record held-out mean absolute error (MAE), the average absolute prediction error. Require additive MAE of 1 within `1e-10` and an MAE improvement of at least 0.90 from adding the cross-term on XOR. On the null, require both MAEs to equal 1 within `1e-10`. If both cases pass, retain this as a technical reference for a later interaction study. Otherwise, stop and record the gap. The comparison tests an explicit cross-term on two synthetic fixtures. Routine engineering risk. No change to critical research contracts and no Fault Tree Analysis triggered.
- **Resource Governor assessment.** Up to 30 minutes once, including evidence. At most four model fits total, two deterministic train/evaluation splits, zero random seeds, resamples, campaigns or research trials. One local process, estimated under 10 seconds and 256 MiB peak memory with a 30-second external deadline. Evidence below 100 KiB. Zero downloads, market-data reads, holdout reads or spend. No recurring work or budget increase. Planning review through the draft took about 34 seconds.

## M2-E04 Learning Card: synthetic interaction comparison, 2026-11-09

- **Result.** `SUPPORTED / PERSEVERE` for the fixed technical comparison. On XOR, the additive MAE was 1.0 and the cross-term MAE was 0.0303030303, an improvement of 0.9696969697 against the 0.90 minimum. On the balanced null, both MAEs were 1.0 and the improvement was zero. Both fixed criteria passed. Retain the comparison as a technical reference. The cross-term was supplied in advance. Open discovery, market effects and M2 acceptance remain unassessed by this probe.
- **Evidence.** `.venv/Scripts/python.exe -B artifacts/m2-e04/compare_interaction.py` exited 0 on native Windows with Python 3.12.12 and scikit-learn 1.9.1. The fit log, script digest and metrics are in `artifacts/m2-e04/interaction.json`. The existing pipeline used the first 32 rows for training and the next 16 for scoring in each fixture. The `python -B -` preflight checked fixture order, balance in each split and rejection of imbalanced inputs with zero fits.
- **Budget and stop.** Exactly four fits, two fixed splits and one execution. The supervised comparison took 1.633 seconds against its 30-second deadline. Elapsed work through the comparison was about 79 seconds. Peak memory was not measured. Zero campaigns, research trials, random seeds, resamples, retries, downloads, market-data reads, holdout reads or spend. No new Linux run or platform acceptance claim.

## M2-E05 Test Card: decision-time causality, 2026-11-09

- **Decision and baseline.** Existing tests separately cover trailing features, fill timing and synthetic holdout separation. Check the combined path from completed-bar features through the momentum score to a simulated decision while prices and volume after that decision change. Reuse `market.features` and `evaluation.simulate`, with the same momentum input used by `evaluation.evaluate`. This covers one causal boundary in the [M2 criteria](MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls).
- **Fixed test.** Use one synthetic 80-bar sequence with seed 7, a known positive momentum score at the close of bar 40 and a three-bar holding horizon. Increase the next bar's OHLC prices by 50 percent and all later volumes by 100 percent in a copy. Validate both inputs. Require exact agreement of features through bar 40 and the same single long decision, signal time and fill indices. Require a different next-bar feature, entry price and realized net result to show the perturbation reached the execution path. Verify that the test rejects a planted one-bar look-ahead using a test-only substitution. Reuse [FTA-M0-A](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes). This test changes no production contract.
- **Resource Governor assessment and stop.** Up to 20 minutes once, no recurring work. Run the new test and the two existing focused feature and fill checks, with one fixed synthetic seed, zero model fits, folds, research trials, campaigns, downloads, market-data reads, holdout reads or spend. Estimate under 10 seconds for the focused tests and under 256 MiB peak memory. No resource limit changes. Record the test results and stop after this check. A detected production fault requires separate diagnosis before modifying the causal contract.

## M2-E05 Learning Card: decision-time causality, 2026-11-09

- **Result.** `SUPPORTED / PERSEVERE`. Changing synthetic prices and volume after bar 40 left all earlier features, the long decision, signal availability and entry and exit indices unchanged. The next-bar feature, entry price and realized net result changed. A test-only substitution that advanced the features by one bar caused the prefix equality assertion to fail as expected. Retain `tests/test_evaluation.py::test_future_bars_do_not_change_an_earlier_momentum_decision` as a regression test. This result covers the simple momentum policy on one fixture. Fitted-candidate behavior under the same perturbation and the full M2 gate remain open.
- **Verification and budget.** The targeted `python -B -m pytest -q` run of the new test and the existing feature and fill checks passed 3 tests in 1.47 seconds on native Windows. The planted-look-ahead check via `python -B -` and targeted `python -B -m ruff check` and `format --check` exited 0. Elapsed work through the focused checks was about 136 seconds. Zero fits, campaigns, trials, market-data reads, holdout reads, downloads or spend. Peak memory and Linux execution were not measured for this check.

## M2-E06 Test Card: fitted candidate causality, 2026-11-09

- **Decision and baseline.** M2-E05 covered the momentum policy with a score taken directly from a trailing feature. Check whether the actual Ridge evaluator gives the same earlier candidate scores and decisions when future bars change. Use one synthetic fixture, the existing fold builder, the `past_return` feature, and one fit per input copy. Reuse [FTA-M0-A](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes). The test changes no production contract.
- **Fixed proof.** Use an 80-bar fixture with seed 7 and deterministic rising prices with varying returns. Build one fold with 40 initial bars, an eight-bar validation span, and the existing three-bar horizon and purge. Change the next bar's OHLC prices by 50 percent and double later volumes, starting immediately after the final scored signal. Use identical costs and settings. Require the same training feature means, candidate scores within `1e-12` absolute tolerance, and the same nonempty candidate decision and timing sequence. Require the last trade's entry price and realized net result to change. Verify detection of a planted one-bar look-ahead by substituting the feature function in a separate test-only invocation. The normal run must pass and the planted-leak run must fail at the score comparison.
- **Resource Governor assessment and stop.** Up to 20 minutes once, with four fits maximum across the original and perturbed evaluations in the normal and planted-leak invocations. One fixed synthetic seed, one fold per evaluation, zero research trials, campaigns, resamples, downloads, market-data reads, holdout reads or spend. The retained regression adds two tiny fits per test-suite run. Estimate under 10 seconds per focused invocation and under 256 MiB peak memory. No limit changes. Stop after the focused checks and record any functional failure separately from an execution stop.

## M2-E06 Learning Card: fitted candidate causality, 2026-11-09

- **Result.** `SUPPORTED / PERSEVERE`. The Ridge evaluator refitted separately on each synthetic copy. Training feature means agreed exactly, candidate scores agreed within `1e-12`, and the simulated trade decisions and timestamps agreed. The last trade's entry price and realized net result changed. Substituting features from the next bar caused the candidate score assertion to fail as expected. Retain `tests/test_evaluation.py::test_future_bars_do_not_change_an_earlier_fitted_candidate_decision` as a regression test. The evidence covers one Ridge configuration and one fixture. M2 acceptance remains open.
- **Verification and budget.** The targeted `python -B -m pytest -q` run passed the Ridge and momentum regressions in 2.21 seconds on native Windows. The normal run and the planted-look-ahead check via `python -B -` each recorded one fit per copy, four fits in total. Targeted `python -B -m ruff check` and `format --check` exited 0. Elapsed work through focused checks was about 167 seconds. Zero campaigns, trials, market-data reads, holdout reads, downloads or spend. No new Linux run or peak memory measurement.

## M2-E07 Test Card: supervised pilot window, 2026-11-09

- **Decision and baseline.** Select a documented local BTCUSDT spot window for a bounded LightGBM versus Ridge development comparison. Use the M2-E03 import receipt, the M1-E02 manifest, checksum sidecars and file metadata. Keep January 5 outside the proposed comparison because M1 already used its outcome results. Require two complete initial training days and two successive full UTC validation-day spans. This is a workflow minimum. Base the selection on cadence, lineage and time boundaries.
- **Acceptance and stop.** For January 1 through 4, 2026 UTC, require all four archive names, matching recorded SHA-256 values in their sidecars, complete one-minute coverage in the existing evidence and two expanding folds from `market.build_folds`. Use the existing M1-E06 30-minute horizon as the planning assumption. Check that the last modeled exit in every training and validation interval precedes its boundary. If evidence is missing or inconsistent, report the gap. Stop at the metadata decision. No production contract changes. Fault Tree Analysis is not triggered by this review.
- **Resource Governor assessment.** One metadata review of up to 15 minutes. Zero archive payload reads, downloads, model fits, research trials, campaigns, resamples, holdout reads or spend. Two fold definitions are calculated from row counts only. No recurring work or budget change.

## M2-E07 Learning Card: supervised pilot window, 2026-11-09

- **Result.** `SUPPORTED / PERSEVERE` for planning the technical comparison. Select the four Binance Vision BTCUSDT spot days from `2026-01-01T00:00:00Z` inclusive to `2026-01-05T00:00:00Z` exclusive. The existing M2-E03 receipt supports 5,760 contiguous one-minute bars across those days. The January 5 archive remains development data with prior M1 outcome exposure and is outside this comparison. January 6 remains reserved. This short window supports a development exercise. Regime coverage, effective independent sample size, economic feasibility and predictive benefit remain untested.
- **Verified fold geometry.** With the inherited 30-minute horizon and a 31-row purge, train initially on January 1–2 and validate on January 3. Expand training through January 3 and validate on January 4. After the 12-row warmup and purge, the folds have 2,837 and 4,277 eligible training rows and 1,409 validation rows each. The latest training exits are January 2 and 3 at 23:59 UTC. The latest validation exits are January 3 and 4 at 23:59 UTC. These are modeled exit bounds derived from metadata and fold indices.
- **Verification and next prerequisite.** A read-only `python -B -` check on Windows matched four archive sidecars to the M2-E03 receipt, cross-checked the January 5 lineage against the M1-E02 manifest, calculated both folds and verified rejection of a third validation span beyond the input (exit 0). Elapsed work through the check was about 123 seconds. Zero archive payload reads, downloads, fits, campaigns, holdout reads or spend. The current CLI supports one spot day and accepts Ridge only. Prepare the model card and a separately scoped plan for validating and using the four-day input with both models under the existing Governor. Revalidate the actual archives before that pilot. No new Linux run.

## M2-E08 Test Card: supervised challenger pilot, 2026-11-09

- **Model card `M2-E08/1`.** `lightgbm` 4.6.0 ([MIT license](https://github.com/lightgbm-org/LightGBM/blob/v4.6.0/LICENSE), [release files](https://pypi.org/project/lightgbm/4.6.0/)), one local CPU regressor, no external model weights. Fix 32 trees, learning rate 0.05, at most 7 leaves, depth 3, at least 50 rows per leaf, deterministic column-wise mode, one thread and seed 42. Compare with the existing scaled Ridge (`alpha=1`, SVD) and zero prediction. The null is no consistent incremental forecast and net policy improvement over Ridge. No parameter or feature search.
- **Fixed comparison.** Revalidate the four archived Binance Vision BTCUSDT spot minute inputs against the M2-E03 digests. Use only January 1–4 UTC, the expanding folds from M2-E07, and the existing 31-row purge. Both models receive past return, relative volume and rolling volatility available at the close. The target is the next-open to 30-minute-exit gross return. Reuse the M1-E06 long-or-flat policy, unit notional, 25 bps illustrative round-trip costs and 2 bps buffer, with momentum and no-trade controls. January 5 and the January 6 holdout are outside the input.
- **Decision and stopping rule.** Keep the existing training-only economic screen. If it stops the candidates, record the screen and stop without changing the inputs or thresholds. Otherwise record aggregate and per-day MAE and net PnL, trade counts and turnover. Use the two paired validation-day deltas as descriptive uncertainty. Consider a later development comparison only if LightGBM has lower MAE and higher net PnL than Ridge on both days and positive combined net PnL. Technical completion is separate. A short development window cannot establish independent or economic acceptance. Require valid provenance, both folds and an intact journal. On Linux compare decisions and metrics within `1e-8` absolute tolerance if Windows completes. Stop on any failed guard, mismatch or exhausted budget, with no automatic retries.
- **Resource Governor assessment.** Up to 90 minutes once. One sequential campaign per platform, two trials, two folds, one seed, four comparison fits and two synthetic preflight fits per campaign. Zero market-data downloads, holdout reads, resampling, recurring work or spend. Allow two pinned platform wheels and at most 25 MiB of new local artifacts, including wheels. Estimate under 30 seconds and 384 MiB sampled worker RSS per campaign, subject to measured preflight. Reuse the 120-second trial, 300-second campaign and 4,096 MiB sampled RSS ceilings. No limit increases.

## M2-E08 Learning Card: supervised challenger pilot, 2026-11-09

- **Execution and evidence.** `BLOCKED / STOP` for the paired comparison. `python -B artifacts/m2-e08/pilot.py artifacts/m2-e08/windows` exited 2, run `3a7d57c4cef449d19383723cbfbf810d`. The four archive digests and combined minute cadence verified. Both synthetic preflights completed one fit. The economic screen admitted the window at 30.9712 bps against 27 bps, and Ridge completed both folds. The LightGBM worker exited 1 after one completed fit and produced no result. Total charge was five fits, with peak sampled worker RSS of 119.34 MiB. The comparison has no paired outcome. The Ubuntu replay stayed pending. The journal passed `PRAGMA integrity_check`, and the receipt recorded zero holdout reads. No retry or market-data download. See `artifacts/m2-e08/windows/report.json` and `research.sqlite3`.
- **M2-INC-01.** The timing preflight exercised `.fit()` and did not exercise fold reporting. The evaluator then expected `named_steps.standardscaler` from a raw estimator, a Ridge pipeline detail. The original worker receipt retained the exit code and fit count but no traceback. A no-training reproducer with a scaler-free estimator raised `AttributeError` at that field, and a local LightGBM 4.6.0 instance confirmed the missing attribute. The evaluator now keeps the actual scaler means for Ridge and uses training input means for an unscaled estimator. The focused regression failed before this correction and passed afterward. A completed corrected LightGBM campaign remains unverified. The incomplete attempt is excluded from research decisions.
- **Verification.** The synthetic scope and fold guards passed before the campaign. The failing regression exited 1 with the expected exception. After the correction, targeted pytest passed three tests in 1.90 seconds, and targeted Ruff lint and format checks passed. These post-stop tests used no additional model fits. Read-only receipt and journal verification passed. Elapsed work through the diagnosis was about 386 seconds. The existing CLI inputs, costs, holdout and enforcement contracts were preserved.

## M2-E09 Test Card: corrected supervised pilot replay, 2026-11-09

Run the corrected pilot once on Windows in a new output directory with the unchanged M2-E08 model card and four-day input. A complete Windows comparison allows the headless non-root Ubuntu replay. Use the same technical and benefit criteria. Budget up to 45 minutes of one-time work, at most six new fits per platform, one seed and two sequential trials per campaign, under the same limits. Expect under 30 seconds and 384 MiB sampled worker RSS per campaign subject to measured preflight. Reuse the staged wheels, with zero new market-data downloads, holdout reads, spend or automatic campaign retries. Stop on another execution failure, budget stop or platform mismatch and retain all charges and evidence.

## M2-E09 Learning Card: corrected supervised pilot replay, 2026-11-09

- **Execution and parity.** `SUPPORTED / PERSEVERE` for the bounded supervised pilot. `python -B artifacts/m2-e08/pilot.py artifacts/m2-e09/windows` and the equivalent `ubuntu` command both exited 0. Windows 11 build 26300, Python 3.12.12, run `9de172568b9842f0840345abd548fe53`. Headless Ubuntu 24.04.5, UID 1000, kernel 6.8.0-147-generic, Python 3.12.3, run `d9f180a7e58345be855702d5af768e7d`. `python -B artifacts/m2-e09/verify_replay.py` exited 0. Dataset bytes, configuration, fold dates and trade decisions matched. Reported metrics agreed within `1e-8` absolute tolerance. Both SQLite journals passed integrity checks. The platform replay is technical reproduction of the same development variant.
- **Benefit finding.** `DEFER` for a LightGBM follow-up under the fixed rule. Aggregate MAE was 10.77443 bps for Ridge and 10.77641 bps for LightGBM. On January 3, Ridge had lower MAE (10.88914 versus 10.96276 bps) and both stayed flat. On January 4, LightGBM had lower MAE (10.59006 versus 10.65972 bps), but its only trade lost 21.87163 bps net on unit notional. Ridge stayed flat on both days. The two paired days did not meet the prespecified benefit threshold. Evidence status stays `INSUFFICIENT_EVIDENCE` for both models. This development comparison does not establish independent predictive or economic evidence.
- **Ubuntu preparation and budget.** The initial offline install lacked the cached `cloudpickle` wheel. After staging it, `pip check` passed. The LightGBM import then identified a missing OpenMP runtime. Extracting the [checksum-verified Ubuntu `libgomp1` package](https://packages.ubuntu.com/noble/amd64/libgomp1/download) into the guest user's directory fixed the import without root. No campaign or model fit ran during either setup stop. Each completed campaign used two preflight fits and four comparison fits. Peak sampled worker RSS was 119.96 MiB on Windows and 127.36 MiB on Ubuntu. Each worker finished in under two seconds. Elapsed work through the comparison was about 306 seconds. Zero campaign retries, holdout reads, market-data downloads, resampling or spend. The archived `ubuntu.log`, both reports and `comparison.json` retain the evidence. M2 acceptance remains open.

**Historical provenance boundary.** M1/v0.2 is the gate label. Its M1-E11 report records package version `0.1.0` and the source fingerprint matched to the accepted Ubuntu replay. Use the frozen configuration and linked receipts above for the M1 evidence. The M2-E08 and M2-E09 report IDs and journal keys identify the recorded attempts and shared scientific variant. The M2-E09 report and Ubuntu setup log record the Python and LightGBM versions. The Ubuntu log also records installed package versions, the AQRS wheel digest, and the OpenMP setup. These records do not bind either platform's attempt to recoverable AQRS and pilot source bytes. The current archived script is an available reference with no verified execution digest for those historical attempts. For any separately authorized reproduction, use the [versioned pilot](../scripts/m2_supervised_pilot.py). It saves the source snapshot alongside the new run, references its digests and installed dependency versions in the report and journal, and runs workers from that snapshot.

## M2-E10 Test Card: Isolation Forest volatility alert, 2026-11-09

**State.** The owner authorized the frozen card, the four named development archives, and the conditional Ubuntu replay on 2026-11-09. The riskiest implementation assumption is that identical fold boundaries govern calibration, scoring, and the hour-level comparison. Verify the registered timing and train-only inputs with zero-fit synthetic tests and a separate read-only review before launching either campaign. M2-E09 provides the workflow baseline. This card is the [M2 unsupervised pilot](MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls), with its own model and evidence lineage.

- **Decision and null.** Determine whether an Isolation Forest alert adds a useful warning of a larger future price move beyond already high trailing volatility. The rival explanation is that a simple volatility threshold identifies the same useful conditions. The null for this screen is that adding the anomaly filter fails to reach the registered improvement. The score carries no directional forecast. Record the forecast comparison, illustrative trading diagnostic, and software acceptance separately.
- **Model card `M2-E10/1`.** Registry ID `isolation_forest`. Pin scikit-learn 1.9.1 under [BSD 3-Clause](https://github.com/scikit-learn/scikit-learn/blob/1.9.1/COPYING). Use local fits without external weights. Fix `IsolationForest(n_estimators=64, max_samples=256, contamination="auto", max_features=1.0, bootstrap=False, n_jobs=1, random_state=42, warm_start=False)` and single-threaded scoring. Fit only the fold's training features `past_return`, `relative_volume`, and `rolling_volatility`, as available after the completed minute. Pass no outcomes to the fit. Use `-score_samples(X)` as the anomaly score and no scaling or tuning. See the [version-matched scoring API](https://scikit-learn.org/1.9/modules/generated/sklearn.ensemble.IsolationForest.html#sklearn.ensemble.IsolationForest.score_samples).
- **Data and timing.** Use only the four archived Binance Vision BTCUSDT spot one-minute UTC days from January 1 through 4, 2026, with the [M2-E03 digests](#m2-e03-learning-card-extended-development-data-coverage-2026-11-09) and the existing personal, non-production research scope. Check each archive digest, date and minute cadence before use. Reuse [M2-E07](#m2-e07-learning-card-supervised-pilot-window-2026-11-09) expanding folds, 12-row warm-up, 31-row purge, and January 3 and 4 validation days. The 30-minute target is the absolute simple return from `open[t+1]` to `open[t+31]`. January 5 and the January 6 reserved holdout are outside the input. January 3 and 4 were used in M2-E09 and are development evidence.
- **Alerts and control.** In each fold fix the 90th percentile of training volatility and the 90th percentile of training anomaly scores with linear interpolation. Within each UTC hour consider only bars opening in minutes 00 through 28 so the complete modeled outcome stays inside that hour. The control alerts on the first eligible completed bar strictly above the volatility cutoff. The challenger alerts on the first eligible completed bar strictly above both cutoffs. Each arm can alert at most once per hour. Pair arms only within the same hour when both alert, count simultaneous alerts as zero paired difference, and report every hour and all unmatched coverage. This compares the filter with its volatility-only ablation in the same high-volatility conditions and time block.
- **Economic screen and diagnostic.** Before real-data fits, reuse the first-fold training-only 90th percentile absolute move screen. At or below 27 bps, record `SCREENED_OUT` and stop. For completed comparisons use the same illustrative long-at-alert policy for both arms over all their registered alerts, with no overlap, unit notional, next open, 30-minute exit, and a flat reference. Use 10 bps fees per side, 1 bp quoted spread and 2 bps slippage per side, or 25 bps round trip, with the additional 2 bps buffer used only in the economic screen. Report net bps per alert, net PnL, cost, alert counts and turnover separately. This is a fixed execution diagnostic and does not enter the volatility follow-up rule.
- **Follow-up rule.** For each validation day report the paired-hour count and mean of `abs(return_challenger) - abs(return_control)` in bps. Advance to a proposal for a separately authorized development window only if both days have at least four paired hours and both daily means are at least 5 bps. Four hours is a workflow coverage floor. Five bps is a practical screening margin on the scale of the illustrative spread and slippage. These are planning choices and provide no significance threshold or economic claim. With sparse, mixed or smaller effects, record `INSUFFICIENT_EVIDENCE / DEFER`, keeping the daily differences visible. Treat hours and days as descriptive blocks and avoid counting them as independent replications. Do not retune the window, cutoff, seed or model.
- **Technical proof and stop.** Reuse the market features and folds, local importer, simulator, Governor and journal. Keep anomaly scores distinct from directional return forecasts and evaluate the alerts against the registered absolute-return target. Engineering selects the scoring implementation within the approved scope. Before real-data execution check train-only fit and cutoff inputs with a spy, reject a planted invalid date or exit boundary, and check that perturbing future rows leaves earlier scores and alerts unchanged. Use synthetic fixtures with zero estimator fits for these checks. Within the pilot, repeat the score check with the same fitted instance and account for the extra scoring in preflight. Reuse the causal and archive failure paths in the [risk register](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes) and complete the separate verification required for any critical change. Require valid guards, exact discrete alerts, common input and configuration IDs, fold boundaries, budget counts, and intact journals. Replay on headless non-root Ubuntu only after the native Windows comparison is complete and valid. Require identical discrete outcomes and absolute numeric agreement within `1e-8` in native report units. Stop on any guard failure, mismatch or budget stop. Record technical failures separately from the benefit decision and keep M2 acceptance open until all M2 criteria pass.
- **Resource Governor assessment.** Estimate one focused implementation and verification session of up to two hours, subject to separate scope approval. Plan at most one sequential campaign on Windows and one conditional Ubuntu replay. Per platform reserve two registered variants, two folds, one seed, one synthetic timing fit and two Isolation Forest fold fits. Reserve two additional budget units for the deterministic control cutoff calibrations, for five units total. Account for the flat reference and same-hour pairing in the plan. Estimate under 30 seconds and 384 MiB sampled RSS per platform subject to a synthetic timing pilot capped at five seconds and conservative preflight. Keep the existing 120-second trial, 300-second campaign and 4,096 MiB sampled RSS limits. Zero resamples, new market-data downloads, holdout reads, retries, spend, or recurring runs. Stop at the two platform receipts or the first blocker.

**Planning verification, 2026-11-09.** The focused Windows check matched four archived checksum sidecars against the frozen M2-E08 allowlist, reproduced the fold counts, and checked all 696 eligible minutes per validation day for exit within their UTC hour. It verified the 25 bps round-trip cost, 27 bps economic screen, and fit budget against the current configuration. Links, changelog coverage, manual English review, both language checks, and `git diff --check` passed. The focused check ran about 80 seconds after the baseline snapshot. Zero archive payload reads, campaigns, fits, protected reads, or new Linux runs. Alert coverage, timing, and benefit remain unmeasured.

## M2-E10 Learning Card: Isolation Forest pilot, 2026-11-09

**Engineering and Verification.** The frozen comparison completed on native Windows 11 (Python 3.12.12, run `0da57660ffe74ad1a9ddcf2d92f4cc8e`) and on headless Ubuntu 24.04.5 as UID 1000 (Python 3.12.3, run `f7ef9ddd05a44a38ba5e8e0603a74955`). Both used scikit-learn 1.9.1. The [Windows receipt](../artifacts/m2-e10/windows/report.json), [Ubuntu receipt](../artifacts/m2-e10/ubuntu/report.json) and [comparison](../artifacts/m2-e10/comparison.json) record matching source, data and configuration IDs, fold boundaries, alert indices, decisions and metrics within the registered absolute tolerance of `1e-8`. Both SQLite journals passed integrity checks and matched their receipts. A separate read-only reviewer verified the run lineage and journal links, recalculated the paired differences from simulated gross moves, and confirmed the entry and exit timing, costs, and registered disposition. Each platform used one synthetic timing fit, two Isolation Forest fold fits and two control calibrations. Campaign wall time was 6.36 s on Windows and 2.78 s on Ubuntu, with peak sampled worker RSS of 123.98 and 127.65 MiB. The timing workers finished in 2.31 and 0.88 s, within the five-second limit. Future-row perturbations changed none of the first 749 validation scores or alerts in either fold on either platform.

**Pre-run verification.** The separate read-only reviewer found two preflight gaps. The implementation now checks the frozen copy of the current Governor limits and validates the four archives and folds before the timing fit. The reviewer checked the final source digests and cleared the corrected snapshot. The focused Windows pytest command (`python -B -m pytest -q tests/test_isolation_pilot.py`) passed six zero-fit checks. It covers training-only fit and calibration, out-of-scope inputs and exits, an intentionally future-dependent scorer, hour pairing and cost arithmetic, replay comparison, and preflight rejection. Ruff and its format check passed on the three Python files. Both campaign invocations and `python -B scripts/m2_isolation_forest_pilot.py --verify-replay` exited 0. The first Ubuntu setup stopped before execution because the uploaded archive name differed from the staging script. Setup resumed after correcting the name, then the offline installation and `python -m pip check` passed. The [guest log](../artifacts/m2-e10/ubuntu.log) retains both setup outcomes. About 215 seconds elapsed from session opening through the first receipt comparison. Zero campaign retries, new data downloads, protected reads, resamples or spend.

**Quant Research.** `INSUFFICIENT_EVIDENCE / DEFER`. The first training fold passed the economic screen at 30.97 bps. January 3 UTC had no alerts and no paired mean. January 4 UTC had six paired hours and one control-only hour. Both arms alerted at the same minute in all six pairs, so the paired mean difference was 0.00 bps. The registered rule required at least four pairs and at least 5 bps mean improvement on each day. The filter dropped one volatility alert and added no timing advantage in the paired hours. Coverage is too sparse to establish whether the filter helps on a different development window. The Ubuntu replay reused the same days.

**Separate execution diagnostic.** With the fixed 25 bps round-trip cost, the volatility-only policy produced 7 long alerts, −30.41 net bps per alert, −0.02129 net PnL on unit positions, 0.0175 total modeled cost and 14 units of turnover. The Isolation Forest arm produced 6 long alerts, −24.34 net bps per alert, −0.01460 net PnL, 0.0150 cost and 12 units of turnover. The flat reference was zero. The economic diagnostic did not enter the follow-up decision.

**Disposition.** Technical pilot `SUPPORTED / PERSEVERE`. Research benefit `INCONCLUSIVE / DEFER`. Keep the window, cutoffs and model frozen. Consider another registered comparison only if suitable new development coverage and a decision-changing question justify separate authorization. No incident postmortem was triggered. The supervised and unsupervised pilot criterion has evidence. Full M2 acceptance stays open pending the remaining [M2 criteria](MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls).

## M2-E11 Test Card: M2 evidence review, 2026-11-09

- **Assumption and baseline.** The closed pilot cards and their receipts can distinguish remaining M2 work from evidence already collected. The baseline is the M2-E10 disposition, which confirms the paired pilots and leaves the other criteria open for review. Map every criterion to a receipt, a scoped demonstration, or a specific missing prerequisite. Pass if the review identifies one decision-changing next step and preserves both pilot dispositions and the M2 acceptance boundary.
- **Budget and stop.** One documentation session of up to 20 minutes. Read only existing cards, catalog entries, and report metadata. Zero campaign trials, model fits, new market-data reads, downloads, resamples, protected reads, spend, or recurring work. Governor limits and research contracts stay fixed. Routine documentation risk, with no Fault Tree Analysis triggered. Stop at the evidence map and the next start condition.

## M2-E11 Learning Card: M2 evidence review, 2026-11-09

`SUPPORTED / PERSEVERE` for using existing evidence to sequence the remaining work. M2 stays `IN_PROGRESS`.

| M2 criteria | Evidence or gap |
|---|---|
| Supervised pilot outcome parity | **MET for the recorded replay.** [M2-E09](#m2-e09-learning-card-corrected-supervised-pilot-replay-2026-11-09) completed on both platforms. Recorded data, configuration, folds and decisions matched, and metrics agreed within the registered tolerance. The research follow-up remains deferred. |
| Supervised pilot source reproducibility | **OPEN for M2 acceptance.** [M2-E16](#m2-e16-learning-card-historical-source-binding-2026-11-10) confirmed the AQRS-A02 evidence gap. During M2 acceptance review, Engineering can reopen this check if it obtains recoverable source with original run linkage. Otherwise the smallest bounded replay with recoverable snapshots on both platforms needs separate authorization. Close applicable [execution-path quality debt](RISK_REGISTER.md#open-execution-path-quality-debt) before reusing a blocked entry. This acceptance condition does not block an independent M2-E14 campaign. |
| Unsupervised baseline pilot and guarded Windows/Linux execution | [M2-E10](#m2-e10-learning-card-isolation-forest-pilot-2026-11-09) completed on both platforms with matching source and result evidence. The research follow-up remains deferred. |
| Trivial and simple forecast baselines | M2-E09 compares zero prediction, Ridge and LightGBM on the same chronological development folds. |
| Decision control for a known filter | M2-E10 matches the volatility-plus-anomaly alerts against volatility alone within each hour. It found no timing advantage among the six paired alerts. This is evidence for the control on an alert policy. |
| Negative control for a deliberately misleading association | [M2-E01](#m2-e01-learning-card-one-event-research-decision-2026-11-09) plants a rebound shared by both arms. The candidate-only result is 7 bps net. The matched advantage is 0 bps, so the decision changes from `ADVANCE` to `DEFER`. The evidence is synthetic. |
| Adversarial causality and planted effect versus null | [M2-E05](#m2-e05-learning-card-decision-time-causality-2026-11-09), [M2-E06](#m2-e06-learning-card-fitted-candidate-causality-2026-11-09) and M2-E10 cover the tested rule and fitted paths. [M2-E04](#m2-e04-learning-card-synthetic-interaction-comparison-2026-11-09) separates the synthetic XOR effect from the null without forced selection. |
| One real-data campaign with two interpretable, versioned alpha candidates | Open. The supervised comparison and the separate nondirectional anomaly alert do not establish the requested candidate generation and registry evidence. |
| Hypothesis origin, input availability and detection cadence per candidate | Pilot cards fix the purpose, target, input timing and decision or alert rules for their comparisons. Completion depends on registering these fields for both candidates in the required campaign. |
| Cost-aware matched rule-based outcome study | Open. [M2-E03](#m2-e03-learning-card-extended-development-data-coverage-2026-11-09) counted two matched price-drop pairs on one date. The registered minimum is a pair per UTC time band on three distinct dates. No forward outcomes were evaluated. |
| Per-candidate costs, turnover, effective independent event count and tried-variant count | Pilot receipts show modeled costs, turnover and trial counts. The descriptive day and hour counts do not establish effective independent event counts or complete exposure accounting for the required candidate campaign. |
| Five remaining `EVALUATE` model cards and decisions | Open. The [catalog](MODEL_TOOL_CATALOG.md#g-milestones-and-minimum-commitments) retains XGBoost, HDBSCAN, PCA, autoencoders and Random Forest. Each needs a model card and a bounded comparison or a reasoned disposition with a specific revisit trigger. |

- **Evidence and resources.** A read-only `.venv/Scripts/python.exe -B -` check reproduced the M2-E01 arithmetic, confirmed both M2-E03 pairs and the count-only disposition, checked all five registry entries, and cross-checked four M2-E09/M2-E10 reports against their two comparison receipts. The first check exited 1 because it treated a fold list as a count. The corrected check exited 0 and verified both validation dates. The review and evidence map took about five minutes. No receipt changed. No fresh Linux execution, campaign, model fit, market-data read, download, or holdout access.
- **Next decision.** Test coverage first with M2-E12. A pass can justify an outcome card for the fixed rule; a miss leaves the study deferred. Repeating either model pilot on its original validation window would leave the rule-based coverage gap unchanged. The separate real-data candidate campaign and remaining model assessments still require their own evidence.

## M2-E12 Test Card: earlier price-drop coverage, 2026-11-09

- **Decision and minimum test.** Determine whether one additional contiguous week provides enough matched events to design the deferred outcome study. Propose the seven BTCUSDT spot UTC archives for December 25–31, 2025, immediately before the existing January 1–5 development window. The calendar boundary fixes the window without using observed outcomes. Subject to separate authorization, reuse the [M2-E03 acquisition and count procedure](#m2-e03-test-card-extended-development-data-coverage-2026-11-09), its unchanged trigger, pairing and three-band/three-date coverage criterion, and its January 1–5 count receipt. Pass only if the combined counts contain a pair per time band on three distinct dates. Record `DEFER` on insufficient coverage and stop on an acquisition, scope, import, or budget failure. A coverage pass warrants a separately scoped outcome card. No threshold search or forward returns in this step.
- **Resource Governor assessment.** Up to 45 minutes of one-time work. Exactly seven allowed ZIP paths and their checksum paths, at most 14 HTTPS requests with no redirects or retries. Cap each archive at 512 KiB and each checksum at 4 KiB, with at most 4 MiB of new storage including the receipt. Bound acquisition at 120 seconds and the local scan at 30 seconds. Scan at most 10,080 new rows plus the five existing count records. Expect under 256 MiB peak RSS for the sequential scan based on the existing small inputs. Transfer time and memory remain estimates. Zero campaign trials, fits, resamples, spend, protected reads, recurring work or Governor limit changes. Recheck the existing scope and acquisition safeguards before execution. Start only after authorization of the named dates and count-only scope.
- **Execution risk screen, 2026-11-10.** Reuse FTA-M1-A, FTA-M1-B and the M2-E03 redirect and URL checks in the [risk register](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes). Replace the historical runner's file scope before use and verify the exact effective allowlist and rejection of protected and out-of-scope paths without network access. Reuse the importer, count scanner and distinct-date predicate. No production contract changes.

## M2-E12 Learning Card: earlier price-drop coverage, 2026-11-10

- **Result.** `REFUTED / DEFER` for sufficient coverage in this fixed window. December 25–31 added five triggers and three pairs. December 26, 29 and 30 each supplied a pair in 08:00–16:00 UTC. Across the new days and the five reused January count records, there were eight triggers and five pairs on four dates. The 00:00–08:00 UTC band had no pair, 08:00–16:00 had four, and 16:00–24:00 had one. The three-band, three-date criterion remains unmet. The counts do not determine the effect after costs.
- **Execution and evidence.** `.venv/Scripts/python.exe -B artifacts/m2-e12/run_coverage.py` exited 0 on native Windows with Python 3.12.12. Acquisition took 13.076 seconds and counting took 0.389 seconds. Both phases exited 0. The [receipt](../artifacts/m2-e12/coverage.json) retains 14 exact requests, all seven verified archive digests, source digests, and counts for 10,080 new one-minute bars. Local files totaled 489,517 bytes. The adapter reused the historical acquisition, importer and scanner. Offline scope and redirect checks and a separate read-only receipt check exited 0. About three minutes elapsed through the run and receipt verification. Zero forward outcomes, model fits, retries, protected reads, spend, or new Linux runs. Peak memory was not measured.
- **Next decision.** Leave the event rule frozen. Consider reopening coverage only with a separate, justified development-window proposal capable of testing the missing UTC band. Assess the five outstanding M2 model cards and dispositions from existing evidence first. The real-data candidate campaign and M2 acceptance remain open.

## M2-E13 Test Card: five model assessments, 2026-11-10

- **Assumption and baseline.** The five open M2 `EVALUATE` entries and existing receipts can support a specific disposition for each. The baseline is the unresolved model row in the M2-E11 evidence map. Pass if every entry has a documented role, a scoped evidence-based disposition, a concrete condition for reconsideration, and the smallest fair comparison if that condition is met. Preserve the planning registry and distinguish indirect evidence from a direct pilot. A documented evidence gap is a valid result.
- **Resource Governor and stop.** One documentation session, up to 20 minutes, with zero campaigns, fits, new data access, downloads, resampling, protected reads, spend or recurring work. Stop at the five verified assessment cards. A future pilot requires its own card and preflight. Routine documentation risk. No critical contract changes or Fault Tree Analysis.

## M2-E13 Learning Card: five model assessments, 2026-11-10

- **Decision.** `SUPPORTED / PERSEVERE` for completing the model assessment record. The [five cards](MODEL_TOOL_CATALOG.md#m2-assessment-cards-2026-11-10) defer XGBoost, Random Forest, HDBSCAN and the autoencoder. The cross-series PCA use is `BLOCKED_DATA` in the qualified scope. Each card records the specific evidence that would reopen the decision and the required comparison. These are assessment dispositions without direct model runs.
- **Verification and resources.** A read-only `.venv/Scripts/python.exe -B -` check confirmed all five `EVALUATE` registry entries and checked the archived M2-E04 synthetic comparison and the M2-E09 and M2-E10 results from both platforms. The review took about two minutes through the evidence check. Zero downloads, fits, market-data payload reads, protected reads or new platform runs.
- **Next decision.** Prepare a Test Card for the separate real-data campaign that must yield two versioned and interpretable candidates. Establish the candidate roles, causal inputs, matched controls and costs before proposing a data scope or execution budget. The matched rule-based outcome study and M2 acceptance remain open.

## M2-E14 Test Card: two interpretable real-data candidates, 2026-11-10

**AQRS-A08 start-condition clarification, 2026-11-11.** Before any outcome run, require the V1-bias rejection / V2 null and planted-effect self-test, a justified precision/decision plan for this campaign, and independent substantive review of its frozen full evaluation path. The illustrative 619-unit calculation does not resolve the missing empirical assumptions. Register each diagnostic view on reused dates in exposure accounting even when the model is unchanged. The future campaign entry must reject incomplete records before outcome access; that entry and its admission tests remain unimplemented. These prerequisites precede M2-E14 and do not silently amend its proposed thresholds or authorize a run.

**AQRS-A07 admission amendment, 2026-11-11.** The original proposed definitions and thresholds below are preserved, not executed or silently relaxed. They are coverage and development-screen conditions, not proof of statistical precision. Six validation dates with at most one event pair per eight-hour band allow at most 18 pairs before missing coverage; they are not automatically 18 independent observations. Under an illustrative independent-pair SD of 20 bps, one-sided alpha 0.05 and power 0.8, detecting a 2-bps mean relative to zero requires 619 units; 18 units detect about 11.72 bps under that approximation. These are assumptions, not measured market dispersion or a calibrated joint false-positive rate.

Before running, explicitly choose the intended descriptive or inferential decision, justify its independent unit and uncertainty method, and demonstrate that the answer can change a decision within the existing budget. The event's paired comparison is a conditional event description; a filter-value claim also needs the baseline's fixed complete opportunity population including skips. Do not substitute the 2-bps paired threshold into a new denominator without registering a revised variant. The forecast path already specifies a one-feature fitted control and common opportunities; preserve it. If adequate effect evidence is unavailable, retain `INCONCLUSIVE / DEFER` for that claim, even if the technical pipeline succeeds. A new data window, policy, horizon or threshold needs a new counted definition and approval; AQRS-A07 grants none of those runs.

- **Decision and baseline.** Determine whether one campaign can register, evaluate and explain two different real-data research candidates under shared execution and causal controls. The earlier model pilots and the deferred price-drop count do not supply this campaign. Both hypotheses below are specified before this campaign. Prior use of these archives makes the results development evidence. The thresholds are proposed decision criteria for a small follow-up screen. No results were inspected to set them.
- **Candidate `VOL_CONFIRM_V1`.** Hypothesis: unusually high relative volume strengthens short-horizon continuation after a positive five-minute BTCUSDT spot move. At each completed minute `t`, compare `close[t] / close[t-5] - 1` with zero. Among positive events, the candidate adds a filter at the training-only 75th percentile of relative volume among positive events. Reuse the existing definition of current volume divided by the mean of the prior 12 completed minutes. The baseline is the positive-move rule alone, evaluated on the same opportunities. Report actions and skips for both. For the event contrast, take at most one non-overlapping pair per UTC eight-hour band per validation day. In chronological order, match the first eligible high-volume event with the nearest eligible below-threshold positive event in that band, breaking ties by earlier timestamp. Both simulated exits must precede the band end. Freeze the cutoff per fold and count uncovered bands and unmatched opportunities.
- **Candidate `RIDGE_INCREMENT_V1`.** Hypothesis: relative volume and rolling volatility improve a 30-minute forward-return forecast over one-bar return alone. At each completed minute use the three existing trailing features and the existing Ridge pipeline. Compare with zero and an otherwise identical Ridge fitted on one-bar return alone. Standardization fits on training rows only. Compare both Ridge decision policies on the same validation rows and position rules, with momentum and flat as additional references. The fitted score changes the baseline long-or-flat decision only by crossing the same cost-plus-buffer threshold.
- **Timing and proposed inputs.** Use only the ten previously acquired BTCUSDT spot minute archives for December 25–31, 2025 and January 1–3, 2026 UTC, with the recorded [M2-E12](#m2-e12-learning-card-earlier-price-drop-coverage-2026-11-10) and [M2-E03](#m2-e03-learning-card-extended-development-data-coverage-2026-11-09) digests. Train through December 28 and validate December 29–31, then train through December 31 and validate January 1–3. Reuse the 31-row purge for the shared 30-minute horizon. Only completed bars through `t` inform the decision. Enter long at `open[t+1]`, exit at `open[t+31]`, use unit notional and one open position per policy. Apply the prior pilot's illustrative 25 bps round-trip cost (20 fees, 1 spread, 4 slippage) and a separate 2 bps Ridge decision buffer. January 6, 2026 UTC remains protected. Validate the exact allowlist before file access and check digests, cadence and strict exit boundaries before fitting or evaluating outcomes.
- **Decision gates.** A technical pass requires both versioned records, including hypothesis and origin, timings, input and source identities, matched controls, gross and net results, turnover, trial exposure and coverage by UTC day and band. Report non-overlapping counts and independent-day evidence separately, with dependence and any unavailable effective sample-size estimate explicit. Check future-only perturbation for both candidates and an artificial shared-outcome case that yields no incremental advantage. For the event follow-up, require at least 12 matched pairs across at least four days, with at least four pairs per fold, mean event net return of at least 5 bps and mean paired advantage of at least 2 bps. For the forecast follow-up, require at least a 1% relative MAE reduction against both forecasts in each fold, at least 12 candidate trades across four days with at least four per fold, mean candidate net return of at least 5 bps per trade, and mean incremental net return of at least 2 bps per common eligible opportunity versus the one-feature Ridge policy, including flat decisions. Otherwise record the failed threshold or insufficient coverage and defer follow-up. Keep both results even if neither advances. These screens do not establish independent alpha or M2 acceptance.
- **Resource Governor and stop.** Planning only was approved, with zero archive reads, fits or campaigns. Proposed execution allows up to three hours of development and one sequential campaign per platform, with Ubuntu conditional on a valid Windows result. Per campaign: two candidate trials, two folds, four Ridge fits including the fitted control, one representative timing fit, one seed, zero resamples, zero network data requests, zero spend and zero protected reads. Reuse the importer, fold builder, evaluator and supervised workers. Retain the existing 120-second trial and 300-second campaign deadlines and 4,096 MiB sampled-RSS ceiling. Estimate under 90 seconds and 512 MiB sampled RSS per campaign and up to 10 MiB of new evidence across both platforms, subject to preflight. Count control fits explicitly before launch. Refine [FTA-M0-A and FTA-M1-B](RISK_REGISTER.md#mandatory-fault-tree-analysis-fta-for-critical-development-changes) and obtain the required independent review before execution. Stop on invalid scope, a timing or cost invariant failure, resource rejection or replay mismatch. No retries, budget increases or alternate windows within this card.

**Planning verification, 2026-11-10.** A read-only `python -B -` check exited 0. The count receipts supply digest records for all ten dates. The existing fold builder on the 14,400 planned rows keeps every modeled exit before its interval boundary. The cost helper reproduces 25 bps, and the two trials and five fits per platform fit the static limits. No archive payload was opened. Live preflight and the execution path remain unverified. Prefer reusing the importer, fold builder, evaluator and worker supervisor behind a campaign entry with its own verified admission. An entry that inherits either open Governor finding still needs that finding closed before reuse. The named data access and run remain `WAITING` for authorization.

### M2-E14 pre-outcome design checkpoint

**Design Test Card, 2026-11-11.** Baseline `1f71d5e` plus the existing
working-tree edits. The riskiest assumption is that this fixed window can
inform a bounded development decision once the comparison populations and
denominators are explicit. The alternative is that an effect claim or an
ambiguous denominator makes the proposed result unusable. Require the exact
ten-day metadata scope, both purged folds, the original costs and gates, known
answers for null and planted controls, and a prospective index for all planned
views. Check the count and denominator arithmetically and exercise existing
timing, cost and control helpers on synthetic inputs. Pass permits a synthetic
campaign-entry implementation proposal. Stop if the design requires changing
the window, thresholds, budget or an existing runtime contract. Allow up to
25 minutes of design and verification, zero market or protected reads, trials,
estimator fits, resamples, network requests or spend. This checkpoint has no
recurring runtime cost. ADR-043/044/049 and IDEA-001/004 favor retaining the
fixed event and controls over a new search. No critical runtime contract changes.
Map the risks for the later implementation before it starts.

**Decision and precision.** Use the existing campaign to test reproducible
discovery and apply the unchanged follow-up screens on the named development
sample. A passing screen permits a proposal for a new, adequately designed
study. A failed screen defers that follow-up. Both outcomes leave the effect
claim open. Show the observed coverage and comparison values separately by
day and fold, and report effective independent units as unknown.
There are at most 18 non-overlapping matched pairs across six validation dates.
Even if all 18 pairs were independent with a 20 bps standard deviation, the
existing calculation needs 619 units for a 2 bps mean effect and detects only
about 11.72 bps at that capacity. Six assumed independent day means at the
same illustrative dispersion would detect about 20.30 bps. Dispersion for either
unit and serial dependence are unknown. The Ridge rows also have overlapping
30-minute labels. The default for market-effect claims is `INCONCLUSIVE / DEFER`.
Quant Research revisits inference when a separately scoped plan can justify
dispersion, independent units and a precision target for the specific claim.

**Population and attribution.** Use the existing 31-row purge and timestamp
actions by the next open, when the signal is available. Attribute fills and
their complete round-trip P&L to the entry's UTC date and eight-hour band.
Run each policy chronologically on the same signal rows as its own control,
with a separate one-position state per policy. Positions may close and reopen
at the same open. A skipped row contributes zero P&L for that policy and
remains in the denominator, including while a position is open.

- **Volume.** Use every fold-eligible positive five-minute move for the policy
  contrast. Estimate the 75th percentile with linear interpolation on the
  purged training positives, with values at the cutoff assigned to high
  volume. An empty calibration population makes the comparison unavailable.
  For the separate paired contrast, use high and below-cutoff positives in
  the same entry band with both exits strictly inside that band. Select the
  first high event with an eligible non-overlapping control, breaking ties
  between equally close controls by earlier entry. A hold occupies the
  half-open interval from entry to exit. Report empty bands, high events with
  no eligible partner, and unselected events under the one-pair cap.
  Event eligibility uses prices and volume known at each respective decision.
  Later matching is retrospective, so a later control may change an earlier
  event's pair without changing either policy's earlier decision. The other
  entry's triggering move may occur during a hold, and the two groups can
  differ in other characteristics. Keep the 2 bps paired gate on that
  conditional comparison. The complete positive-move policy contrast is a
  descriptive view with no new advancement threshold.
- **Ridge.** Compare both fitted forecasts and zero over the same eligible
  signal rows. Require the original relative MAE threshold in each fold for
  each control. A zero control MAE makes the relative reduction undefined.
  The shared training-only movement screen can record an unavailable
  forecast comparison. Use the same strict 27 bps score threshold for both
  fitted long-or-flat policies and the momentum reference. Keep flat as an
  always-flat reference. There are 4,289 eligible rows per fold, 8,578 in all.
  Divide the full unit-notional candidate minus one-feature net P&L by 8,578
  and convert to bps. The original 2 bps screen therefore requires 17,156
  bps of total incremental return across trades, even though each policy
  can fill at most 286 non-overlapping trades. Preserve this gate and report
  its demanding scale explicitly. Per-trade returns use their own denominator.

**Reuse and verification boundary.** Use `load_spot_day` and a campaign-specific
allowlist with the historical archive digests. Reuse `market.features`,
`market.targets` and `market.build_folds`, `evaluation.model`,
`evaluation.prediction_metrics`, `evaluation.simulate`, the supervised worker,
fit reservations and the existing journal and source snapshot. The existing
evaluator's reference set omits a fitted one-feature control within a
comparison, and the price-drop count matcher implements a different rule.
The new entry needs the small candidate-specific orchestration and exact
admission checks. AQRS-A02-F2/F5 have documented closure. Verify the new
entry's effective limits and one shared preparation/timing/worker deadline.
Check the expected digest allowlist and authorization before opening input,
then compare observed archive digests during qualification. Source and report
persistence remain outside the worker watchdog. The
[exposure index](../evidence/exposure.json) registers both prospective
diagnostic plans. Persist each evaluated view with the predictor role where
applicable, prospective variant ID, exact dataset scope, published revision
and source identity. Verify evidence consolidation retains the association
and the views from each attempt, including replays. A screened comparison
can complete an engineering attempt while the actual Ridge comparison and
the two-family real-data milestone criterion remain open.

**Governor accounting.** Retain the original five estimator fits (four
forecast fits and one timing fit). Reserve up to two additional calibration
charges for the two fold-specific volume cutoffs under the existing Governor
rule for calibration. The prospective upper bound is seven fit charges
across two sequential trials. This fits the default ceiling of 12.
The training movement check is a diagnostic that can stop the forecast path.
It does not set a prediction or trading parameter. Count calibration and
estimator outcomes separately. The named campaign plan and effective preflight
must carry all seven charges. This checkpoint authorizes no campaign.

**Design Learning Card, 2026-11-11.** `SUPPORTED / PERSEVERE` for the
descriptive plan. Market-effect inference remains `INCONCLUSIVE / DEFER`.
Native Windows Python 3.12: the inline `python -B -` design check detected the
missing diagnostic plan on the original revision (exit 1) and passed on the
revised files (exit 0). It checked all ten expected archive/checksum metadata
pairs, fold bounds, original gates, 30 planned Ridge diagnostic views,
Governor arithmetic, synthetic null and 7.5 bps planted policy contrast per
opportunity, unchanged historical exposure and changelog coverage. Focused
`python -B -m pytest -q` on research logic, market timing and evaluation passed
48 tests (49 deselected), including both V1/V2 known-answer fixtures. A
separate read-only reviewer verified the revised design, including the
cutoff-calibration accounting, digest-check order and diagnostic bindings.
Both language checks, manual English review and `git diff --check` passed.
About nine minutes elapsed from 20:30:45 UTC through the recorded review.
Zero market or protected payload reads, fits, campaigns, resamples or spend.
The next bounded proof is the synthetic campaign entry through both complete
comparison paths, including pre-loader rejection tests and attempt receipts.
Linux execution, independent full-path review, consolidation of actual
attempts, publication and named real-data admission remain open.

### M2-E14 market data claim review

**2026-11-11.** The M2-E03 and M2-E12 count receipts contain archive digests
for all ten planned BTCUSDT dates. The shared fold builder and prospective
exposure records agree on six validation dates, December 29–31 and
January 1–3, with 4,289 eligible signal rows per fold after the purge.
Prior use and the concentrated year-end period limit transfer. AQRS-D01
qualifies December 1–24 for BTCUSDT and ETHUSDT outside this definition.
The receipts establish recorded scope and provenance. Actual archive bytes,
candidate coverage, fills and outcomes still require campaign qualification
and measurement.

- **Volume filter.** The window can describe how high-volume and below-cutoff
  positive moves differed in the matched sample and how the two policies
  differed over all eligible positive moves. The 12-pair coverage floor uses
  at least two-thirds of the 18 possible day/band slots. Actual coverage and
  independence are unknown. As a sensitivity calculation, even treating all
  102 slots across the combined 34 recorded BTCUSDT days as independent
  validation pairs, before reserving any training dates or losing any matches,
  gives a detectable mean of 4.92 bps under the same illustrative 20 bps SD
  and one-sided 5% / 80% assumptions. A 2 bps mean would require 619 units
  under those assumptions. The larger calendar alone therefore gives no
  precision basis for that claim.
- **Ridge.** The window can describe whether the extra features lowered
  forecast error against both references in each fold, changed actions and
  improved simulated net return at the assumed costs. The 2 bps threshold
  across 8,578 opportunities amounts to 17,156 bps of summed unit-notional
  net improvement. For scale, if the one-feature control stays flat, the
  candidate would need about 60 bps net per trade at the 286-fill maximum
  and about 1,430 bps with 12 fills. With an active control the difference
  also includes its gains or losses. Adjacent 30-minute targets share future
  returns, so the row count gives no independent precision estimate.

**Decision.** `SUPPORTED / PERSEVERE` for the fixed-window descriptive
design. A screen pass can justify proposing a separate study, and a miss can
defer it. `INCONCLUSIVE / DEFER` for an independent market effect, stability
across periods or instruments, or profitability under real fills. The 25 bps
cost and next-open fills are modeling assumptions. The lowest-cost next
proof for M2 is the guarded synthetic entry with the known null, planted
effect and admission rejection cases. Keep the existing candidate and cost
definitions. Named market access and execution still require the existing
independent review, published binding, authorization and preflight.

**Verification.** About 3 minutes 4 seconds elapsed through the review
checkpoint, excluding orientation and final documentation checks. A read-only
inline Python check on Windows verified both historical digest lists, the
qualified scope, fold indices, purged label boundaries, prospective exposure
records and capacity calculations. This review used zero archive payload reads,
market outcomes, trials, fits, resamples or protected access. Documentation
only. No new fault tree or Linux runtime verification was required.

## AQRS-SC01 Test Card: Sierra Chart and ACSIL round trip, 2026-11-10

- **Decision and baseline.** Determine whether the installed Sierra Chart x64 runtime and its ACSIL headers can provide both sides of a research-only round trip. The current AQRS baseline handles completed OHLCV bars and deterministic signals. Sierra Chart interoperability has no execution evidence. The owner selected both directions under [FR-003](requirements/REQUIREMENTS.md#functional-requirements). Compare a single versioned synthetic fixture through the real host with the Python reference. Use the local ACSIL headers and the [official ACSIL build](https://www.sierrachart.com/index.php?page=doc%2FHowToBuildAnAdvancedCustomStudyFromSourceCode.html) and [ACSIL function documentation](https://www.sierrachart.com/index.php?page=doc%2FACSIL_Members_Functions.html).
- **Minimum proof.** Load one synthetic series of at most 120 fixed one-minute bars in an isolated Windows Sierra Chart replay. Export only bars confirmed complete by the ACSIL Study. Normalize explicit UTC opening and availability timestamps and compare bar keys and values with the fixture before evaluating a fixed, explainable momentum signal using the existing AQRS feature path. Return a versioned signal file containing chart identity and bar key. Display only matching signals whose availability is at or before the current replay position in a read-only ACSIL Study. Require exact bar and decision identity and record the numeric tolerance for chart price precision before execution. Replay the fixture in steps and repeat a full recalculation. Verify that the active bar, a future-bar change, a shifted timestamp and a duplicate or wrong chart key cannot introduce or move an earlier signal. Replay the same interchange fixture through the headless AQRS side on Linux. Record the actual Sierra Chart build, ACSIL header revision, source digests, input/output evidence, and chart comparison. See [FTA-AQRS-SC01](RISK_REGISTER.md#fta-aqrs-sc01-sierra-chart-interchange).
- **Resource Governor and stop.** Propose up to four hours once, including one bounded Windows replay and one headless Linux fixture check, with a 10-minute limit per check and up to 10 MiB of evidence. Zero research campaigns, estimator fits, new market data, protected reads, order routes, spend or recurring compute commitment. Expect only one small local exchange of files per synthetic run. Later per-chart resource use remains unmeasured. The existing research budgets stay fixed. Establish a supported local build and isolated replay workspace before coding. Stop on missing prerequisites, unsupported time semantics or parity failure. Review the evidence before adopting the implementation.

**Planning and prerequisite check, 2026-11-10.** The owner approved M2-E14 planning and selected both AQRS-SC01 directions. The installed Sierra Chart executable and local ACSIL header were found on Windows, with `SC_DLL_VERSION` 2911. Visual Studio Build Tools provided the x64 MSVC compiler. The `vcvars64.bat` and `cl /nologo /Zs /EHsc /TP` header check reached compilation and exited 2 with `C1083` for `windows.h`. The standard Windows SDK directory search found no matching SDK header or import library. No ACSIL DLL was built and no chart replay was launched. About six minutes of planning and prerequisite work through the SDK check. Zero market-data payload reads, fits, campaigns, protected reads or new Linux runs.

## M2-E16 Test Card: historical source binding, 2026-11-10

- **Assumption and decision.** A run-linked source digest and recoverable source bytes may still exist for both M2-E09 executions. The baseline is the AQRS-A02 finding that the matched outcomes and the available reference script do not establish source identity. A wheel, script, or snapshot that cannot be tied to the recorded run supports the alternative explanation that it is only a later or unbound copy. This is the smallest test that could remove the acceptance gap without a new replay. IDEA-001 rules out a search by repeated execution.
- **Minimum proof and stop.** Inspect the two reports, two read-only journals, comparison receipt, Ubuntu setup log, and saved M2-E08/E09 source or package references. Pass only if each original run ID binds the pilot and AQRS worker source to exact digests and matching recoverable bytes. Require exact digest equality. Otherwise retain the source gap and record which links are missing. Preserve the original outcome parity and scientific disposition. Record the commands, available lineage, and elapsed review time. Stop after the named records and their immediate source references. Do not infer historical use from a current file or run another campaign.
- **Resources and risk.** Up to 20 minutes of one-time review. Zero estimator fits, trials, market-data payload reads, downloads, protected reads, spend or recurring work. No change to critical contracts or prior evidence. Fault Tree Analysis is not triggered. M2-E14 remains on its own authorization path.

## M2-E16 Learning Card: historical source binding, 2026-11-10

- **Result.** `REFUTED / DEFER` for recovering both exact source bindings from the named bundle. The reports and [comparison receipt](../artifacts/m2-e09/comparison.json) match the two original run IDs and configuration and data identities. Both read-only journals passed SQLite integrity checks. Their experiment keys reproduce from configuration, data identity and candidate name. The [Ubuntu setup log](../artifacts/m2-e09/ubuntu.log) records an AQRS wheel digest and the completed run ID, but the wheel bytes and a digest for the executed pilot are absent from the inspected bundle. The Windows record supplies neither a run-bound pilot digest nor a recoverable worker snapshot. The M2-E08 reference pilot is available without an execution-time digest. Keep the original outcome parity and research deferral. The separate source criterion remains open.
- **Verification and resources.** `python -B -` checked report and journal lineage, recomputed the keys, and checked the saved package and pilot references (exit 0). About two minutes elapsed from the start of the review through the receipt and planning checks. Zero new Linux runs, fits, downloads, archive payload reads or protected reads. The next campaign remains M2-E14 under its existing start conditions.

### Preserved campaign implementation and acceptance history

These stable headings link to the complete immutable records integrated from
`96df879` during AQRS-ER01. This avoids duplicating nine historical cards.
The current queue governs authorization and dispatch; historical start
conditions do not reopen completed campaigns.

### M2-E19 Test Card: volatility regime filter

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e19-test-card-volatility-regime-filter).
Historical registration only; it does not authorize a new execution.

### M2-E19 Learning Card: paired volatility gates

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e19-learning-card-paired-volatility-gates).
The historical result remains INCONCLUSIVE / DEFER; HMM stays conditional.

### M2-E14 guarded campaign entry Test Card

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e14-guarded-campaign-entry-test-card).
Historical registration only; it does not authorize a new execution.

### M2-E14 Windows campaign Learning Card

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e14-windows-campaign-learning-card).
The historical development screen remains deferred; its observation and precision limits are unchanged.

### M2-E17 Test Card: training window feasibility

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e17-test-card-training-window-feasibility).
Historical registration only; it does not authorize a new execution.

### M2-E17 Learning Card: training window feasibility

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e17-learning-card-training-window-feasibility).
The training-window feasibility result supports E18 preparation, not predictive value.

### M2-E18 campaign proposal

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e18-campaign-proposal).
Historical registration only; it does not authorize a new execution.

### M2-E18 guarded campaign entry Test Card

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e18-guarded-campaign-entry-test-card).
Historical registration only; it does not authorize a new execution.

### M2-E18 Windows and Ubuntu Learning Card

[Complete historical record](https://github.com/RealMonoid/AQRS/blob/96df879626d7c2ffe3c0f4374550a667cfeeb9e3/docs/MILESTONE_STATUS.md#m2-e18-windows-and-ubuntu-learning-card).
The two-family workflow passed; both candidates remain deferred and M2 remains in progress.

## Template for milestone acceptance record

```text
Milestone:
Status:
Commit/release:
Date (UTC):
Verified DoD criteria:
Commands actually run and exit codes:
Platform evidence (native Windows run and independent Linux run: OS/build/distro, architecture, Python, privileges, worker/memory modes):
Compute Governor evidence (preflight, fits, limits, timeout, RAM mode, stop reasons):
Run IDs / artifacts / dataset fingerprints:
Open critical bugs:
Deviations / ADRs:
Acceptance by:
Backward Development requirement → proof → minimum change:
Forward Execution commands and observed evidence:
FTA risk ID and critical negative tests (or why not applicable):
Postmortem incident ID and verified prevention (or NOT_TRIGGERED):
Rejected/deferred IDEA-### lookup and new decision (if any):
Build–Measure–Learn assumption, result and evidence:
Next smallest vertical increment:
```

**Important:** A research run's execution status is distinct from a software release gate. A well-tested negative-alpha campaign may meet a software gate.

## M2-E15 library check

**Test Card, 2026-11-10.** Check whether the owner-selected `python-statemachine` v3.2.2 ([GitHub source](https://github.com/fgmacedo/python-statemachine/tree/d5282e0c89e04411de2326b8e89f8c0ad33aae2f), MIT) can express a finite setup lifetime and price invalidation before an entry trigger. Use a synthetic waiting state as the baseline scenario, with a trigger as its normal exit. In the guarded version, start at bar 100, treat age 3 as expired and invalidate on a completed bar's low at or below the setup's fixed price level. Pass if a trigger at age 2 confirms once, the first expired bar and a trigger at age 50 cannot confirm, a simultaneous price touch and trigger aborts, and a new setup can confirm after the old one is cleared. These are fixture values. The selected entry rule will govern any later market test.

**Resource Governor assessment.** One isolated Windows Python 3.12 source-import check, with at most 15 minutes of work, a 15-second runtime limit, and up to 20 MiB for the pinned source and local evidence. Zero research trials, fits, market-data reads or fees. The check adds no campaign work. Stop after the focused check or on failure. Routine risk review for an isolated synthetic fixture. FTA not triggered.

**Learning Card, 2026-11-10.** `SUPPORTED / PERSEVERE` for synthetic feasibility. The shallow GitHub checkout resolved to the pinned commit and occupied about 4 MiB. On native Windows with Python 3.12.12, `.venv/Scripts/python.exe -I -S -B artifacts/m2-e15/setup_probe.py` exited 0 within the 15-second watchdog limit. All five cases passed, including expiry and price invalidation on the trigger bar, the stale trigger at age 50, single confirmation, and a fresh setup after invalidation. The ignored local `artifacts/m2-e15/setup_probe.log` records the exact command, probe digest and test output. Elapsed work through the focused check was about two minutes and 31 seconds. Zero trials, fits or market-data reads. Keep the library as a candidate for a concrete entry rule after the M2-E14 review. Integration and Linux verification remain separate.

## Model/tool registry (not yet implemented)

Planning sources: [`MODEL_TOOL_CATALOG.md`](MODEL_TOOL_CATALOG.md) and [`../configs/model_tool_registry.json`](../configs/model_tool_registry.json). Registry `CORE`/`EVALUATE`/`CONDITIONAL`/`DEFERRED` labels are **planning decisions**, not release-pass results. M2 includes the LightGBM and Isolation Forest pilots and [five additional assessment cards](MODEL_TOOL_CATALOG.md#m2-assessment-cards-2026-11-10). The `model_registry_audit` occurs at M8. Status: `NOT_STARTED`.
