---
name: create-pr
description: "Creates or reuses a PR for the current branch and links the configured ticket when authorized."
---

# Create a pull request

Read the profile and .agents/integrations/github.md. Use GitHub, the code provider
supported in this version. Other providers need their own adapter. Do not change
the remote to satisfy the skill.

Confirm repository, source, base and task files. Work with relevant commits;
do not select or discard others' changes. Search for an open PR with the exact
identity (repo/head/base) before creating one. Clarify multiple matches; reuse
the URL when there is one. For genuinely ambiguous choices, use the shared
native-question guidance in WORKFLOW.md; do not ask when the identity is clear.

If needed and authorized, commit/push the branch to the validated remote.
Create a draft PR by default, with a descriptive title and body covering the
problem, resulting behavior and validation actually performed.
Read back the PR and confirm URL, head and base.

If tracking.provider is github or clickup, read the integration and resolve the
ticket by explicit ID/URL or unique match. Add the link only when authorized,
avoiding duplicates. Without a connector, provide the pending text/link and
record that the link was not made. With none, provide only the PR.
Do not merge or close the ticket.
