# Node.js context

Use this context only when selected for the project. Inspect the actual runtime,
package manager, lockfile, workspaces, module format, framework and scripts before
choosing commands. Preserve the project's versions and conventions; do not install
dependencies, rewrite lockfiles or change package managers as a side effect.

Respect the project's documented module and service boundaries. At applicable
server boundaries check input validation, authorization, error handling and
sensitive logging; respect existing environment and secret handling. For async
work, follow project conventions for cancellation, cleanup and failure handling.
Consider Node/browser boundaries in shared packages and avoid exposing server-only
code or secrets to client bundles.

Discover actual lint, type-check, build, unit and integration scripts, their cwd,
prerequisites and coverage; configure only confirmed commands. Do not assume that
a package.json script exists or that TypeScript, a framework or a test runner is
used. Run only task-authorized checks with their real dependencies.
