---
name: enrich-plan
description: "Analyzes and completes a ticket plan without implementing code, creating a branch or opening a PR."
---

# Enrich a plan

Read .specdev/project.json and .agents/rules/WORKFLOW.md. Resolve the identifier
and folder under paths.plans. If there are multiple candidates, clarify the
identity before editing. Read the README, existing plans, paths.status when it
exists, and the actual code for the services, endpoints, components and tests
involved.

Identify missing criteria, open decisions, dependencies, risks and validation.
Gather related open decisions and use the shared native-question guidance in
WORKFLOW.md. Clarify scope before writing criteria that depend on the answer;
continue independent investigation while waiting when the session permits it.

Use .agents/templates/:
- A README with context, branch, status, verified priority and dependencies,
  criteria with stable IDs, existing references, validation and exclusions.
- Separate BACKEND.md and FRONTEND.md when both surfaces exist.
- PLAYWRIGHT.md for a UI using Playwright; TESTS.md for another runner. Include
  actual behavior, transient states, responsiveness and supported themes.

Adapt the format to the project. Fields without a source remain explicitly
undefined; do not turn assumptions into facts. Cite only verified paths.
Link each criterion to the planned implementation or test and expected evidence.
Before execution, keep the status pending and describe the expected result; do
not fill in evidence as if the test already passed. For long work, prepare a
checkpoint with last step, review/evidence, blocker and next action; preserve
existing records when enriching an ongoing plan.
Delegation follows .agents/rules/DELEGATION.md and separates independent
investigations. The lead decides and edits the plan.

Validate links, criteria, scope boundaries and commands against the profile and
code. Deliver the files and decisions. Do not create a branch, product code,
commit, PR or a completed implementation status in this workflow.
