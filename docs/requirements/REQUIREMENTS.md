# AQRS confirmed requirements

This register is the central source of truth for confirmed AQRS requirements. Entries link to the governing specifications for full scope and verification details. The initial entries index selected existing commitments. Existing binding contracts and milestone criteria also apply. If a source and an entry diverge, raise the discrepancy in [Open Questions](OPEN_QUESTIONS.md) and resolve it with the owner.

## Functional requirements

| ID | Scope | Confirmed requirement | Acceptance criteria | Governing source |
|---|---|---|---|---|
| FR-001 | Through v1.0 | AQRS supports short-horizon trading research and limits all trading decisions to simulation. | A review of supported interfaces and the release configuration finds no path to submit live orders. | [Product vision](../PRODUCT_VISION.md#1-what-we-ultimately-intend-to-build), ADR-002 in [Project Decisions](../DECISIONS.md) |
| FR-002 | M2 | AQRS evaluates a LightGBM supervised challenger and an Isolation Forest unsupervised hypothesis generator. | Each pilot is reproducible, runs within its declared budget, and includes a comparison with a simple baseline. An evidenced blocker leaves the gate blocked. | [M2 acceptance criteria](../MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls) |
| FR-003 | By v1.0 | AQRS supports two-way, research-only interoperability with Sierra Chart and ACSIL. AQRS evaluates completed chart data exported by an ACSIL Study, and Sierra Chart displays a versioned AQRS signal on its intended bar through an ACSIL Study. | A native Windows Sierra Chart replay matches the AQRS reference for bar identity, UTC availability and signal placement through incremental updates and full recalculation. Invalid timing and identity are rejected. The same interchange fixture is reproducible in headless AQRS on Linux. FR-001 applies. | [Product vision](../PRODUCT_VISION.md#2-the-experience-from-a-users-perspective), [AQRS-SC01](../MILESTONE_ARCHIVE.md#aqrs-sc01-test-card-sierra-chart-and-acsil-round-trip-2026-11-10) |
| FR-004 | By v1.0 | AQRS helps users start research from their own observation or from a selected market alone. | **Observation:** Given a concrete user observation, AQRS returns a testable hypothesis, a fair comparison and an observable criterion tied to the observation. **Market:** Given a market with eligible development data and no user-supplied hypothesis, AQRS proposes a testable research idea linked to evidence in those data. On a predefined case with insufficient evidence, AQRS abstains and explains the gap. FR-001 and existing data and research admission rules apply. | [RD-001](DECISIONS.md#rd-001-two-entry-points-for-research) |
| FR-005 | All research stages | AQRS stops the affected test and requires rework when its question is unclear, ill-posed or insufficiently operationalized. It derives study scope from a testable question and its required evidence, including justified statistical methods, relevant academic research and a prospective test design. It does not launch an effect study whose planned information has no credibly justified ability to inform that question or its registered decision. Technical capacity does not establish scientific sufficiency. | The admission and closeout cases below pass. An inconclusive outcome remains possible after an adequate design; an unclear question or known uninformative design is not admitted as an effect study. | [RD-002](DECISIONS.md#rd-002-question-led-evidence-and-decisive-study-planning), [evidence sufficiency](../SEQUENCE_PREFLIGHT.md#research-evidence-sufficiency), [claim admission](../RESEARCH_PROTOCOL.md#precision-and-claim-admission) |

### FR-005 acceptance cases

1. **Question readiness before testing.** An unclear, ill-posed, contradictory
   or insufficiently operationalized question stops the dependent test before
   outcome access or fitting. AQRS identifies the defect and requests specific
   rework: the intended decision, target/population, measurable quantities,
   comparison where applicable, horizon, observation/availability rules, and
   how the possible findings would answer the question. Explain why a flawed
   formulation cannot support the intended claim; disagreement with a possible
   result alone is not a defect. Do not silently invent a proxy question,
   outcome, time window or acceptance threshold. Clarification and necessary
   design work can continue under FR-004; the test resumes only after the
   corrected question is recorded and readiness is rechecked. Known ambiguous,
   contradictory and undefined-measure cases must stop with actionable rework;
   their corrected versions must reach the evidence/feasibility assessment.
2. **Evidence and methods before capacity.** Before outcome access, the study identifies
   its question, intended decision, target population/comparison, relevant
   effect or descriptive quantity, and which observations could answer it.
   It justifies applicable statistical methods, required precision or detection
   ability, and assumptions connecting observations to the intended claim. Address
   dependence, selection and multiple testing where relevant; compare plausible
   alternatives sufficiently to explain the choice. Follow the existing
   [literature checks](../RESEARCH_PROTOCOL.md#decision-linked-literature-checks):
   identify relevant primary academic evidence, counterfindings and limitations,
   explain their applicability to this question, and record how they inform
   the hypothesis, method, baseline or design. State what existing evidence
   already answers and the remaining AQRS-specific gap, if any. Reuse applicable
   prior reviews.
   Published support for a method does not establish an AQRS market effect.
   No directly matching paper is required when a defensible methodological
   basis exists; missing or inaccessible evidence remains explicit.
3. **Prospective test design.** In the existing Test Card or linked artifact,
   specify the observations and measurement/availability rules, eligible
   population and sampling, comparison/control, observation and analysis units,
   and justified data scope. Specify relevant chronological splits, leakage and
   overlap controls, metrics, estimator, uncertainty procedure, effect/precision
   targets, and the sufficiency assessment under plausible dependence and
   dispersion assumptions. Include applicable selection/exposure accounting,
   stopping rules and the interpretation of positive, negative and inconclusive
   results. Explain how those results would answer the question or change its
   intended decision. Economic claims retain matched execution/cost assumptions;
   protected confirmation retains its existing separation and authorization.
   Use the elements applicable to the study's claim and stage; explain material
   omissions. Record the origin of each binding limit: scientific rationale,
   owner choice, data availability, implementation capability or provisional
   technical default. A method that cannot support the intended claim, missing
   measurement rules or a critical unjustified design assumption must trigger
   specific rework before the dependent test. A corrected, justified case must
   reach the feasibility assessment. Do not rescue outcomes by changing the
   design retrospectively; changed questions or designs follow registration rules.
4. **Reject an uninformative design.** A known-answer case in which the
   feasible data cannot distinguish the decision-relevant effects under the
   stated assumptions is not admitted as an adequate effect study. A shorter
   runtime or an LLM-selected default window cannot override that result.
   No universal sample minimum or probability cutoff is introduced here.
5. **Admit a justified design.** A feasible case with justified precision,
   dependence treatment and a realistic prospect of informing its question
   can proceed when its existing permissions and guards pass. Requiring
   final-confirmation evidence prematurely must not block a separately
   justified exploratory question. Success is not guaranteed significance.
6. **Establish feasibility or stop and park.** When required evidence exceeds
   current capability, either establish and verify the missing prerequisites
   within authorized scope/budgets, or stop the affected test and retain it as
   parked work. Preserve its original question and required evidence. The
   parked record names exactly what is missing (for example data, compute,
   implementation, a defensible method or authorization), why this prevents
   the intended answer, and the observable condition for resumption. Identify
   a resolution route and its effort when one is known; explicitly state when
   no viable route is known. Reopen only after the missing prerequisite changes
   and readiness is rechecked. Do not silently shorten the study, weaken its
   criteria, repeatedly run an inadequate substitute or classify inability to
   test as evidence of no edge. Parking with a stated reason is a valid outcome.
7. **Keep pilot claims honest.** A technical test or preliminary study is
   allowed only for its own declared, decision-relevant question and acceptance
   criterion. A completed effect study cannot be relabelled as a pilot after
   an unhelpful result. Narrowing the question or changing the population must
   be explicit and prospective, with the original objective retained.

### FR-005 execution enforcement and verification

Every supported research execution attempt must have a current, recorded
admission decision before acquiring study data, accessing study outcomes or
starting its study computation. This includes repeat/resume attempts and
alternative launch paths. A CLI check alone is insufficient if a supported
campaign or worker entry can bypass it. Purely declarative planning may remain
available; a data-based feasibility study or pilot needs its own justified
question, admission and authorization under the cases above.
Apply prerequisites to the requested action: authorized work to establish a
missing prerequisite can proceed under its own bounded purpose and applicable
guards. For example, missing data prevents analysis but need not prevent an
admitted acquisition whose purpose is to obtain those data. This does not
admit the dependent effect study or weaken its required evidence.

Admission combines **scientific readiness** (the question, literature/method
basis, design and evidence sufficiency) with **execution readiness** (required
data scope, implementation capability, permissions, exposure, protected-data
controls and resource guards). Satisfying one does not establish the other.
Mechanical completeness checks cannot establish scientific adequacy. Require
a reasoned scientific review with attributable provenance and resolved material
findings, assessed separately from the plan author's assertion. A bare `PASS`,
filled fields or a confident LLM response is insufficient. A review procedure
must be qualified on independently assessed clear, ambiguous and unsuitable
cases before its decisions are relied on automatically. Unresolved uncertainty
about a required admission condition stops the dependent test; expected
statistical uncertainty does not itself prohibit a justified study.
The review mechanism is an implementation choice, not a claim
that software or an LLM can guarantee scientific correctness.

Bind admission to the reviewed question/design revision, relevant code and
configuration, data identity/scope, evidence and applicable authorization.
Check that binding and current prerequisites on every launch. Changes affecting
the claim, method, comparison, data scope or execution invalidate affected
checks. Unchanged, applicable scientific evidence may be reused with a recorded
reason; prior approval does not waive current resource, exposure or permission
checks. Existing valid owner authorizations do not require renewed approval
for every run. Missing, rejected, unverifiable or stale admission stops launch.

Record the requested attempt, decision, evidence/review references, exact
reason, required correction or missing prerequisite, and observable resumption
condition in existing run/journal records. A failed admission check must not
fall through to execution. If durable recording fails, do not launch; return
an explicit failure without claiming that a record was saved. If a required
condition fails during execution, stop affected work safely and prevent further
dependent trials. Preserve incurred exposure and distinguish this stop from a
scientific finding. Resume only after relevant rework and renewed admission;
do not automatically retry an unchanged rejected request.

Implementation acceptance must exercise the real supported launch paths on
native Windows and headless Linux, with observable data-access and worker/fit
counters. Public engineering fixtures verify control behavior; independent
scientific qualification data, when needed, are supplied by the owner.

| Case | Required observable result |
|---|---|
| Missing, contradictory or insufficiently operationalized question | Specific rework; zero study-data/outcome accesses, study workers and fits. |
| Fully populated plan with an unsuitable method or unjustified information sufficiency | Scientific rejection or unresolved review blocks the test despite complete fields. Correcting the design permits a fresh assessment. |
| Missing data/capability/permission, exhausted budget or unavailable required guard for the requested action | Park that dependent action with exact reason and restart condition; zero blocked study work. Separately admitted prerequisite work may proceed. |
| Missing/failed review, unresolved material finding, forged or mismatched approval, or record-storage failure | No launch; explicit failure, never a default approval or invented audit record. |
| Plan, data scope, relevant code or permission changes after review | Old approval cannot launch the changed work; the actual executed inputs match the admitted version. |
| Repeat/resume, alternate command or direct supported campaign/worker entry | The same admission conditions hold; an uncovered path is not enabled for research. |
| Valid reviewed public engineering case with all current prerequisites | One authorized bounded execution starts, and its admission references and actual work are recorded. Blanket rejection does not pass acceptance. |
| Required execution condition is lost during a run | Safe stop, no next dependent trial, retained exposure and an explicit non-scientific stop reason. |

These criteria specify intended enforcement. The current
[implementation gap](OPEN_QUESTIONS.md#fr-005-execution-enforcement-gap)
remains open; documentation review does not demonstrate runtime enforcement
or validate a scientific reviewer. Existing market stops, protected-data
controls and Resource Governor limits remain binding.

## Nonfunctional requirements

| ID | Scope | Confirmed requirement | Acceptance criteria | Governing source |
|---|---|---|---|---|
| NFR-001 | From M0 | AQRS supports native Windows and headless, non-root Ubuntu on the declared CPU-only matrix. | The required clean-install, CLI, and test sequence passes independently on both platforms as specified by the platform contract. | [Platform support matrix](../PLATFORM_COMPATIBILITY.md#2-platform-support-matrix-and-honest-release-claims) |
| NFR-002 | Permanent | AQRS-authored repository artifacts use English. | The language audit and its self-test pass, and manual review confirms English prose in added and modified artifacts. | [Language policy](../LANGUAGE_POLICY.md#acceptance) |

Use [Open Questions](OPEN_QUESTIONS.md) for unresolved requirements and [Requirements Decisions](DECISIONS.md) for approved choices and their rationale. Implementation approval and milestone evidence remain separate in the [milestone record](../MILESTONE_STATUS.md).
