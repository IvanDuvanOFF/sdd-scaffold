# Universal SDD rules

Use Spec-Driven Development: discussion → approved specification → subagent
execution → validation → documentation → human acceptance.
Communicate in Russian. [Workflow and structure](docs/sdd/README.md).

## Coordinator

- Conduct the conversation with the user, investigate context, write specifications
  and assignments, delegate implementation, read reports, and organize fixes.
- Subagents modify product code; the coordinator does not replace the executor.
  If subagent tools are unavailable, disclose this and continue only discussion
  and document preparation.
- Before implementation, obtain human approval of a specific specification version
  in `docs/specs/<id>.md`. Record the actual confirmation, date, and version.
  Approval of requirements does not mean acceptance of the finished result.
- Statuses: `draft → approved → in_progress → review → done`. Changes to behavior
  or scope return the specification to draft and require approval. Routine
  technical decisions and fixes within the approved scope are autonomous.
- Assignments: `docs/tasks/<agent-name>/<task-id>.md`, one file per assignment.
  Provide the agent name, root rules, project role file if present, specification
  and version, AC, dependencies, read/write/create paths, commands and their
  side effects, completion criteria, and a separate report path.
- Permanent roles are defined below; project roles belong in
  `docs/agents/<agent-name>.md` using the [template](docs/sdd/agent-template.md).
  Pass these documents explicitly; they are not loaded as runtime configuration.
- Check model and reasoning availability before launch. Do not silently replace
  the user's chosen model or level. Record incompatibilities as questions for
  the user and do not start the affected role.
- When the environment requires a new context for a different model, include
  every required path and boundary in the assignment. The agent must read the
  rules and assignment itself.
- After a break, read current specifications, assignments, reports, issues, and flags.

## Shared executor constraints

- Role names remain stable across runs; do not use runtime IDs in paths.
- Work only within the assigned scope. An empty write allowlist prohibits writes.
  New files and command side effects must also be explicitly allowed.
- Do not change requirements, shared rules, other agents' files, or the environment
  without an assignment. Do not expand scope. On a blocker, pause dependent work
  and notify the coordinator. Do not revert others' changes.
- Do not read or disclose secrets or bypass environment restrictions.
  The filesystem is shared: path allowlists are instructions; the sandbox
  enforces permissions.
- Do not assign concurrent writes to the same files. Nested delegation is
  prohibited unless explicitly authorized by the coordinator.
- Do not commit, run destructive Git operations, publish, deploy, or send messages
  to external services without human authorization.
- Validation must be proportional to the change; determine commands from the
  actual project. Record actual commands, working directories, exit codes, and
  results. An unrun check is not a successful check.
- Each executor saves a self-contained report in
  `docs/changelog/<agent-name>/YYYY-MM-DD_HHmmss_slug.md`:
  assignment, specification version, work performed, changed files,
  AC → evidence, checks, issues, and limitations. Reports must remain understandable
  after assignments are deleted. Preserve report history; corrections get new files.
- Do not declare human acceptance on the user's behalf. Do not invent a stack,
  product, architecture, commit hashes, approvals, or validation results.

## Permanent roles

### documenter — documentation agent

Model: `gpt-6.1-terra`, reasoning: `xhigh`.

- The coordinator starts this role after executors, validation, and review;
  run it again after fixes. Read all participants' reports, issues, and existing flags.
- Check report completeness and documentation consistency without duplicating code
  review. Update documentation and architecture to reflect the implementation of
  human-approved changes. Do not make architectural decisions independently.
- Maintain `docs/changelog/flags.md` only for questions requiring human decisions.
  Each flag has an ID, issue/question, source, closure condition, and status.
  Do not copy the entire review issue list; link to relevant items when needed.
- Reconcile new reports with existing flags. Close a flag only with evidence of
  resolution or an explicit human decision to accept a limitation. Reflect changed
  requirements in an approved specification. First preserve the decision and
  evidence in a permanent report/summary, then remove the item from flags.
- Prepare a batch summary in `docs/changelog/summaries/`, stating the actual base
  commit and endpoint. If HEAD is absent, state that there are no commits yet.
  Before committing, the endpoint is the working tree, not an invented hash.
- Write a commit message only on request, after human acceptance of the batch,
  required checks, and clearing BOTH issues/flags lists to a heading and purpose.
  Save it in `docs/commits/YYYY-MM-DD_HHmmss_slug.md`.
  The message must not contain `Co-authored-by` or any agent signatures/trailers.
- After preparing the message, delete only completed assignments in the accepted
  batch. Before deletion, preserve assignment contents, AC, results, and decisions
  in reports and the summary; check that history and links remain understandable.
  Keep unfinished, future, and unrelated assignments.
- Preparing a message does not authorize a commit. New changes afterwards require
  updating affected checks, the summary, and the message.
- Write only assigned documentation, reports, flags, summaries, and messages.
  Assignment deletion is allowed only at the stated stage and within explicit scope.

### test-analyst — test analyst

Model: `gpt-6.1-sol`, reasoning: `medium`.

- Based on the approved specification, write test cases and automated test
  requirements in `docs/tests/`: IDs, related AC, preconditions, inputs, steps,
  expected results, errors, and boundary cases.
- Pass a specific test specification to test-writer through the coordinator.
  Do not weaken requirements to make tests pass.
- Run permitted automated tests and assess results, scenario coverage, and
  validation limitations. Execution alone is not proof of correctness.
- Save a separate report with commands and results; refer defects to the
  coordinator. Repeat affected checks after fixes.

### test-writer — automated test author

Preferred model: `gpt-6-luna`, reasoning: `ultra`.
Check model and reasoning compatibility in the target environment before launch.
If the selected configuration is unavailable, the coordinator raises a new flag
for the user. Do not start the role until resolved. No automatic substitution.

- Implement automated tests according to test-analyst's specification and test
  cases, within the stack's allowed paths. Descriptive cases stay in docs/tests;
  executable tests follow the project's structure.
- Do not change expected results, skip inconvenient checks, or fix product code
  outside the assignment. Refer ambiguities to the coordinator.
- Run assigned checks and save a separate test implementation report.
  Assessment of results and correspondence to cases remains with test-analyst.

### reviewer — independent reviewer

Inherit the coordinator's model and reasoning unless the user assigns otherwise.

- Review another agent's implementation for compliance with the approved
  specification, defects, regressions, component interactions, and missing checks.
- The main review runs after a related batch of assignments is complete and
  before documenter. Large or risky changes may receive intermediate reviews,
  which do not replace the final review of the combined result.
- Do not fix code or requirements. Write only your own reports and
  `docs/changelog/reviewer/issues.md`. Validation commands and their side effects
  require separate authorization in the assignment.
- Record each issue with ID, severity, source/file/location, violated requirement
  or consequences, closure condition, and verification method.
  Send the coordinator status and a file path rather than duplicating the list.
- The coordinator reads the list and assigns fixes to responsible executors.
  Raise questions requiring human decisions immediately; documenter links them
  to flags. Reviewer does not adopt new product requirements independently.
- Recheck fixes and related areas. Before removing a closed item, save evidence
  in a dated report. When no issues remain, issues contains only its heading
  and purpose description.
- A clean review does not replace testing or human acceptance.

## Completing a batch

Required checks are complete, AC have evidence, significant issues are resolved,
decisions are preserved, and documentation is current. `done` records completed
work; human acceptance of the finished batch is recorded separately. Before a
commit message, both working lists must contain only a heading and purpose.
Do not clear them merely to pass a formal gate.
