# Versioned Data Understanding and Graph Context Artifacts

The copepod assistant stores Data Understanding and Graph Context as structured, versioned session artifacts instead of treating them as conversation-only summaries. The displayed summaries remain useful for the user, but the artifacts are the canonical state used to build the graph plan and execute Analyse Mode, so the system can tie a graph plan to the exact validated understanding of files, columns, units, quality limits, and user corrections.

**Status:** accepted

**Considered Options**

- Conversation history only: simpler to implement, but too fragile because the LLM must recover critical state from prior prose.
- Single mutable artifact: easier to read, but unsafe when files are re-uploaded, corrected, or added during Analyse Mode.
- Versioned artifacts with draft and active states: chosen because automatic inspection can remain provisional until user validation, while Analyse Mode can reference the validated versions that made the plan executable.

**Consequences**

Each automatically generated Data Understanding or Graph Context starts as `draft` and becomes `active` only after user validation or correction. Graph Context versions must reference the Data Understanding version used to construct them. File entries need stable identity fields, including a content hash, so stale understanding can be detected when a file name is reused with different contents.
