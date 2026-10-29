# ClickUp

Use only when tracking.provider = clickup and the request authorizes the operation.
Use the available authenticated connector; never copy credentials or configure a
personal MCP from another project.

Use tracking.list_id and the workspace provided by the project. If either is
missing, perform the required read-only lookup or request the information before
mutation. Use the explicit plan ID/URL; otherwise require a unique match by the
ticket identifier. Do not select the closest-looking task.

Discover valid statuses. tracking.statuses maps pending, in_progress, and done
intents to exact names; validate the mapping against the list before updating.
Without a mapping, require an unambiguous status for the intent; otherwise clarify.
Reread the task after changing it.

To link a PR, prefer a comment with the URL when authorized. If comments are not
available, preserve the description and prepare a change to the Pull Request
section; apply it only if authorization includes editing that description.
Avoid duplicate comments and do not trigger notify_all by default.
