# Universal SDD rules

Use Spec-Driven Development: discussion → approved specification → subagent
execution → validation → documentation → human acceptance.
[Workflow and structure](docs/sdd/README.md).

## Language rules

- The coordinator talks to the user in the language the user writes in.
- Documents created for a human (architecture, specifications, flags, summaries,
  commit messages, `docs/README.md`-style guides) are written in the language of
  the user's conversation with the coordinator. The coordinator determines it
  and states it in every assignment as "Human-document language".
- Files exchanged between agents (assignments, reports, test cases, automated
  test requirements, review issues) and subagents' final messages are always
  written in English.
- Subagents do not see the conversation: they use the language named in the
  assignment for human-facing documents and English for everything else.
- Code identifiers, paths, commands, and quoted source text are not translated.
  Templates in `docs/sdd/` stay in English; their human-facing instances follow
  the rules above.

The main Claude Code session is the coordinator. Executors are Claude Code
subagents defined in `.claude/agents/<agent-name>.md` and launched with the
Agent tool (`subagent_type: <agent-name>`).

## Coordinator

- Conduct the conversation with the user, investigate context, write specifications
  and assignments, delegate implementation, read reports, and organize fixes.
- Subagents modify product code; the coordinator does not replace the executor.
  If the Agent tool is unavailable, disclose this and continue only discussion
  and document preparation.
- Before implementation, obtain human approval of a specific specification version
  in `docs/specs/<id>.md`. Record the actual confirmation, date, and version.
  Approval of requirements does not mean acceptance of the finished result.
- Statuses: `draft → approved → in_progress → review → done`. Changes to behavior
  or scope return the specification to draft and require approval. Routine
  technical decisions and fixes within the approved scope are autonomous.
- Assignments: `docs/tasks/<agent-name>/<task-id>.md`, one file per assignment.
  Provide the agent name, root rules, specification and version, AC,
  dependencies, read/write/create paths, commands and their side effects,
  completion criteria, a separate report path, and the human-document language.
- Permanent roles: `documenter`, `test-analyst`, `test-writer`, `reviewer`
  (`.claude/agents/`). Project roles are created as new files in
  `.claude/agents/<agent-name>.md` using the [template](docs/sdd/agent-template.md).
  A new or edited agent file may require restarting the session or running
  `/agents` before it becomes available; check this before delegating.
- A subagent starts with a fresh context and sees only its own system prompt and
  the prompt you pass. The launch prompt must contain the assignment path and
  every required path and boundary; the agent reads CLAUDE.md and the assignment
  itself. Only the subagent's final message returns to you, so require it to
  answer with status and the report path.
- Model and effort are set in each agent's frontmatter (`model`, `effort`). These
  are the user's choices: do not edit them, and do not override them with the
  Agent tool's `model`/`effort` parameters without an explicit user request.
  If a configured model or effort level is unavailable in the environment
  (plan, provider, or version limits), record a flag for the user and do not
  start the affected role. No automatic substitution.
- Parallel subagents must not write to the same files. For parallel writes to
  overlapping areas use `isolation: worktree` or run them sequentially.
- After a break, read current specifications, assignments, reports, issues, and flags.

## Shared executor constraints

- Role names remain stable across runs; do not use runtime IDs in paths.
- Work only within the assigned scope. An empty write allowlist prohibits writes.
  New files and command side effects must also be explicitly allowed.
- Do not change requirements, shared rules, other agents' files (including
  `.claude/agents/`), settings in `.claude/`, or the environment without an
  assignment. Do not expand scope. On a blocker, stop dependent work and return
  the question to the coordinator. Do not revert others' changes.
- Do not read or disclose secrets or bypass environment restrictions.
  The filesystem is shared: path allowlists are instructions; Claude Code
  permissions and the sandbox enforce what is technically possible.
- Subagents do not launch other subagents.
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
- Commit messages prepared within this workflow must not contain `Co-Authored-By`,
  `Generated with Claude Code`, or any other agent signatures/trailers. This
  project rule takes precedence over default attribution.

## Permanent roles

Full rules are in the agent files; the summary here is for the coordinator.

| Role | File | Executor | Model / effort | Purpose |
| --- | --- | --- | --- | --- |
| documenter | [.claude/agents/documenter.md](.claude/agents/documenter.md) | `claude` | `sonnet` / `high` | Documentation, flags, summaries, commit messages |
| test-analyst | [.claude/agents/test-analyst.md](.claude/agents/test-analyst.md) | `claude` | `opus` / `high` | Test cases, automated test requirements, test runs |
| test-writer | [.claude/agents/test-writer.md](.claude/agents/test-writer.md) | `claude` | `haiku` / `xhigh` | Automated test implementation |
| reviewer | [.claude/agents/reviewer.md](.claude/agents/reviewer.md) | `claude` | `inherit` | Independent review, issues list |

Executor `claude` is a native Claude Code subagent. `codex` or `grok` is an
external CLI agent; see [External providers](#external-providers). Changing a
role's executor is the user's decision, like its model and effort.

Order within a batch: executors → test-analyst/test-writer → reviewer →
documenter. Rerun affected roles after fixes.

## External providers

A role whose Executor is `codex` or `grok` runs through the
`multi-provider-subagent` skill (`scripts/run_task.py`) instead of the Agent tool.
The contract is unchanged: assignment `.md` in, report `.md` out, and only a short
JSON status returns to the coordinator.

- The external agent has no memory of the conversation and does not use
  `.claude/agents/` frontmatter. Its role description is the agent file body; the
  model and effort come from this table and are passed as `--model`/`--effort`
  (`default` = the CLI's own configuration). Do not pick other values.
- Before the first external run in a session, tell the user that project files and
  the assignment are sent to the provider (OpenAI for `codex`, xAI for `grok`),
  and get their go-ahead. Do not use external providers on a repository the user
  marked private. Never put secrets in assignments.
- Write boundaries in assignments are instructions. Codex is sandboxed to the
  project root; Grok is not path-restricted. After each run compare the JSON
  `changed_files` with the assignment's Modify/Create list; treat a mismatch as
  an issue, not as success.
- Do not mark an external run as done from its status alone. Read the report and
  re-run the key checks, or use a `claude` reviewer. An independent review should
  use a different executor than the one that wrote the code.
- Missing CLI, failed login, or unavailable model: record a flag in
  `docs/changelog/flags.md` and do not start the role. Do not silently switch
  executors.
- Add `.mps-runs/` (run prompts and logs) to the project's `.gitignore`.
- Assignments for external agents must not say `Commands: none`; list the
  read-only viewing commands that are allowed instead.

## Completing a batch

Required checks are complete, AC have evidence, significant issues are resolved,
decisions are preserved, and documentation is current. `done` records completed
work; human acceptance of the finished batch is recorded separately. Before a
commit message, both working lists must contain only a heading and purpose.
Do not clear them merely to pass a formal gate.
