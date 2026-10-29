# Setup decisions

Use this map to find gaps, not as a mandatory questionnaire. Prefer existing
sources and answers already provided. IDs remain stable on resumption; for
projects with multiple components, use a stable suffix derived from the real
component, for example validation.commands.api.
Collect every applicable answer before writing decisions, destinations or state.
During the interview, interpret the recording instructions below as in-memory
notes; apply them only after the interview ends.

| ID | When to check/ask | Confirmed destination |
| --- | --- | --- |
| product.identity | Project name is missing or only an unconfirmed default | Profile: project.name |
| product.purpose | Purpose, audience or domain terms are unclear | Local context: product |
| product.language | Language of tickets and plans is undecided | Profile: project.language |
| architecture.structure | Components, responsibilities or applicable dependency boundaries are unclear | Local context: architecture |
| architecture.context | Stack/project conventions exist that agents need to read | Profile: context; local document |
| environment.setup | Setup, dependencies or required services are undocumented | Local context: environment |
| validation.commands | Validation, lint, static-analysis or architecture checks, scope, directories or prerequisites are undefined | Profile: validation; context if needed |
| delivery.git | Remote, base, branch pattern or repository are undefined for the project | Profile: git |
| delivery.plans | Plan/status paths do not match a confirmed convention | Profile: paths |
| delivery.tracking | Provider, identity or applicable statuses are undefined | Profile: tracking |
| delivery.pr | PR preference matters to the team and is undecided | Profile: delivery.create_pr |
| agents.models | There is an explicit need for choices by tool/role | Profile: models |
| agents.conventions | There are specific, confirmed agent instructions | Local context or existing local instructions |

For each applicable decision, identify the source and expected result; if the
project does not need it, record not_applicable after evidence or explicit
answer. Do not ask for tracker IDs, statuses or integration configuration when
there is no provider; a default such as none still requires confirmation if no
evidence shows it represents the project's decision. Do not ask for models
when inheritance meets the team's needs. The request may limit the interview;
report what was not assessed instead of filling gaps with assumptions.

## Decisions with multiple fields

For architecture.structure, assess real components and responsibilities, then
applicable dependency and responsibility boundaries separately. An observed
import or directory alone is not proof of a mandatory rule. Capture confirmed
rules, their source, scope, explicit exceptions and existing enforcement checks
in the local context. Where a field is unknown, keep the ID pending or inferred;
use not_applicable only with evidence or explicit confirmation. A project can
have no formal architecture: do not impose one. Existing checkpoints keep their
stable ID and are reassessed on resumption without inventing or discarding data.

Each ID's status summarizes all its applicable fields. For each field, store a
short origin in source: a user response or directly verified source. An optional
field is not applicable only when supported by evidence or explicitly stated;
null or absence alone does not prove this. Record confirmed fields in their
proper destinations and preserve them on resumption. Also list pending fields
in source without exposing sensitive values. If any field is hypothetical or
pending, keep the ID inferred or pending, included in the pending list, and ask
one decision at a time. Mark the ID confirmed when all applicable fields are
confirmed and the remainder are demonstrably not applicable; use not_applicable
for the entire ID only when none of its fields apply.

On resumption, reassess each field of composite IDs even when the earlier state
marked them confirmed. For example, source: "README and context" alone does not
prove purpose, audience and terms were resolved. Read the actual sources again
and record each proven field's origin in source; identify remaining fields as
pending or hypotheses. If evidence is missing for any field, reclassify
product.purpose as pending or inferred, include the ID in pending, and update
the next question and overall status. Preserve existing answers and files, and
ask only about the unresolved field.

For example, in delivery.git assess remote, base_branch, branch_pattern and
repository separately. If only the base was verified, remote and pattern remain
pending. The repository can be not applicable if confirmed that the project
does not use GitHub; do not infer this from repository: null. Record the base in
the profile, keep delivery.git pending and ask one of the remaining decisions.
A possible source is: base_branch: verified local file; remote and
branch_pattern: pending; repository: not applicable, confirmed by user.

In product.purpose, assess purpose, audience and domain terms separately. If
purpose was verified but the audience remains unknown, record the purpose in
context and keep the ID pending. Terms are not applicable only if confirmed or
verified; do not conclude there are none because documentation is absent.
source might record purpose: verified documentation; audience: pending; terms:
not applicable, confirmed by user. Ask about the audience without repeating the
already confirmed purpose.

For validations, discover intended behavior and record each command only when
confirmed: id, cwd relative to the root, argv as a list, surfaces, requires and
required. Preserve existing commands and IDs; before changing or replacing a
command that conflicts with discovery, clarify the divergence. The presence of
a project file alone does not prove that a command works. Do not run commands
just to collect this configuration.
Include existing lint, type-check, static-analysis and architecture-boundary
checks when applicable; discover their actual scripts, scope and prerequisites.
An absent or unknown check is not proof that validation is unnecessary. Do not
install tools, invent commands or assume a check is mandatory.

## Profile contract

The installed kit supplies .specdev/project.json with schema_version: 1 and
sections project, git, paths, context, validation, tracking, delivery and models.
Preserve unknown keys and existing values. project requires name and language;
git contains remote, base and branch pattern with {ticket} and {slug} placeholders
when used. paths, context and validation cwd paths are relative to the project
root, without ..; select only existing context files. tracking.provider accepts
none, github or clickup; IDs, when applicable, are strings, and statuses maps
pending, in_progress and done to real names. delivery.create_pr is boolean and
does not authorize publication. models groups options by client/role; preserve
inheritance until there is a confirmed need for an override. Do not invent
options or client capabilities.

For each command, argv contains separate non-empty arguments; surfaces is a
non-empty list, requires is a list of prerequisites and required is boolean.
An empty validation array means coverage is not configured yet. Compare
information with actual files and the request without assuming structural
validity proves tools, dependencies or services are available.

Example contextual question: "I found separate integration and unit suites. The
documentation mentions a database. Does the team use an isolated database when
running integration tests?" If the source or prerequisite is not yet known,
present it as a hypothesis. Adapt questions to the profile language and already
available information.
