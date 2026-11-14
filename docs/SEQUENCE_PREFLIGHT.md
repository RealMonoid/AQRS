# AQRS Sequence Preflight

This is the binding procedure for sequencing material AQRS work under the
[development dispatch rules](DEVELOPMENT_PROCESS.md#experiment-queue).

## When to check

Codex applies this dispatch check to material work, including owner-directed
work outside the queue and work resumed with changed prerequisites. Run it at
**PRE-START**, **QUEUE CHANGE**, **NEW FINDING**, **REQUIREMENT CHANGE**,
**EXPERIMENT COMPLETION**, **BLOCKER RESOLUTION**, and **MILESTONE TRANSITION**
when the event affects the intended work or its dependents. Use the current
Queue, Test/Learning Cards, contracts and finding records. If related work or
decisions span branches or worktrees, reconcile the applicable revisions and
receipts against the intended execution path and confirmed owner scope. A row's
`READY` label or an older checkout cannot establish eligibility by itself.
Use [completion reconciliation](DEVELOPMENT_PROCESS.md#completion-reconciliation)
to record material follow-up from new findings and completed work. Base each
replan on the updated open items, prerequisites, closures, and priorities.

## What to check

- Identify the next decision and authorized milestone objective. Work backward
  from the evidence needed to the smallest useful test and capability. Name
  the downstream work that a pass unlocks and what remains necessary, is
  cancelled, or is deferred after a miss.
  If the capability is only needed after the assumption holds, test the
  assumption first when a cheaper valid test can resolve it.
- Before marking material work `READY`, check the [Test Card's threshold basis](DEVELOPMENT_PROCESS.md#1-write-a-compact-test-card-before-implementation).
  Confirm that the comparison and measurement can distinguish an outcome
  relevant to the next decision. When the threshold itself is unknown, a
  bounded, authorized calibration can proceed under its own evidence and stop
  rule. Work that relies on the eventual acceptance threshold waits for it.
- Trace the hard prerequisites to their contracts, verification, applicable
  material findings, and owner, data and budget gates. A prerequisite is hard
  when its absence would invalidate the work, its evidence, or its authority.
  Rank eligible work using decision value, unlock value, milestone relevance,
  risk, reversibility, effort, waiting time and displaced work. Treat optional
  ordering preferences as non-blocking and check for future-scope work.

### Research evidence sufficiency

Before dispatching a material research experiment, use the existing Test Card
and the [research claim admission rules](RESEARCH_PROTOCOL.md#precision-and-claim-admission).
Start with the research question, the decision and current disposition.
Work backward from the smallest relevant effect or benefit to the matched
comparison, observation unit, plausible dependence and required precision.
State the minimum evidence that could change the decision and derive the
eligible data window and smallest authorized test from it. The same card
states what a positive, negative or inconclusive result changes and when to
stop. For work aimed at an effect claim, complete this check before accessing
market outcomes or starting fits.

- **Check relevant literature.** Apply the
  [decision-linked literature gate](RESEARCH_PROTOCOL.md#decision-linked-literature-checks)
  before a new material hypothesis/design and at a decision-changing method
  or interpretation trigger. Reuse the same Card's source/transfer note;
  a clear shortage of data alone does not trigger more literature work.
- **Check usable information.** Describe label and holding overlap, common
  shocks, clusters, regime coverage and serial dependence as applicable.
  Compare available eligible units and plausible dependence with the
  required precision, for example an interval width around a decision
  threshold. Use a justified effective count or another defensible
  uncertainty method for the contrast. Mark the effective count unknown
  when it cannot be justified. Rows, dates, instruments, non-overlapping
  trades and repeat runs alone cannot establish independent information.
  Use ranges and sensitivity to plausible dispersion and dependence.
  Illustrative power calculations are conditional on their assumptions.
- **Decide what the evidence can support.** Use the existing dispatch
  decisions below. Allow a claim-specific outcome test only when the
  available evidence has a realistic chance of resolving the registered
  decision. If inputs or assumptions are inadequate, block that test and
  consider a separately authorized, bounded coverage or methods calibration
  with a defined output and stop rule on development evidence. A technical
  replay or descriptive screen may proceed with a smaller justified window
  for its own registered decision. Market screens retain all applicable
  admission, publication, exposure and Governor requirements. Match the
  claim to the evidence through the funnel: a mechanism or question, a
  cheap screen, a method and sufficiency check, predictive evidence where
  relevant, economic evidence, robustness and separately authorized protected
  confirmation. Follow the stages needed for the question.
  A credible early miss can end the downstream work.
- **Derive any extension.** First check whether fairer matching, a more
  informative valid contrast, or dependence-aware aggregation can use
  existing information. Preserve causality and comparability. If changing
  the target, population or selection rule, register a prospective variant
  and retain the original result. For an owner data decision, state the
  research question, existing evidence, unresolved gap, required data
  properties, smallest defensible scope, stop rule and holdout boundary.
  Justify the window by the evidence it can supply, such as eligible events,
  regimes or precision. A fixed technical or reproduction objective may
  supply its own window rationale. Combine access requests when justified
  by shared needs, with separate registrations and usage scope for each
  study. Count selection of windows, features, models, regimes, thresholds,
  costs and diagnostic views under the [existing exposure rules](RESEARCH_PROTOCOL.md#10-exposure-and-pre-run-registration).
  Keep protected data and results outside development and calibration.
- **Rank by the limiting uncertainty.** Name the dominant research
  bottleneck in the existing queue or card. Check the journal for prior
  negative results and the observable [revisit conditions](DEVELOPMENT_PROCESS.md#experiment-queue).
  Prioritize the authorized action that can resolve the limitation at
  lowest justified cost. New model work earns priority through a concrete
  mechanism, a fair simple baseline and adequate evidence for the question.
  Require a confirmed requirement, a priority research dependency or an
  observed failure path for new research infrastructure.

## Dispatch decision

Return exactly one decision for the proposed next action.

| Decision | Dispatch consequence |
|---|---|
| `ALLOW` | The action is authorized, its hard prerequisites are evidenced, and the order is justified. Continue under rule 1. |
| `ALLOW_WITH_NOTE` | A non-blocking uncertainty remains. Note it in the existing record and continue under rule 1. |
| `BLOCK_DEPENDENT_WORK` | A hard prerequisite, required guarantee, required valid evidence, authorization, or data/budget gate is missing or a material finding invalidates this path. Keep only affected work waiting under rules 1, 3 and 4. |
| `REPRIORITIZE` | An already authorized, eligible item supplies a necessary prerequisite or has materially higher current decision value. Apply rule 1 to that item and record the affected order or start condition. Preserve owner gates and the single active experiment limit. |

Use the existing queue or card to show why the work matters now. Reference the
decision, the prerequisite evidence and what follows. When work is too early,
link the missing condition and the work item or existing record that will
provide observable proof. Reassess priority when that proof arrives. Keep
deferred work subject to rule 5. Continue necessary, eligible steps inside the
same authorized work item automatically. The
[Resource Governor](RESOURCE_GOVERNOR.md) still controls campaign admission
and execution budgets. A dispatch decision grants no scope, data access or
campaign permission.

## Decision record

Add a short entry below when a preflight changes the planned order, blocks
dependent work, or clears a previously recorded block. Record the UTC date,
work item, decision, evidence link, and resulting order or resumption
condition. Link the entry from the affected queue row or existing work record.
Keep current status and operative start conditions in the
[experiment queue](MILESTONE_STATUS.md#experiment-queue), and keep test results
in their existing evidence records. Routine checks that leave the plan intact
use the existing queue or card.

The [AQRS-A09 walkthrough](MILESTONE_STATUS.md#aqrs-a09-sequence-audit-and-dispatch-check)
provides examples from the original audit.

### 2026-11-12 — M2-E21 Scout pilot

**QUEUE CHANGE — `BLOCK_DEPENDENT_WORK` for dispatch.** Add the owner-approved
[Scout pilot](MILESTONE_STATUS.md#m2-e21-scout-pilot-feature-preflight) after
M2-E20 in priority and ahead of B01 reassessment. M2-E20 addresses the
remaining acceptance evidence recorded in
[AQRS-A10](MILESTONE_STATUS.md#aqrs-a10-learning-card-m2-evidence-and-threshold-decisions).
The E09 source gap governs use of that replay for acceptance. It is independent
of a qualified synthetic Scout path. M2-E21 waits for a committed benchmark
with defensible scoring criteria, a verified isolated handoff, and a bounded
execution path. On a pass, reassess what benchmark B01 should use. A miss
keeps the capability question open. B01 remains subject to its own execution
finding, delivery, budget and start gates.

### 2026-11-12 — M2-E20 evidence readiness

**EXPERIMENT COMPLETION — `BLOCK_DEPENDENT_WORK`.** The
[M2-E20-P01 review](MILESTONE_STATUS.md#m2-e20-p01-learning-card-effective-observation-readiness)
closed the authorized methods preparation. Effective counts wait for a
decision-specific, eligible chronological contrast and defensible dependence
assumptions under the existing admission rules. The independent E09 route
waits for the [owner's replay decision](OPEN_QUESTIONS.md#m2-supervised-pilot-replay)
and the exact execution-path checks. M2-E21 remains next in the existing
priority order with its own readiness and implementation scope. The
remaining rows have no eligible action under the current mandate.

### M2-E20 and M2-E15 dispatch correction

**2026-11-12 UTC, 2026-11-13 local. BLOCKER RESOLUTION — `REPRIORITIZE`.**
The previous dispatch exit was premature for authorized preparation.
Pull [M2-E20-P02](MILESTONE_STATUS.md#m2-e20-p02-test-card-effective-count-design)
to specify the comparison, then pull the independent
[M2-E15-P01](MILESTONE_STATUS.md#m2-e15-p01-test-card-state-persistence-count-design)
design before its separate data and run authorization. Both preparations
closed. No priority change is needed among the six pending parent rows.

**EXPERIMENT COMPLETION — `BLOCK_DEPENDENT_WORK`.** Effective-count outcome
work waits on a decision-relevant eligible ordered comparison or defensible
independent evidence about dependence. The fixed six-day series cannot
resolve that need by another report calculation. The E09 and E15 runs
retain their separate authorizations. Scout requires a committed independent
benchmark and qualified isolation within approved implementation scope.
The other rows retain their owner or predecessor gates. See the
[E15 closeout rescan](MILESTONE_STATUS.md#m2-e15-p01-learning-card-state-persistence-count-design).

### M2-E20-P03 completion and next dispatch

**2026-11-13. EXPERIMENT COMPLETION — `BLOCK_DEPENDENT_WORK`.** The
[source and receipt preparation](MILESTONE_STATUS.md#m2-e20-p03-learning-card-supervised-replay-readiness)
closed. The E09 reproduction remains the first decision in the current
queue that the owner can unblock. It needs the [separate replay authorization](OPEN_QUESTIONS.md#m2-supervised-pilot-replay)
for one Windows run on the four named archives and a conditional Ubuntu
replay. Independent exact-path review and the Governor preflight still apply
before each eligible execution. Effective-count work awaits the eligible
series or dependence evidence identified in P02.

**Rescan.** The independent [Scout preparation](MILESTONE_STATUS.md#scout-preparation-and-remaining-start-conditions)
traced reuse and isolation. The independent commitment and implementation
scope remain missing. B01 remains deferred behind Scout, with AQRS-A10-F1
and the delivery, trial exception and start gates governing external use.
E15 has a fixed count design and synthetic oracle. Its named access and
count require the recorded owner decision, after which the scoped entry and
preflight are necessary. SC01 remains owner-deferred. M4-E01 depends on
authorized M4 planning. No eligible action remains in the current mandate.

### M2-E20-P04 source-bound replay and next dispatch

**2026-11-14. PRE-START — `ALLOW` for the Windows comparison.** The owner
approved the fixed four-day scope. The
[published Test Card](MILESTONE_STATUS.md#m2-e20-p04-test-card-source-bound-e09-replay)
fixed the source, limits and conditional Ubuntu gate. Independent Windows
verification cleared that replay.

**EXPERIMENT COMPLETION — `BLOCK_DEPENDENT_WORK` for further E20 outcomes.**
The [paired receipts](MILESTONE_STATUS.md#m2-e20-p04-learning-card-source-bound-e09-replay)
close the supervised source-reproducibility slice. The
[capacity follow-up](MILESTONE_STATUS.md#m2-e20-capacity-and-forecast-evidence-follow-up)
establishes local calendar capacity. The next outcome slice needs an
eligible ordered comparison and a defensible dependence and precision basis.
Final M2 release verification requires the remaining evidence and the
selected release revision. The other pending entries retain their start
conditions. No additional execution is eligible under this mandate.

### AQRS-ER01 / M2-E20-P05 completion and next dispatch

**2026-11-14. `ALLOW` for the authorized reset and evidence design.**
The owner explicitly requested ordinary Git consolidation, necessary fixes,
verification and decision-specific E20 preparation. The
[reset record](MILESTONE_STATUS.md#aqrs-er01-execution-reset) preserves the
integration evidence. The [P05 design](MILESTONE_STATUS.md#m2-e20-p05-learning-card-decision-specific-evidence-design)
supplies the unit, fixed estimand, precision sensitivity and verified capacity.
It closes the autonomously solvable research-design wait.

**Subsequent owner approval: `ALLOW` for the single P06 diagnostic after entry verification.**
The [P06 packet](OPEN_QUESTIONS.md#m2-e20-p06-report-only-calibration) is one
archived-report planning diagnostic, not a new period or model campaign.
P02 explicitly reserved that additional look. The owner supplied approval
in this reset session. The published freeze and pre-read checks completed.
The original execution order was: publish
its frozen diagnostic/exposure registration, verify the exact calculation
on synthetic inputs and bind A16-P01 before the single authorized read.
Calibration leaves independence unknown and does not close M2. No data
expansion or repeated look follows automatically.

**Completion: P06 executed once and verified.** Its fixed branch is
`DEFER_LOCAL_OUTCOME_EXPANSION`; inferential sufficiency stays unknown.
No further data access or count is eligible on that branch.

**Queue rescan.** E21 is the next proposed research objective and
separately needs owner scope, an independent benchmark/scoring commitment
and verified isolation; B01 depends on a credible new discovery path, but
E21 does not depend on B01 success. A16-P01 observes a host and cannot block
it. SC01 is owner-deferred; M4-E01 awaits its milestone and fixed claim;
H01 awaits its recorded trigger. No cyclic dependency was found. A16-P01
closed its P06 observation and H01 is 2/3. No independent authorized READY
execution remains after the reset's normal closeout.
The governance freeze leaves existing verification and follow-ups active.

### M2-E15 count authorization and dispatch

**2026-11-14. PRE-START — `ALLOW` for count-entry qualification.** The
[owner authorization](OPEN_QUESTIONS.md#m2-e15-state-persistence-count)
unblocks independent E15 work. E20 still needs an eligible ordered comparison
and precision basis. E21 needs the independent benchmark, approved scope and
qualified isolation. B01 still depends on the capability review. Pull E15 as
the first eligible row. The [count card](MILESTONE_STATUS.md#m2-e15-count-entry-and-execution)
gates the single market read on verified source, synthetic checks, an
independent review and Governor admission. A pass only permits consideration
of a separately scoped outcome proposal. A miss ends this work item.

**PRE-START — `ALLOW` for one Windows count.** At 07:10:36 UTC the
independent check matched the reviewed source digest, unused run reservation,
ten fixed archive and sidecar pairs, preflight limits and prospective
[exposure record](../evidence/exposure.json). The actual guarded entry
passed the synthetic input, receipt and duplicate-run checks. The scope
contains none of the January 6 holdout files.

**EXPERIMENT COMPLETION — `BLOCK_DEPENDENT_WORK`.** The independently
verified [count](MILESTONE_STATUS.md#m2-e15-learning-card-state-persistence-count)
closes E15. Rescanning the five pending rows found no eligible next action.
Resume E20 with an eligible ordered comparison, justified dependence and
precision, and scoped approval for any new market access. Final M2 verification
requires the effective-count evidence and a selected release revision.
E21 awaits approved implementation scope and an independent benchmark with
verified isolation. B01 awaits E21's capability evidence and retains its
execution gates. SC01 awaits owner reprioritization. M4-E01 awaits authorized
M4 planning. A new E15 outcome study requires its own decision, evidence plan
and scope. M2 remains `IN_PROGRESS`.
