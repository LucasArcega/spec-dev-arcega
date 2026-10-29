# Delegation by complexity

The principal retains scope, architecture, shared contracts, integration, Git
decisions, final validation, plan state, and handoff.

| Class | Criterion | Approach |
| --- | --- | --- |
| S0 | Small, tightly coupled local task | Execute on the principal. |
| S1 | Focused read-only question about a subsystem | Use specdev-explorer when independent work provides real benefit. |
| S2 | Bounded implementation, decided contract, exclusive files | Use specdev-worker for the bounded portion. |
| S3 | Architecture, multiple layers, security, migration, or data risk | Principal decides and integrates; delegate only evidence or S2 parts. |

Delegate only with a concrete objective, verifiable output, exclusive ownership,
and independently actionable work. Do not delegate the entire ticket or the same
investigation to more than one agent.

## Roles and models

Canonical roles are in .agents/roles/. The installer converts them to formats
available in each tool. specdev-reviewer reviews; investigator is reserved for
unknown or divergent behavior with no established cause. Read-only roles do not
edit. This is an instruction; permission isolation depends on the tool and session.

By default, the model is inherited. Tool- and role-specific overrides are in
models. The legacy string model ID format remains valid. Codex also accepts
model and reasoning_effort; configure a compatible effort when changing model.
Claude accepts a per-role tools allowlist, without granting additional permissions.
Restrict tools only when the task and required validation remain possible. Do not
translate these options to clients that do not support them.
Do not translate model IDs between providers. If a requested model is unavailable,
report the limitation and run sequentially when feasible; do not create an agent
just to change model. Use only context and parallelism options supported by the
runtime. Do not force an agent count based on the number of folders.

## Delegation contract

Before each spawn, provide:

- Objective and S1, S2, or S3 classification with justification.
- Role and settings supported by the tool.
- Allowed files or responsibilities; state read-only when applicable.
- Already decided contracts and applicable criteria.
- Expected output and verification command or evidence.
- Restrictions: no Git operations, external services, scope changes, or plan
  completion outside the assigned responsibility.
- Coordination: you are not alone; do not revert others' changes, adapt to the
  current state, and report conflicts. Do not edit another owner's files.

Two workers do not edit the same file or logical component. The principal keeps
non-overlapping work, reviews each delivery, and runs final checks. If delegation
is unavailable, preserve the process sequentially.

## Return and interruption

Each agent returns, in a format proportional to the task: observed result, files
read or changed, evidence (command/result or path/line), blockers/limitations, and
next action. Distinguish tests executed from tests only read. The worker identifies
incomplete changes; read-only roles do not claim to have fixed anything.

On failure, interruption, or conflict, stop mutations in the affected part and
report the last confirmed step, potentially partial files, and remaining validation.
Do not undo changes to simulate a clean state or assume cancellation reverted files.
The principal checks actual state before reassigning or closing, preserves a plan
checkpoint when needed, and continues sequentially if delegation is unavailable or
provides no benefit.
