---
name: record-test
description: "Records video of a requested UI test using the available runner, especially Playwright."
---

# Record a test

Read the profile and actual runner configuration. Resolve a spec and test
project; ask if the identity is missing. Do not record the entire suite as a
side effect. Use the shared native-question guidance in WORKFLOW.md to clarify
the test when needed. Check services, test credentials and the project's required minimum
version; do not hard-code Node, ports, folder or project from another repository.

In Playwright, video is a use configuration; do not assume a --video flag.
Use the existing environment mechanism or a temporary configuration that extends
the real one and enables video for this run. Do not leave video=on permanently
or change product configuration to fulfill a recording request.

Run the spec in the correct cwd. Record the start and output directory.
Locate the WebM actually created in that run, distinguishing the requested test
from setup/login and retries. Do not reuse an old video as evidence.
If the test fails but there is a video, deliver the file with the failure result.
If no recording was produced, explain why without inventing an artifact.

Return a Markdown link to the absolute path and the observed result.
Do not commit videos, reports, authenticated state or credentials.
If the runner does not support an available recording method, report the limit.
