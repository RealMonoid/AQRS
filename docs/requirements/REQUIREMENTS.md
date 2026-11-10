# AQRS confirmed requirements

This register is the central source of truth for confirmed AQRS requirements. Entries link to the governing specifications for full scope and verification details. The initial entries index selected existing commitments. Existing binding contracts and milestone criteria also apply. If a source and an entry diverge, raise the discrepancy in [Open Questions](OPEN_QUESTIONS.md) and resolve it with the owner.

## Functional requirements

| ID | Scope | Confirmed requirement | Acceptance criteria | Governing source |
|---|---|---|---|---|
| FR-001 | Through v1.0 | AQRS supports short-horizon trading research and limits all trading decisions to simulation. | A review of supported interfaces and the release configuration finds no path to submit live orders. | [Product vision](../PRODUCT_VISION.md#1-what-we-ultimately-intend-to-build), ADR-002 in [Project Decisions](../DECISIONS.md) |
| FR-002 | M2 | AQRS evaluates a LightGBM supervised challenger and an Isolation Forest unsupervised hypothesis generator. | Each pilot is reproducible, runs within its declared budget, and includes a comparison with a simple baseline. An evidenced blocker leaves the gate blocked. | [M2 acceptance criteria](../MILESTONE_DOD.md#m2--v03-alpha-discovery-with-genuine-controls) |

## Nonfunctional requirements

| ID | Scope | Confirmed requirement | Acceptance criteria | Governing source |
|---|---|---|---|---|
| NFR-001 | From M0 | AQRS supports native Windows and headless, non-root Ubuntu on the declared CPU-only matrix. | The required clean-install, CLI, and test sequence passes independently on both platforms as specified by the platform contract. | [Platform support matrix](../PLATFORM_COMPATIBILITY.md#2-platform-support-matrix-and-honest-release-claims) |
| NFR-002 | Permanent | AQRS-authored repository artifacts use English. | The language audit and its self-test pass, and manual review confirms English prose in added and modified artifacts. | [Language policy](../LANGUAGE_POLICY.md#acceptance) |

Use [Open Questions](OPEN_QUESTIONS.md) for unresolved requirements and [Requirements Decisions](DECISIONS.md) for approved choices and their rationale. Implementation approval and milestone evidence remain separate in the [milestone record](../MILESTONE_STATUS.md).
