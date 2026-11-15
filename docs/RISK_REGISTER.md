# AQRS — Project risks and mitigations

## FTA-FR-005: study admission

**2026-11-15, Engineering owns implementation; independent review verifies it.**
Top event: an unclear, unsuitable, unqualified or unauthorized study accesses
outcomes or computes despite FR-005. Credible OR paths: only the CLI checks;
parent-side import/registration/replay bypasses workers; a caller invents PASS;
an approved plan changes before execution; an old request is replayed; required
data/authorization/containment disappears; audit storage fails but execution
continues. A scientific false approval is a separate path: an accepted review
AND an unqualified reviewer can enforce the wrong decision perfectly.

Reuse existing scope checks, journal transactions, source fingerprints and
worker containment. Enforce admission before parent study I/O and Popen, bind
the actual request/source/configuration, verify the worker launch record and
recheck required conditions. Block unqualified entry paths rather than invent
approval. Only a narrowly qualified public engineering contract is eligible
for automatic positive cases; no caller flag qualifies market science.
Independent scientific qualification remains a prerequisite for that scope.

Negative tests cover missing/unclear questions, incompatible design, unsupported
claim, missing prerequisites, forged/stale/replayed records, changed requests,
direct/legacy entry, storage failure and revoked conditions. Observe zero
blocked study reads/workers/fits; a real valid execution prevents an always-deny
implementation from passing. Verify native Windows and headless Linux. Existing
historical artifacts and pure calculation unit tests are not admission evidence.
This is an application-interface control, not isolation against arbitrary Python
or an operator who rewrites executable code or the trusted local journal.

Independent review found two concrete missed paths in the first implementation:
the direct Spot acquisition callback and unused grants surviving abrupt issuer
death. Guard the callback and bind grants to live PID plus process creation time,
worker ancestry and finite campaign validity. Test an actual orphan-grant worker.
The running admission check uses a separate thread with a one-second freshness
limit; delayed metadata I/O must not delay the external wall watchdog. Reuse
the original process-tree/parent-loss tests and verify no next dependent trial.

## Second synthetic next-bar rule

**AQRS-W01-P05, 2026-11-15.** The top event is an invalid comparison that appears
to show an advantage. It can arise from a cutoff fitted on validation or
holdout rows, a volume and return aligned to the same bar, or different scores
or uncertainty for the two rules. Retain the common purged folds and worker
prefix. Check exact training medians and the one-bar shift, mutate reserved rows,
and verify known positive, negative and short cases against both constants.
Keep real sources blocked before opening data and report synthetic evidence
under the existing conservative status. Engineering owns these guards.

## Structured selection boundary

**AQRS-W01-P00, 2026-11-14:** format-only risk screen; no runtime guard or
selector is changed. Prospective top event: unauthorized or misleading work is
selected. Paths: proposal override of the central map OR false/stale qualification
receipt OR fabricated admission/cost record; execution additionally requires
a missing independent launch guard. Before implementation, verify strict fields,
reference/version binding, both qualification checks, admission before ranking
and recheck before dispatch. Cases 02/03/04 specify rejection, qualification and
STOP; their expected outputs are not executed safeguards.

Independent-evidence failure: developer access to hidden cases OR adaptive
retuning on their results. Freeze code/scoring first, keep encrypted cases and
keys outside agent access, store only the owner's checksum, and test while
Codex is inactive. Check release records before an independence claim.

Known weakness `BINARY_RELEVANCE_COST_BIAS`: cheap questions may repeatedly
displace expensive important questions with equal relevance/blocking status.
Case 05 records this limitation. Do not call a schema pass quality evidence or
silently add weights. Revisit after an external comparison demonstrates harm
and a bounded alternative can be tested.

**P00A prospective extension, 2026-11-14:** repeated inconclusive work can arise
from omitted history OR a new-ID reset; avoid with terminal state reconstruction
and evidence-backed reopen events. Missing failure/selector charges OR double
charging reservations corrupts the budget; compare authoritative operation
receipts and exact accounting at the next implementation gate. Qualification
transfer can arise from wrong tested scope OR stale revision; require both in
each receipt and exact scoped-record matching. Orphan qualification plans can
create unrequested work; only permit registered tasks linked to current proposals.
Benchmark failure paths include leaked oracle answers, using the internal
relevance score as truth, or omitting costs from one policy. Use the same frozen
scenario/admission/budget, isolated histories and external C/F/E scoring. Verify
unseen IDs and malformed file handling in P04 before any runtime claim. No such
runtime checks have been implemented in this documentation slice.

## Lessons retained from archived cards

One-time owner cleanup, 2026-11-14. These nine lines retain untested implications
of the archived observations, not new rules, audit work or authorized tests.
Existing timing, cost arithmetic, causal, coverage, source-binding, exposure,
watchdog and journal regressions remain the safeguards for their tested cases.
The suggested checks below were not implemented in this cleanup; E22's separate
synthetic sizing regression does not close its empirical confirmation question.

| Source | Transferable lesson and useful future check |
|---|---|
| [M2-E16](MILESTONE_ARCHIVE.md#m2-e16-learning-card-historical-source-binding-2026-11-10) | A later reproducible source cannot authenticate missing original executed bytes; a useful evidence-review case would distinguish original run linkage, later replay and unresolved provenance. |
| [E20-P01/P02](MILESTONE_ARCHIVE.md#m2-e20-p02-learning-card-effective-count-design), [P06](MILESTONE_ARCHIVE.md#m2-e20-p06-learning-card-local-expansion-deferred) | Effective information depends on the exact contrast, weighting, gaps and dependence; a future known-dependence case should challenge unequal groups and empty calendar days rather than equating dates or trades with independent units. |
| [E14 design](MILESTONE_ARCHIVE.md#m2-e14-pre-outcome-design-checkpoint), [A10](MILESTONE_ARCHIVE.md#aqrs-a10-learning-card-m2-evidence-and-threshold-decisions) | An opportunity-level hurdle can require an implausible total gain at low action frequency; a future threshold-design example should relate the chosen effect to action frequency and matched costs, beyond the already-tested denominator arithmetic. |
| [E22](MILESTONE_ARCHIVE.md#m2-e22-learning-card-prediction-before-costs) | Reserving 61 days does not establish power; future confirmation design needs claim-specific small-effect, dependence and joint-gate power/error evidence, not the new fixed synthetic examples alone. |
| [M1-E05](MILESTONE_ARCHIVE.md#m1-e05-learning-card-real-data-execution-check-2026-11-08), [E22](MILESTONE_ARCHIVE.md#m2-e22-learning-card-prediction-before-costs) | Correct fixed-cost arithmetic does not validate historical spread, latency or fills; future execution qualification should compare known delayed/partial-fill cases under the same opportunities and cost components. |
| [M1-INC-01](MILESTONE_ARCHIVE.md#m1-e10-learning-card-cached-windows-wheels-and-replay-2026-11-09) | A startup timeout does not identify slow fitting; a future bounded cold/warm check should separate imports, handshake and fit while retaining the existing deadline. |
| [M1-E08/E09](MILESTONE_ARCHIVE.md#m1-e09-learning-card-windows-wheelhouse-and-replay-2026-11-09), [M1-E04](MILESTONE_ARCHIVE.md#m1-e04-learning-card-first-real-data-campaign-2026-11-08) | One cache's missing package is not proof of absence from all caches, and a staged environment may lack the required CPU baseline; useful setup checks would cover platform-specific wheel inventory, top-level metadata and import compatibility before a campaign. |
| [M1-E06](MILESTONE_ARCHIVE.md#m1-e06-learning-card-complete-real-data-campaign-2026-11-09) | A zero stage timer can mean below clock resolution, not zero work; a future timing/report fixture should preserve that distinction. |
| [A03/A11/A12](MILESTONE_ARCHIVE.md#aqrs-a12-learning-card--autonomous-work-management), [A16-P01](MILESTONE_ARCHIVE.md#aqrs-a16-p01-learning-card-p06-observation) | Passing document walkthroughs does not demonstrate future agent behavior or time savings; actual adherence can only be checked on ordinary authorized work at existing observation triggers, without inventing another audit. |

## M2-E22 predictive study and holdout

**2026-11-14, before implementation.** Critical research-path change, bounded
by the [E22 Test Card](MILESTONE_ARCHIVE.md#m2-e22-test-card-predictive-first-spot-reversal).
Top event: false predictive claim OR protected-data access. Paths: wrong
bar alignment OR OOS-fitted baseline OR row-level independence assumption OR
outcome-driven sample choice; protected access requires an eligible request
AND an ineffective date guard. Safeguards: fixed monthly allowlist and
owner-only holdout intervals checked before network/file reads, train-only
baseline, explicit close/open alignment, daily HAC with fixed sensitivity,
source-bound prospective publication and complete attempts. Negative tests
cover holdout months/days before I/O, malformed cadence/checksums, future
perturbation and changed OOS labels not changing fitted baseline. Known-answer
and null fixtures check inference and skip cost computation after a miss.
Budget/journal top event: an unbounded or unrecorded run; prevent with existing
supervised workers, explicit fit reservation, two-worker preflight and durable
terminal statuses. Check actual containment, failure and duplicate attempts.
HAC assumptions and outside-tool isolation remain limitations, not proven
guards. No new process audit or Governor limit change is introduced.

**Status:** Qualitative risk hypotheses, not claimed empirically measured probabilities. Reassess priorities after milestones and when new evidence arrives. The previously discussed “99% failure rate” is **not** an established AQRS metric. R-01 through R-06 are the six original research/compute risks; R-07 adds cross-platform portability.

| ID | Category | Failure mode | Early warning | Mitigation / stop criterion | Acceptance gate |
|---|---|---|---|---|---|
| R-01 | Research economics | No after-cost economically exploitable alpha exists in the investigated data. | Predictors fail matched/zero/momentum controls; net edge is below realistic costs. | Stop tuning; revisit market/data hypothesis. “No alpha” is a legitimate software output. | M1–M5 |
| R-02 | Scientific validity | Research Manager prioritizes lucky correlations and generates false alpha. | Excellent in-sample results, weak OOS performance, many variants, low effective count of independent events. | Count trials, matched controls, train-only fits, chronological folds, multiple-testing control and isolated holdout. | M0, M2, M4 |
| R-03 | Data and execution | Data, timestamps or cost model do not resemble actual executability. | Unexplained volume spikes, missing bars, optimistic next-bar fills, changing spreads/slippage. | Source and quality audit, market/venue contract, time-aware costs and execution stress; `INSUFFICIENT_EVIDENCE` on unreliable inputs. | M0, M1, M5 |
| R-04 | Compute explosion | Cartesian model/parameter/fold/seed searches run for months or years. | Exploding fit count, large preflight estimates, unbounded grids. | Resource Governor with fit/trial/wall/RAM/campaign limits and bounded pilot; reject in preflight. | **M0**, M3 |
| R-05 | Validation explosion | Nested CV, bootstrap, permutation, cost and regime variants multiply uncontrollably. | Validation consumes more than authorized campaign budget; final holdout queried repeatedly. | Cheap staged screens first, explicit statistical-validation budget, report insufficient evidence rather than running indefinitely. | M3, M4 |
| R-06 | Recalibration loop | Retuning, restart and retesting recur after every miss. | Growing retrain chains, repeated trial IDs, no terminal state. | Terminal statuses, `auto_retry_count=0` at M0, no unapproved budget increases/restarts, controlled pause. | **M0**, M3, M6 |
| R-07 | Platform portability | Core implementation works on the developer's Windows PC but fails on a Linux VM (or vice versa); resource guards become no-ops. | OS-only imports, shell-specific paths, runtime WSL/Docker requirement, worker grandchildren survive cancellation, missing RAM guard. | Native Windows and independent Linux CI/run gates, portable paths, platform adapter with capability preflight, honest fail-closed status; provider-neutral deployment audit at M7. | M0, M7, M8–M9 |

## Keep business and technical outcomes separate

A failed/no-alpha research hypothesis is **not** a software failure if its test was implemented and executed correctly. Conversely, clean code and a completed backtest are **not** scientific validation. A resource-aborted trial cannot be used as evidence for or against alpha.

## Research management, not rigid bans

Repeated failures may lower a research family's priority, but a changing market, improved data or cost structure can justify reconsideration. No universal prohibition such as “never research sub-15-minute signals when average spread exceeds 0.05%” is authorized; feasibility depends on the *net conditional edge* and specific execution assumptions.

## Procedure for a new risk

### FTA-AQRS-A16: literature learning and frozen evidence

**Screen, 2026-11-14:** the documentation explicitly maps literature learning
to existing scientific exposure and protection contracts; no runtime change.
Top event: an external paper is used to promote an unsupported AQRS claim.
OR paths: source assumptions do not transfer; counterevidence is omitted;
external findings are counted as AQRS observations. AND path: literature is
read after outcomes AND the original gate or protected test is rewritten.
Safeguards: decision-specific source/transfer notes, targeted countersearch,
unchanged original tests, prospective origin/parent-linked variants, and the
existing holdout-independence rules. Negative walkthroughs: supporting paper
without AQRS evidence, post-result model/gate change, reusing seen protected
results, unreviewed preprint, contradictory sources, and a three-observation
shortage that must not launch automatic research. Verify all owner cases A–H
and obtain independent review under the A16 Test/Learning Card. This check
establishes documented routing, not runtime enforcement or future adherence.

### FTA-AQRS-A15: exposure reconstruction and value-stream lineage

**Screen, 2026-11-14:** critical provenance/accounting change; runtime science
and journal schemas are unchanged. Top event: the consolidated index hides
exposure or presents reused evidence as independent. OR paths: only local
artifacts are indexed; nested metrics are skipped; duplicated archive rows
inflate counts; a descriptive replay is recast as a new discovery; a planned
status survives a completed attempt. AND path: a source is missing or changed
AND a partial projection is written as complete.

Safeguards: digest-bound archived journals, complete inventory comparison,
unchanged original identities and statuses, explicit replay non-independence,
flat/nested format agreement, preserved legacy/manual/unknown records, and
validation before replacing the index. Negative tests remove an attempt,
duplicate an identity, alter a diagnostic list, leave an executed registration
planned, corrupt a source, and present conflicting formats. An independent
review checks the real archive projection and the named lineage chains.
The source receipts and prior index remain recoverable; no historical
registration time or source identity may be invented. The Learning Card in
`MILESTONE_STATUS.md` records outcomes and remaining limits.

**AQRS-ER01 integration extension, 2026-11-14.** The older discovery branch
and the newer exposure projection must coexist without reopening completed
registrations or losing candidate/source-binding validation. The top event
is a silently weakened admission or misattributed archived attempt. OR paths:
resetting completed index records to planned; adapting tests by weakening the
runtime guard; or discarding the older candidate/scope/binding check during
the merge. Use the digest-bound historical registration as a test fixture,
retain current completed statuses byte-for-byte, reject changed candidate or
diagnostic identities, and verify the entire archive projection unchanged.
An independent reviewer checks these resolutions before `main` integration.

### FTA-AQRS-B01: blind synthetic search

Top event: a blind-test result is invalid or falsely attributed. OR paths are
answer leakage (unexpected file OR link escape OR external notes), hindsight
registration (outcomes read AND no verified remote preregistration), noncausal
features or labels, a simpler parent masquerading as incremental discovery,
an uncounted search, or a resource stop mislabeled as no effect. A second top
event is unauthorized work: payload delivery AND absent start/budget checking,
or repeated entry AND no exclusive attempt reservation.

Safeguards: exact flat input allowlist and reparse rejection before reads;
source/dataset/plan binding; remote commit verification before worker release;
immutable preregistration plus separate results; train-only calibration and
next-open fills; same opportunity grid/costs, complement and both-parent
contrasts; finite candidate ledger including untested rows; explicit authorized
trial-count override only for this test; existing worker handshake/watchdog,
fit reservation, sampled-RSS policy and exclusive attempt directory. No code
path searches for a solution. Operator discipline is not an OS sandbox against
an agent with general filesystem access. Publication and final report I/O are
bounded control-plane operations, not a strict kernel wall-clock guarantee.

Negative checks follow the AQRS-B01 Test Card, including bad publication/source
bindings, future mutation, redundant conjunction, null, missing approval and
duplicate/timeout failures. Independent verification must inspect the actual
entry, not just isolated helpers. Any accidental solution exposure requires an
immediate owner report and suspended blind interpretation. No market-evidence
status or M2 acceptance follows from this synthetic engineering test.


**Minute order-flow amendment, 2026-11-11.** An invalid decision can result
from future-minute values entering features OR a missing field being treated as
zero OR candidate slots diverging from the recorded header. An over-budget
preparation can result from extra quantiles without corresponding fit reserves.
Bind staged activity and availability to the authorized CSV and registered array
digest. Derive features from the completed row and trailing history. Select
slots from header presence and reserve each available feature's fit. Test
future-row mutations, partial headers, known memberships, actual fit receipts,
and stage-to-registration consistency. Use an independent review before closure.

**Evidence amendment, 2026-11-11.** Incorrect evidence can follow an export
grouping that differs from the actual comparison OR a partial worker write
being promoted as complete OR a digest detached from the exact input bytes.
Bind the selected CSV and original input manifest digests, export group IDs
and match flags from the measured strata, write files atomically, and include
candidate evidence only after a completed receipt. Verify counts against
result strata, reject low disk space and mutated pre-run evidence, and retain
an incomplete status and untested IDs on a stop. The publication check remains
before outcome work. Use independent review of these boundaries.

**Sequential delivery amendment, 2026-11-11.** The next payload could be opened
early because an ID is skipped OR an unpushed or changed verdict is accepted OR
two processes acquire the same slot OR preparation probes a later file. Bind
the current published append-only sequence, one token-owned start, delivery
manifest and exclusive run directory before reading the current CSV. Inspect
only the current CSV. A false evaluable verdict could follow a missing or changed
artifact OR closure while work is active. Require a terminal receipt, verify the
required evidence digests and publish an immutable verdict plus gap log. Verify
rejections and handoff with a local remote and independent review. A hard stop
without terminal evidence blocks automatic advancement.

Assign an ID, owner, observable trigger, budget/stop rule, proposed test and affected milestone; add it to this registry and the relevant release gate. Record evidence rather than inventing precision. Apply the [material finding rule](DEVELOPMENT_PROCESS.md#experiment-queue) when a pending action depends on the affected guarantee. If the risk requires a changed norm, add an ADR to `DECISIONS.md`.

### FTA-AQRS-D01: Spot data expansion

**Top events:** (1) a broader importer exposes protected or wrong-time data; (2) an incomplete or misidentified series is published as qualified; (3) acquisition exceeds its declared scope or budget. OR paths include a mutable URL/redirect, path traversal, wrong epoch units, duplicate/missing/foreign minutes, mixing symbols, stale checksums, invalid activity values, an archive bomb, an unbounded socket read or a partial run labeled complete. Safeguards: freeze explicit symbol/date entries before I/O; keep the January 6 reservation and original M1 wrapper/config restrictions; derive one canonical HTTPS URL per entry, deny redirects, validate bytes/member size/digest/cadence and all retained fields; join separately by symbol; execute acquisition and preparation under the existing supervised handshake and common deadline; publish completion only after every entry passes. Negative fixtures cover each affected boundary, including reserved-date rejection before any open, blocked worker termination, resource preflight and no overwrite. External review is required before adoption. Technical file access isolation beyond the supported entry remains under the separate protected-evaluation gate. No financial outcomes are assessed.

### FTA-AQRS-A08: descriptive diagnostics and admission

**Top event:** a diagnostic creates unsupported research confidence or an uncounted look at exposed data. Paths: constant predictions OR incorrect tie handling produce a false coefficient; pooled association AND hidden fold reversals imply stability; more metrics or instruments AND unchanged exposure accounting inflate evidence; a synthetic self-test OR a prospective freeze is mistaken for complete scientific admission. Reuse the prediction arrays and existing reports; do not feed diagnostics into fitting, screening, decisions or status promotion. Test known ties/signs/zero association, undefined inputs, unchanged arrays/fit counts, flat trading and fold reversals. Test the actual V1/V2 selection plus simulator against no-forward-effect and planted-effect fixtures. Require the precision/design review and recorded additional diagnostic exposure before M2-E14. Engineering owns this additive reporting slice; the future campaign retains scientific uncertainty and the protected-evaluation gate. No critical fill, data-access or compute-enforcement contract is relaxed.

**AQRS-A08 verification.** The bounded reporting and exposure safeguards passed
138 local tests, an independent read-only review and four Windows/Linux CI jobs
on the same source tree. Null and planted fixtures reject the known V1 bias and
preserve V2's expected response; duplicate model attempts retain their diagnostic
views. See the [Learning Card](MILESTONE_ARCHIVE.md#aqrs-a08-learning-card-descriptive-signal-diagnostics).
This closes the scoped engineering actions, not the future campaign's precision,
independent full-design review, runtime admission or protected-evaluation gates.

### FTA-AQRS-A07: research-logic audit correction

**Top event:** a mechanically favored or uninformative comparison advances a research claim. Paths: a control hold includes the event-defining price fall OR only mutually selected observations enter a filter comparison OR a movement-scale screen is treated as prediction evidence OR a minimum trade count is treated as a precision guarantee. Existing causal features, fills and conservative evidence statuses do not prevent these selection and interpretation errors. Engineering owns correction under AQRS-A07; Quant Research owns the future campaign design.

- **Q1, confirmed:** the historical nearest-control rule admits holds ending at the event. Freeze `PRICE_DROP_V1` as historical count evidence and block any outcome study using it. A new registered count rule must end each earlier control hold strictly before the event lookback and keep unmatched coverage visible. Test the planted 50-bps decline without a rebound, rejection at equality including a close/open price gap, future perturbation and missing eligible controls. This guard does not establish causal identification or authorize a new coverage run.
- **Q3, design gate:** M2-E14 has coverage floors but no demonstrated precision for its intended claim. Preserve its thresholds; before an outcome run, distinguish descriptive engineering evidence from an effect claim, fix the eligible population and assumptions about independent units/dispersion, and show what result could change the decision within budget. An analytic normal approximation is conditional planning, not an error-controlled confirmation test. Unknown assumptions keep research admission unresolved.
- **Q4, confirmed limitation:** M2-E10's main comparison conditions on both arms alerting; six simultaneous pairs omit the control-only hour. Add an explicitly separate common-opportunity net diagnostic including skips, test all action combinations and reconcile with the existing simulator. Preserve the legacy rule and historical verdict; any future decision based on the new diagnostic needs a new registered variant.

Residual risks are the narrow holiday/weekend sample, observational confounding, uncertain independent sample size, sparse trades, illustrative costs and a weak raw one-bar momentum reference. Do not infer a structural inability to trade, change costs to manufacture activity, or require interactions from the synthetic XOR result. Stop dependent outcome work until its applicable design gate is met; synthetic implementation and platform checks remain permitted.

**Implementation verification, 2026-11-11.** AQRS-A07's strict control-window and
complete-opportunity guards passed independent review and four Windows/Linux
CI jobs at `a7c11bf`; see the [Learning Card](MILESTONE_ARCHIVE.md#aqrs-a07-learning-card-research-comparison-and-precision-boundaries).
The reviewer found and verified correction of the initial equality boundary
using an actual close/open price jump. Q1's V1 outcome restriction remains;
Q3's scientific design admission remains open. Verified software and new
diagnostics do not resolve those remaining research prerequisites.

### FTA-M2-E14: pre-outcome implementation plan

The top event is an invalid comparison or unauthorized outcome run. The
[design checkpoint](MILESTONE_ARCHIVE.md#m2-e14-pre-outcome-design-checkpoint)
fixes the descriptive scope. The future entry must exercise these paths:

| Failure path | Safeguard and required proof |
|---|---|
| Unpublished or changed definition OR incomplete authorization/diagnostics OR altered input allowlist permits an archive read | Bind the exact published definition, source and named authorization. Reject each missing or changed record, wrong date or symbol, and January 6 before the loader is called. Reject a historical digest mismatch before ZIP decoding, including when both the ZIP and its sidecar have changed. |
| Late features, labels across fold or band boundaries, or cutoff fitted on validation creates apparent value | Reuse causal features and purged folds. Test earlier policy decisions under future-only perturbation, training-only scaling and cutoff, touching/overlapping pair holds, band-end equality and exact next-open fills. Retrospective pair membership can change with a later control. |
| Unequal costs or dropping skipped rows inflates incremental value | Reuse the simulator with matched policies. Test hand-computed one-sided and both-skipped action cases, a shared-gross-outcome null with equal trade counts and costs, a planted contrast, and the historical V1/V2 null and planted fixtures. Reconcile trade, day, fold and opportunity totals. |
| Extra fit, expired deadline, or exposure persistence failure makes the result unauditable | Verify two trials and up to seven fit charges including timing and both cutoff calibrations, one deadline and supported memory mode before work. Verify a screened/no-estimator-fit path and reject a tight or unsupported configuration. Retain both candidate records, including screened or failed outcomes. Bind every evaluated view to the attempt, dataset and source. |

Independent full-path review remains a campaign admission condition. The
matched event comparison is observational. Non-overlap controls the holding
windows, with serial dependence and trigger contamination still possible.

### FTA-M2-E18: scope-bound reuse

Apply [FTA-M2-E14](#fta-m2-e14-pre-outcome-implementation-plan) to the
registered December 1–10 BTCUSDT scope. The additional top event is an
apparently valid result attributed to the wrong campaign or training set.
Credible paths are an earlier definition, receipt or variant identifier
being reused across scopes, or a correct calendar with different archive
bytes or a different first training prefix. Bind the new variants, exact
D01 archive and checksum digests, and the M2-E17 training dataset ID to
the published scope. Test rejection of cross-scope input and receipts,
altered digests, a mismatched training fingerprint and missing diagnostics.
Preserve the previous scope's CLI and attempt identities. Independent review
and a frozen-revision platform comparison are required before closing the
[Test Card](MILESTONE_ARCHIVE.md#m2-e18-guarded-campaign-entry-test-card).

### FTA-M2-E19: regime filter

The top event is a false after-cost advantage or access outside the approved
window. Credible paths include future-smoothed state scores or test-fold
calibration, unfair fills or costs, outcome access before qualified coverage,
and a wrong or redirected input path. Reuse E18's exact archive allowlist,
verified dataset identity and simulator. Verify that deleting or changing
future observations leaves earlier scores and decisions unchanged, reject a
planted future-dependent scorer, and exercise the null and planted cost-aware
comparisons. An incomplete count or outcome admission must fail before outcome
access. Run with the existing isolated workers and explicit fit and time caps.
The reused days support descriptive evidence with unresolved dependence and
cost uncertainty. See the [Test Card](MILESTONE_ARCHIVE.md#m2-e19-test-card-volatility-regime-filter).

## Mandatory Fault Tree Analysis (FTA) for critical development changes

Fault trees here are **qualitative engineering guards**, not numeric failure-probability predictions. They are written before implementation when a critical contract changes and rechecked after a material incident. The source of truth for thresholds is [`DEVELOPMENT_PROCESS.md`](DEVELOPMENT_PROCESS.md). Codex keeps FTA findings **in this existing risk register** and links the active Test Card rather than generating separate fault-tree documents.

| Top event | Illustrative credible top-level causal paths (refine against implementation) | Required control / observable negative test | Linked risks |
|---|---|---|---|
| **FTA-M0-A: falsely admitted alpha due to future knowledge** | Future-derived feature **OR** overlap-contaminated training label **OR** future-fit transform **OR** final-holdout feedback used to select a candidate. | Future-bar perturbation must not alter earlier features; purged folds, train-only transforms and holdout access-control tests must fail closed on planted leakage. | R-02, R-03 |
| **FTA-M0-B: over-budget campaign launched or allowed to continue** | Missing/inaccurate preflight **OR** worker timeout not actually enforced **OR** memory guard unavailable but bypassed **OR** a retry loop independently launches more work. | Extreme 75,000-fit plan rejected before fitting; worker killed on timeout; unsupported required RAM protection blocks launch; no automatic budget escalation or retries. | R-04, R-05, R-06 |
| **FTA-M1-A: imported data reach AQRS with wrong time boundaries or missing bars** | Wrong epoch units or inclusive close treated as the availability boundary **OR** a missing, duplicate, reordered, or foreign-day row is accepted **OR** a changed archive is used under the original provenance. | Validate the exact UTC day and cadence, map the verified inclusive source close to the next minute, and verify the published archive digest before reading. Check the first and last boundaries, deterministic output, and reject a removed minute, shifted close, or bad checksum before output publication. | R-03 |
| **FTA-M1-B: a real-data campaign leaks its holdout or reports fictitious execution value** | A foreign-day file is accepted as research input **OR** a target or fill crosses a fold or holdout boundary **OR** a synthetic policy permits shorting in spot **OR** a missing or double-charged fee, spread or slippage distorts PnL. | Select only the declared research day's archive by name and validate every timestamp. Reject validly checksummed foreign-day content before preflight fitting. Reuse the strict fold cutoff and check the last eligible exit. Require long or flat and verify exact fill indices, cost components and identical policy assumptions for the controls. The original M1 acceptance recorded the reservation as metadata. The audit follow-up below adds the fixed date guard. | R-02, R-03 |
| **FTA-M4-A: protected evidence reaches adaptive research before authorization or is reused as independent evidence** | A protected scope exists **AND** the research identity can reach it directly, through alternate storage or credentials, or by modifying deployed policy. Other paths are candidate access to future outcomes **AND** an observable output channel, or an exposed result influencing selection **AND** an overlapping scope being admitted as untouched. Another path is protected execution proceeding without a fixed confirmation plan or beyond its limits. | Use synthetic secrets to test real identity and storage denials, policy immutability, future-input denial, egress and result release, atomic slot consumption, and rejection of exposed descendants. Check that incomplete plans, out-of-plan requests, and exhausted slot budgets are rejected before protected data access. Require a successful authorized replay as the positive control. Refine against deployment and pass [SEC01–SEC24](ADAPTIVE_QUANT_RESEARCH_PROPOSAL.md#security-acceptance-sec01sec24) before protected data use. | R-02, R-05 |

**Audit follow-up for FTA-M1-B.** The audited CLI routed a reserved date to the importer when the configured day changed. The top event is a reserved BTCUSDT day opened as development input. It requires a path to reserved input (changed research date OR direct importer invocation) AND an accessible archive. Bind the M1 campaign to its authorized date and derive the reservation independently of the user-supplied date. Reject the reserved day or its archive and checksum names at the importer before file access. Negative tests change the configured day and invoke the importer with a reserved date or archive name, using missing files to establish that the check precedes I/O. The approved development-day fixture is the positive control. This guard covers the supported local paths. The separate protected-evaluation gate still governs storage permissions, alternate acquisition paths, and result release.

For the one-off M2-E03 acquisition, a protected-day request could follow an out-of-scope URL **OR** a redirect from an allowed URL. Enforce the exact HTTPS file allowlist before opening a connection and refuse redirects. Exercise both denials with synthetic requests before any network call. Apply FTA-M1-A to the returned archive before counting.

For M2-E08, an invalid comparison can follow a foreign-day archive **OR** a fold reaching beyond its boundary **OR** unequal model inputs or costs **OR** an unsupervised or over-budget fit. Use a literal four-date allowlist and recorded digests, validate each day and the concatenated cadence, derive both folds with the existing purge, pass one shared evaluation request, and use the existing worker handshake and limits. Check forbidden dates and out-of-window folds without opening protected data. Verify both fit counts and matched evaluation rows before interpreting any result.

For M2-E10, a misleading comparison can follow a validation row influencing fit or either cutoff **OR** an alert whose exit crosses its UTC hour **OR** counting unmatched or simultaneous alerts incorrectly **OR** treating an anomaly score as a signed trading forecast. Reuse FTA-M1-B and the four-archive guard above. Spy on fit and calibration inputs, reject a planted exit boundary, and perturb future bars before rescoring the earlier prefix with the same estimator. Check matched, unmatched, simultaneous and empty hours. Feed only the registered alert flags to the common long-or-flat cost diagnostic. Require the worker guards, fixed budget and independent verification before interpreting paired results. The [M2-E10 evidence](MILESTONE_ARCHIVE.md#m2-e10-learning-card-isolation-forest-pilot-2026-11-09) records the prevention checks and both guarded receipts.

Actual logical AND dependencies and minimal single-point paths should be derived when the relevant implementation exists, not confidently invented in advance. If a control failure is found, the linked milestone remains blocked until the protective regression test passes. Postmortems for significant incidents follow the existing milestone record / issue workflow, with prevention steps and recheck criteria.

### FTA-AQRS-SC01: Sierra Chart interchange

The top event is a signal displayed against an earlier or wrong bar. It can follow an active or future bar being exported **OR** an incorrect UTC conversion, chart identity or bar key **OR** stale or duplicate output being accepted after replay or full recalculation. Reuse FTA-M0-A and FTA-M1-A. Require a completed-bar check at export, separate open and availability timestamps, strict key checks at both ends and deterministic recomputation. In [AQRS-SC01](MILESTONE_ARCHIVE.md#aqrs-sc01-test-card-sierra-chart-and-acsil-round-trip-2026-11-10), change an active and a later bar, plant a shifted timestamp and a duplicate or wrong chart key, and compare stepped replay with full recalculation. Require the earlier signal prefix to remain identical or the invalid exchange to be rejected. Review source and runtime evidence before adoption. The first fixture covers fixed one-minute UTC bars only. Cross-timeframe joins and session or daylight-saving transitions require separate evidence if introduced.

### FTA-M2-E21: Scout pilot

The top event is a false capability pass. It can follow the Scout having a
route to later data or benchmark truth **AND** that material being reachable;
an evaluator accepting a changed rule **OR** timing beyond the available
prefix; or the null case being dropped **OR** a partial result being promoted.
Bind the allowed inputs, benchmark commitment, and exact candidate before
evaluation. Accept data-only candidate definitions through the bounded
evaluator. Through the chosen entry, reject a substituted or later input,
a changed rule, and a planted lookahead. Verify that null, abstention and
interruption stay visible and that the complete planted fixture can pass.

Reuse FTA-M0-B to prevent unbounded invocations and charge each attempted
call and trial under its declared limit. Test an over-limit request and an
interruption before blind execution. The [M2-E21 card](MILESTONE_ARCHIVE.md#m2-e21-scout-pilot-feature-preflight)
owns readiness. Qualify the actual isolation and supervision path before
dispatch. B01's open findings still govern its own admission flow.

### FTA-M2-E15: state persistence count

The top event is an invalid feasibility decision or an out-of-scope read.
An invalid count can follow (inherited training state OR future-price use OR
trigger before cooling/invalidation OR acceptance beyond a fold boundary)
AND credit toward the band gate, or duplicate events being counted as distinct
bands. An out-of-scope read can follow an expanded date or instrument, a
substituted archive, or execution without the required worker guard. Bind the
ten names and D01 digests before parsing. Require the existing containment,
sampled RSS watchdog and bounded deadline before archive access. Test exact
age and time boundaries, future-prefix invariance, duplicate band credit,
substituted input, unsupported memory mode and a single guarded synthetic
worker. A passing count admits neither forward returns nor a claim of
independence. Engineering and the independent reviewer check the entry before
the registered run. Decision: proceed within the bounded count scope.

### FTA-M2-E20-P03: supervised replay evidence

The top event is acceptance of an unbound or unequal replay. It can follow
both platform reports agreeing on the same wrong source **OR** a valid-looking
report and an inconsistent journal **OR** a partial comparison or changed
decision passing the parity check. Verify snapshot bytes against the exact
selected Git objects and their report digests, require terminal journal rows
bound to those results, and compare complete model outputs with exact decision
identity and the frozen numeric tolerance. Exercise these failures with
synthetic receipts. Platform identity and the actual run scope still require
the independent acceptance review under the [replay decision](OPEN_QUESTIONS.md#m2-supervised-pilot-replay).

## Open execution-path quality debt

Engineering owns closure. The affected entry is a prerequisite under the [queue rules](DEVELOPMENT_PROCESS.md#experiment-queue) whenever a planned task uses or carries forward that entry's admission flow. Use the minimum authorized verification needed for closure and record the independent check before campaign reuse. Shared helpers remain eligible when the selected entry does not inherit the affected admission flow.

- **AQRS-A10-F1 · OPEN · B01 threshold application and reporting.** At `044363c`, the contrast passed with 60 matched observations per arm although only 16 per arm entered the interval. A positive completed trial followed by a timeout also produced a local dataset report with `complete=false` and `effect_claimed=true`. The published verdict correctly withheld the dataset claim. Before external B01 execution, independently verify three cases through the affected entry: discarded days cannot supply the coverage minimum for an interval, a positive trial followed by a stop preserves candidate evidence and withholds the dataset claim, and a mismatch between registered and executed horizon, stride, warmup, block length or trial count is rejected or impossible by construction. Use synthetic fixtures under a separately scoped correction. The existing capability, delivery, budget and start gates also apply. See the [A10 review](MILESTONE_ARCHIVE.md#aqrs-a10-learning-card-m2-evidence-and-threshold-decisions).
- **AQRS-A02-F2 · CLOSED 2026-11-11 · Supervised replay admission.** The former fixed-limit path now loads the effective validated Governor policy. The real entry rejects tighter fit limits, unsupported strict memory mode and malformed configuration before archive access or fitting; a compatible configuration completes the real synthetic comparison with unchanged research costs. A separate read-only reviewer and all four Windows/Linux CI jobs verified the correction at `70005cc`. See the [AQRS-A06 Learning Card](MILESTONE_ARCHIVE.md#aqrs-a06-learning-card-audit-controls-and-recoverable-evidence). This does not make historical source linkage complete or make pilot parent I/O externally supervised.
- **AQRS-A02-F5 · CLOSED 2026-11-11 · Core CLI campaign deadline.** Expired admission now rejects before staging even with timing disabled. Core preparation, timing and candidate workers share the original campaign deadline; the blocked-preparation regression and existing watchdog tests pass on Windows and Linux. The independent reviewer verified the corrected boundary at `70005cc`; see the [AQRS-A06 Learning Card](MILESTONE_ARCHIVE.md#aqrs-a06-learning-card-audit-controls-and-recoverable-evidence). Source/report persistence, journal finalization and cleanup remain outside the external worker watchdog. This is a bounded compute guarantee, not a hard end-to-end I/O deadline. Future entries must preserve or explicitly qualify this boundary before reuse.

### M0 implementation controls

- **FTA-M0-A.** A false admission can follow an offline leak (future input OR an out-of-window label OR a transform fitted outside training) AND reuse of the contaminated result as evidence. A separate path is a holdout value entering model selection or evaluation. Build features from trailing bars only, physically cut off the holdout before labeling, enforce strict exit-before-boundary inequalities, and pass only training slices to fitting. Perturb future bars, check exact open indices, test a holdout mutation against research rows, and inspect fitted training statistics. Keep synthetic evidence inconclusive.
- **FTA-M0-B.** Over-budget work can start if preflight miscounts fits OR permits unsupported containment. A running trial can escape limits if the watchdog fails OR descendants outlive termination OR a required memory mode is bypassed. Repeated launches also require a failed attempt AND an unguarded retry or duplicate reservation. Reject extreme fit counts and unsupported memory modes, gate worker entry until supervision attaches, test blocking and memory-pressure workers with descendants, and check the persistent attempt ledger for retry/identity behavior.
- **M0 cost and persistence risks.** An early fill, missing cost component or unequal control policy can fabricate economic value. Test fixed trades with increased costs, matching controls and exact fill indices. A crash between reservation and result can erase a failure or duplicate evidence if the scheduler relaunches it. Reserve in SQLite before worker entry, update terminal status transactionally, preserve nonterminal interrupted records and use a stable evidence key. Exercise rejection, timeout and repeat campaigns.

### FTA-AQRS-A06: audit remediation

Top events: over-budget or unapproved work begins; an invalid status is treated as evidence; an accepted result cannot be reconstructed. Credible paths: stale remaining-time admission OR configuration bypass OR blocking data preparation outside supervision; ordinary parent exception AND nonterminal journal; a successful pilot screen AND an undefined evidence value; local-only evidence OR lost source-to-run linkage OR a retrospective rule mislabeled as preregistered. Reuse the native worker handshake, shared deadline, strict config validation, SQLite transactions and archived source digests. Negative tests must exercise the real pilot admission against strict/tighter limits before archive reads, expired core preflight with timing disabled, blocking preparation, unexpected exceptions, screen-only and positive-screen status paths, corrupted/missing evidence and duplicate exposure records. Positive controls must retain approved costs, causal inputs and valid execution on native Windows and Linux. Preserve historical reports and unproven provenance; distinguish manifest verification from independent backup and development exposure from independent confirmation. Engineering owns correction; a separate read-only review verifies the fixed criteria before affected entry reuse. No new market-data or holdout access is authorized by this engineering card.
