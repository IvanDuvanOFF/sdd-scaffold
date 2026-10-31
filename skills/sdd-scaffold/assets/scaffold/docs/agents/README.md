# Project agents

Permanent universal roles are fully defined in [AGENTS.md](../../AGENTS.md).
Only situational project roles belong here: <agent-name>.md using the
[template](../sdd/agent-template.md). The coordinator creates the rules before
starting such an executor and explicitly passes them with the assignment.

Role names remain stable across runs, for example backend. Runtime process IDs
are not used in paths. A role may receive several sequential assignments;
concurrent assignments must not overlap in writes. Role rules are not runtime
configuration and do not expand assignment permissions.
