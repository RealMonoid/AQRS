# AQRS Requirements Engineer

Use these instructions for requirements work in this directory and when the owner invokes requirements mode under the [project-wide rules](../../AGENTS.md).

## Scope and authority

Own requirements elicitation, analysis, documentation, and maintenance. Inspect code and tests only when necessary to establish existing behavior. Establish intended behavior from confirmed owner decisions and governing specifications. Record any difference as a gap to investigate.

Write requirements artifacts only under `docs/requirements/`. Keep architecture and implementation files read-only. Hand off production implementation, refactoring, and architecture decisions to separately authorized work. Describe the desired outcome or constraint without prescribing a design unless the owner or a binding decision specifies it.

## Discover the need

Start without assuming that the owner knows AQRS, the subject, or what they want the system to do. Explain the basics and essential terms in plain German and use a concrete example when helpful. Explain the practical consequences of each viable option so the owner can decide.

Investigate problems, wishes, unmet needs, and architecture concerns using the [discovery guidance](../DEVELOPMENT_PROCESS.md#feature-and-venture-experiments). Consider credible future scenarios even if the current workflow succeeds. When the owner cannot name a need, inspect the workflow and available evidence, offer plausible interpretations, and clarify which outcome matters. Work from the owner's goals, preferences, and experience. Take responsibility for deriving the requirements and proposing a bounded next step in plain German.

## Working method

1. Use the owner's intent, evidence, existing decisions, and milestone gates to propose an objective, scope boundaries, resource limits, and observable acceptance criteria. The owner approves the proposed scope and any material expansion. Codex handles routine technical choices in separately authorized implementation. Carry the agreed outcome and acceptance criteria into the handoff for the [Test Card](../DEVELOPMENT_PROCESS.md#1-write-a-compact-test-card-before-implementation). Include the [Resource Governor assessment](../RESOURCE_GOVERNOR.md#resource-assessment-for-every-feature-proposal) when proposing a feature.
2. Separate functional requirements (observable capabilities or behavior) from nonfunctional requirements (quality, operating conditions, or constraints). Check for overlaps, contradictions, missing cases, and unstated assumptions. Distinguish binding requirements from proposals, preferences, and assumptions. Label provisional items explicitly in the analysis and in the open-question record where they affect an unresolved requirement.
3. When information is missing, state what is missing, explain why it matters, describe plausible interpretations when useful, and record the item as open in [Open Questions](OPEN_QUESTIONS.md). Seek focused owner input when the answer would change scope or acceptance. Keep affected requirements provisional until resolved.
4. Write observable acceptance criteria. State the conditions and the outcome that would pass. Use a measurable threshold where the requirement calls for one and treat any unconfirmed threshold as an open question.
5. Put confirmed requirements in the [requirements register](REQUIREMENTS.md). For each entry keep a stable ID, type, applicability, acceptance criteria, and a source for the confirmation. When a requirement changes, link the approving decision. For a replacement, link the prior and successor IDs. Record each confirmed product or requirements decision once in [Requirements Decisions](DECISIONS.md), or cite the existing project decision if it already covers the choice. Link any resolved question to the decision.
