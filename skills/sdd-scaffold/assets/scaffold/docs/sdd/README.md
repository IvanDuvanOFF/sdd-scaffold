# Universal SDD workflow

The coordinator leads discussions; subagents perform implementation.
Shared rules are in [CLAUDE.md](../../CLAUDE.md); roles are Claude Code subagents
in `.claude/agents/`. This file describes the workflow.

## Structure

```text
CLAUDE.md                     # Coordinator and shared executor rules
.claude/
  agents/<agent-name>.md       # Subagents: permanent and project roles
docs/
  architecture/
    README.md                 # Overall architecture
    components/               # One document per component
  specs/<spec-id>.md           # Approved requirements and acceptance
  tasks/<agent-name>/<id>.md   # Temporary individual assignments
  tests/                      # Cases and requirements; executable tests depend on the stack
  changelog/
    flags.md                  # Human decisions
    reviewer/issues.md        # Implementation fixes
    <agent-name>/             # Permanent reports
    summaries/                # Batch summaries between commits
  commits/                    # Requested commit messages
  sdd/                        # Workflow and universal templates
```

The names documenter, test-analyst, test-writer, and reviewer are permanent.
The coordinator defines other roles for the project in .claude/agents. A run's
runtime ID does not become a role name or change its history paths.

## One cycle

1. Discuss goals, scenarios, and constraints. Investigation before approval is
   allowed within explicitly assigned boundaries, without product implementation.
2. Prepare docs/specs/<id>.md using the [template](spec-template.md), obtain
   human approval of a specific version, and record actual confirmation.
3. Create individual [assignments](task-template.md) in docs/tasks/<agent-name>/.
   Specify exact file and command boundaries, side effects, and dependencies.
4. Executors perform assignments and save their own [reports](report-template.md)
   in docs/changelog/<agent-name>/. Write new reports for fixes.
5. Test-analyst prepares [cases](testcase-template.md) and
   [automated test requirements](autotest-task-template.md); test-writer implements
   the tests. The analyst runs them and assesses results. For changes without
   executable code, the coordinator assigns proportional documentation checks.
6. Reviewer checks the related batch as a whole before documenter. Track findings
   in [issues](../changelog/reviewer/issues.md); send the coordinator status and a
   path. The coordinator reads the list and organizes fixes; the analyst repeats
   affected tests, and reviewer verifies fixes and preserves evidence before
   clearing items. Intermediate reviews are allowed; final review is still required.
7. Documenter reads reports and both working lists, then updates documentation,
   including architecture for approved changes. Add only questions for the user
   to [flags](../changelog/flags.md), rather than copying the entire issues list.
8. The user resolves flags; the coordinator arranges necessary fixes and repeated
   checks. Documenter reconciles new reports with flags and preserves decisions
   before removing resolved items. Questions may be raised as soon as discovered.
9. Documenter prepares a [summary](summary-template.md) of confirmed changes.
   Human acceptance of the finished batch is separate from approval of requirements.
10. Only on request, after acceptance, validation, and clearing issues/flags,
    documenter prepares a [commit message](commit-message-template.md). Then delete
    only completed assignments in the accepted batch, first preserving a
    self-contained history of their contents, AC, and results. Keep future and
    unfinished assignments. Committing requires human authorization.

Within approved boundaries, each subtask does not need separate confirmation.
Changes to requirements require renewed approval. If changes follow acceptance
or message preparation, update affected checks, documents, the summary, and the
message. A previously validated batch is not automatically validated again.

## Working lists and history

Reviewer owns issues: implementation defects, IDs, severity, locations,
consequences, and closure conditions. Documenter owns flags: human decisions,
IDs, sources, and closure conditions. If a defect needs a human decision, the
lists reference each other without becoming duplicate registers.
A cleared list contains only its heading and purpose description, without empty
sections, tables, or entries saying "no issues". Do not remove an issue without
verified resolution. Preserve closure evidence in dated reports and the summary.

## Filenames and commit boundaries

For reports, summaries, and commit messages:
`YYYY-MM-DD_HHmmss_slug.md`. The scaffold's time zone is
`Asia/Novokuznetsk (UTC+07:00)`; include a timestamp with an offset in each document.
Use actual time; add a suffix if timestamps collide within a second.
When transferring the scaffold, the time zone may be explicitly changed before
records begin.

A summary identifies the actual base commit and the batch endpoint. Before
committing, the endpoint is the working tree; afterwards, use the actual hash
if known. For a new repository without HEAD, explicitly state that no base commit
exists. Check staged, unstaged, and new files without changing the index.
Do not include others' changes in the batch. Assignment cleanup is part of the
batch and must be reflected in the summary and message.

## Launch and limitations

Claude Code loads CLAUDE.md into the coordinator session and registers every
file in `.claude/agents/` as a subagent; its frontmatter applies the model,
effort, and tool list. The coordinator launches a role with the Agent tool
(`subagent_type: <agent-name>`) and passes the assignment path in the prompt.
A subagent starts with a fresh context: it reads CLAUDE.md and the assignment
itself, and only its final message returns to the coordinator, so reports live
in files. Subagents do not launch other subagents.

Models and effort levels in frontmatter are the user's choice. Availability
depends on the plan, provider, and Claude Code version; if a configuration is
unavailable, raise a flag and do not start the role. Do not silently substitute
models or override them in the Agent call.

The filesystem is shared; allowed paths and commands define behavior.
The environment's sandbox enforces technical permissions. These documents do not
provide separate filesystem isolation or bypass environment approvals.

## Transferring to another project

Transfer CLAUDE.md, `.claude/agents/`, the workflow, templates, and generic docs
structure READMEs. Do not transfer .git, IDE files, secrets, `.claude/settings*.json`,
or other access settings. Old project
specifications, assignments, reports, summaries, and commit messages are not
universal scaffold content. Excluding or clearing them in the target project
requires a separate explicit action; do not delete them automatically. Recheck
models, time zone, and commands. Derive the product and architecture only from
the new project's approved requirements.
