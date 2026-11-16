# Open requirements questions

Record new requirements questions raised in this mode here. For each question, record the missing information, why it matters, plausible interpretations when useful, and any affected requirement IDs. Link to the decision when the question is resolved.

Check the [project-wide open questions](../OPEN_QUESTIONS.md) first. If a question already has a record there, cite that record in the relevant requirements artifact.

## Research entry without a formulated hypothesis

**Resolved, 2026-11-14.** Raised on 2026-11-09 in the Requirements Engineer
discussion. The owner confirmed both a user observation and a selected
market as research entry points. See [RD-001](DECISIONS.md#rd-001-two-entry-points-for-research)
and [FR-004](REQUIREMENTS.md#functional-requirements).

## RQ-001 Probabilistic strategy assessment

**Proposed, 2026-11-15; requirements work only.** The owner asked to turn the
probability-versus-threshold discussion into a concrete requirement in chat
`01a1e020-aa73-7120-a42c-bd3d16a153ba`. The drafting objective is confirmed;
the output package and decision role below are a recommendation awaiting
confirmation. No estimator, numerical threshold, implementation, market run,
or replacement of an existing decision rule is approved by this draft.
After confirmation, assign functional/nonfunctional IDs in the
[register](REQUIREMENTS.md) and record the decision in [Decisions](DECISIONS.md).

**Proposed requirement.** By v1.0, AQRS shall report a reproducible,
model-conditional probability assessment of a frozen strategy, together with
effect sizes, uncertainty, limitations and a separately explained research
decision. Qualify the method under M4 and its cost/risk uses under M5. Preserve
[FR-001](REQUIREMENTS.md#functional-requirements), the prediction-before-costs
sequence, and the existing [candidate admission gates](../MILESTONE_DOD.md#10-candidate-gates-independent-of-software-releases).
The subsequently confirmed [FR-005](REQUIREMENTS.md#fr-005-acceptance-cases)
also applies: probability outputs do not make an uninformative study useful
or justify repeated inadequate tests. An unclear, ill-posed or insufficiently
operationalized question first requires a stop and specific rework. Establish
the missing prerequisites for a clarified question, or stop and park the study
with its question, gaps and resumption condition.

### Four output groups

Before evaluation, register the candidate/version, benchmark, eligible
population, forecast horizon, performance units, cost and sizing assumptions,
data cutoff, model and any prior assumptions. Let `D` be the admissible evidence
and `M` the declared probability model. Every probability below is conditional
on `D, M`; it is not an unconditional promise of future profitability.

| Output | Exact proposed meaning | Role in evaluation |
|---|---|---|
| Predictive advantage | `P(delta_pred > delta_pred_min given D, M)`. `delta_pred` is the population improvement in a preregistered prediction score over the benchmark, oriented so positive is better. | Evaluate prediction before costs; retain a possible forecasting contribution even when trading economics fail. This is not a single trade's win probability. |
| Economically useful net advantage | `P(mu_net > net_min AND delta_net > incremental_min given D, M)`. `mu_net` is the strategy's expected net return and `delta_net` its expected net advantage over the benchmark on matched opportunities. | Distinguish useful absolute net value from improvement over a weak benchmark. Report both marginal probabilities alongside the joint result; never multiply them without a justified independence model. |
| Loss over a future period | `P(R_net(T) < 0 given D, M)` for the frozen policy and specified future period `T`. | Describe finite-period loss risk, including parameter uncertainty and future outcome variation; a positive expected edge can coexist with this risk. |
| Drawdown exceedance | `P(MDD(T) > drawdown_limit given D, M)`, where MDD is the maximum peak-to-trough loss of the simulated net equity path over the same `T`. | Show path risk separately from the probability of ending the period at a loss. Specify initial equity, sizing, reinvestment and equity observation frequency. |

Minimum relevant effects, `T`, the drawdown limit and allowed risk are
study-specific inputs fixed and justified before outcomes, not new universal
defaults. The three minimum effects are nonnegative; zero means any strictly
positive advantage, not a claim of practical importance. `T` is a future
evaluation period, separate from the strategy's forecast/holding horizon.
Use the existing [open cost/risk decisions](../OPEN_QUESTIONS.md)
where applicable. All return comparisons use the same opportunity grid,
including flat periods, execution, sizing and cost treatment. A drawdown
claim applies only to its declared observation frequency and fill model.

For every available group, show the underlying effect estimate or predictive
distribution, interval/quantile definition and units, model assumptions and
predeclared sensitivity results. Record source/data/configuration identities,
research exposure, evidence stage and numerical error where applicable.
Distinguish uncertainty about an expected effect from variation in future
realized outcomes. A p-value, historical win rate or model state probability
must not be relabelled as one of these strategy probabilities.

### Influence on strategy evaluation

1. **Report evidence continuously.** Preserve the numeric results and their
   uncertainty regardless of the eventual status. No single success percentage
   or universal probability cutoff shall replace the assessment.
2. **Keep three decisions distinct:** further prediction research, further
   economic/risk research, and eligibility for independent confirmation or
   paper monitoring. A probability does not itself grant any authorization.
3. **Use a predeclared, reproducible decision policy.** Explain the next action
   using the probability profile, effect size, downside, evidence validity and
   the cost of obtaining decision-changing evidence. Compare only compatible
   candidates; expose trade-offs instead of averaging probabilities into a
   score. Use explicit scenarios when expected information value is not
   defensibly estimable. Computational outputs and rule-based decisions follow
   the project's deterministic-software preference; an LLM may explain them.
   Useful prediction with weak net economics can justify prediction research,
   but does not qualify an economic claim. A plausible material net benefit
   with unresolved uncertainty can justify a bounded follow-up when its
   decision value warrants its cost. A risk profile outside the declared
   tolerance prevents advancement of that frozen policy even with high
   estimated benefit. Insufficient evidence remains inconclusive.
4. **Make limits visible.** Unsupported dependence/selection assumptions,
   inadequate data, missing risk inputs or failed numerical checks must yield
   an unavailable/unqualified result with a reason, never a fabricated 0%,
   50% or 100%. A cost stage skipped under its registered rule remains not
   evaluated. Sensitivity that changes the recommended action leaves that
   action inconclusive until the named uncertainty is resolved.
5. **Preserve admission and exposure.** High estimated probabilities do not
   bypass data, holdout, budget, risk or independent-confirmation requirements.
   Count additional analyses on reused data. Historical results and frozen
   gates remain intact; any prospective replacement needs its own recorded
   decision and verification. A failed economic assessment does not erase
   measured predictive information.

### Observable acceptance criteria for a later implementation

- Known-answer public fixtures distinguish all four output groups, posterior
  parameter uncertainty and future outcome uncertainty. Joint economic
  probability agrees with the common joint model and is no larger than either
  marginal; independence cannot be assumed merely to multiply them. Tolerances
  are fixed before testing.
- A fixture with positive expected net value and appreciable future loss risk
  retains both facts. Two paths with the same terminal return and different
  drawdowns, treated as known deterministic paths, give different exceedance
  results for a limit strictly between their maximum drawdowns.
- Missing `T`, sizing or drawdown limits suppress only dependent outputs and
  explain why; failure of an economic prerequisite preserves prediction results.
- Stored identities reproduce outputs and actions on native Windows and
  headless non-root Linux within justified numerical tolerances. If simulation
  is necessary, record its algorithm, seed, budget and numerical uncertainty.
- Qualify inference under known generating models and examine prior/model
  sensitivity. Evaluate predictive probabilities on eligible chronological
  observations with calibration diagnostics and a preregistered proper score
  against a simple baseline. Fix sample sufficiency and acceptance tolerances
  before results; if precision is inadequate, the qualification remains open.
  Synthetic computational calibration is not proof of real-market calibration.
- Include null, dependence, selection and misspecification cases. Treat omitted
  search exposure or unsupported dependence as an explicit qualification limit,
  not independent evidence. Independent benchmarks, if needed, are supplied by
  the owner; public developer fixtures only establish engineering behavior.
- Decision examples cover inconclusive evidence, useful prediction with failed
  economics, qualified further research, and unavailable risk estimates. The
  same evidence and declared policy yield the same explanation and next action;
  none of these cases starts a protected evaluation or live order automatically.

### Basis, resources and remaining choice

**Evidence basis, checked 2026-11-15.** This is a requirements specification,
not a finding that a Bayesian method outperforms AQRS's existing intervals.
The [ASA statement (2016), principles 2-5](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf)
supports separating evidence and effect size from a single significance cutoff.
[Witzany (2021), sections 3 and 5](https://www.mdpi.com/2227-9091/9/1/18)
shows a strategy-selection application and its model dependence; its simple
stable-return assumptions and mixed naive-model results do not qualify it for
AQRS. [Gneiting and Raftery (2007), section 1](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf)
supports proper scoring and calibration of predictive distributions.
[Talts et al. (2020 v2), abstract](https://arxiv.org/abs/1804.06788v2)
concerns computational inference validation, not market validity. No numerical
acceptance threshold is borrowed from these sources. Reuse the existing
[method-selection guide](../MODEL_EVALUATION_PROTOCOL.md#validation-method-selection)
and [scenario-based allocation](../ADAPTIVE_QUANT_RESEARCH_PROPOSAL.md#82-standard-mode-explicit-scenarios-without-invented-probabilities).

**Resource Governor assessment.** Drafting/verification estimate: 20-40 minutes
in this turn, plus an estimated 15-30 minutes of prior unmeasured discussion
and source review in this chat. Documentation only: zero research trials,
fits, resamples, market-data reads or recurring computation. No dependency,
storage or concurrency expansion. Implementation and per-candidate recurring
costs remain unknown until a model and qualification scope are selected. Their
smallest useful measurement must be bounded before execution by the effective
Governor (currently at most 120 seconds/trial, 300 seconds/campaign, 4096 MiB
observed RSS, one worker and no automatic retries). This is not a new run plan
or budget increase. Risk screen: no runtime, scientific gate or protected-data
contract is changed by recording this proposal.

**Preparation evidence.** Measured drafting and review on 2026-11-15:
17:05:56-17:12:55 UTC (6m 59s), before publication. The language audit and
self-test, whitespace check, ten local links/anchors and complete changed-path
changelog check passed. Manual review corrected the joint-probability bound
and made the drawdown comparison fixture unambiguous. These are documentation
checks, not evidence that the proposed statistical capability works.

**Owner choice.** Adopt these four output groups and their role in research
decisions (recommended), or limit the requirement to descriptive reporting.
The first option permits a separately qualified future decision policy; the
second improves transparency without changing prioritization or admission.
Method selection and study-specific inputs come later under M4/M5; this draft
does not authorize immediate adoption or resumption of market research.
Current default: existing evaluation rules. Draft preparation and publication
are authorized; binding adoption is pending this product-scope choice.

## FR-005 execution-enforcement gap

**Implementation authorized, 2026-11-15, owner chat
`01a1e020-aa73-7120-a42c-bd3d16a153ba`.** The owner requested the runtime start
barrier and actual Windows/Linux negative and valid cases. The
[FR-005 card](../MILESTONE_STATUS.md#fr-005-test-card-enforced-study-admission)
records current implementation evidence and limits. This supersedes the earlier
requirements-only boundary for this bounded engineering item, without resuming
market research or the general AQRS-H01 audit.

**Owner correction, 2026-11-16:** the five-part prerequisite plan was rejected;
automated research is the goal and no human expert is assumed. Other LLMs are
allowed under the revised FR-005 known-answer accuracy requirement; the question
author does not provide its admission judgment or benchmark reference answer. Question-meaning assessment is
a later step, with no runtime LLM judgment in the current increment.

[FR-005-P01](../MILESTONE_STATUS.md#fr-005-p01-detectability-before-a-synthetic-study)
replaces the fixed sentence with structured fields and adds bounded conditional
detectability for `bar_reversal` and `volume_movement` on synthetic data. Its
card records implementation and verification. This does not lift the market
stop or enable legacy study entries. The owner will assess unseen study plans;
local generated cases are public engineering fixtures, not that blind evidence.
