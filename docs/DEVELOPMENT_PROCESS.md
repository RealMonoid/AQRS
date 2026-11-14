# AQRS development process: Lean Build–Measure–Learn with backward planning and fault learning

**Status:** Binding for Codex across every milestone. **Backward Development → Forward Execution, risk-triggered Fault Tree Analysis and incident-triggered postmortems are mandatory parts of this workflow.** This governs **AQRS development and founding decisions**. Market alpha has its own research protocol. Never substitute a product-development check for out-of-sample financial evidence. Use the [experiment queue](MILESTONE_STATUS.md#experiment-queue), its start conditions, and recorded owner authorization to determine the current scope. Acceptance follows the applicable [milestone DoD](MILESTONE_DOD.md).

## Objective

Maximize **credible uncertainty reduced per unit of development time and compute**, not number of features, files, commits, tests, backtests or models. Use Eric Ries's Build–Measure–Learn loop with a Walking Skeleton, explicit riskiest-assumption tests and small vertical slices. Select the **evidence and success criterion before coding**, then build the minimum needed to obtain them. A falsified assumption is progress; an unmeasured feature is not.

## Recommended methods: adopt only what is useful

| Practice | Decision | How AQRS uses it |
|---|---|---|
| **Build–Measure–Learn (BML)** | **MANDATORY** | Every meaningful increment starts with an explicit question, produces measurable evidence and ends with a documented decision. |
| **Backward Development / Forward Execution** | **MANDATORY** | Plan backward from an observable milestone gate and failure criterion to the smallest necessary change; implement and verify forward in dependency order. This is AQRS terminology, not a claim of a separate formal industry standard. |
| **Fault Tree Analysis (FTA)** | **MANDATORY for critical changes and serious incidents; lightweight otherwise** | Start with a defined undesirable *top event*, decompose credible causes using AND/OR, and derive controls and targeted negative tests. Record findings in `RISK_REGISTER.md`. No invented failure probabilities. |
| **Postmortem / recurrence prevention** | **MANDATORY after material incidents or repeated failure patterns** | Blameless, evidence-based timeline, failed safeguards, corrective action with verification; update existing records, no per-incident document unless strictly unavoidable. |
| **Rejected-idea memory** | **MANDATORY for consequential rejected approaches** | Save a concise evidence-backed entry in the existing `DECISIONS.md`; preserve why, observed limitations and conditions for reconsideration. |
| **Riskiest-Assumption Test / assumption mapping** | **MANDATORY** | Prefer the highest-impact, least-supported, cheaply testable assumption over convenient features. Risk: research correctness, feasibility, runtime, portability or usability. |
| **Test Card + Learning Card** | **MANDATORY, lightweight** | Record hypothesis, evidence threshold and budget **before** building; record observation, conclusion and next action **after** testing in the existing milestone status/issue, not one new document per test. |
| **Walking Skeleton / thin vertical slices** | **MANDATORY** | Keep one working end-to-end path; extend a real path rather than implementing detached services. |
| **Kanban / Work-in-Progress (WIP) limit** | **MANDATORY** | At most **one active development experiment** for a single Codex worker; queued ideas are not concurrently built. |
| **Innovation accounting** | **ADOPT, simplified** | Track decisions backed by evidence and cycle time/compute, not vanity metrics. |
| **Five Whys / root-cause review** | **CONDITIONAL** | Use briefly for repeated defects or recurring resource waste, not for each ordinary failure. |
| **DORA metrics** | **CONDITIONAL** | Track lead time and rework once there are repeatable releases/operations; deployment frequency is not a meaningful M0 target. |
| **Lean Canvas, business funnels, paid SaaS platforms** | **NOT NEEDED** | AQRS is currently a single-researcher engineering product, not a customer-acquisition venture. |
| **A/B tests, feature flags, complex project-management systems** | **DEFERRED** | Add only when a concrete product/user hypothesis makes them necessary. |

## Feature and venture experiments

- **Discover needs and opportunities.** A problem, wish, unmet need or foreseeable change can start the inquiry. Use a recent case or a plausible future scenario. If the owner cannot identify one, inspect existing workflows, reports and decisions, then offer interpretations and ask focused questions where the answers would change priorities. Clarify what the researcher wants to achieve and why it matters. Separate observed facts, assumptions, preferences, binding constraints and proposed solutions. Agree on the intended outcome and observable evidence before proposing implementation. Check what the existing workflow or a manual step can already provide. Carry the agreed outcome into the existing Test Card for substantive work.
- **Explore architecture concerns.** Describe a concrete condition and the response AQRS would need to show. For example, a new data source should be usable without rewriting the evaluation logic. Explain how the concern affects the workflow, which qualities or constraints are in tension, and what evidence would distinguish viable choices. Consider credible future risks even when the current workflow succeeds. Rank them by consequence, likelihood and cost of acting early. Record agreed architecture decisions in [DECISIONS.md](DECISIONS.md).
- **Feature adoption.** Plan freely within milestone scope. Before integration, use the existing Test Card to state the hypothesis, baseline, success and failure criteria, budget, and stop or rollback rule. A pilot is provisional. After evaluation, record an explicit decision to adopt, revise, remove, or defer in the Learning Card. Adoption requires observed benefit over the baseline, acceptable recurring costs, and applicable quality and release gates.
- **Founding decisions.** Before a material spending or scope commitment, work backward from the decision to the least-supported assumption that could change it. Check value in a real workflow and include recurring operating costs and maintenance effort. Compare against the current manual workflow or simplest viable approach. If considering an external offering, test the problem with prospective users and look for concrete pilot commitment or repeat use before investing in delivery. Use the same timeboxed cards and record actual time, spend, compute, and the resulting decision.
- **Test the process itself.** Use measured time, spend and compute to compare how much effort it takes to reach comparable decisions with traceable evidence. Keep estimates of avoided work separate from observed savings. Keep engineering, venture and alpha conclusions separate. The existing risk-based FTA and scientific gates apply at their respective boundaries.

## Mandatory planning order: backward design, forward execution

**Backward Development (before changing code):** Start with the current authorized milestone's *observable outcome* and independent DoD evidence. Derive, in reverse order: what a passing test must demonstrate → what data/behavior/contract is required → what minimal component change enables the proof → what could invalidate the proof. Identify the riskiest assumption and the smallest falsification test. Never decompose the entire v1.0 roadmap into simultaneous implementation jobs. This is consistent with the verification-first logic of systems engineering's V-model, but executed in lean increments.

**Forward Execution (after the plan):** Check the baseline → implement the smallest dependency-complete vertical change → run the predeclared targeted test → measure actual resource/time and regression impact → capture the result → decide `PERSEVERE`, `PIVOT`, `STOP` or `DEFER`. Repeat only by opening a *new, bounded* learning loop. A planned sequence is not permission for an unbounded run.

**Proof-of-control example (M0):** Outcome: no eight-year calibration starts. Backward: release gate requires `REJECTED_PREFLIGHT` with zero model fits → plan must account for fits/folds/seeds and pessimistic runtime → tiny plan fixture and hard limit are necessary → implement `research plan` gate first. Forward: build bounded estimator and test the 75,000-fit negative case before adding expensive fitting. Also test that the guard cannot silently bypass an unavailable enforcement mechanism.

### Risk grading and Fault Tree Analysis gate

| Change / incident | Required analysis | Record location |
|---|---|---|
| **Critical:** potential lookahead/holdout leakage; false-alpha admission; broken costs/fills; missing compute kill-switch; journal corruption; unintended broker/live order; unsafe or silently nonportable Windows/Linux execution | **Small qualitative FTA BEFORE implementation or release**; revisit after an incident, and create at least one observable prevention/detection test for each material single-point path. | Existing `docs/RISK_REGISTER.md`, linked from current Test Card. |
| **Significant:** new dependency across data/decision/execution boundaries; repeated regressions; unbounded calibration proposals; failing release gates | Document a compact failure-path review. Expand to AND/OR fault tree if multiple causes interact or severity could be critical. | Existing risk and milestone record. |
| **Routine:** formatting, wording, narrowly scoped refactor with no changed high-risk contract | Normal test and regression evidence. **No compulsory FTA or postmortem.** Record "FTA not triggered" if the task was explicitly risk-screened. | Existing Test Card or issue. |

**Compact qualitative FTA template (no new file):**

```text
Risk / top event (observable):
Impact and analysis boundary:
Credible causes: (A OR B), (C AND D), including common-cause failures:
Single points / minimal critical combinations (if evident):
Existing guard / detection gap:
Preventive check + negative regression test:
Residual uncertainty and owner:
Decision: PROCEED | NARROW | BLOCK | ESCALATE
```

Two M0 example *top events* are `A false alpha candidate is admitted because future data leaked` and `An over-budget training campaign starts or keeps running`. Enumerate only credible causes and actionable gates; do **not** create gigantic exhaustive fault trees or invent probabilistic precision. The purpose is to stop a severe failure, not to produce ornamental safety engineering.

### Postmortems: capture lessons without writing an encyclopedia

Trigger a **blameless, concise postmortem** when a critical invariant is violated, a worker actually exceeds an approved runtime/memory limit, a test leak or silent scientific error reaches milestone acceptance, a milestone is blocked by a recurring cause, or the same significant defect has occurred twice. A test failing during ordinary local development is **not automatically an incident**; fix and log it in the active Test/Learning Card. A deliberately rejected eight-year calibration *before it starts* is a successful prevention test, not a fabricated incident.

For a triggered incident, record in `docs/MILESTONE_STATUS.md` (or one existing linked GitHub issue), **not** a separate Markdown file:

```text
Incident ID / date UTC / severity:
Expected vs. observed / user or research impact:
Short evidence-based timeline (commands, commit, outputs):
Technical causal factors and safeguards that failed or were absent:
Correction + prevention action, owner and verification command:
Decision to resume / stop / redesign, and open residual risk:
Link to relevant risk ID, ADR or rejected-idea entry:
```

A postmortem is **not complete until its preventive action is testable**, with follow-up tracked at the next affected milestone gate. Avoid blaming individuals or treating guesses as established causes. If the root cause remains uncertain, mark that uncertainty openly. Use a targeted regression test when possible; *do not* automatically rerun all costly research experiments.

### Failed ideas and duplicate-prevention memory

Differentiate **failed engineering approaches** from **failed financial hypotheses**. Keep substantive design failures, rejected tooling and abandoned approaches as compact `IDEA-###` records in the existing `docs/DECISIONS.md`; financial candidate tests live in the AQRS Research Journal when that software exists. `CHANGELOG.md` records which files changed, not an extra collection of standalone failure narratives.

```text
Idea ID / date UTC / proposed approach:
Claim or assumption / attempted scope:
Evidence actually seen (or "not tested"):
Why rejected, deferred or contradicted:
Cheaper replacement / negative test preventing recurrence:
When to reconsider (specific changed evidence or constraints):
Linked risk, code, milestone and/or experiment ID:
```

**Before trying a previously rejected approach**, Codex must search the decision ledger and relevant research journal for similar hypotheses, read the prior reason, and identify genuinely new evidence or constraints. An old rejection is not an eternal ban: documented market or technical changes can justify a new bounded test. Do not generate hundreds of empty records or write a postmortem for every trivial discarded thought.

## One development loop: the binding contract

### 0. Select the riskiest assumption

Choose the next **smallest decision-changing uncertainty**, not the most exciting algorithm. Prioritize severity of being wrong, lack of evidence, cost of testing and dependency on the current working path. Do not invent a complicated numerical score to justify a subjective priority.

### Experiment queue

Use the [experiment queue](MILESTONE_STATUS.md#experiment-queue) as the canonical work plan for concrete development, founding and project-level research work. Give each planned work item a stable ID and its original addition date in YYYY-MM-DD format. Record the decision or required outcome, minimum check or card link, start conditions, and any parent ID. Project-level market research plans may link to the Research Journal for trial details. Apply [completion reconciliation](#completion-reconciliation) when follow-up affects the plan.

1. **Order and start.** Apply the [Definition of Ready](#work-authorization-and-definition-of-ready) and [Sequence Preflight](#sequence-preflight) to the intended work. Resume the single covered `ACTIVE` item while its conditions hold. Otherwise record the failed condition, move affected work to `WAITING`, and pull the first eligible `READY` row in priority order. Mark it `ACTIVE` before starting. After completion or a blocker, follow [next dispatch](#work-item-definition-of-done-and-next-dispatch) within the recorded authorization. Order rows by expected decision value against effort, waiting time and displaced work.
2. **Update after learning.** Record the result, evidence link, and next decision in the row or its linked Learning Card. Close evaluated tests. Add a follow-up with a new ID, addition date, and parent ID only when it can change a remaining decision within budget. Reorder the queue after each result. For a deferral, apply rule 5. A deferred test that has not run stays `WAITING`. After an evaluated test, keep its result closed and use a separate row for any justified follow-up. Mark obsolete or superseded tests `CANCELLED` with a reason or replacement ID. Keep closed and cancelled entries or links to their records below the pending rows.

3. **Material findings.** A verified violation or missing required evidence is material for dispatch when it invalidates a planned action, use of evidence, or gate. Before the next dependent action, Engineering records the finding ID, the affected guarantee, evidence or execution path, and the observable resumption check in the existing risk record, Test/Learning Card, or issue. For every pending row that depends on it directly or through another prerequisite, link the finding in the start conditions and set it to `WAITING`, including rows that were `READY` or `ACTIVE`. Apply the same check before marking a new row eligible or choosing or changing its execution path.
4. **Resume affected work.** Keep a row in `WAITING` while any linked material finding is open. Close each condition only when the named check passes and its evidence is recorded, with independent verification where required. Set the row to `READY` only when all other start conditions and authorization also hold. Follow rule 1 for dispatch. Independent rows retain their status and eligibility. Keep closed attempts and original evidence intact. Record any change in the eligibility of that evidence or the affected gate in the existing record.

5. **Revisit deferred decisions.** Use `DEFER` when missing decision-relevant evidence can change a named decision and obtaining it now is impractical or outside authorized scope. In the existing decision record or Learning Card, record why, the observable revisit condition, the default until it occurs, and who checks it in which existing workflow. Link any dependent work. A date or milestone can prompt a review. Reopening requires the recorded condition. For pending work in `WAITING`, name the missing approval or prerequisite, the technical obstacle and affected path, or the evidence needed to justify the work. When qualifying new data, reviewing candidate evidence, or checking an acceptance gate, check the relevant linked decisions at their named observation points. On a trigger match, reassess the decision and priority before proposing new work. Meeting a trigger does not authorize execution or change the status of the closed attempt. Apply rules 1–4 to any justified follow-up. Stop an unchanged comparison when the evidence supports that decision within the tested scope. When sufficient evidence leaves a material choice reserved to the owner, present the choice and a recommendation for decision.

6. **Governance freeze, owner decision 2026-11-14 (AQRS-ER01).** Prioritize
   eligible research and its necessary technical enablers. Do not start
   general governance, role, autonomy, value-stream, literature, harness or
   process audits, including new A-series audits, unless actual work reveals
   a concrete material failure mode, existing verification demonstrates a
   rule violation, a persistently defined revisit trigger occurs, or an
   evidence-integrity risk needs immediate protection. Cosmetic cleanup or
   speculative future usefulness is insufficient. Restrict any triggered
   work to that cause. Existing QA, verification, Test Cards, Sequence
   Preflight, literature rules, Resource Governor and recorded follow-ups
   (including AQRS-H01) remain active; routine checks are not permission
   boundaries. This rule adds no governance layer.

### Work authorization and Definition of Ready

Use the [experiment queue](MILESTONE_STATUS.md#experiment-queue) as the
repository entry point for resuming AQRS work across chats. Follow the row
to its governing card or queue record for the current mandate and next
eligible action. The record must be usable without searching past chats.

When the owner grants, changes, or withdraws authorization in chat, update
the governing card or queue record and its queue reference in the same
session, before acting on the decision or handing off. Retain a faithful
English account with the decision date and source, confirmed objective,
covered work, completion boundary, reserved approvals and cumulative effort
estimate. For a chat decision, include the chat or message reference when
available for audit. Update affected scope and start conditions so a later
change takes effect for the next chat.

A multi-item objective covers necessary derived work that fits its confirmed
requirements and limits. Each covered row can link to the same authorization.
An explicitly standalone mandate ends at its stated outcome. Queue membership
and priority alone grant no authority. If the repository records leave a
material authorization gap, apply the
[permission-boundary check](#permission-boundary-before-stopping-or-asking-the-owner).
Continue independent authorized work and identify the exact missing approval
for the affected action. A general search of previous chats is unnecessary.

Mark an item `READY` only when all applicable conditions hold.

1. The proposed outcome is covered by the recorded owner authorization.
2. The next action and required inputs are available, dependencies are satisfied,
   and relevant material findings have their verified closure evidence.
3. The [Test Card](#1-write-a-compact-test-card-before-implementation) fixes the
   decision, baseline, evidence, threshold basis, budget and stop rule.
   A routine correction uses the existing ordinary change-record exception.
4. [Sequence Preflight](SEQUENCE_PREFLIGHT.md) explains why this item comes now.
5. Required owner, data, holdout, resource and release permissions for the action
   are present. The estimate includes analysis, implementation, tests, routine
   corrections, verification, records and reconciliation for the entire item
   or authorized sequence. Apply [standing approval](../AGENTS.md#working-method)
   to time already spent plus all remaining work. At eight hours or more,
   obtain approval for that effort. Splitting cards, rows or chats does not
   reset the estimate. An already approved larger effort follows its recorded limit.

Use `WAITING` for dependent work when a required condition fails. Apply the
[permission-boundary check](#permission-boundary-before-stopping-or-asking-the-owner)
before reporting that status.

### Permission boundary before stopping or asking the owner

Before stopping or requesting owner input, Codex must check the active item
and the entire [canonical queue](MILESTONE_STATUS.md#experiment-queue) against recorded
authorization. Identify the remaining work in two parts:

1. **Authorized work.** Identify and complete all available authorized
   preparation before reporting the work item as `WAITING`. This includes
   analysis, research design, Test/Learning Cards, existing evidence checks and
   other necessary steps with available inputs, permissions and budgets.
2. **Dependent work.** Identify the affected action and the specific reserved
   decision, permission, data access, budget approval or external prerequisite
   it requires. `WAITING` applies only to the work that depends on the missing
   prerequisite. Record the missing requirement and observable resumption
   condition in the existing queue row or card.

Continue preparation in the active item when it can proceed there. If the
queue needs to track a separate eligible slice, link it to the waiting
parent and apply the normal readiness and pull rules. Check the queue
for the first eligible covered action, including preparation under waiting
parents. End autonomous dispatch only when no covered eligible action remains
in the active item or the queue. Request only the owner input that unblocks
the named action, or report the specific external prerequisite.

### Continuous execution and decision boundaries

| Event | Required action |
|---|---|
| Checkpoint, completed substep or progress update | Report meaningful progress and immediately continue the next necessary authorized step. A reply is required only for a named reserved decision. |
| Decision within the approved plan | Apply the predeclared criteria, record the result and continue the authorized consequence. Closing a Test/Learning Card triggers dispatch review. |
| Ordinary implementation or test defect | Diagnose, correct and rerun the affected checks within the work item's budget and stop rule. Research campaign retries retain their separate authorization and counting rules. |
| Material verification finding or blocker | Record the finding and resumption check. Apply queue rules 3–4 to dependent work and evidence. Complete an authorized in-scope correction when feasible. Otherwise select independent eligible work through rule 1. |
| Owner-reserved decision | Apply the [permission-boundary check](#permission-boundary-before-stopping-or-asking-the-owner), persist the choice in the canonical record, and ask only for the missing decision. |
| Work-item completion | Apply the Definition of Done, reconcile follow-up, reevaluate the queue and execute the next eligible item covered by the mandate. |

Owner decisions are required for reserved product choices, requirement or scope
changes, increased budgets, additional data or holdout access, owner-reserved
scientific choices, materially irreversible architecture decisions, expressly
reserved release or milestone gates, and effort beyond standing or explicit
approval. Identify the actual reservation when escalating. When a genuine
blocker leaves no independent authorized work, report what must change to
resume and request only the input or decision needed. Routine implementation
choices use the existing engineering authority.

### Work-item Definition of Done and next dispatch

A work item is `DONE` only when its agreed outcome is evidenced, required
implementation, tests, routine corrections and retests are complete, required
independent verification is recorded, and documentation and evidence are
current. Apply [completion reconciliation](#completion-reconciliation) and
resolve all in-scope obligations before closure. A valid negative experiment
can complete its declared investigation. A feature with unmet acceptance
criteria remains incomplete. Record its blocked or stopped disposition
explicitly.

Retain the existing queue statuses. Record a finished attempt as `CLOSED`
with its result. State explicitly when an attempt closes `BLOCKED`, `DEFER`
or `REJECTED` while the requested capability remains open, and link its
remaining work. Use `CANCELLED` for abandoned unrun work with a reason.
The scientific and execution statuses keep their existing meanings.

After each Learning Card, new finding, blocker resolution or completion,
update the affected state and priority before another dispatch. When the
active item ends or cannot proceed, scan pending rows in priority order.
Start the first item satisfying the Definition of Ready within the recorded
mandate by setting it `ACTIVE`. This pull is mandatory even when it has a
different work-item ID. Skip ineligible rows and continue independent covered
work. Recheck stale `READY` labels against current evidence.

Before ending the session, apply the
[permission-boundary check](#permission-boundary-before-stopping-or-asking-the-owner)
and record the dispatch outcome in the current card or queue record.
Identify the next item actually started or the exact condition that prevents
further authorized work. An explicit owner instruction to pause still
governs. A new chat follows the [handoff rule](../AGENTS.md#working-method)
and carries the same authorization and cumulative estimate.

### Sequence preflight

Follow the binding [Sequence Preflight procedure](SEQUENCE_PREFLIGHT.md).
Its [decision record](SEQUENCE_PREFLIGHT.md#decision-record) holds material
changes to work order and eligibility.

### 1. Write a compact Test Card **before implementation**

Use a GitHub issue if available; otherwise update the **current-loop section of `docs/MILESTONE_STATUS.md`**. Do **not** create a file for each card.

For a routine correction with a known outcome and no change to a critical contract, use the ordinary change record and targeted checks. Use a Test Card when a plausible result could change the approach, scope, safeguard, or acceptance decision. Keep one Test Card across setup attempts that seek the same proof. Record each attempt, its outcome, and its resource use separately under the existing stop and authorization rules. A material change to the question or criteria requires a new bounded loop.

Record the complete Test Card before implementation begins and before collecting or inspecting the first contributing result for the decision. A complete earlier plan in the same record can serve as the card. Include exact decision thresholds and comparison tolerances where applicable, and state what changes if the result passes, fails, or remains inconclusive. For a test based on existing records, identify prior evidence used to plan it. Label later additions and preserve the original criteria and attempts. Treat criteria chosen after seeing an affected result as exploratory for that result.

For each material threshold, record the decision, baseline, measured quantity,
comparison population or workload, and the smallest difference that would
change the decision. Seek applicable academic primary literature first. Cite
the source and explain which assumptions transfer. When the source supports
the method only, derive the value from the applicable requirement, risk,
baseline, or measurements. State the basis for any heuristic. If the value
cannot yet be justified, scope a bounded calibration with an observable output
and stop rule. Label its evidence as calibration and qualify the resulting
threshold on a separately fixed validation case before using it for acceptance.

For a material research hypothesis or scientific design choice, apply the
[decision-linked literature check](RESEARCH_PROTOCOL.md#decision-linked-literature-checks)
in this same Card before freeze. Reuse its source, transfer and decision note;
the research protocol defines proportional depth, mid-research triggers and
engineering exemptions. This extends the threshold rule without requiring a
literature review for routine development.

- **Research benefit.** Relate the smallest worthwhile net effect to costs,
  action frequency and the common opportunity population. Check whether
  sample size, dependence and measurement uncertainty let the test distinguish
  that effect. State how a result close to the threshold affects advancement.
  Use the [research evidence check](SEQUENCE_PREFLIGHT.md#research-evidence-sufficiency)
  in this same card or linked research definition.
- **Technical performance.** For a performance decision, measure the baseline
  and change on representative typical and upper workloads on the relevant
  platforms. Use an appropriate clock and record run-to-run variation. Where
  startup matters, distinguish cold and warm startup, import, worker handshake
  and fit from the external safety deadline. Keep safety limits in force.

```text
Loop ID / milestone:
Assumption (falsifiable):
Expected mechanism and observation that would favor a plausible alternative:
Why this is the riskiest next uncertainty:
Minimum test / vertical slice:
Backward-derived release outcome and proof:
Risk severity / FTA top event (or reason not triggered):
Prior similar rejected ideas checked:
Baseline or existing behavior:
Predetermined pass, fail and inconclusive criteria, with threshold basis and applicability:
Evidence to capture (commands, artifacts, measurements):
Expected decision value versus effort, waiting time, and work displaced:
Development timebox and research compute budget:
Stop/rollback condition:
```

For material or hard-to-reverse development and founding decisions, briefly explain why the proposed action should work and identify an observation that would distinguish it from a plausible alternative. If the evidence cannot distinguish the explanations, record the mechanism as unresolved in the Learning Card.

For a long or costly test, record the best decision with current evidence, what result could change it, and why a cheaper test would leave material uncertainty. Use brief estimates or ranges. Where useful, set checkpoints in advance and continue only when the expected value of the remaining evidence justifies the remaining effort and delay. Keep the agreed evidence criteria and scientific safeguards.

Examples of acceptable questions: *Can Windows and Linux each reject a 75,000-fit plan before training?*; *Do causal feature tests fail if a future bar leaks in?*; *Can an existing CLI command produce a reproducible journal entry?* Avoid *Build an intelligent Research Manager* as a single loop: it has no finite test.

### 2. BUILD: smallest executable change

- Preserve existing contracts and the last working end-to-end path.
- Prefer **one coherent vertical slice**, one active task, minimal modified files and no speculative abstractions.
- Implement a cheaper test/probe/prototype first when it can answer the question without a full feature.
- Keep the default development loop **timeboxed to one focused session (target <= 60 minutes)**; if evidence cannot be obtained within the agreed budget, stop and narrow the question or mark it blocked. For longer experiments, state the budget before starting and apply the [standing approval rule](../AGENTS.md#working-method). The **enforced research runtime limits** are defined in `docs/RESOURCE_GOVERNOR.md`.
- Do not launch new model sweeps, large recalibrations or repeat tests autonomously when the original plan exceeds budget. Escalating budgets/scope requires owner approval.

### 3. MEASURE: evidence versus preregistered criteria

Run the **narrowest relevant automated tests first**; run the broader regression/CLI/Windows/Linux/English checks at the integration and milestone gate. Do not rerun expensive full validation after every trivial edit. Measure relevant observable behavior, for example:

- Correctness: assertions, time-causality invariants, CLI output, regression outcome.
- Reliability: reproducibility, recovery from failure, safe worker termination.
- Performance: wall time and peak memory on declared reference hardware, actual versus preflight estimate.
- Usability: a documented command works for a human operator on a clean native Windows or Linux machine.

A test's passing status proves only the **defined engineering claim**, not that real-market alpha exists. Save commands, exit statuses, relevant artifacts and the measured baseline. Never manufacture results or quietly change the threshold after observing them.

#### Independent verification

Before closing a [critical contract change](#risk-grading-and-fault-tree-analysis-gate) or marking a milestone `ACCEPTED`, assign a separate read-only verification task to a reviewer who did not implement the change. Ask for **verification mode** and provide the exact revision or working-tree snapshot, the predeclared Test Card or applicable [milestone DoD](MILESTONE_DOD.md), and links to the evidence and any applicable FTA.

Where a Test Card governs the decision, identify its predeclared contents by a dated entry, revision, or snapshot. The reviewer checks whether they precede implementation and the first contributing result and match the criteria actually applied. Report late, changed, or unverified criteria separately.

The reviewer derives checks from the criteria and governing contracts. For each applicable criterion, report whether it is met, failed, or lacks evidence, with a reference to the check or the gap. Reuse valid evidence and keep any additional checks within the authorized scope and budget. Return implementation or evidence gaps to Engineering and apply the [material finding rule](#experiment-queue) to dependent work. The change owner records or links the review in the existing Learning Card or acceptance record. The affected gate stays open while required evidence is missing or a criterion fails. Criteria changes and release approvals follow the existing authorization rules.

Before a market-outcome campaign, publish its fixed Test Card and definition as a separate revision under the [research registration rule](RESEARCH_PROTOCOL.md#10-exposure-and-pre-run-registration). This does not imply historical cards were independently timestamped. Engineering fixtures are not market-outcome campaigns.

### 4. LEARN and DECIDE

Record one short Learning Card in the same issue or current-loop section:

```text
Experiment or incident ID, date, and actual elapsed working time through the recorded decision:
One-line outcome and its effect on the decision:
Execution outcome and benefit finding, recorded separately:
Expected versus observed, baseline or criterion, and evidence reference:
Established cause, plausible explanations, open questions, and safeguards if applicable:
Postmortem trigger: YES | NO (if YES, link evidence/action):
Consequential approach rejection recorded in DECISIONS.md: ID | NOT_APPLICABLE
Conclusion: SUPPORTED | REFUTED | INCONCLUSIVE | BLOCKED
Action: PERSEVERE | PIVOT | STOP | DEFER
Which assumption changed or remains unresolved, and which queued tests are now unnecessary?
Material follow-up and affected queue changes, with links to their canonical records:
Next action, any required authorization or prerequisite, estimated effort, and how to verify it:
```

If the full interval is unavailable, state the measurement endpoint. Report concrete avoided work separately from measured savings. Apply [completion reconciliation](#completion-reconciliation) to the consequences of each Learning Card.

#### Diagnosis in existing records

Use the short diagnosis fields above in the existing Learning Card for development work and in the Research Journal attempt record or its linked evidence for research runs. Keep these outcomes distinct:

- **Technical or infrastructure stop.** Record where the run stopped, the environment, the exit status or log, any partial outputs, and whether safeguards worked. State what must be restored or checked before a safe retry. Mark the benefit as unevaluated when the stop prevented its measurement.
- **Functional failure.** Record the violated requirement, a minimal reproduction with expected and observed behavior, and which runs, outputs, or decisions are affected. This applies even when the run reports success. Exclude affected evidence from decisions pending correction and verification. Record the fix and a regression check that fails before the fix and passes after it. If the scope is uncertain, record that uncertainty. Use the existing incident review when its trigger applies.

- **Expected benefit not observed.** For a valid test, record the baseline, result, and missed criterion. Mark the hypothesis refuted only when the evidence rules out the declared benefit within the tested scope.
- **Inconclusive.** Record what evidence is missing and what could resolve it. Use this outcome when a valid result falls short but the evidence cannot rule out the declared benefit.

For any material unresolved outcome, state the open claim, the specific reason
the evidence cannot decide it, the decision that applies now, and the smallest
observable check or trigger that could change it. Use the existing deferral
rules when the evidence is plausibly obtainable and the trigger justifies a
future review. If there is no credible decision-changing follow-up, stop the
current line of work and preserve the uncertainty. Record which work can be
dropped and reconcile the queue before dispatching another comparison.

If a run both stops and violates a requirement, record both diagnoses under the same attempt or link the two records.

- **SUPPORTED:** continue only if current release gates or the next riskiest uncertainty warrant it.
- **REFUTED:** abandon or change the approach; preserve the evidence, do not optimize until it looks successful.
- **INCONCLUSIVE:** define a cheaper or better discriminating test; do not automatically increase trial counts.
- **BLOCKED:** report the blocker, the affected work and the condition for resuming. Continue independent authorized work. Ask for an owner decision only when one is required.
- A `PIVOT` that changes scope, science contracts, budget ceilings, security, or platform compatibility needs explicit approval and an ADR in `docs/DECISIONS.md`.

### 5. Close the loop, not just the ticket

Close any triggered FTA or postmortem action with a reproducible prevention test before accepting the affected gate. Update the **existing** `docs/MILESTONE_STATUS.md` current-loop record and the sole root `CHANGELOG.md` for substantive repository changes (date, purpose and **every changed path**). Keep the current system usable; run applicable policy checks; state what was actually verified and what is still unknown. No per-loop Markdown reports, separate progress trackers or multiple changelogs. Git commits/issues provide detailed historical traceability; the milestone status captures the current loop and acceptance evidence.

#### Completion reconciliation

Chat output is communication. The repository holds project state. As soon as
a material unresolved follow-up is identified, record it in its canonical
location. Before reporting any material work item complete or handing off
unfinished work, reconcile the original scope and newly discovered follow-up.

1. Check what was completed against its evidence. Review Learning Cards,
   verification and audit findings, and decisions made during the work.
   Identify work that became necessary, changed priority, lost a prerequisite,
   became obsolete, or needs a decision or revisit. Complete and verify a
   necessary small fix within the current authorization as part of the same
   work item.
2. Keep a follow-up as open work only when it serves a confirmed requirement
   or acceptance gate, reduces a concrete relevant risk, enables a prioritized
   decision, follows necessarily from a Test/Learning result, fixes a confirmed
   defect, has been confirmed as work by the owner, or has a concrete revisit
   trigger. Assign each point one primary category and canonical record. Use
   an existing ID or a stable entry ID or section anchor. Link related records
   where they affect readiness, eligibility, or a gate.

| Category | Canonical record and required detail |
|---|---|
| Ready / planned work | [Experiment queue](MILESTONE_STATUS.md#experiment-queue). Give separate work a stable ID, addition date, scope, evidence or minimum check, and any parent ID. Use `READY` when the dispatch rules permit it. |
| Waiting | Queue row in `WAITING`. State the missing prerequisite and the observable condition for resuming. |
| Blocked | Record the obstacle and affected work in the governing card, risk record, or linked issue. Link the resumption check in each dependent row's start conditions and keep those rows `WAITING` under rules 3–4. Use `BLOCKED` for the affected work outcome where applicable. |
| Deferred | Existing decision record or Learning Card under rule 5. Record current status, reason, concrete revisit trigger, default until then, and who checks it and when. Link from the queue when it affects planned work. Keep a planned but deferred row in `WAITING`. |
| Owner decision required | [Project Open Questions](OPEN_QUESTIONS.md) or [Open Requirements Questions](requirements/OPEN_QUESTIONS.md). Reuse the existing record if present. State the choice, what it affects, and the current default. Record it before asking the owner and link any dependent work. On resolution, link the confirmed decision in the appropriate decision register. |
| Quality or risk finding | Existing [Risk Register](RISK_REGISTER.md), verification record, or linked card or issue under rules 3–4. Record evidence and the observable closure check. Update the affected gate, evidence eligibility, and dependent start conditions as applicable. |
| Rejected | Close obsolete or rejected work in its existing record, with reason or replacement. Record consequential rejected engineering approaches in [DECISIONS.md](DECISIONS.md) with revisit criteria. Record tested financial candidates in the Research Journal or its linked evidence. |
| Information only | Keep incidental ideas out of the queue. Label any such suggestion in the report as an optional idea outside the work plan. |

3. Update the affected canonical records. Close completed entries and cancel
   or close obsolete ones with their reason or replacement. Recheck that
   every remaining material point raised during the work, in a report, or in
   chat has a live reference. Use the updated records in [Sequence Preflight](SEQUENCE_PREFLIGHT.md)
   to reassess priority and eligibility when follow-up changes the plan.
4. Derive the next recommendation from the current work plan after applying
   dispatch rules. Cite the ID, status and canonical location for each
   material next step in the report. If nothing is eligible within the
   mandate, identify the recorded prerequisite. Continue the next eligible
   action within existing authorization. Recording a point, changing its
   priority, or satisfying a revisit trigger grants no new authorization.

## Measurement: minimal innovation accounting

Start with **four modest metrics**, measured per completed loop or milestone, not as hard quotas:

1. **Evidence rate:** number of *resolved* critical assumptions (supported or refuted) per completed loop or time spent. `INCONCLUSIVE` and `BLOCKED` are recorded, not counted as resolved.
2. **Time to evidence:** elapsed working time from the Test Card through the recorded decision. Use the Learning Card's measurement endpoint and compare budget with actual duration when meaningful.
3. **Regression/rework:** failures in previously passing critical gates, and time spent correcting them.
4. **Reproducibility and native Windows/Linux acceptance:** fraction of required commands/tests actually passing in the declared environment, with their observed runtimes.

Also note **recurrences of previously documented causes** (no artificial quotas): a repeat incident is a process failure signal, even if the current test run passes.

Qualitative owner feedback also matters: *Can one researcher run and interpret the result?* Never count lines of code, number of model families, backtest profit, green checkboxes without real execution, or document count as development success.

## Cheap evidence before expensive evidence

Use a progressive verification ladder:

1. **Static review / tiny fixture:** one command, a few assertions, no training.
2. **Focused integration:** one real vertical path, bounded synthetic data and targeted tests.
3. **Milestone integration:** the complete offline CLI, native Windows/Linux CI, invariant suite, journal and resource checks.
4. **Scientific candidate validation:** only after its own separately specified data/economic/scientific gates; **never** as an automatic development-loop step.

Each step must stop when it already answers the question. A pass on (1) does not substitute for (3) when an actual release gate requires (3).

## How Codex should start M0/v0.1

Suggested early learning order, subject to actual constraints:

1. Prove a minimal native Windows install/CLI can produce a deterministic dataset and an inspectable artifact.
2. Prove timestamps/features/labels cannot leak future observations.
3. Prove cost parity and at least one simple predictive/trading baseline.
4. Prove a bounded candidate can be selected, fitted, evaluated and journaled through the full path.
5. Prove Resource Governor preflight can reject an extreme plan **before** full computation, then separately prove enforced timeout/memory behavior before accepting M0.
6. Prove the completed M0 end-to-end CLI and DoD on native Windows and in an independent headless Linux environment.

This sequence is **not permission** to defer a mandatory M0 acceptance test or run unguarded expensive training. The Resource Governor must supervise relevant workloads whenever they are executed.

## Tooling: reuse the existing lightweight stack

- **Git + optional GitHub Issues:** version control, one active issue/test card, traceable decisions. No Jira/Trello requirement.
- **pytest:** explicit regression and invariant tests, fast targeted fixtures and minimal integration checks.
- **Ruff:** quick code-quality feedback; avoid duplicate linter/formatter stacks.
- **GitHub Actions on Windows and Ubuntu:** a small dual-OS test matrix is the preferred cheap portability gate; run the complete M0 suite at release gates. Extend existing CI where practical; do not duplicate workflows without need.
- **SQLite Research Journal:** for **market-research experiments**, not an excuse to build a separate product-development telemetry service.
- **Existing `CHANGELOG.md` and `MILESTONE_STATUS.md`:** development evidence; no further documentation tracker.

Do not install Lean Canvas software, paid Strategyzer subscriptions, workflow-management platforms, analytics dashboards or DORA tool suites for this project without a demonstrated need.

## References (methodology, not runtime dependencies)

- Eric Ries, Lean Startup principles: https://theleanstartup.com/principles?level=1
- Rita McGrath and Ian MacMillan, Discovery-Driven Planning (1995): https://hbr.org/1995/07/discovery-driven-planning
- NSF I-Corps, customer discovery: https://www.nsf.gov/funding/opportunities/nsf-national-innovation-corps-teams-nsf-national-i-corps-tm/solicitation
- Steve Blank, Hypotheses, Experiments, Tests, Insights (2015): https://steveblank.com/2015/05/06/build-measure-learn-throw-things-against-the-wall-and-see-if-they-work/
- Camuffo et al., A scientific approach to entrepreneurial decision-making (2024), sections 4 and 7: https://doi.org/10.1002/smj.3580
- INCOSE systems engineering process and verification: https://incose.github.io/process-model/
- NASA software fault tree analysis and top-down hazard investigation: https://swehb.nasa.gov/spaces/SWEHBVC/pages/140640490/8.7%2B-%2BSoftware%2BFault%2BTree%2BAnalysis
- Google SRE blameless postmortems and actionable prevention: https://sre.google/workbook/postmortem-culture/
- Google SRE postmortem action items: https://research.google/pubs/postmortem-action-items-plan-the-work-and-work-the-plan/
- DORA small software batches and fast feedback: https://dora.dev/capabilities/working-in-small-batches/


- Lean Startup principles and Build–Measure–Learn: https://leanstartup.co/about/principles/
- Test Cards: https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card
- Learning Cards: https://www.strategyzer.com/library/capture-customer-insights-and-actions-with-the-learning-card
- Select critical hypotheses first: https://www.strategyzer.com/library/how-to-test-your-idea-start-with-the-most-critical-hypotheses
- Kanban WIP and flow: https://kanban.university/kanban-guide/
- DORA delivery metrics: https://dora.dev/guides/dora-metrics/
