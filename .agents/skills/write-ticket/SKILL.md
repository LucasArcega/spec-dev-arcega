---
name: write-ticket
description: "Creates or reviews tickets with motivation and verifiable acceptance criteria in the configured tracker or local documentation."
---

# Write a ticket

Read .specdev/project.json and .agents/rules/WORKFLOW.md. Identify the problem,
the audience, the outcome and the authorized tracker. Consult available context
before asking for information.

Before drafting, clarify important open decisions using the native-question
guidance in WORKFLOW.md. Do not ask again about decisions already made in the request or project. Do not
invent a priority, dependency, estimate or identifier.

Use the profile language and write:

- A short title following the project convention.
- Why: the problem and value in one or two sentences.
- A user story when the outcome affects end users.
- Required, observable, pass/fail acceptance criteria.
- Brief technical context with real contracts and paths when needed.
- Out-of-scope items for relevant exclusions.

If the request is only to draft, deliver the text. To create or edit in a tracker,
read the relevant integration and perform only the authorized operation.
With tracking.provider = none, use the local file specified in the task.
Confirm creation or editing by reading the result and provide the file or URL.
