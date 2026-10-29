# React context

Use this context only when selected for the project. Inspect the installed React
version, framework, renderer, routing, state, data-fetching and test conventions;
do not assume a particular framework, TypeScript, client-side rendering or folder
structure. Preserve established component and package boundaries.

Keep rendering free of unintended side effects and respect hook ordering and
dependency semantics. Review state ownership, effect cleanup, asynchronous races,
loading, empty and error states when relevant to the changed flow. Account for
accessibility, keyboard interaction and responsive behavior where applicable.
For server-rendered projects, respect client/server boundaries and avoid exposing
secrets or server-only modules to the browser.

Discover actual lint, type-check, build and UI-test commands and prerequisites;
do not assume a script or tool is present. Test behavior at the appropriate level
using the project's existing tools and configured supported browsers.
