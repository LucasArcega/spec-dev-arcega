# .NET and Angular profile

Read only when selected in context. Concrete paths, versions, commands, and
conventions come from the profile and existing code.

## Backend

Preserve the direction of dependencies in the adopted layers. When the project
uses Clean Architecture, the application depends on abstractions; infrastructure
implements them. Controllers handle HTTP and delegate business rules.
Use status constants, domain validation in factories/update methods, NRT, async,
and CancellationToken in line with existing patterns.
Organize entities by context; do not move files as an incidental refactor.
Define who owns the unit-of-work commit; do not add SaveChanges in each repository
if the project uses a coordinated commit. Avoid loading tables for bulk delete and
preserve tenant filters. Migrations require validation with a real database when
they change relevant persistence behavior.

## Frontend

Follow the actual application version and patterns: standalone, strict templates,
modern control flow, inject, and OnPush where compatible. Tear down subscriptions
and keep business logic/HTTP in existing services.
Inspect inputs, outputs, and defaults before reusing components.
Validate actually open overlays on desktop/mobile, as well as the underlying page.
If the product uses ngx-translate, maintain keys across all configured languages.
Do not impose i18n or dark mode on products that do not offer those features.

## Environment and tests

Distinguish unit tests from Docker-backed integration tests and UI tests.
Rebuilding images and exercising the changed route are required to prove the
running code when containers are updated. Keep credentials in secrets/environment.
Ports and data must be explicitly isolated per worktree.
