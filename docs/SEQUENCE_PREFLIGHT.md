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
