# GitHub

Use when the task authorizes a GitHub action. Prefer the available connector;
use authenticated gh as an alternative. Get owner/repo from git.repository when
populated and check the configured remote. If absent, derive and validate it from
the remote. Never silently replace a remote.

For a PR, resolve source and base branches from the task and profile. Before
creating one, look for an existing PR with the exact source, base, and repository.
Update only when requested. Avoid duplicate PRs.
Use a description with the problem, observable change, and validation. With gh,
preserve multiline text with --body-file rather than constructing commands with
interpolated text. After creation, reread the PR and confirm source/base/URL.

GitHub tickets require the exact repository and number. For links and closure,
check identity; do not use title similarity as authorization. For merge, follow
merge-and-close. Do not bypass protection or use --admin or --force.

The kit does not configure tokens, connections, remotes, or permissions. Report an
unavailable tool as a limitation; do not simulate a result.
