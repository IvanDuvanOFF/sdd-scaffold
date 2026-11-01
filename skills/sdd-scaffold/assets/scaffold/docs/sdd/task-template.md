# <task-id>: <assignment>

- Agent: <stable name>
- Role: <.claude/agents/<agent-name>.md>
- Specification: <docs/specs/<id>.md>, version <n>, approval <link>
- Criteria: <AC-* or investigation question>
- Status: pending
- Dependencies: <launch prerequisites>
- Permanent report: <docs/changelog/<agent-name>/dated-filename.md>

## Assignment and completion

<Specific result, completion criteria, and who verifies it and how.
Implementation requires an approved specification.>

## Boundaries

- Read: <paths/sources>
- Modify: <exact paths; empty = no writes>
- Create: <files/limited directories, including the report>
- Delete: <nothing by default>
- Commands: <commands, working directory, side effects>
- Prohibited: <additional constraints>
- Nested delegation: subagents do not launch other subagents.

If additional permissions or decisions are needed, notify the coordinator before
dependent work. Do not write to the same files concurrently with another agent.

## Handoff

Save a separate self-contained report using docs/sdd/report-template.md and send
its path to the coordinator. Do not keep the only evidence in this assignment:
completed assignments may be deleted after the commit message is prepared.
