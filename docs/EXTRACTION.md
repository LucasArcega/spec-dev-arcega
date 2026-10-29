# JourneyCore extraction

Source: LucasArcega/journey-core, `develop` branch,
commit `8084d288b0432dff01747a5832c71c20cd07cddd`.
The extraction uses the centralized `.agents/skills/` version after the pull.
Personal copies in `.codex/skills` are not the source of this kit.

## Skills

| Source | Shared destination |
| --- | --- |
| write-kanban-tickets | write-ticket |
| enrich-plans | enrich-plan |
| implement-feature-ticket | implement-ticket |
| codex-review-json | review-changes |
| pr-to-clickup | create-pr + integrations |
| merge-and-close-ticket | merge-and-close |
| fast-merge | fast-merge |
| implement-feature-ticket-worktree | implement-in-worktree |
| test-record | record-test |

Preserved: verifiable criteria, scope clarification before writing dependent
criteria, separate plans, plan/code audit, structured review, surface-based
validation, result confirmation and handoff. Portability obstacles removed:
personal paths, fixed model profiles, MCP names, fixed runtime versions, ports
and application-specific data.

## Rules and AGENTS.md

| Source material | Treatment |
| --- | --- |
| AGENTS.md: product, entities and pipeline | Consumer context; not part of the core |
| scope-guardian.mdc and plans-no-optional.mdc | .agents/rules/WORKFLOW.md |
| codex-subagent-delegation.mdc | .agents/rules/DELEGATION.md + roles |
| tickets-plans-branches.mdc | Profile, templates and integrations |
| issues-tickets-ptbr.mdc | Configurable project.language; initially pt-BR, now English by default for new profiles |
| clean-architecture-dependencies.mdc | dotnet-angular context |
| controllers-services-patterns.mdc | dotnet-angular context |
| domain-entities-organization.mdc and domain-validation.mdc | dotnet-angular context, respecting existing architecture |
| repository-bulk-operations.mdc | dotnet-angular context; project defines the commit owner |
| angular-frontend-patterns.mdc and i18n-angular.mdc | dotnet-angular context, including open overlays and supported languages |
| naming-conventions.mdc and clean-code.mdc | Existing conventions; no universal line limits or automatic refactors |
| codex-cli-path.mdc | Environment capability resolution; no mandatory personal path |

The source rules differed on repository persistence and delegation profiles.
The kit preserves an explicit owner for the unit of work and one delegation
contract; each project retains its actual architecture.

## Scripts, configuration and worktrees

The extraction considered create-worktree, setup-worktree, worktree-run,
worktrees.json, local templates and track launchers. The generic skill uses native
or Git capabilities and requires explicit service isolation where necessary. It
does not copy JourneyCore pools, ports, database names, Azure infrastructure or
wave automation.

CLICKUP_USAGE_RULE and MCP_SETUP became capability-based integration contracts.
Personal MCPs, credentials, environment files and permission settings are not
redistributed. Legacy ADO files are not kit dependencies.

The example at `examples/journey-core/project.json` retains that project's remote,
base, commands and specific list/workspace IDs. It is an example to review, not
an operation to migrate JourneyCore. Adoption in the source project is separate.
The example retains its original `pt-BR` language and tracker status names; new
generic profiles default to English.
