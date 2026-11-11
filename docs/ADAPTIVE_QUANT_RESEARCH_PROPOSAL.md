# Adaptive, Decision-Oriented Quant Research

**Status.** This is the AQRS target design adopted under [ADR-045](DECISIONS.md#adaptive-research-integration), translated from the owner-supplied German proposal. The phase names below belong to the source design. Use the [binding Lean research rules](../AGENTS.md#lean-research-rules-binding), [research protocol](RESEARCH_PROTOCOL.md) and the integration mapping in ADR-045 to select the smallest workflow for the current research question. Scope authorization and acceptance follow [CODEX_START.md](../CODEX_START.md) and [MILESTONE_STATUS.md](MILESTONE_STATUS.md).

- This technical integration specification and roadmap targets the owner's existing quant research framework.
- Source version 1.1 is dated 2026-11-08. A comparison with the supplied v1.0 copy found that v1.1 carries forward its substantive research design and strengthens protected evaluation requirements.
- The source discussion covered anomaly discovery, strategy construction, causal spaces, adaptive experiment planning and multiple causes.
- The source author had no repository, language, concrete classes or data providers to inspect when drafting.
- The integration scope excludes live trading, broker account changes and paid data acquisition.
- Version 1.1 adds enforced information barriers for AI agents, generated code and evaluation. Security acceptance precedes access to real protected data.
- The source records the design stage. Repository controls, OS permissions, services and deployed access restrictions require separate operational evidence.

> **Proposed work:** Extend the existing framework with auditable, budgeted research management. Reuse data, feature, backtest, risk and reporting components. Begin with a small complete research cycle with enforced data separation and an audit trail. Use synthetic fixtures for protected evaluation until the M1-S security acceptance passes. Evaluate advanced learning methods as interchangeable extensions after the cycle has been tested. Derive interfaces from the repository and integrate methods in separate increments.

## Reading conventions and decision status

- **MUST / MUST NOT** identify requirements within the proposal.
- **SHOULD** identifies a reasoned default. Deviations call for a documented architecture decision.
- **MAY** identifies an optional extension outside the first increment.
- **Discussion outcome** summarizes the resulting methodology.
- **Design choice** identifies a proposal added to make the specification actionable. Adoption remains open.
- **Repository assessment** identifies questions to resolve against the actual project before editing files.

The architecture is a methodological proposal. Its advantage over simpler searches and the profitability of resulting strategies remain unproven. Illustrative returns, thresholds, budgets and charts from the discussion are examples. The references at the end provide traceable background.

---

## 0. Mandatory security correction in version 1.1

Development and confirmation data must be separated even when an AI agent ignores its instructions. A prompt, role name, client-side Python flag or different file path provides insufficient isolation when the same agent can reach the data through a shell, filesystem, database, tool or administrator privilege.

Version 1.0 required data roles and preferred a separate evaluator but allowed in-process adapters too broadly. Version 1.1 allows research logic in the same process and requires the security boundary for real confirmation data to sit outside the research agent's authority. The deployed permissions and information flows determine whether this boundary holds.

This change covers C08/C09, new components C13–C15, the interfaces in section 5, the protection architecture in sections 10.6–10.17, milestone M1-S and tests SEC01–SEC24. Apply these requirements if older in-process wording conflicts.

Implementation depends on the repository. The permission, release and sandbox rules below specify the intended design. They require separate operational evidence.

## 1. Scope of the proposed increment

### 1.1 Objective

Build hypothesis-led, adaptive and sequential research management that:

1. Describes economically relevant search domains.
2. Generates plausible mechanisms and competing explanations.
3. Accommodates unexplained data structures and new causal classes.
4. Identifies uncertainties that could affect a decision.
5. Selects suitable investigations under a finite budget.
6. Updates hypotheses, parameter regions and priorities as evidence arrives.
7. Assesses exploratory findings, confirmed predictions, causal claims and tradable strategies separately.

The layer coordinates two linked research processes:

- **Anomaly discovery.** Which observable configurations add predictive or economic value over a defined reference model?
- **Strategy discovery.** Which concrete trading decision can use that finding under the available data, latency, costs, capital and risk constraints?

Strategy research may inform anomaly research when, for example, an effect is too short-lived or only executable at certain liquidity levels. Treat each such change as development and assign it new provenance.

### 1.2 Scope boundaries

The scope is research on the existing framework. It excludes a broker, replacement of the whole backtester, a universal causal proof system, exhaustive mapping of market causes and autonomous live trading.

A statistically significant effect needs further evidence before it can qualify as alpha. A causal explanation gives no trading authorization. An independently supported conditional forecast can have economic relevance while its mechanism remains unresolved. Label its evidentiary status accordingly.

### 1.3 Design rationale

| Problem | Design response |
|---|---|
| Unrestricted optimization of indicators, thresholds and strategies creates a vast search space. | Structure it using mechanisms, economic decision boundaries and small, justified experiment families. |
| Rigid filter cascades permanently discard alternatives and miss new explanations. | Version and extend the model space. Allow reversible deferral and justified reopening. |
| Some unknown quantities have little bearing on decisions. | Select experiments based on their plausible effects on decisions and their statistical information. |
| Several causes may act jointly, at different times or through alternative paths. | Represent configurations, interactions, moderators and temporal feedback as distinct model objects. |
| Univariate filters can miss pure informational synergy. | Preserve dedicated interaction and open discovery paths without a universal main-effect gate. |
| Adaptive selection can make findings overly optimistic. | Record full development provenance, protect confirmation and evaluate the search policy separately. [^S2] |
| An agent with broad tool access can bypass logical data separation. | Use external authorization, separate runtime identities, sealed evaluation and controlled result release. |
| Complex methods can consume unbounded resources. | Use a small deterministic core and optional budgeted method plugins. |
| Economic value depends on execution and risk. | Screen for rough tradability early, then run realistic strategy tests through existing infrastructure. |

Use literature as a documented starting point, reference model or testable assumption. Keep the search open to explanations outside that literature.

## 2. Research workflow

### 2.1 Preparation for each campaign

Before the first data-dependent screen, Codex or the operator defines:

- Research objective, market universe, allowed data, decision timestamps and target horizons.
- Economic minimum requirements, available execution methods and risk limits.
- Research budget and stop conditions.
- Data roles and access rights.
- Reference models and comparisons.
- Statistical claims, confirmation rules and responsibilities.
- Search policy, model versions and rules for permitted learning.

Missing production configuration blocks production use. Synthetic tests can use explicitly labeled fixture values.

### 2.2 Inner adaptive research cycle

```text
Check economic decision boundaries and available data capabilities
    -> Generate mechanisms, configurations and gaps in explanations
    -> Identify uncertainties that may affect decisions
    -> Formulate alternative investigations
    -> Select the next investigation under budget and evidence rules
    -> Version the experiment plan before accessing outcome data
    -> Execute through existing analysis or backtest components
    -> Record evidence, cost and actual data use
    -> Decide whether to deepen, revise, park, reject, leave the cause
       unknown or prepare confirmation
    -> Update the model space and priorities
    -> Repeat or end the campaign
```

Exploratory work can generate further hypotheses. Set the rules of a later confirmatory test before accessing its results. The exploratory hypothesis space can remain open.

### 2.3 Outer confirmation and handoff

```text
Freeze the candidate and full test rule
    -> Run protected chronological confirmation
    -> Assess prediction, causal claims and tradability separately
    -> Hand off to existing strategy development if evidence is sufficient
    -> Confirm the resulting trading policy independently
    -> Observe prospectively or run a separately authorized pilot where appropriate
```

Reserve the final holdout from iterative refinement. Inspecting a result exposes that scope to any descendant influenced by it. A formally justified reuse protocol would require separate evaluation as a statistical plugin. [^S2]

### 2.4 When the search ends

End a campaign at budget exhaustion, satisfaction of a predeclared handoff condition, lack of economic justification for the next trial, or absence of essential data or identification conditions.

`NO_TRADE`, `NO_CANDIDATE` and `INCONCLUSIVE` are valid outcomes. Parking a candidate on budget grounds leaves its existence unresolved. A resource decision can be made before establishing robust dominance over every alternative.

---

## 3. System boundary and integration points

### 3.1 Integration principle

The proposed layer orchestrates and governs existing functionality. Version 1.1 requires a technically independent enforcement layer for real protected evaluation. The names below identify logical contracts pending a repository mapping.

| Existing area, if available | Proposed integration | Interface obligations |
|---|---|---|
| Data catalog, loader or storage | `DataAccessPort` and `DataAccessGuard` | Versioned snapshots, availability timestamps, data roles and access audit. |
| Feature pipeline | `FeaturePort` | Separate fit and transform, track training provenance, compute point-in-time features and avoid transformations prefit on the full sample. |
| Event and label generation | `EventLabelPort` | Event definition, detection timestamp, feature cutoff and full label interval. |
| Model training and optimization | `ModelPort` | Bounded search space, reproducible fits, frozen artifacts and explicit training budget. |
| Event study or statistics | `ExperimentExecutor` plugins | Defined estimand, null model, comparison groups, dependence treatment and uncertainty report. |
| Backtester or execution simulator | `BacktestPort` | Execution after signal availability, net PnL, cost breakdown, fill assumptions and capacity limits. |
| Risk or portfolio module | `RiskPort` | Permitted actions, sizing, capital usage and comparable risk budgets. |
| Experiment tracker or artifact store | `EvidenceStore` and `SelectionLedger` | Immutable versions, complete lineage, failed attempts and cancellations. |
| Strategy registry | `StrategyHandoffPort` | Structured candidate handoff with separate production authorization. |
| Scheduler, jobs or CLI | `ResearchOrchestrator` | Budget reservation, idempotency, recovery, cancellation and job status. |
| Reports or dashboard | `ResearchReportPort` | Visible evidentiary status and selection history, with distinct development and confirmation views. |

### 3.2 Proposed logical components

| ID | Component | Responsibility | Initial stage |
|---|---|---|---|
| C01 | `ResearchCampaign` / `ResearchOrchestrator` | Campaign state machine and workflow. | Required |
| C02 | `OpportunityModel` | Economic decision boundaries, action sets and exclusion rationale. | Required |
| C03 | `MechanismRegistry` / `HypothesisRegistry` | Causal components, configurations, competing explanations and revisions. | Required |
| C04 | `CandidateGenerator` | Mechanistic proposals, unexplained residuals and new configurations. | Rule-based core, optional ML |
| C05 | `DecisionSensitivityAnalyzer` | Link uncertainty to decisions. | Scenario-based core |
| C06 | `ExperimentPlanner` / `ResearchAllocator` | Experiment design, selection, budget and protection for exploration. | Transparent heuristic |
| C07 | `ExperimentExecutor` | Invoke existing analysis, training and backtest functions. | Required |
| C08 | `ValidationGate` / `DataAccessGuard` | Scientific data roles, freeze and client-side prechecks. Route protected access through C13/C14 only. | Required |
| C09 | `EvidenceStore` / `SelectionLedger` | Findings, assumptions, access and full selection provenance, with separate development and protected views. | Required |
| C10 | `ModelRevisionManager` | Rules for extending the causal grammar and reopening work. | Required |
| C11 | `StrategyHandoffBuilder` | Anomaly-to-strategy handoff package. | Required |
| C12 | `PolicyEvaluator` | Compare complete search policies under equal budgets. | Start with synthetic benchmarks and replay |
| C13 | `IsolationControlPlane` | Authenticated identities, authorization, protected catalogs, scoped evaluation tickets and deployment control. | Required before real protected evaluation |
| C14 | `SealedEvaluationService` | Trusted replay and scoring harness with an isolated candidate runtime and point-in-time inputs. | Required before real protected evaluation |
| C15 | `ResultReleaseGate` / `ExposureRegistry` | Controlled release, global holdout slots and exposure inheritance. | Required before real protected evaluation |

Research functions may run in the existing process. Real protected data require a boundary outside the broadly privileged agent process. Run C13–C15 in a separately authorized trust zone and isolate untrusted candidate code from the full evaluation dataset. An existing host can suffice if its operational and sandbox controls enforce the boundary. A single service can combine trusted components while preserving privilege separation. The design leaves distributed agents, Kubernetes and graph databases optional.

### 3.3 Repository assessment before implementation

Inspect project instructions, tests, configurations, data models and execution paths. Produce a mapping:

```text
Logical contract -> actual module, class or function
                 -> reuse, extend or add
                 -> affected tests
                 -> migration and compatibility risks
```

Plan specific file changes after the mapping. Use narrow adapters or explicit `UNSUPPORTED_CAPABILITY` results for missing components. Label simulations of unavailable data explicitly.

## 4. Central data objects

### 4.1 Common metadata

All persistent research objects will receive at least:

```text
id, version, schema_version, content_hash,
created_at_utc, created_by, campaign_id,
parent_ids, source_refs, assumption_refs,
code_version, config_hash, data_snapshot_refs,
selection_lineage_id
```

`content_hash` is calculated via a canonical serialization of the technically relevant content. Versions are immutable; changes create new versions. Confidential raw data and credentials do not belong in the ledger.

### 4.2 Research objects and required fields

| Object | Essential content in addition to metadata |
|---|---|
| `ResearchCampaign` | Target, scope, policy version, budget, data access permissions, allowed actions, stop rules, status. |
| `ResearchDomain` | Instruments, venues, data sources, horizons, families of mechanisms, maximum order of interaction, scope limits. |
| `Assumption` | Statement, type, source, scope, availability, revision trigger, status. |
| `ParameterRegion` | Parameters with units, common permitted region, restrictions, origin, type of uncertainty. |
| `Mechanism` | Actors, objectives, constraints, triggers, liquidity/information path, time structure, frictions, counter-arguments. |
| `CausalConfiguration` | Components, directed/unexplained relationships, interactions, moderators, lags, latent variables, alternative models. |
| `Hypothesis` | Precise statement, event, target variable, baseline, horizon, expected difference, rival explanations, falsification conditions. |
| `DecisionUncertainty` | Unknown quantity or model family, permitted values, decisions affected, relevant borderline cases. |
| `ExperimentPlan` | Question, Candidates, Method, Estimand, Data Role, Evaluation Rules, Costs, mapping from outcomes to decisions. |
| `ExperimentRun` | Plan hash, resources, actual data usage, fit artifacts, execution status, error, result reference. |
| `EvidenceRecord` | Effect sizes, intervals, methodology, data quality, dependencies, evidentiary status, support/counter findings. |
| `ResearchDecision` | Selected action, considered alternatives, justification, budget follow-up, evidence references, recovery condition. |
| `StrategyCandidate` | Signals, timing, actions, size/exit candidates, cost model, lineage of anomalies. |
| `PolicyEvaluation` | Comparison policies, identical resource regime, evaluation window, overall distribution of results and constraints. |

### 4.3 Assumptions and intervals must not be confused

`Assumption.kind` SHALL distinguish:

```text
STRUCTURAL_CONSTRAINT
EMPIRICAL_ESTIMATE
SUBJECTIVE_SCENARIO
PROBABILISTIC_MODEL
```

Examples: a documented stock market rule, a cost range estimated from development data, a subjective stress case or a common probability distribution.

`ParameterRegion` also stores `uncertainty_semantics`, such as `scenario_range`, `confidence_region` or `posterior_credible_region`. A plausibility interval shall not be represented as a confidence interval. Dependent parameters must not be replaced unnoticed by a Cartesian product of independent individual intervals.

### 4.4 Representing multiple causes

A configuration MUST map more than a list of simultaneously existing features:

- additive effects;
- conjunctive conditions and statistical interactions;
- Moderation: state changes strength or direction of an effect;
- mediation through downstream variables;
- alternative pathways to the same observed outcome;
- feedback via explicit time indices;
- unobserved or unidentified common causes.

An interaction with three components is not automatically fully represented by three paired edges. Therefore, the model is given a separate object `InteractionTerm` with `participant_ids`, `order`, `lag_spec`, `functional_form`, `target` and `evidence_refs`.

Time feedbacks are developed in time at the core, for example `price[t] -> forced_flow[t+1] -> price[t+2]`. Unexplained simultaneous relationships are not arbitrarily oriented towards the enforcement of a DAG. Plugins can return partially oriented graphs; latent confounding is explicitly allowed. [^S8]

### 4.5 Separate evidence dimensions

Each result is given separate axes:

```text
prediction_evidence:
  UNTESTED | EXPLORATORY | CONFIRMED_WITHIN_SCOPE | FAILED | INCONCLUSIVE

causal_evidence:
  UNASSESSED | PLAUSIBLE | ASSUMPTION_DEPENDENT | IDENTIFIED_WITHIN_ASSUMPTIONS

economic_evidence:
  UNASSESSED | ENVELOPE_PLAUSIBLE | SIMULATED_NET_POSITIVE |
  PROSPECTIVELY_SUPPORTED | UNATTRACTIVE | INCONCLUSIVE

execution_fidelity:
  NONE | QUOTE_PROXY | QUEUE_MODEL | PAPER | LIVE_OBSERVED
```

`PAPER` is not automatically more accurate than a good queue model. The execution specification is a category, not a linear quality score. A confirmed forecast requires neither identified causality nor live observed profitability. Each confirmed status is bound by scope, method, period and version.

### 4.6 Machine-readable results and decision rules

The following embedded value objects concretize the interfaces. They inherit the provenance of their parent artifact and do not require a stand-alone registry entity.

```text
MetricEstimate:
  metric_id: string
  target_ref: id
  estimand: string
  value: number | null
  unit: string
  interval: {lower, upper, level, method, semantics} | null
  sample_counts: {rows, events, episodes, instruments, sessions}
  dependence_spec_ref: id
  estimation_status: ESTIMATED | INSUFFICIENT_DATA | INVALID
  scope_ref: id

DecisionRule:
  rule_id: string
  priority: integer
  required_estimation_status: string
  predicates: [{metric_ref, field, operator, value, unit}]
  combine: ALL | ANY
  action: CONTINUE | REFINE | PARK | REJECT_WITHIN_SCOPE |
          PROPOSE_REVISION | PREPARE_CONFIRMATION | HANDOFF | STOP
  rationale_template: string

ResourceBudget:
  cpu_seconds: nonnegative number
  gpu_seconds: nonnegative number
  peak_memory_bytes: nonnegative integer
  monetary_limit: {amount, currency}
  max_runs: positive integer
  wallclock_deadline_utc: timestamp | null
  human_review_minutes: nonnegative number | null
```

In particular, `interval.semantics` distinguishes confidence, credibility and pure scenario boundaries. A missing reading is `null`, never automatically zero in the numerical sense. The meaning of a metric and its comparability are determined by Target, Estimand and units, not just by a name like `alpha`.

Rules are interpreted by registered operators such as `lt`, `lte`, `gt`, `gte`, `eq` and `in`, not by `eval` of an LLM-generated expression. The rule set has a clear priority order, explicit conflict management and a fallback `INCONCLUSIVE` at results level, followed by a research action `PARK` or `CONTINUE`. Missing values shall not implicitly satisfy any numerical rule.

A confirmation rule identifies the adjusted tests or intervals used and the test family. It must not accidentally consume an unadjusted development value under the same metric name. Unit or data-role errors lead to a validation error before the decision.

## 5. Interface contracts

The following signatures are language-neutral contract notation, not an already existing or immediately executable source code. Codex implements them idiomatically in the existing stack. In-process adapters are sufficient for development data and synthetic fixtures; for true protected evaluation, the externally enforced limits of section 10.6–10.17 apply.

### 5.1 Data and features

```text
DataAccessPort.capabilities(scope) -> CapabilityReport
DataAccessPort.request_view(plan_id, role, selector, requester) -> DataViewHandle
DataAccessPort.materialize(handle, decision_schedule) -> PointInTimeDataset
FeaturePort.fit(feature_spec, training_view, fit_context) -> FeatureArtifact
FeaturePort.transform(feature_artifact, authorized_view) -> FeatureDataset
EventLabelPort.build(event_spec, target_spec, authorized_view) -> EventDataset
```

**Contract rules:**

- `CapabilityReport` describes available data depth, time resolution, history, availability stamp, data quality and cost information.
- `DataViewHandle` is an authorized, logged reference to a snapshot and data role. It must not circumvent protected data through a freely changeable file path.
- `requester` is derived from the authenticated identity on the server side. A transmitted role name does not authorize anything. For research identities, `request_view` and `materialize` shall not provide real `CONFIRMATION`-/`POLICY_EVALUATION` data or their still protected derivatives, nor shall `PROSPECTIVE` data blocked at this time. The research client receives only an opaque submission reference for such examinations via `SealedEvaluationPort`.
- A client-side `DataAccessGuard` is convenience and error detection. The actual refusal must also exist on the server/operating system side after removal or manipulation of this guard.
- `PointInTimeDataset` contains per observation instrument, venue, event time, availability time, data version, quality flags and units.
- `EventDataset` also includes event ID, event/episode cluster, decision time, feature time domain, label start, label end and target definition.
- `FeatureArtifact` contains Fit dataset, normalization, feature/model version and allowed application. Embeddings, clusters, quantiles and dimension reduction are also fit artifacts.
- Historical values may be used as a lookback in later predictions. Forbidden are future observations, not yet available revisions and transformations learned outside the permitted training role.
- The label builder may read later target values within its authorized data window, but only as outcomes. It stores `label_available_at`; training and online updates are only allowed to use mature labels. This permission must not be passed on to the feature calculation.
- If `available_at` is not historically reliably known, a documented conservative availability assumption must be used and the evidence limited accordingly. An event stamp alone proves no tradability at that time.

### 5.2 Research management

```text
CandidateGenerator.propose(context, registry_snapshot, budget) -> CandidateBatch
OpportunityModel.assess(candidate, actions, parameter_region) -> FeasibilityAssessment
DecisionSensitivityAnalyzer.analyze(candidate, evidence, actions) -> UncertaintySet
ExperimentPlanner.propose(uncertainty, capabilities, budget) -> ExperimentPlanDraft[]
ResearchAllocator.choose(plans, campaign_state) -> AllocationDecision
ExperimentPlanner.freeze(draft, validation_spec) -> FrozenExperimentPlan
ExperimentExecutor.run(frozen_plan, authorized_handles) -> ExperimentRun
EvidenceStore.append(run) -> EvidenceRecord
ModelRevisionManager.review(registry, new_evidence) -> RevisionProposal[]
ResearchOrchestrator.step(campaign_id) -> ResearchDecision
```

`CandidateBatch` may contain new candidates, new domains and extension proposals. It may not directly modify registry schemes or data access permissions.

`FeasibilityAssessment` provides `FEASIBLE_WITHIN_SCENARIOS`, `ROBUSTLY_INFEASIBLE_WITHIN_SCOPE`, `UNRESOLVED` or `UNSUPPORTED_CAPABILITY`, each with assumptions and a reasonable calculation. A negative screening result alone is not a robust certificate of impossibility.

`FrozenExperimentPlan` contains the hash of all decision-relevant specifications. Changes after freeze create a new plan, not an edited past.

### 5.3 Models, backtests and handover

```text
ModelPort.fit(model_spec, train_view, tuning_spec, budget) -> ModelArtifact
ModelPort.predict(model_artifact, authorized_view) -> PredictionArtifact
BacktestPort.evaluate(strategy_spec, authorized_view, execution_spec, risk_spec)
    -> BacktestResult
ValidationGate.preflight(frozen_candidate, frozen_protocol) -> PreflightResult
SealedEvaluationPort.submit(bundle_digest, slot_id, idempotency_key) -> SubmissionReceipt
SealedEvaluationPort.receipt(receipt_id) -> SubmissionReceipt
ResultReleasePort.release(release_request) -> ReleasedValidationReport
StrategyHandoffPort.publish(handoff_package) -> RegistryReceipt
PolicyEvaluator.compare(policy_specs, benchmark_spec) -> PolicyEvaluation
```

`BacktestResult` SHALL show at least gross and net results, fees, spread/slippage treatment, impact assumptions, fill and non-fill events, risk exposure, capital requirements and data fidelity. A spread already calculated from execution prices may not be deducted again as a flat-rate cost.

`ValidationGate` pre-checks the eligibility and formal suitability of the package. The results are evaluated in protected harness. An existing `ValidationGate.evaluate` may be reused as an internal contract not freely executable by the research agent. Neither of these contracts produces a general statement “strategy is true” or “market mechanism is proven”.

The same limits apply to `PolicyEvaluator.compare` and `BacktestPort.evaluate`: the return of full results is allowed in development/synthetic mode. In real protected scopes, these methods only run internally in the released harness; the research client initially receives only the opaque receipt. Apply the release logic to every port.

`SubmissionReceipt` does not contain any scores, pass/fail decisions or data-driven error details before results are released. `ResultReleasePort` is a privileged service interface, not a tool freely available to the search agent. The detailed contracts are in 10.14.

### 5.4 Uniform error semantics

At least the following failure states shall be technically distinguishable:

```text
MISSING_CONFIGURATION
UNSUPPORTED_CAPABILITY
INSUFFICIENT_DATA
DATA_QUALITY_FAILURE
TEMPORAL_LEAKAGE
ROLE_ACCESS_DENIED
HOLDOUT_ALREADY_EXPOSED
INVALID_STATISTICAL_ASSUMPTIONS
BUDGET_EXCEEDED
EXECUTION_MODEL_UNCALIBRATED
EXPERIMENT_FAILED
ISOLATION_NOT_VERIFIED
PRINCIPAL_NOT_AUTHORIZED
ARTIFACT_DIGEST_MISMATCH
UNSAFE_ARTIFACT_FORMAT
EVALUATION_SLOT_EXHAUSTED
RESULT_RELEASE_DENIED
EXPOSURE_STATUS_UNKNOWN
EXPOSURE_INCIDENT
AUDIT_UNAVAILABLE
```

A technical error is not a statistically negative result. Missing data must not be stored as zero return, zero information or excluded cause.

## 6. Economic decision boundaries and exclusions

### 6.1 Minimum model

The first economic test uses a documented combination of:

- expected effect remaining **from the first executable decision time**;
- available actions including `NO_TRADE`;
- costs, latency and fill assumptions;
- frequency and dependence of opportunities;
- capital requirements, loss distribution, liquidity and capacity;
- a predefined margin of safety or risk-benefit function.

For a simplified consideration of returns in identical units, the possible limit is:

\[
\mu_{\mathrm{gross}}(a,s,\theta)-c(a,s,\theta)>m.
\]

`m` is an explicit minimum margin, not a statistically derived confidence level. An appropriate net benefit/risk assessment is required for the final decision. A positive mean alone is not enough.

### 6.2 Parametric inversion

Instead of first looking for the largest possible backtest values, `OpportunityModel` determines which combinations of effect strength, lifetime, cost, capacity and frequency could meet the requirements at all.

The output is a permitted region, for example:

```text
decision_boundary:
  remaining_alpha_bps > roundtrip_cost_bps + required_margin_bps
  signal_lifetime_ms > decision_latency_ms + routing_latency_ms
  capacity_notional >= configured_minimum
  risk_constraints_satisfied == true
```

This is a structure, not a production-ready trading rule. Parameters are filled from sources, estimates or labeled scenarios.

### 6.3 Robust exclusion is scope-bound

For the investigated domain `d`, available actions `A_d` and common parameter region `Theta_d`, a robust economic exclusion is only allowed if even the upper allowed utility does not meet the minimum requirement:

\[
\sup_{a\in\mathcal A_d,\,\theta\in\Theta_d}
\bigl[U(a,\theta)-U(\mathrm{NO\_TRADE},\theta)\bigr]
< u_{\min}.
\]

The certificate stores scope, region, model and calculation. A handful of favorable/unfavorable scenarios are not evidence of a continuous region. Checking boundary points is sufficient only if the functional structure is duly justified; otherwise, the result is `UNRESOLVED` or ‘unattractive in tested scenarios’.

The exclusion applies only to the currently realistically available execution modes and assumptions. Other fees, better data, different capacity or new execution procedures may justify a resumption.

### 6.4 Three different negative decisions

- `REJECT_WITHIN_SCOPE`: economic or empirical exclusion rule fulfilled.
- `PARK`: too expensive, too uncertain, currently inadequate data or low priority.
- `STOP_CAMPAIGN`: budget/time/target condition achieved.

These decisions shall not be used interchangeably. Even dominant alternatives are judged only relative to the utility function under consideration and the modeled assumptions.

## 7. Causal space and candidate generation

### 7.1 Three complementary generation channels

**Mechanistic:** Combinations of actor, target, restriction, trigger, information and liquidity response, time structure and backlash. Generation includes aggressive orders, passive quotes, cancellations and changes in liquidity provision. Price changes are not limited to completed market order transactions. [^S1]

**Data-driven abductive:** Recurring, relevant model deviations, conditional distributions, residual structures and new state configurations. First, data errors and known model flaws are checked. An unexplained residual can motivate an investigation. Causal identification requires separate evidence.

**Environmental:** Changes in market rules, data availability, institutions or liquidity structure provide new candidates. A change is not automatically an exogenous natural experiment; alternative simultaneous changes must be considered.

### 7.2 Morphological generation with compatibility testing

A morphological box is a proposal generator, not a complete world model. Combinations need:

```text
actor -> objective / constraint -> trigger -> action or quote response
      -> transmission channel -> observable implications -> timing
```

Impossible temporal processes, contradictory assumptions and institutionally excluded actions are removed. Unknown categories are allowed. The assignment to an existing cell must not be a prerequisite for the acceptance of a new candidate.

### 7.3 Competing explanations

Any substantially further pursued hypothesis SHOULD contain at least one plausible alternative explanation or relevant artifact test. For example:

- temporary liquidity pressures versus continuing flow of information;
- true mid-quote response versus bid-ask bounce;
- stand-alone effect versus joint market/sector shock;
- Mechanistic interaction versus measurement, timing or selection artifact.

Several explanations may remain plausible after a test. The system does not have to force a clear cause if the data does not identify it.

### 7.4 Extension of grammar

`ModelRevisionManager` examines an extension if documented deviations recur, are economically relevant or important to the explanation and existing models do not sufficiently capture them under their allowed adjustments.

The revision is carried out in two steps:

1. **Provisional proposal:** record new component, relationship, state variable or domain with distinguishable predictions. No independent confirmation is required for this.
2. **Evaluation:** Check against new development periods or an appropriate confirmation plan. Only then can the knowledge status increase.

This avoids a circular conclusion: New explanations may be proposed before their cause is known. At the same time, a subsequent declaration without verifiable consequences must not be regarded as a gain in knowledge.

Each revision records the trigger, discarded alternatives, expected new predictions, complexity costs and affected candidates. There is an explicit category `UNEXPLAINED` whose size is not interpreted as a complete measure of the unknown world.

## 8. Decision-sensitive uncertainty and research allocation

### 8.1 Decision relevance

An uncertainty is relevant when plausible different responses can change at least one permissible action: which area to examine, which attempt to perform, park a candidate, execute a strategy differently or not to act.

Uncertainties can affect parameter groups, model structures or measurement/execution errors. It is not necessary to fully identify each cause if all currently plausible models suggest the same resilient action.

### 8.2 Standard mode: explicit scenarios without invented probabilities

The first `ResearchAllocator` does not use claimed discovery probabilities. It shall:

1. removes inadmissible or non-executable experimental plans;
2. identifies possible, decision-changing outcome areas for each plan;
3. compares limitations, disturbances, expected effort and required data;
4. prefers within a research queue the more favorable sufficient experiment;
5. In the case of non-resolvable equals, use is made of a documented deterministic sequence or protocoled randomization.

The assessment is called `HEURISTIC` or `SCENARIO_BASED`, not EVSI. Scenarios show possible decision consequences, no hidden equal distribution as a supposedly data-free probability of success.

### 8.3 Optional probabilistic mode

An EVSI plugin requires a common probability model, an observational model for experimental results, a set of actions and benefits definition, and consistent costs. Then it can calculate the expected net information value:

\[
\mathrm{NEVSI}(e)=
\mathbb E_{y\mid D,e}\left[\max_a\mathbb E[U(a,\theta)\mid D,y,e]\right]
-\max_a\mathbb E[U(a,\theta)\mid D]-C(e).
\]

Research costs must be in the same utility/money units or taken into account with documented conversion rules. Costs may not be deducted simultaneously in `U` and again in `C(e)`.

EVPPI of a parameter group is an upper limit for the EVSI of an experiment about this group only under a corresponding information structure. If the test additionally informs other decision-relevant variables, this one-parameter threshold is not automatically valid. [^S3]

For multi-step research, the above one-step rule is only an approximation. The value of later experiments and newly possible actions must be taken into account separately in a more extensive model.

### 8.4 Budget protection for open and multicausal search

Allocation MUST distinguish at least three activities:

```text
REFINEMENT: Deepening existing promising hypotheses
INTERACTION: Consider well-founded configurations and cross-domain synergies
OPEN_DISCOVERY: Explanatory gaps and investigate new mechanisms/domain proposals
```

For `INTERACTION` and `OPEN_DISCOVERY`, a positive resource share or equivalent minimum budget is configured per campaign. The share is a conscious heuristic and is not output as optimal. The discussion did not set a numerical allocation. Set and expose it in configuration.

Budgets refer to resources, not just trial numbers. A GPU run and a small event study do not automatically count the same. If a queue does not contain permitted attempts, unused budget is redistributed only with a logged rule.

### 8.5 Bandits and Bayesian Optimization only as an interchangeable extension

UCB, Thompson Sampling or Bayesian Optimization MAY later support the choice between described domains. For this purpose, reward, delayed results, costs, non-stationary environment and model uncertainty must be specified.

The allocator selects among investigations. The `CandidateGenerator` still proposes candidates and domains. New domains require their own descriptions and integration rules. A high uncertainty value in a surrogate model guarantees neither unknown causes nor correctly calibrated epistemic uncertainty.

Internal validation results are allowed to control the allocator and are thus development information. Results of the protected external test are not a freely reusable bandit reward to optimize the same claimed evaluation.

## 9. Multiple causes and interaction discovery

### 9.1 Three strictly separate terms

1. **Statistical Interaction / Information Synergy:** common statistical information or non-additive model effect.
2. **Causal interaction:** An intervention-related effect on a defined effect scale depends on a further cause or condition.
3. **Economic added value:** the joint information improves a genuinely available decision based on costs and risks.

None of these terms may be automatically upgraded to another. PID, O-information and model attribution do not provide independent causal identification. [^S4][^S5][^S6][^S7]

### 9.2 Binding protection rules against overlooked synergies

- A weak marginal correlation, mutual information or transfer entropy is insufficient grounds for permanently removing a feature across all model families.
- Such a result may reduce the priority of a specific model family. The interaction channel and its origin data remain accessible.
- Models with “strong heredity”, which allow interactions only at existing main effects, are only an optional family, not the only search procedure.
- The candidate space must also allow interactions between domains, delayed interactions, and selected higher orders.
- A state x impulse scheme is a preferred search family, not an exclusive theory of all market mechanisms.

### 9.3 Three model families as a controlled comparison

| Family | Content | Purpose |
|---|---|---|
| `ADDITIVE_BASELINE` | Sufficiently flexible individual effects, joint time/regime controls, no explicit cross-terms. | Reference for additional interaction benefits. |
| `STRUCTURED_INTERACTION` | Small mechanistically based selection of cross terms, state dependencies and lags. | Economically limited search for synergy. |
| `OPEN_NONLINEAR` | Budgeted nonlinear model without a mandatory main effect gate. | Search outside of preformulated interactions. |

All models use the same decision time, the same target size, the same data roles and comparable tuning budgets. Different regularization, basic model under-adjustment or additional data must not be recorded unnoticed as an “interaction”.

A possible first comparison is:

\[
\Delta L=L_{\mathrm{additiv}}-L_{\mathrm{interaktiv}}.
\]

`L` is a pre-determined forecast loss measure. Its positive difference initially only proves better forecasts in the test in question. Common errors per day/episode and the same test observations shall be considered in the uncertainty.

In addition, when the strategy map is available, `delta_net_utility` is measured. An improved variance prognosis shall not be called an improved direction prognosis. MSE, log loss, distribution scores and trading benefits test different goals.

### 9.4 Catalog of methods: first small procedures, then optional plugins

| Procedures | Role | Requirement / Limit |
|---|---|---|
| Conditional Event Study | Initial assessment of event profiles, direction, lifetime and context. | observational comparison, not automatically causal. |
| Regularized cross-terms / condition-dependent models | First structured interaction models. | Interactions must be expressly generated or permitted. |
| Residual analysis/ablations | Investigate gaps in explanation and added value. | Ablation is not automatic intervention; observe correlated features. |
| ReliefF / suitable relief variants | Optional interaction-sensitive feature prioritization. | Select classification/regression variant appropriately; check neighborhood quality and dimension. [^S10] |
| Common/conditional MI, PID | Optional statistical information analysis. | Specify target, estimator, discretisation, uncertainty and PID definition. [^S4] |
| O-information | Optional analysis of multivariate dependency structure. | Without target reference, no proof of return information. [^S5] |
| NID / Integrated Hessians | Extract interaction candidates from already trained models. | Explain the model function, not automatically the market. [^S6][^S7] |
| Representation Learning | Learn helpful state representations. | Latent variables are not automatically independent or causally identified. [^S9] |
| Causal Discovery | Restricting competing causal structures. | Document assumptions, consolidation, time resolution and remaining equivalence class. [^S8] |
| Symbolic regression/genetic search | Limited generation of new functional candidates. | Own proof of selection, complexity limits and validation are required. |

The core research cycle must remain usable when optional plugins are unavailable. For an uninstalled plugin, return `UNSUPPORTED_CAPABILITY`.

### 9.5 Mathematical regression tests against errors from the dialog

**A. Zero correlation is not zero information.** For independent standard normal `X1`, `X2` and independent errors `epsilon ~ N(0, sigma²)` with `sigma² > 0`:

\[
Y=X_1X_2+\epsilon,\qquad
\operatorname{Cov}(X_1,Y)=0,\qquad
\operatorname{Var}(Y\mid X_1=x)=x^2+\sigma^2.
\]

Therefore, despite the lack of linear correlation, `X1` is not independent of `Y`. This fixture must not be labeled as true zero-MI synergy.

**B. Genuine discrete XOR.** For independent fair bits and `Y = XOR(X1, X2)`, the following applies:

\[
I(X_1;Y)=I(X_2;Y)=0,\qquad I((X_1,X_2);Y)=1\ \text{bit}.
\]

The values are calculated exactly from the four equally probable states, not from a noisy MI estimator.

**C. Rough representation does not provide an upper limit of information.** `Z = g(X)` applies:

\[
I(Y;X)=I(Y;Z)+I(Y;X\mid Z)\geq I(Y;Z).
\]

A weak coarse signal therefore does not prove that the complete data is uninformative. In the case of transfer entropy, changes in the conditioning set must be accounted for before transferring the inequality.

**D. Synergy minus redundancy is not pure synergy.** Under a corresponding bivariate PID applies:

\[
I(X_1;Y\mid X_2)-I(X_1;Y)=\mathrm{Synergy}-\mathrm{Redundancy}.
\]

The selected decomposition must be documented in the plugin. A positive difference value is not a clear causal synergy value. [^S4]

**E. Late nonlinear combinations remain possible.** Two initially separated paths `h1 = x1`, `h2 = x2` can interact later through `f = (h1 + h2)²`. The common input into the same first hidden neuron is not a universal necessary condition for neural interaction.

### 9.6 Asynchronous configurations

States can build up before an impulse. Every such hypothesis therefore names:

```text
state_observation_window
state_update_rule
state_max_age
impulse_window
lag_candidates
prediction_horizon
availability_lag
```

Decay constants, lookbacks and lag grids are development parameters with their own selection provenance. They are not readjusted after consideration of the confirmation window. Forward smoothing and retroactively available position data are not allowed.

A bipartite search over `p_Z * p_X` state/impulse pairs can be bounded, but still scales quadratically for similarly sized groups. It does not eliminate combinatorics in general.

## 10. Experimental design, data roles and evidence protection

### 10.1 Mandatory content of an experiment plan

A plan MUST answer at least before execution:

| Field | To be documented |
|---|---|
| `research_question` | Which decision should influence the investigation? |
| `hypothesis_versions` | Which specific candidates and alternatives are examined? |
| `estimand` | What effect or difference is estimated on which scale? |
| `target_spec` | Price definition, return/distribution target, horizon and timing. |
| `comparison` | baselines, control groups and relevant counter-hypotheses. |
| `data_spec` | Sources, time periods, instruments, snapshot and role. |
| `fit_scope` | Which transformations/models are learned where? |
| `dependence_spec` | Overlap, episodes, daily/instrument clusters and resampling. |
| `testing_spec` | Test family, error rate, interim analyses, stop rules or explicitly exploratory status. |
| `decision_rules` | Rules for support, refutation, further investigation and insufficient evidence. |
| `cost_and_budget` | caps on computing time, data, human effort and, where applicable, trade risk. |
| `failure_policy` | Procedure for data errors, non-convergence or insufficient sample. |

A non-significant result is not a confirmation of “no effect” without corresponding power/equivalence arguments.

### 10.2 Mandatory data roles

```text
DEVELOPMENT: exploration, partition design, feature and model selection, and triage
INNER_VALIDATION: Comparison and tuning within development
CONFIRMATION: Frozen candidate and pre-determined test
POLICY_EVALUATION: External examination of the entire search policy
PROSPECTIVE: new data arriving after the protocol starts
```

`INNER_VALIDATION` is explicitly part of the development. Roles apply to claims and lineage across file names. Derived features, summaries and reports read by humans also count as data usage.

A frozen batch of multiple confirmatory tests may use the same test data if this is covered by the predefined multiple test procedure. It is not necessarily necessary to have a separate data set for each hypothesis.

### 10.3 Temporal and grouped validation

For intraday data, chronological evaluation is the standard. The split module MUST take into account overlapping label intervals, asynchronous information and common event clusters.

- Training labels must not extend into a test period whose information was still unknown at the time of training.
- Purging is based on actual information/label intervals. An additional embargo requires a documented time justification.
- Combined market/liquidity shocks are not counted as many independent asset experiments.
- Millions of ticks are not an automatic guarantee of a high effective sample size.
- The treatment of temporal dependence depends on statistics and estimand. A universal `N_eff` for all tests is not accepted.
- Bootstraps, block permutations and other zero models must obtain the structure relevant to the respective zero hypothesis. Each method has its own assumptions.

A time split alone guarantees neither independence nor future stability. Older periods are allowed to become training data in a later walk-forward iteration after their predictions at that time were steadily evaluated. This does not legitimize a retroactively adjusted historical performance.

### 10.4 Multiple tests and repeated observation

Test families also include selected horizons, targets, event filters, models and relevant subgroups. The ledger counts and describes search decisions; it does not replace error control.

The first implementation SHOULD use a small, frozen test family with a documented error-control method suited to the confirmatory claim. Holm's procedure, for example, requires valid p-values. A valid correction cannot repair a misspecified time-series null model.

Online FDR, alpha investing, sequentially valid confidence procedures, reality check, SPA, DSR or PBO are optional, claim-specific tools. They are not installed as any interchangeable “overfitting correction”. DSR addresses specific distortions of Sharpe interpretations, not any adaptive causal search. [^S11]

Repeated checking and stopping at a favorable result is only allowed with pre-matched sequential rules. Otherwise, the result will remain exploratory.

### 10.5 Access and consumption protocol

For each access, `SelectionLedger` stores:

```text
who, when, data_snapshot, interval, instruments, role,
plan_id, derived_artifacts, purpose, selection_lineage,
result_visibility, subsequent_decision_refs
```

A successor candidate influenced by results inherits the relevant data usage of its predecessors. Renaming a feature, creating a new path or reloading the same data does not create a fresh holdout.

For protected evaluation, the search agent receives neither direct raw data access nor uncontrolled access to results generated therefrom. **A separately authorized evaluation environment is mandatory.** A mere Python flag in the same unrestricted agent process is not a robust access lock. The following sections replace the non-binding preference from version 1.0.


### 10.6 Enforced information barriers

**Safety invariant:** Until the planned release of results, no information from the protected evaluation results may flow back into hypothesis generation, feature development, model selection, parameter selection, budget allocation or prompt revision. Submission and administration channels must not circumvent this limit.

Three different problems have to be covered:

1. **Direct exposure:** The AI, its tool process or its generated code reads protected data, labels or reports.
2. **Indirect exposure:** The search learns from scores, rankings, errors, plots, caches, embeddings, other agents or summaries relayed by humans.
3. **Temporal leakage within the test:** The frozen strategy receives information at a simulated time that was not yet available at that time, even though the research AI itself never sees the test.

The architectural principle is minimal authorization with external enforcement points. Authentication and authorization must not be replaced by model responses or claimed roles. NIST and OWASP describe these security principles; the following concrete division is the project design. [^SEC1][^SEC2]

**Delimitation:** Access protection does not by itself guarantee independent samples, correct p-values or stationarity. Conversely, a clean time split does not replace access protection. Both requirements apply simultaneously.

### 10.7 Threat model and residual limits

Treat the research agent, its subagents, external text, candidate packages and generated code as untrusted relative to the protected zone. Cover accidental access, overly broad tool permissions, prompt injection and deliberate bypass attempts. The barrier must also hold if the agent explicitly tries to open the holdout.

The trusted base consists of approved platform configuration, identity/key management, admission logic, replay/scoring harness, and release logic. It must be small, versioned and administered separately. An LLM is not the policy enforcement point.

There is no guarantee of protection against a compromised host/cloud administrator, intentionally colluding privileged persons, all hardware or timing side channels or unknown sandbox/hypervisor gaps. Sandbox selection and hardening must take into account the real threat model; even strong sandboxes are not an absolute guarantee of security. [^SEC4]

Historical information already contained in model weights, previous conversations or human knowledge cannot be removed by subsequent file rights. Historical replay results with unknown prior exposure are marked accordingly. A new chat window does not prove independence. For more stringent temporal statements, a prospective test frozen before its outcomes occur should be provided.

### 10.8 Separate trust zones and identities

| Zone / Identity | Task and Permitted View | Prohibited powers |
|---|---|---|
| `research_principal` | Research, code proposals, `DEVELOPMENT` and `INNER_VALIDATION`, development reports. | Protected data storage, evaluation credentials, restricted logs, deployment or release rights. |
| `admission_principal` | Check candidate package, bind registered test slot, authorize run. | Open any new holdouts for the agent or change the test rules based on results. |
| `evaluator_principal` | The trusted harness reads the assigned snapshot, controls virtual time and calculates predefined metrics. | Unrestricted LLM or web access and uncontrolled feedback to the research agent. |
| `candidate_runtime_principal` | Run frozen model/strategy program; receive only permitted point-in-time messages. | Read full holdout, future events, immature labels, host files or evaluator credentials. |
| `release_principal` | Deliver released report to pre-registered recipients; record exposure. | Grant ongoing research access or request additional metrics ad hoc. |
| `security_admin` | Deploy independently approved infrastructure and policy changes and handle incidents. | Delegate this authority to `research_principal` or offer it as an autonomous research tool. |

Multiple research agents inherit the same data restrictions. Different model providers or model weights are not required. The same model type can be used in neatly segregated sessions; common contexts, memories, tools or credentials must not open forbidden channels of information. By default: **no LLM required in the protected evaluator**.

The operator can technically manage several roles in a small project. Then the credentials and working environments still have to remain separate. If the operator sees results and subsequently influences the search, record that exposure in the lineage. Software cannot completely prevent an intentionally privileged human return channel.

### 10.9 Technically enforceable rights

These requirements apply to any platform selected.

- Research and candidate runtimes must lack holdout read credentials, vault decryption keys and the authority to grant themselves either. Knowing file paths or object IDs is not enough for access.
- Protected storage is not mounted in the research environment. In addition, direct database, object store, backup and snapshot accesses are denied by the respective service. `read_only` for a protected record would not be a permitted research permission.
- No access to host root, `sudo`, container/hypervisor admin sockets, cluster administration, cloud metadata credentials or privileged CI secrets. A container with appropriate host/daemon access would not be a sufficient limit. [^SEC3]
- Authorization is decided outside agent-modifiable libraries based on authenticated identity, resource, operation, time, plan and test slot. Missing policies, unknown identities or failure of mandatory auditing requires a fail-closed denial.
- Research code may propose Enforcement/Evaluator code in the repository as a change. However, the running protected infrastructure uses a separately approved, immutable build. The agent can neither deploy it itself nor change its secrets, protection rules or result release policy.
- Network access of the protected zone and candidate sandbox is blocked by default; only required, predefined service connections are allowed. HTTP, DNS, cloud metadata and alternative outputs are part of the check. Disable dynamic package downloads during evaluation.
- During a blindly claimed historical evaluation, research tools must not retrieve blocked periods via market providers, web, connectors or alternative data mirrors. Freely available historical prior knowledge is thus not retroactively eliminated.
- Development and protected data get separate storage views, caches, search indices, vector stores, traces and backups. Role marking in the cache key is useful, and must be backed by storage authorization.
- Raw data, test labels, single trades, equity curves, fit artifacts from protected data, debug dumps and summaries generated from them initially inherit the protected status. Data origin is not erased by aggregation or renaming.
- Shared agent memory, automatic conversation summaries and global retrieval indices may not receive protected content. Telemetry providers and support exports are also part of the inventoried data flow.

**Minimum permitted deployment:** A development environment without test data and admin rights as well as a separately authorized evaluation environment with fixed harness; untrusted candidate code runs behind an additional sandbox/process boundary. Separate machines are not mandatory, but a mere other Python process with identical rights and freely readable common memory is not enough. For any native candidate code, a suitable hardened sandbox/VM solution must be selected. [^SEC4]

### 10.10 One-way submission of frozen candidates

```text
Research zone with development data
    -> immutable CandidateBundle
    -> authorized admission and binding to a registered evaluation slot
    -> Protected replay/scoring harness
         -> isolated candidate runtime with only timely available inputs
         <- predictions and actions
    -> Protected result store
    -> ResultReleaseGate
    -> approved one-time result release with exposure recorded
```

`CandidateBundle` SHALL contain at least:

```text
bundle_schema_version, bundle_digest, candidate_id, candidate_version,
lineage_root, parent_artifact_digests, research_policy_digest,
source_digest, dependency_lock_digest, runtime_image_digest,
model_artifact_digests, feature_spec_digest, event_spec_digest,
target_spec_digest, execution_spec_digest, risk_spec_digest,
training_provenance, learning_rule_digest_or_none,
registered_protocol_id, hypothesis_family_id, resource_limits
```

The `lineage_root`, protocol and data source fields claimed by the client are not authoritative. Admission compares it with the server-side registry and actual identity; freely selected IDs must not reset consumption or prior exposure.

A freeze also includes preprocessing, cost model, thresholds, seeds as relevant, execution rules and allowed online updates. The trusted admission checks the full content and certifies the bound version. A hash provided by the agent alone does not establish trust. Execute exactly the content verified at admission.

**Standard for the MVP:** Prefer Declarative feature/strategy plans with registered operators and suitable, non-executable model formats. No uncontrolled deserialization of executable objects, no custom import when loading protected data. An operator register must be outside the change authority of the research agent.

Required custom candidate code is executed only as an immutable package in the isolated candidate runtime. The candidate runtime receives neither the full holdout nor the label store. Static checks and LLM review cannot substitute for the runtime boundary.

### 10.11 Point-in-time isolation inside the evaluator

The trusted Harness manages the virtual clock. It only provides data to the candidate runtime whose `available_at` does not exceed the current allowed decision time. The candidate cannot advance the clock or request an arbitrary full historical data frame.

- Features are generated from authorized past views. Already fit transformations come from development; new fits in the test are only part of a previously fixed, causally executable learning rule.
- The scorer is allowed to know future paths and subsequent execution prices for the valuation. These rights are not passed on to the candidate. Model prediction and result evaluation do not share a freely readable memory.
- In the case of online learning, only already mature labels approved according to the protocol are handed over. Allowed updates, their time and state transfer between windows are predefined.
- Predictions, orders and model states are logged in a timely manner before the associated outcomes are used for the evaluation. Subsequently observed execution information must not alter previous actions.
- A backtester that passes the full test series to arbitrary strategy code fails this contract. Reuse is only allowed with a trusted streaming/replay adapter or correspondingly limited strategy execution.
- For `POLICY_EVALUATION`, the frozen search policy is allowed to learn within its approved inner development window. The external outcome data and policy scores remain hidden until the intended evaluation. Nesting does not automatically extend rights.

### 10.12 Holdout access, feedback and repetition

**Default `ONE_SHOT_BATCH`:** A registered scope receives a final, pre-frozen batch with a defined test family and a joint release of results. Several hypotheses contained in the batch are allowed, provided that their error control and joint evaluation are specified. A release is not a substitute for multiple test correction.

The default allows **one** autonomously submitted final batch per slot. This is a conservative technical operating rule of this MVP, not a general mathematical threshold. New slots require independent authorization and a data scope that is still allowed. A new candidate name or campaign ID does not create a new slot.

Pre-planned evaluation of several policies or candidates without intermediate feedback is possible. The entire test family must be determined before the first release. Adaptive access to intermediate results, on the other hand, requires a separate, formally based protocol and is not enabled in the MVP. Uncontrolled adaptive holdout use can itself lead to overfitting. [^S2]

`ExposureRegistry` manages slots on the server side across campaigns, agents and forks. Reservation and consumption are atomic. Relevant data intervals, instruments, known derivatives and exposure lines are taken into account; mere file hashes are not sufficient to detect overlapping market data.

Identical repetitions return the same Receipt reference. An infrastructure retry is only allowed for the exact same frozen content under the specified retry protocol; it does not create a new adaptive attempt. Errors after protected data contact are also counted internally. They must not serve as a free query channel.

### 10.13 ResultReleaseGate: No hidden research feedback

The research zone receives only a minimal receipt during the protected evaluation. No live updated metric, no best asset, no best time period, no preview of partial trades and no “improving feature X”. Also, a data-controlled pass/fail is already result information and remains withheld until the intended release.

The trusted scorer only generates predefined metrics. The candidate can neither inject their own metric functions nor any text fields into the report to be released. A structured scheme alone does not prevent encoded data outflows; in addition, the calculation, the recipients and the number of releases must be specified.

`ResultReleaseGate` MUST:

1. Verify plan, artifact, receiver, release time, slot and result format;
2. permanently and atomically register the exposure process before disclosure;
3. release only the metrics and decisions set out in the protocol;
4. keep raw technical logs, tracebacks, file contents, stdout/stderr, candidate artifacts and any debug fields in the protected area;
5. Reject partial queries, retrospective subgroups, alternative cost models and unplanned repetitions.

Preflight errors without protected data contact may be returned. Result-dependent errors, runtime details and progress indicators are not interactively disclosed before release; status queries must be minimized and time-bundled as needed. Complete freedom from all timing side channels is not claimed.

A released aggregated report remains a disclosure. Once used to adapt a candidate, subsequent candidates may not use the associated scope as untouched confirmation. The test initially frozen does not lose its validity retroactively due to its regular publication; the restriction concerns the further selection affected by it. A possible selection of the “best” candidate from a batch is additionally covered by its predefined evaluation.

### 10.14 Additional interfaces and security objects

The following contracts are server-side in C13–C15. A client may not authorize them by setting role parameters.

```text
AdmissionPort.preflight(bundle_digest, public_protocol_id) -> PreflightResult
SealedEvaluationPort.submit(bundle_digest, slot_id, idempotency_key) -> SubmissionReceipt
SealedEvaluationPort.receipt(receipt_id) -> SubmissionReceipt

# Only trusted services, not a freely available research tool:
EvaluationSlotStore.reserve(slot_id, verified_bundle_digest, verified_principal)
    -> BoundEvaluationTicket
PointInTimeBroker.next_frame(bound_ticket, candidate_instance) -> AuthorizedFrame
TrustedScorer.record_prediction(bound_ticket, prediction) -> InternalAck
TrustedScorer.finalize(bound_ticket) -> RestrictedReportRef
ResultReleasePort.release(release_request) -> ReleasedValidationReport
ExposureRegistry.record(event) -> DurableExposureReceipt
ExposureRegistry.check_eligibility(scope, lineage, recipient_history) -> EligibilityResult
```

`verified_principal` is derived from service authentication. `BoundEvaluationTicket` is short-lived, resistant to forgery and bound to identity, artifact digest, snapshot, protocol, operation, slot and usage limit. It authorizes the specified evaluation only. The candidate runtime does not receive any usable vault credentials.

| Object | Additional mandatory fields / rule |
|---|---|
| `DataScopeManifest` | Canonical scope, source snapshot, time/instrument coverage, known aliases/derivatives, developmental use, exposure status. |
| `PrincipalPolicy` | Authenticated identity, trust zone, allowed services/operations, denied stores, policy version. |
| `EvaluationSlot` | Scope, approved test family, release authority, submission/release limits, atomic state. |
| `SubmissionReceipt` | Opaque ID, package digest, allowed infrastructure status; no test metric and no data-driven outcome before release. |
| `RestrictedValidationReport` | Complete internally calculated result with sensitive evidence; only protected identities. |
| `ReleasePlan` | Predefined metrics, precision, receiver, timing, scope, handling of errors and budget. |
| `ExposureEvent` | Actual receiver including human/agent/tool, content scope, derivatives, timing, lineage, release reason. |
| `EligibilityResult` | `ELIGIBLE`, `EXPOSED`, `UNKNOWN` or `BLOCKED`, with scope-related justification. |
| `IsolationAttestation` | Tested deployment/policy version, negative access tests, environment, time, test instance; no substitute for ongoing enforcement. |

`UNKNOWN` is not synonymous with fresh. Confirmation claims with unknown relevant exposure shall be blocked or explicitly reclassified as non-independent exploration.

`EvidenceStore` is divided into development and restricted views. The research ledger may initially contain only opaque references for protected runs. The complete security/data access audit is separately authorized; a log entry may also contain protected information.

### 10.15 Exposure inheritance and incident management

Exposure concerns information, not just a file. Reports, feature rankings, decisions and selection justifications are linked to their scope and recipient group. Successors assume the relevant exposure of their inputs, decision history, and research contexts involved. A new model, git branch or agent name does not reset this status.

The technical lineage cannot prove every semantic influence. Therefore, conservative rules apply: Reuse of protected reports in a common research workspace makes the corresponding scope for later adaptive selection there consumed. Unclear origin is treated as `UNKNOWN`. Existing correlation/event groups complement byte-related derivative recognition; they do not demonstrate general statistical independence.

In case of undue exposure:

```text
Stop access and revoke credentials
    -> Identify affected data, recipients, sessions and derivatives
    -> Record exposure status in an immutable entry
    -> Suspend or downgrade downstream confirmation claims
    -> Fix the security failure and rerun the negative tests
    -> Use new permitted scope or prospective data for new confirmation
```

Deleting logs or sending a prompt “forget this data” does not restore independence. Already valid tests completed before the incident are considered separately; the scope of the incident must be identified.

### 10.16 Configuration and operational assumptions

Productive authorization, release limits and deployment releases are in a separately administered configuration. An agent-editable Research-YAML must not overwrite these values. The example below defines a proposed schema for future implementation.

```yaml
isolation:
  required_for_real_protected_data: true
  deny_by_default: true
  research_role_can_administer_evaluation: false
  candidate_runtime_can_read_full_holdout: false
  protected_zone_external_llm_calls: false
  separation_attestation_required: true

confirmation:
  mode: ONE_SHOT_BATCH
  final_batches_per_slot: 1
  result_releases_per_slot: 1
  interactive_metric_queries: false
  allow_unknown_exposure_status: false
  release_requires_registered_recipients: true

operations:
  immutable_evaluation_build: true
  audit_failure_policy: DENY_NEW_PROTECTED_ACCESS
  live_trading_enabled: false
```

If a tested isolation environment is missing, the application is allowed to work with synthetic data but must refuse true protected evaluation with `ISOLATION_NOT_VERIFIED`. A “Developer Mode” must not turn off this protection for real data.

A network failure after evaluation has already begun leads to a predefined safe stop/quarantine behavior, not to an unrecorded continuation with later return of results. Retention, encryption and backup permissions are also to be configured.

### 10.17 Migration of the existing framework

Before integrating real holdouts, Codex must create a concrete data flow and rights matrix within the framework of M0/M1-S. The inventory includes not only loaders, but also shell access, local records, `.env` files, CI secrets, Git history, notebooks, exports, trackers, vector stores, agent memory, provider logs, backups, network routes and alternative data sources.

Test data already read out or available in common work environments are not subsequently classified as guaranteed untouched. The migration shall investigate its actual use and potential exposure; `UNKNOWN` shall be set in case of uncertainty. Merely earlier accessibility does not yet prove an actual reading process, but does not allow any assurance of technical isolation without further evidence.

The result of the migration is a verifiable state: research identities cannot circumvent the protective boundary either directly or via their delegated tools; protected evaluations run exclusively via the registered services; the result return channel is limited. Security controls must be re-examined after changes to tools, roles, memory, runtime, networks or evaluator deployment.


## 11. From an anomaly to a tradable strategy

### 11.1 Mandatory handover package

The package produced by `StrategyHandoffBuilder` contains:

```text
anomaly_hypothesis_version
mechanism_configuration_versions
alternative_explanations_and_causal_status
feature_definitions_and_availability
entry_eligible_timestamp_rule
target_and_event_profile
estimated_effect_and_uncertainty
supported_scope_and_failure_regimes
execution_assumptions_and_fidelity
remaining_alpha_by_latency
cost_capacity_and_risk_envelope
evidence_and_selection_lineage
candidate_actions_and_invalidations
unused_validation_data_or_prospective_plan
```

No package contains a claim of independent validation if its data has already been used to develop the relevant strategy.

### 11.2 Small, predeclared strategy set

Few economically justified alternatives are derived from the anomaly, such as immediate aggressive entry, confirmed entry, passive entry and non-action.

The strategy decision includes regime filters, direction, timing, order type, exit, position size and risk limitation. Interactive decisions are evaluated together. An entry must not be described as optimal in isolation, if its advantage only results from a matching exit or fill mechanism.

### 11.3 Real execution is part of the hypothesis

For passive entry, condition the relevant return on actual fills. Model fill probability and subsequent returns jointly when fills depend on the price path.

Partial fillings, queue position, order cancellation, maker/taker costs, latency, market impact and unexecuted opportunities are modeled where necessary. An assumed full execution with a mere limit touch is not a standard.

Reports shall be separated as a minimum:

- Result per identified opportunity including non-action/non-fill;
- Result per executed trade;
- earnings per calendar time and capital employed;
- Risk, capacity and total costs.

Non-fills can have zero trading PnL but still incur resource or order costs. The execution model must explicitly state this convention.

### 11.4 Independent validation after strategy design

Anomaly validation does not replace strategy validation. Execution, entry/exit selection and size rules create new degrees of freedom. Accordingly, the frozen strategy requires its own new or still protected test in the higher-level protocol.

A lack of high-precision execution simulation does not block all anomaly research. However, it limits the economic knowledge status and prevents unjustified production release.

## 12. Evaluation of the full research policy

`PolicyEvaluator` does not only test the best candidate found. Complete search histories are compared, including costs, failed attempts, discarded candidates, and non-action.

### 12.1 Comparative framework

At least one simple reference policy shall be provided, such as a fixed, small event/feature screening with an identical data and computing budget. In addition, `NO_RESEARCH / NO_TRADE` is an economic reference where appropriate.

For the first implementation, synthetic tasks and historical, time-ordered replay campaigns are sufficient. Prospective comparisons are the later addition. Label simulated execution explicitly.

### 12.2 Measurements

The primary measure is the comparable economic value of decisions after trading and research costs, where measurable. Otherwise, report a named research outcome separately from realized trading value.

Secondary: resource requirements, time to a robust decision, confirmed false discoveries, stability, capacity, uncertainty, and stop and recovery behavior. The mere number of significant hypotheses is not a primary criterion of quality.

### 12.3 Independence of the policy comparison

Policy code, budget rules and evaluation protocol are fixed before the external test. The policy may act adaptively within its frozen learning rule. Subsequent human code/prompt changes, on the other hand, generate a new policy version.

The selection of many policies optimized on the same benchmark is itself development. For a confirmation claim, a new external evaluation is then required. There is no need for unlimited meta-validation recourse; limit the claim to the version actually frozen and its tested conditions.

The relative performance of two methods can be studied without knowing the globally best undiscovered alpha. Statements about all possible anomalies or all future markets are not derived from this.

Historical replay also requires a documented approximation of the market reaction. In the event of a significant market impact of its own, the same historical price series cannot apply unchanged for each hypothetical action.

---

## 13. Rejected or corrected approaches

This table documents dead ends from the entire dialogue. The methods themselves are not generally prohibited; in each case the named claim or use as a mandatory gate is discarded.

| Rejected / Corrected | Why | Specification for implementation |
|---|---|---|
| Test any number of rules and choose the highest backtest Sharpe ratio. | Mixes search, selection and confirmation. | Limited experiments, lineage and external testing. |
| Rigid, just shrinking filter cascade. | New explanations and revised assumptions can make excluded options relevant again. | Support parking, resumption and model revision. |
| Completely literature-free or fully developed cause space. | Data choice and model architecture also contain assumptions; completeness is not a proven state here. | Make sources and limitations visible; use literature as revisable information. |
| Every return requires an irrationally losing counterparty. | Mixes absolute return, risk/liquidity remuneration and relative trading benefits. | Examine financial costs, goals and frictions, not invent a necessary loser. |
| Only transactions cause quota/price changes. | Quotes may also change through cancellation. [^S1] | Fully consider order book events according to existing data capability. |
| Frictionless does not mean any predictable return. | Arbitrage freedom is not the same as constant or vanishing expected return. | Friction is a search clue, not a universal condition of existence. |
| New causes must fit into the existing taxonomy. | Excludes unknown mechanisms by definition. | Allow provisional new categories and relationships. |
| Uncertain disturbances inevitably make experiments worthless. | The separation sharpness depends on the observation model, not only on the variance of an interference parameter. | Examine observational models and possible decisions. |
| EVSI/EVPPI values without a probability and benefit model. | Expected values require corresponding assumptions. | Scenario mode clearly separated from probabilistic evaluation. [^S3] |
| Low marginal MI/transfer tropy excludes a subspace. | Common and contextual information can be preserved. | No final general margin filter. |
| Rough MI is an upper information limit. | Deterministic compression can lose information. | Section 9.5C as a regression test. |
| `Y = X1*X2 + epsilon` for centered Gaussian variables is automatically zero-MI synergy. | Conditional variance depends on the single variable. | Separate correlation, information and target terms. |
| All synergies need recognizable main effects. | Real XOR refutes that. | Interaction path without main effect prerequisite. |
| VAE/ICA states, PID, O-information or neural attribution automatically identify causes. | Statistical representation and model interpretation do not provide a general causal guarantee. | Separate axes of evidence and identification assumptions. [^S4][^S5][^S7][^S9] |
| Causal discovery always requires complete observation of all causes and always provides a DAG. | There are methods with latent consolidation and partial orientation. | Respect results structure and assumptions of the respective plugin. [^S8] |
| NID captures a universally necessary first-layer structure. | Non-linear merging can take place later. | Document architectural dependence and model boundaries. |
| Relief, neural networks or a bipartite cut generally solve the combinatorics. | They use structure assumptions and have their own blind spots. | Maintain benchmarks, budgets and open control search. |
| UCB/Bayesian Optimization automatically generates new cause classes. | Budget allocation and domain creation are different tasks. | Separate generator and allocator interfaces. |
| More ticks / more assets are automatically more independent evidence. | Temporal and common shocks limit the growth of information. | Model dependencies and episode/asset groups. |
| Counting tested hypotheses and calculating DSR is sufficient for all selection. | No universal procedure for any adaptive question. | Use claims-specific statistics and new data. [^S11] |
| A holdout in the other folder is independent. | Data usage follows information and ancestry, not file names. | Track consumption and derivatives. [^S2] |
| A prompt or a second agent with the same rights protects the holdout. | Role descriptions do not prevent actual access. | Externally enforced rights and separate contexts/tools according to 10.6–10.17. |
| The evaluator may execute any generated code with the entire test data set. | This code could use future/labels or output data. | Separate candidate runtime from the full dataset and scorer. |
| Any number of aggregated scores or pass/fail responses is not a leakage. | Result feedback can align adaptive selection to the holdout. | Frozen batch, registered slots and controlled results release. |
| New session, new file hash or new campaign makes exposed data fresh again. | Prior knowledge and derived selection are retained. | Continue information and receiver lineage; no automatic resets. |
| Good prognosis score, high entropy reduction or causal graph are already alpha. | Feasibility, cost, risk and time availability are missing. | Independent economic and strategic audit. |
| Trade advantage must be fully causally identified. | Economic forecasts and scientific causal claims are different goals. | No invented causality; passing on predictions with their real status. |
| A single successful search proves a good search procedure. | Success selection and research costs remain unvalued. | Evaluate entire policy against relevant baselines. |

## 14. Technical details and edge cases

### 14.1 Time, availability and data quality

**Mandatory time stamp:** `event_time`, `available_at` and, where appropriate, `ingested_at`. All calculations use a unique UTC time base with sufficient resolution. Exchange calendars, time zones and daylight savings time are handled by the existing calendar logic, not by a fixed UTC offset.

The time usable for a trade results from the actual availability of information plus processing/routing assumptions. A retrospectively corrected message or position estimate must not appear to be known at that time with its original event date.

The following shall also be treated:

| marginal case | Necessary behaviour |
|---|---|
| Missing L2-/L3-data | Mark Depth/Queue dependent claims as unsupported; no reconstruction without marking. |
| Missing messages | Not to be interpreted as “no information on the market”. |
| Dealer positioning only as a proxy | Store estimation model, publish latency, and uncertainty; claim no observed forced flow. |
| Stale quotes / asynchronous assets | Define maximum age and as-of-join rule; no values filled backwards from the future. |
| Data gaps / sequence jumps in the order book | Affected reconstructions are blocked or explicitly downgraded. |
| Trading Interruption / Auction / Locked-Crossed Book | Event-specific treatment instead of normal continuous execution. |
| Futures Roll / Corporate Actions / Delistings | Point-in-time instrument stem and consistent label/price treatment. |
| Different units | Tick, piece, contract multiplier, notional, currency and basis points convert explicitly. |
| Lack of cost or risk values | No automatic net positive or release result. |
| Rare common conditions | `INSUFFICIENT_DATA` or broad uncertainty, not “interaction does not exist”. |
| Lack of joint support | Limit comparison/causal statement to observable range; no hidden extrapolation. |
| Different mechanisms with the same observable behavior | Equivalence class; not an artificially clear explanation. |
| Regime change / drift | Predefined monitoring; versioning new evidence; no retroactive redefinition of the measure of success. |

### 14.2 State machines

**Campaign:**

```text
DRAFT -> CONFIGURED -> RUNNING
RUNNING -> PAUSED | COMPLETED | STOPPED_BUDGET | STOPPED_DATA | FAILED
PAUSED -> RUNNING (only with logged reason and unchanged history)
```

**Experiment:**

```text
DRAFT -> FROZEN -> RESERVED -> RUNNING -> COMPLETED | FAILED | ABORTED
```

**Candidate:**

```text
PROPOSED -> ACTIVE | PARKED | REJECTED_WITHIN_SCOPE
ACTIVE -> READY_FOR_CONFIRMATION | PARKED | REJECTED_WITHIN_SCOPE | INCONCLUSIVE
READY_FOR_CONFIRMATION -> CONFIRMED_WITHIN_SCOPE | REJECTED_WITHIN_SCOPE |
                          INCONCLUSIVE | PARKED
```

A resumption or substantive revision creates a new candidate version in the status `PROPOSED` with reference to the old decision. After a negative or unclear confirmatory test, no silent relapse is allowed to adjust the same frozen candidate. `CONFIRMED_WITHIN_SCOPE` relates to the claim defined in the test, not automatically all axes of evidence and not automatically production.

### 14.3 Persistence, parallelism and costs

- The ledger is append-only; registry snapshots can be reconstructed from it or from linked versions.
- Experimental plans and artifacts receive stable IDs and hashes; identical content must be recognizable.
- Give each run an idempotency key. Restarting a run must preserve a single evidence record and avoid counting the same success twice. Actual re-executions get distinct `attempt_id` entries and record the extra cost. Reconcile an unknown job state before rerunning.
- Budget is reserved nuclear before the start of the job and compared with actual costs after the end. Aborted and failed attempts count with their real costs.
- Parallel agents must not use the same holdout uncontrollably for successive adaptive hypotheses. Releases require atomic, agent and campaign valid slots and exposure testing under 10.12; local in-process locks alone are not enough.
- Cache keys include data role, snapshot, fit scope, code/feature version, and configuration. A cache must not circumvent role separation.
- Shared data acquisition and infrastructure costs are allocated in the policy comparison according to a predefined rule.
- Data protection, deletion and retention are based on the project; sensitive raw content should not be reproduced unnecessarily in immutable logs.

### 14.4 Role of an LLM/Codex agent

The agent is allowed to generate suggestions, plan experiments and comment on approved results. It receives no administrator/deployment rights over the protection infrastructure, no protected storage credentials and no unreleased evaluation reports. The technical rights under 10.6–10.17 also apply to its shells, sub-agents, tools, caches and persistent memories. It must not store returns generated from text as measured values, must not independently raise an evidence level without a gate and must not trigger live orders based on a research result alone.

Prompts, model/tool versions, sources and relevant answers are part of the provenance. In the case of non-deterministic model responses, the result actually used is stored; a seed alone does not guarantee the reproducibility of external services.

External texts and model responses are untrusted input. External text and model responses have no authority to change access rights or trigger code, shell commands or data purchases. Executable experiment code requires sandbox, resource limits, and defined sharing.

Historical research replays with today's language models may contain later information. This limit must be included in the policy report. A clean prospective test cannot be replaced by retroactive rewriting of a historical prompt.

### 14.5 Minimum operating algorithm

```text
step(campaign):
    verify_configuration_and_capabilities()
    load_versioned_state()
    proposals = generate_or_load_candidates(DEVELOPMENT_only)
    assess_economic_scope_and_research_uncertainties(proposals)
    plans = create_decision_relevant_experiment_drafts()
    allocation = choose_under_budget_and_exploration_rules(plans)
    if no_valid_plan:
        record_reason_and_stop_or_park()
    else:
        frozen = freeze_plan_and_decision_rules(allocation.plan)
        reservation = reserve_budget_atomically(frozen)
        handles = authorize_data_access(frozen)
        result = execute_with_existing_framework(frozen, handles)
        append_run_costs_evidence_and_accesses(result)
        decision = apply_predeclared_rules_or_mark_exploratory(result)
        update_versioned_candidates_and_revision_proposals(decision)
        emit_research_report()
```

This pseudocode applies to the internal development cycle. For real protected evaluation, the research process ends at `SealedEvaluationPort.submit(...)`; it does not run `authorize_data_access` or the protected run itself. Only the evaluation service processes protected data. Processing of results in the research process takes place only after authorized approval and with updated exposure lineage.

Authorization may also fail after budget reservation; then the reservation is released and the error logged. After a process termination, the orchestrator must determine which steps have actually taken place on the basis of the ledger.

## 15. Technical dependencies and configuration

### 15.1 Mandatory capabilities, not a mandatory new platform

Structured schemes with validation, basic numerical/statistical functions, versionable data/model artifacts, a test framework, time-correct data selection and persistent research protocols are required.

Additionally required for true protected evaluation: independent runtime/service identities, server/operating system-side storage authorization, locked unauthorized network paths, secure key management, suitable isolated candidate runtime, immutably referenced builds, and an authorized release and audit path. Verify cryptographic digests against a trusted, approved reference. Specific operating system/cloud/sandbox products shall be selected and versioned according to M0; this specification does not require a new orchestration platform.

For an existing Python project, for example, already used NumPy/SciPy, DataFrame and ML libraries come into consideration. This is not an instruction to rebuild another stack on Python or introduce parallel libraries.

Codex MUST check existing dependency locks, Python/compiler versions and test conventions first. Package versions are set in the actual repository. This document does not claim any specific, already compatible versions.

### 15.2 Optional dependencies

Neural networks, Gaussian processes, causal detection, relief variants, PID and Bayesian optimization are integrated exclusively via optional plugins. The method selection follows a demonstrable research question and a baseline comparison.

GPU, graph database, vector store, distributed worker and external LLM service are not mandatory for the MVP. An existing experiment tracker and artifact memory SHOULD be reused.

### 15.3 Mandatory configuration before real research

| Area | Setting Before the First Real Run |
|---|---|
| Scope | Instruments, venues, calendars, data sources, permitted horizons. |
| Timing | Availability model, maximum data age, latencies, event/label limits. |
| Economics | Units, cost model, risk budget, capacity and minimum requirements. |
| Search | Generators, interaction orders, permitted model families, exploration budget. |
| Statistics | Data roles, test families, error rates/intervals, dependency model, stop rules. |
| Resources | CPU/GPU/memory/cost limits, maximum runs, human releases. |
| Governance | Responsibilities, holdout access, logging, live trading disabled by default. |
| Isolation | Trust zones, authenticated principals, memory views, sandbox, network policy, protected deployments and successfully tested isolation version. |
| Release of results | Registered recipients, test slots, submission/release budget, allowed metrics, exposure inheritance and incident behavior. |

No blanket “optimal” lookbacks, alpha horizons, stop-loss values, fees or probabilities of success are taken from the chat.

## 16. Implementation roadmap for Codex

### M0. Take inventory and create integration map

**Deliverable.** Assignment of all ports to real modules, existing test base, data capabilities and documented gaps. In addition, complete data flow/rights matrix from 10.17 and classification of existing test data as permitted, exposed or unknown. Do not change productive trading logic.

**Acceptance.** Each logical contract from Section 3 has a real owner or a specified adapter. Run the existing regression tests and record the results.

### M1. Schemas, ledgers, data roles and budget protection

**Deliverable.** Versioned core objects, access protocol, experiment freeze, role testing, idempotency, and budget reservation. A synthetic data adapter suffices.

**Acceptance.** Pass tests T01, T02, T03, T04, T05, T06, T20 and T21. Invalid or missing production configuration leads to controlled discontinuation.

### M1-S. Technical isolation and sealed evaluation

**Deliverable.** C13–C15 with separate identities and memory views, immutable candidate handover, external admission, isolated point-in-time candidate runtime, protected scorer, atomic slots, release gate and exposure inheritance. Existing backtest logic is reused only within these limits. The enforcement components cannot be deactivated or deployed by the research agent itself.

**Acceptance.** Implement and execute SEC01–SEC24 in an actual isolated test environment containing synthetic secrets. Pure mock tests are not enough for file system, network, credential and process boundaries. The deployed policy/runtime version matches the tested one. A lack of infrastructure indicates `ISOLATION_NOT_VERIFIED`.

**Order:** M2–M5 may initially be further developed synthetically. Genuine protected data may only be integrated after M1-S acceptance has been passed. An agent may propose security code; privileged deployment and release are separate.

### M2. A complete small research cycle

**Deliverable.** Rule-based mechanism generator, scenario-based opportunity model, uncertainty analysis, transparent allocator and event study executor. At least one rival explanatory model and the decisions `PARK`, `NO_CANDIDATE` and recovery are executable.

**Acceptance.** A synthetic campaign runs from the candidate to a reasoned result and generates a reproducible report. Pass tests T07, T08, T17, T18 and T22. No causality or trade claim is automatically upgraded.

### M3. Interaction path and configuration revision

**Deliverable.** Additive baseline, small structured interaction model, a budgeted open interaction path, and versioned grammar revision. No large neural model is absolutely necessary.

**Acceptance.** Pass tests T09 to T14 and T23. True XOR synergies are not excluded in the intended simple fixture by marginal screening. Higher order and asynchronous configurations are supported as data objects; discovery guarantees are not claimed.

### M4. Connect existing backtester and strategy registry

**Deliverable.** Cost/execution adapter, net benefit assessment, action `NO_TRADE` and complete anomaly handover package. Separate validation plan for strategies developed from it.

**Acceptance.** Pass tests T15, T16, T19 and T24. Live trading remains deactivated. Anomaly and strategy validation are distinguishable.

### M5. Outer policy evaluation

**Deliverable.** Repeatable synthetic benchmarks, chronological replay campaigns and at least one simple comparison policy. Costs and failed attempts are part of the evaluation.

**Acceptance.** Pass tests T25 to T28. Limitations of historical execution and transferability are also reported. No automatic claim of universal superiority.

### M6. Selectively supplementing optional methods

Only after M1 to M5 will EVSI, Bandits, Causal Discovery, Relief, PID/O Information, NID, Integrated Hessians or comprehensive representation learning be supplemented on the basis of concrete bottlenecks.

Each plugin requires a contract test, at least one synthetic task with a known mechanism, a null case, documented prerequisites and a benefit/cost comparison against the simple basic path. A method is not built in alone, because it was mentioned in the conversation.

### Implementation discipline

Per milestone: first record expected behavior as tests, test failing tests, implement minimal integration, run existing and new tests, and only then mark the milestone as completed. No complete framework rebuild before a end-to-end slice works.

Concrete file paths, test commands and commit limits are derived from the actual project after M0. Changed public interfaces require migration indication and backward compatibility check.

## 17. Mandatory test matrix

The following are acceptance tests to implement. Use deterministic fixtures for quick contract and unit tests. Run statistical Monte Carlo benchmarks separately with predefined seeds, replications and tolerances.

| ID | Case or fixture | Expected behavior |
|---|---|---|
| T01 | An event occurs at 10:00 and becomes available at 10:00:02. The decision is at 10:00:01. | The feature snapshot excludes the event. |
| T02 | An attempt is made to fit normalization, quantiles or embeddings on `CONFIRMATION`. | Return `ROLE_ACCESS_DENIED` and create no fit artifacts. |
| T03 | A period previously used for selection is offered as a holdout under a new path. | Detect matching snapshot or lineage and return `HOLDOUT_ALREADY_EXPOSED`. |
| T04 | A hypothesis, horizon or threshold changes after the plan is frozen. | Preserve the original hash and require a new version and evaluation authorization. |
| T05 | Two workers simultaneously try to reserve the remaining budget. | Grant only the permitted reservation and stay within budget. |
| T06 | The same completed run is restarted. | Reference the existing result without duplicating evidence or cost entries. |
| T07 | Even the best allowable effect under minimum costs is provably too small. | Return `ROBUSTLY_INFEASIBLE_WITHIN_SCOPE` with scope and supporting calculation. |
| T08 | A few scenarios are unfavorable and the parameter region or execution model leaves untested possibilities. | Return `UNRESOLVED` or a scenario-specific finding and leave broader exclusion open. |
| T09 | Use an exact XOR truth table with four equally weighted states. | Marginal MI is 0 and joint MI is 1 bit within tolerance `1e-12`. Features stay available for interaction discovery. |
| T10 | Use the Gaussian product model from section 9.5A. | Verify zero covariance and conditional variance `x² + sigma²`. Label the fixture as nonzero marginal MI. |
| T11 | A latent common cause produces strong observable correlation. | A good forecast alone must leave `causal_evidence` below `IDENTIFIED_WITHIN_ASSUMPTIONS`. |
| T12 | Use additive data without a true interaction. | Require the predeclared external comparison before preferring the interaction model. |
| T13 | A state builds from past data and has an effect only with a later impulse. | Permit lag and state features available at decision time and reject smoothing with future state. |
| T14 | Individual main effects carry no information and a simple joint configuration predicts perfectly. | The configured interaction path can test the fixture without a universal upstream marginal filter. |
| T15 | Limit orders fill disproportionately before negative subsequent returns. | Evaluate fill-conditioned outcomes and exclude favorable unfilled paths from earned PnL. |
| T16 | Execution prices already reflect the spread and there is an explicit fee field. | Count the spread and fees exactly once. |
| T17 | Exploration finds an interesting unexplained pattern. | Record a hypothesis or explanatory gap without asserting causality or forcing it into the old taxonomy. |
| T18 | Costs change after a candidate is parked. | Reopen it as a new version linked to the trigger and earlier decision. |
| T19 | A decline in flow can be confirmed only after part of the rebound. | Start labels and trading PnL at the entry implied by actual availability and latency. |
| T20 | A training label overlaps a protected test period. | Purge the affected observation under the protocol or reject the split. |
| T21 | A job fails after consuming resources or accessing data. | Retain the cost and access records and distinguish failure from negative anomaly evidence. |
| T22 | Refinement consistently scores highly while other queues have eligible candidates. | Preserve the configured resources for interaction and open discovery. |
| T23 | A provisional new cause makes no new testable prediction. | Leave the revision unproven or defer it. |
| T24 | A positive anomaly finding is followed by a new choice of entry and exit. | Give the strategy its own selection lineage and require an independent test still eligible for that purpose. |
| T25 | Only the successful half of the research runs are submitted for policy evaluation. | Detect missing campaign or run coverage and mark the comparison incomplete. |
| T26 | The policy changes after someone inspects the outer test. | Create a new policy version and disallow the same outer test as independent confirmation of that version. |
| T27 | Repeat synthetic campaigns on pure noise. | Report the false discovery rate with uncertainty and compare it with pre-calibrated bounds. |
| T28 | Two policies have identical gross outcomes but different research and execution costs. | Count both types of cost exactly once and apply the same capital and risk conventions. |

### Security acceptance SEC01–SEC24

These tests are mandatory in addition to T01–T28. They check the deployed isolation with only synthetic Vault data. A successful unit test for a role function does not replace a negative access test from the real agent process. These tests define future acceptance evidence.

| ID | Attack or failure case | Acceptance criterion |
|---|---|---|
| SEC01 | The research process attempts to read the vault through a direct path, alternate mount, symlink or backup. | OS or storage permissions deny access. The process receives no raw data. |
| SEC02 | The agent removes its local guard and sends `role=evaluator` or forged requester fields. | Service-side authorization still applies and the payload grants no privileges. |
| SEC03 | The agent requests the same data scope through SQL, object storage or a known alias. | Protected reads are denied while authorized development data remain available. |
| SEC04 | The agent searches for admin keys, `.env` secrets, CI tokens, the Docker socket, host root or cloud metadata credentials. | The actual deployment exposes no usable path to evaluation or deployment privileges. |
| SEC05 | The candidate attempts unauthorized HTTP, DNS or other egress during evaluation. | The network policy denies egress and allows only explicitly required internal connections. |
| SEC06 | The candidate or evaluator attempts an unplanned external LLM or tool call. | Credentials and network routes are unavailable, so protected data stay in the zone. |
| SEC07 | The agent searches memory, retrieval, trackers, caches, traces or shared artifacts for test content. | Authorized development views expose neither protected content nor its derivatives. |
| SEC08 | A bundle, model, dependency or runtime is swapped after admission. | Digest or attestation verification fails and execution is denied. |
| SEC09 | The candidate requests labels, future quotes or the full test data frame. | No such handle exists. The broker supplies only authorized inputs available at the current simulated time. |
| SEC10 | A malicious model format or strategy plan attempts code execution on load. | Reject it or process it solely inside the candidate sandbox. The privileged scorer never executes it. |
| SEC11 | Candidate output includes synthetic secrets in stdout, stderr, a traceback or result text. | Keep the output restricted. Receipts and released reports exclude it. |
| SEC12 | The agent repeatedly requests partial metrics, data-dependent errors or fine-grained progress. | The only available response is the minimal infrastructure receipt defined by policy. |
| SEC13 | Multiple agents or campaigns race for the last test slot. | Grant at most one reservation and prevent bypass through renamed candidates or forks. |
| SEC14 | The same or a modified submission is resent after timeout. | The same frozen content references the existing run. Modified content requires new authorization. |
| SEC15 | The agent requests early release, an extra metric, an unplanned subgroup or an unauthorized recipient. | Return `RESULT_RELEASE_DENIED`. Only the registered release plan can run. |
| SEC16 | A final report is released, then features or thresholds change. | The descendant inherits the exposure and cannot claim the same scope as untouched confirmation. |
| SEC17 | Exposed data are renamed, snapshotted again or registered under a known vendor alias. | Scope, derivative and exposure checks detect known overlaps. Unknown provenance stays blocked from automatic release. |
| SEC18 | The agent edits security YAML, evaluator code or CI definitions in the research workspace. | Deployed enforcement stays unchanged. The agent cannot sign or run privileged deployment. |
| SEC19 | Authorization or mandatory audit fails before new protected access. | Fail closed before data access or result release. |
| SEC20 | Simulate unauthorized exposure and submit a downstream candidate. | The incident workflow blocks affected claims and scopes and requires renewed review. Resetting the session cannot clear the exposure. |
| SEC21 | Configuration is incomplete, exposure is unknown or isolation lacks attestation. | Deny real protected evaluation and allow only explicitly labeled synthetic development for that path. |
| SEC22 | A candidate tampers with virtual time or uses immature labels for online updates. | The harness or broker denies the attempt. Only the frozen rule can learn from available labels. |
| SEC23 | A normal synthetic campaign completes freeze, replay, scoring and an authorized release. | Verify correct metrics, logged costs and exposure recorded before release. Raw data stay inside the boundary. |
| SEC24 | The research agent tries to retrieve restricted historical periods through alternative tools or sources. | The approved tool and network policy blocks retrieval. Report unknown prior model knowledge as a limitation. |

Recheck active read and write privileges, network rules and effective process identity against the approved matrix after each relevant infrastructure change. A canary verifies a specific access or leakage path. Encoded and hardware side channels require separate evidence.


### Additional Optional Plugin Testing

When integrating a corresponding plugin, the following are further tested: late neural merging from Section 9.5E; non-target negative O information; complete lack of neighborhood quality; constant features; insufficient common state coverage; incorrectly specified PID/CI estimators; drift and missing causal assumptions.

In these cases, a plugin may provide a justified non-statement. A forced numerical result is not a quality feature.

## 18. Worked example: intraday liquidity shock

This implementation example uses a hypothetical trading setup.

### 18.1 Initial hypotheses

- `H_reversal`. A strong sell impulse in a shallow book partly reverses after selling pressure eases and liquidity returns.
- `H_persistence`. The same initial move can continue if information or order flow persists.
- `H_artifact`. The apparent rebound partly reflects how trade prices or quotes were measured or timestamps were aligned.

Features cover aggressive buys and sells, quote changes and cancellations, depth, spread, the market context and information proxies available at decision time. Unobserved news remains a possible explanation.

### 18.2 Decision-relevant uncertainty

Is enough of the move left after stabilization becomes observable? Does it appear in suitable midquote targets and matched controls? Would combining the impulse, depth and easing pressure change the decision compared with a simple price-decline filter?

### 18.3 First experiment

The `ExperimentPlanner` specifies event rules, comparison groups, target horizons, clusters and cost scenarios for a development event study. Timestamp the event when the complete condition is first detectable. The low identified in hindsight is a separate observation.

Compare an additive baseline, a structured interaction and a bounded alternative interaction path. Report profiles over time with dispersion and adverse paths alongside the mean.

### 18.4 Possible decisions

- Reject the specific finding or classify it as an artifact if it disappears after fixing the price or timestamp specification.
- Record a scope-specific economic exclusion if the predictive effect is too small under every justified available execution option.
- Propose a replay or execution study if costs or fill selection could change the decision.
- Advance a robust decision with a limited causal claim if the mechanism remains ambiguous.
- Form a new hypothesis or provisional grammar revision if unexplained subgroups recur.

### 18.5 Confirmation and strategy discovery

Freeze the event definition, features, target, scope and test rule before confirmation on protected data. The handoff then specifies a small action set, such as immediate entry, entry after confirmation, passive entry or no trade. Further selection or optimization within that set counts as development.

A run that returns a justified `NO_TRADE` meets the technical objective. Software acceptance is independent of backtest profitability.

## 19. Definition of Done and handover report

### 19.1 MVP acceptance

The MVP shall be considered as implemented when M0, M1, M1-S and M2 to M5 are completed with documented tests and:

- a complete research cycle runs over the genuine project adapters or clearly labelled synthetic adapters;
- all mandatory tests T01 to T28 and SEC01 to SEC24 are in place and their actual results have been documented; safety limits are not only tested with mocks;
- a test report distinguishes between unit/contract tests and statistical benchmarks;
- data source, assumptions, selection line and evidentiary status are available for each key finding;
- final confirmation data, immature labels and unreleased results are technically sealed off from research agents and untrusted candidate code;
- research principals lack authority to administer the protected infrastructure or change its result release rules;
- approved result releases and consequent exposure inheritance have been demonstrated to work;
- the schema admits multiple causes and new classes of explanation;
- reports keep missing data, execution errors and forecast success separate from causal and economic evidence;
- existing functionality demonstrably continues and no live activation took place.

Empirical profitability requires a separate research finding after software acceptance.

### 19.2 Final report to be provided by Codex

Specifically, the report mentions: modified files, newly introduced contracts, reused components, schema/configuration migrations, executed test commands and results, sample campaign, remaining capability gaps, deviating architectural decisions, and as yet unimplemented optional plugins. Additionally: actual trust zones, effective identities/rights, dataflow matrix, tested sandbox/policy/build versions, result release rules, holdout migration status, and explicitly remaining security/knowledge limits. Planned controls may not be designated as already deployed.

Unexecuted tests are called unexecuted. Repository/data assumptions are not subsequently issued as verified facts.

### 19.3 Points still to be clarified in the repository

| Unknown in chat | Consequence before productive use |
|---|---|
| Programming language and package structure | Map ports to existing idioms; do not use assumed Python file paths. |
| Actual data resolution and availability | Check capabilities and coverage; missing data blocks only affected claims. |
| Existing backtester and fill model | Execution fidelity and cost conventions explicitly check. |
| Real research/risk budgets | Lock production runs without configuration; do not adopt fixture values. |
| Previous use of historical test data | Inventory data consumption; unknown past does not mean assured untouchability. |
| Infrastructure for protected evaluation | Implement binding trust zones, rights, candidate sandbox, protected scoring and release gate from 10.6–10.17 and check with SEC01–SEC24. |
| Existing experimental and model registries | Bringing them together instead of creating parallel, contradictory histories. |

These points are integration tasks for M0, not an occasion to restart the entire conceptual work.

---

## 20. Technical references and traceability

The references support individual methods and explain their limitations. The architecture, status models, ports, prioritization rules and implementation phases are project design choices. The combined method still needs validation. The mathematical counter-examples in Section 9.5 are directly traceable derivations.

[^S1]: Rama Cont, Arseniy Kukanov, Sasha Stoikov: *The Price Impact of Order Book Events*. Journal of Financial Econometrics 12(1), 47–88, 2014; DOI `10.1093/jjfinec/nbt003`; Preprint `arXiv:1011.6402`. Considers limit orders, market orders and cancellations, as well as the relationship between order flow imbalance, depth and short-term price changes. Reference: `https://arxiv.org/abs/1011.6402`.

[^S2]: Cynthia Dwork, Vitaly Feldman, Moritz Hardt, Toniann Pitassi, Omer Reingold, Aaron Roth: *Generalization in Adaptive Data Analysis and Holdout Reuse*. NeurIPS 2015; `arXiv:1506.02629`. Treats adaptive data use and controlled holdout reuse under its own methodological prerequisites. Reference: `https://arxiv.org/abs/1506.02629`.

[^S3]: Anna Heath et al.: *Calculating the Expected Value of Sample Information in Practice: Considerations from 3 Case Studies*. Medical Decision Making 40(3), 314–326, 2020; DOI `10.1177/0272989X20912402`; `arXiv:1905.12013`. Reference for EVSI, observational models and the assumption that study data inform other parameters only mediated about the studied parameter group. The scope of the work is health economics; here the decision logic is transferred, not a trading proof is claimed. Reference: `https://arxiv.org/abs/1905.12013`.

[^S4]: Paul L. Williams, Randall D. Beer: *Nonnegative Decomposition of Multivariate Information*. 2010; `arXiv:1004.2515`. Basics of a partial information decomposition and the distinction between redundancy and synergy. A concrete implementation must state its chosen disassembly. Reference: `https://arxiv.org/abs/1004.2515`.

[^S5]: Fernando E. Rosas, Pedro A. M. Mediano, Michael Gastpar, Henrik J. Jensen: *Quantifying high-order interdependencies via multivariate extensions of the mutual information*. Physical Review E 100, 032305, 2019; DOI `10.1103/PhysRevE.100.032305`. O-information is a symmetric variable for characterizing redundancy-dominated or synergy-dominated dependencies, not in itself a target prognosis or causal identification. Reference: `https://journals.aps.org/pre/abstract/10.1103/PhysRevE.100.032305`.

[^S6]: Michael Tsang, Dehua Cheng, Yan Liu: *Detecting Statistical Interactions from Neural Network Weights*. ICLR 2018; `arXiv:1705.04977`. NID extracts statistical interactions from a trained neural model. Reference: `https://arxiv.org/abs/1705.04977`.

[^S7]: Joseph D. Janizek, Pascal Sturmfels, Su-In Lee: *Explaining Explanations: Axiomatic Feature Interactions for Deep Networks*. Journal of Machine Learning Research 22(104), 1–54, 2021. Integrated Hessians explains paired interactions within a model function. Reference: `https://jmlr.org/papers/v22/20-1223.html`.

[^S8]: Andreas Gerhardus, Jakob Runge: *High-recall causal discovery for autocorrelated time series with latent confounders*. NeurIPS 2020. Methodological basis of LPCMCI; illustrates that latent confounding can be explicitly modelled in certain causal discovery procedures, under the respective conditions. Reference: `https://proceedings.nips.cc/paper/2020/hash/94e70705efae423efda1088614128d0b-Abstract.html`.

[^S9]: Aapo Hyvärinen, Hiroaki Sasaki, Richard Turner: *Nonlinear ICA Using Auxiliary Variables and Generalized Contrastive Learning*. AISTATS 2019, PMLR 89, 859–868. Identifiability requires the specific model structure and appropriate additional information; any latent representation is not sufficient. Reference: `https://proceedings.mlr.press/v89/hyvarinen19a.html`.

[^S10]: Ryan J. Urbanowicz, Melissa Meeker, William La Cava, Randal S. Olson, Jason H. Moore: *Relief-Based Feature Selection: Introduction and Review*. Journal of Biomedical Informatics 85, 189–203, 2018; DOI `10.1016/j.jbi.2018.07.014`; `arXiv:1711.08421`. Describes interaction-sensitive feature selection and the prerequisites or limits of different relief variants. Reference: `https://arxiv.org/abs/1711.08421`.

[^S11]: David H. Bailey, Marcos López de Prado: *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality*. 2014; SSRN `2460551`; DOI `10.2139/ssrn.2460551`. Claim-specific Sharpe diagnostics; not to be used as a general release for adaptive cause research. Reference: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551`.

[^SEC1]: NIST, Scott Rose et al.: *Zero Trust Architecture*, SP 800-207, 2020. Principles of explicit authorization and lack of implicit trust. This reference is not a trading-specific leakage proof. Reference: `https://www.nist.gov/publications/zero-trust-architecture`.

[^SEC2]: OWASP Cheat Sheet Series: *AI Agent Security Cheat Sheet*. Primary project documentation on minimal tool rights, external authorization, memory isolation, agent testing and exfiltration risks. Retrieved on 2026-11-08. Reference: `https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html`.

[^SEC3]: Docker: *Docker Engine security*. Official documentation on the security effects of namespaces, capabilities, mounts and in particular the privileges of the Docker daemon. Retrieved on 2026-11-08. Reference: `https://docs.docker.com/engine/security/`.

[^SEC4]: gVisor: *Security Model*. Official documentation on isolation untrusted codes, attack surfaces and borders, including side channels. An exemplary technical reference, not a mandatory product selection. Retrieved on 2026-11-08. Reference: `https://gvisor.dev/docs/architecture_guide/security/`.

**Additional safety principle:** The AI is free to make its research decisions within the permitted development data. It must not be able to determine for itself which protected data it may read or which test results are reported back to it prematurely.

**Guiding principle for implementation:** The research algorithm should not identify as many causes as possible or generate as many backtests as possible. With documented evidence and limited budget, it should examine the next economically relevant uncertainty, expand his model space and not confuse his own selection decisions with independent confirmation.
