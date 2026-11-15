# AQRS confirmed requirements

This register is the central source of truth for confirmed AQRS requirements. Entries link to the governing specifications for full scope and verification details. The initial entries index selected existing commitments. Existing binding contracts and milestone criteria also apply. If a source and an entry diverge, raise the discrepancy in [Open Questions](OPEN_QUESTIONS.md) and resolve it with the owner.

## Functional requirements

| ID | Scope | Confirmed requirement | Acceptance criteria | Governing source |
|---|---|---|---|---|
| FR-001 | Through v1.0 | AQRS supports short-horizon trading research and limits all trading decisions to simulation. | A review of supported interfaces and the release configuration finds no path to submit live orders. | [Product vision](../PRODUCT_VISION.md#1-what-we-ultimately-intend-to-build), ADR-002 in [Project Decisions](../DECISIONS.md) |
| FR-002 | M2 | AQRS evaluates a LightGBM supervised challenger and an Isolation Forest unsupervised hypothesis generator. | Each pilot is reproducible, runs within its declared budget, and includes a comparison with a simple baseline. An evidenced blocker leaves the gate blocked. | [M2 acceptance criteria](../MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls) |
| FR-003 | By v1.0 | AQRS supports two-way, research-only interoperability with Sierra Chart and ACSIL. AQRS evaluates completed chart data exported by an ACSIL Study, and Sierra Chart displays a versioned AQRS signal on its intended bar through an ACSIL Study. | A native Windows Sierra Chart replay matches the AQRS reference for bar identity, UTC availability and signal placement through incremental updates and full recalculation. Invalid timing and identity are rejected. The same interchange fixture is reproducible in headless AQRS on Linux. FR-001 applies. | [Product vision](../PRODUCT_VISION.md#2-the-experience-from-a-users-perspective), [AQRS-SC01](../MILESTONE_ARCHIVE.md#aqrs-sc01-test-card-sierra-chart-and-acsil-round-trip-2026-11-10) |
| FR-004 | By v1.0 | AQRS helps users start research from their own observation or from a selected market alone. | **Observation:** Given a concrete user observation, AQRS returns a testable hypothesis, a fair comparison and an observable criterion tied to the observation. **Market:** Given a market with eligible development data and no user-supplied hypothesis, AQRS proposes a testable research idea linked to evidence in those data. On a predefined case with insufficient evidence, AQRS abstains and explains the gap. FR-001 and existing data and research admission rules apply. | [RD-001](DECISIONS.md#rd-001-two-entry-points-for-research) |
| FR-005 | All research stages | AQRS stops the affected test and requires rework when its question is unclear, ill-posed or insufficiently operationalized. It derives study scope from a testable question and its required evidence, and does not launch an effect study whose planned information has no credibly justified ability to inform that question or its registered decision. Technical capacity does not establish scientific sufficiency. | The admission and closeout cases below pass. An inconclusive outcome remains possible after an adequate design; an unclear question or known uninformative design is not admitted as an effect study. | [RD-002](DECISIONS.md#rd-002-question-led-evidence-and-decisive-study-planning), [evidence sufficiency](../SEQUENCE_PREFLIGHT.md#research-evidence-sufficiency), [claim admission](../RESEARCH_PROTOCOL.md#precision-and-claim-admission) |

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
2. **Question before capacity.** Before outcome access, the study identifies
   its question, intended decision, target population/comparison, relevant
   effect or descriptive quantity, required precision and the assumptions
   needed to assess information sufficiency. It explains what positive,
   negative and inconclusive findings would change. Record the origin of
   each binding limit: scientific rationale, owner choice, data availability,
   implementation capability or provisional technical default.
3. **Reject an uninformative design.** A known-answer case in which the
   feasible data cannot distinguish the decision-relevant effects under the
   stated assumptions is not admitted as an adequate effect study. A shorter
   runtime or an LLM-selected default window cannot override that result.
   No universal sample minimum or probability cutoff is introduced here.
4. **Admit a justified design.** A feasible case with justified precision,
   dependence treatment and a realistic prospect of informing its question
   can proceed when its existing permissions and guards pass. Requiring
   final-confirmation evidence prematurely must not block a separately
   justified exploratory question. Success is not guaranteed significance.
5. **Establish feasibility or stop and park.** When required evidence exceeds
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
6. **Keep pilot claims honest.** A technical test or preliminary study is
   allowed only for its own declared, decision-relevant question and acceptance
   criterion. A completed effect study cannot be relabelled as a pilot after
   an unhelpful result. Narrowing the question or changing the population must
   be explicit and prospective, with the original objective retained.

These cases apply to study planning now. This requirements change does not
establish that every runtime entry already enforces them; verification of
implementation coverage remains a separate authorized task. Existing market
stops, protected-data controls and Resource Governor limits remain binding.

## Nonfunctional requirements

| ID | Scope | Confirmed requirement | Acceptance criteria | Governing source |
|---|---|---|---|---|
| NFR-001 | From M0 | AQRS supports native Windows and headless, non-root Ubuntu on the declared CPU-only matrix. | The required clean-install, CLI, and test sequence passes independently on both platforms as specified by the platform contract. | [Platform support matrix](../PLATFORM_COMPATIBILITY.md#2-platform-support-matrix-and-honest-release-claims) |
| NFR-002 | Permanent | AQRS-authored repository artifacts use English. | The language audit and its self-test pass, and manual review confirms English prose in added and modified artifacts. | [Language policy](../LANGUAGE_POLICY.md#acceptance) |

Use [Open Questions](OPEN_QUESTIONS.md) for unresolved requirements and [Requirements Decisions](DECISIONS.md) for approved choices and their rationale. Implementation approval and milestone evidence remain separate in the [milestone record](../MILESTONE_STATUS.md).
