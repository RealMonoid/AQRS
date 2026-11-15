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

**Preparation checkpoint, 2026-11-15:** recording and review from 17:30:04 to
17:35:02 UTC (4m 58s), including both subsequent owner clarifications, before
publication. Reuse the unchanged source checks from `dceae89`; fresh language,
link, changelog and whitespace checks qualify these documentation changes.
