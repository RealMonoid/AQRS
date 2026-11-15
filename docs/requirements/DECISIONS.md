# Requirements decisions

Record product choices and requirements decisions the owner confirms in this mode. Include the date, status, decision, rationale, affected requirement IDs, and links to any resolved questions.

Use [project decisions](../DECISIONS.md) as the source for existing decisions and architecture decisions. Cite an existing decision where it already provides the rationale.

## RD-001 Two entry points for research

**Accepted, 2026-11-14.** The owner confirmed both options in the AQRS
requirements discussion. Support users who bring an observation and users
who begin with only a market. Both paths lead to a testable research idea.
The market path uses eligible development data and abstains when the
evidence is insufficient.

This resolves the [research entry question](OPEN_QUESTIONS.md#research-entry-without-a-formulated-hypothesis)
and establishes [FR-004](REQUIREMENTS.md#functional-requirements) as a v1.0
product requirement. [M2-E21](../MILESTONE_ARCHIVE.md#m2-e21-scout-pilot-feature-preflight)
can test the market path on synthetic data under its own start conditions.
Implementation and pilot execution require their existing authorizations.

## RD-002 Question-led evidence and decisive study planning

**Accepted, 2026-11-15.** In chat `01a1e020-aa73-7120-a42c-bd3d16a153ba`,
the owner rejected running research tests without meaningful information
value. The owner also rejected substituting LLM-chosen technical limits for
the scope required by the question. The owner's final clarification requires
either establishing the missing technical or other prerequisites, or stopping
and parking the test with an explicit account of what is missing. A parked
question is retained for a justified later resumption, not kept artificially
active through repeated inadequate tests or unexplained postponement.
The owner additionally requires an earlier stop and specific rework whenever
the question itself is unclear, incorrectly framed or insufficiently
operationalized. A dependent test cannot begin on an invented interpretation.
Question clarification remains valid preparation; it is not a research result.

**Evidence/design clarification, 2026-11-15, same owner chat.** Determining
which observations could answer the clarified question explicitly includes
the appropriate statistical procedures, relevant existing academic research,
and the test design needed to support the intended inference. FR-005 requires
a justified connection from question to observations, method, assumptions and
decision, using the existing decision-linked literature review and Test Card.
Method/design defects require specific rework; an unresolved prerequisite
stops and parks the dependent test with its reason and resumption condition.
The absence of a directly matching paper alone is not such a prerequisite.
Acceptance covers missing measurement rules, a method that cannot support the
claim, critical unjustified assumptions, and a corrected design reaching the
feasibility assessment. No statistical family, test window or numerical
threshold is selected by this clarification.

**Enforcement clarification, 2026-11-15, same owner chat.** The owner asked
how AQRS will actually check these requirements before every research run and
stop for unclear questions, unsuitable designs or missing prerequisites.
[FR-005 execution criteria](REQUIREMENTS.md#fr-005-execution-enforcement-and-verification)
make the required behavior observable: current scientific and execution
readiness, a decision bound to the actual study, fail-closed launch behavior,
actionable recorded stops and coverage of every supported execution path.
The implementation must distinguish qualified scientific judgment from form
validation. This specifies the existing stop requirement; it does not select
a review provider, mandate repeated owner approvals, implement a gate or lift
the market-research stop. The source-inspection gap and qualification limits
are retained in [Open Questions](OPEN_QUESTIONS.md#fr-005-execution-enforcement-gap).

[FR-005](REQUIREMENTS.md#fr-005-acceptance-cases) records this requirement and
its observable admission/closeout cases. It makes the existing
[question-led sufficiency rule](../SEQUENCE_PREFLIGHT.md#research-evidence-sufficiency)
explicit in the requirements register; it does not create a new universal
power, duration or sample-size threshold. A justified study may still end
inconclusively. A small study is appropriate when it can answer its own
declared question, not merely because it is technically convenient.
Realizing feasibility means demonstrating support for the required study,
not redefining the question to fit the current implementation. An unknown
resolution route is reported as unknown. No universal restart date is promised.

**Boundary and resource assessment.** This decision authorizes requirements
documentation, not a new research run, implementation, general audit or budget
increase. It does not release the current market-research stop. Requirements
recording and focused documentation checks are estimated at 10-20 minutes;
the prior RQ-001 package took about 18 measured minutes including publication
and CI, with 15-30 minutes of earlier discussion/source review estimated, plus
about 6 minutes of this follow-up discussion before recording began. This
increment adds zero research trials, fits, data access or recurring computation.
Reuse the current Test Card, preflight and Governor. If a runtime enforcement
gap is found in separately authorized work, estimate its smallest correction
before implementation. Documentation alone is not proof of enforcement.

The evidence/design clarification adds an estimated 10-15 minutes of
requirements recording, focused checks and publication, with zero additional
research trials, fits, data access or recurring computation. Risk screen:
requirements wording only; no runtime, data boundary, resource enforcement or
operative research contract is changed. A new fault tree is not triggered.
Documentation acceptance is a traceable methods/literature/design obligation,
actionable failure cases and consistent links, language and changelog paths.

**Preparation checkpoint, 2026-11-15:** recording and review from 17:30:04 to
17:35:02 UTC (4m 58s), including both subsequent owner clarifications, before
publication. Reuse the unchanged source checks from `dceae89`; fresh language,
link, changelog and whitespace checks qualify these documentation changes.

**Clarification checkpoint, 2026-11-15:** measured recording/review after
resumption from 18:12:59 to 18:15:56 UTC (2m 57s), excluding earlier dialogue
and subsequent publication. Documentation criteria are supported: manual
review, 22 local link/anchor checks, exact three-path changelog coverage,
language audit/self-test and whitespace checks passed. Non-documentation
source matches `dceae89`; its accepted Windows/Linux checks remain applicable.
Full runtime enforcement remains unverified; no research run is dispatched.

**Enforcement resource assessment.** Requirements clarification, bounded source
inspection, independent review and documentation checks are estimated at
15-30 minutes. They add zero research trials, fits, market-data reads or new
runtime dependencies. Implementation effort and recurring scientific-review
latency, model/API cost and memory use are not yet measured; no budget fit is
claimed. Reuse an applicable review of an unchanged design, while checking
current launch conditions every time. The smallest later qualification must
prove rejection before data/worker access and a valid bounded synthetic start;
it is not an authorization to run it here. Retain current Governor limits;
budget any review or calibration explicitly rather than hiding it outside
the campaign. Any implementation touching launch, journal or protected-data
boundaries requires the existing risk assessment before coding. This increment
changes requirements documentation only and does not modify those mechanisms.
