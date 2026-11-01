# SDD Scaffold for Claude Code

A Claude Code skill for creating a Spec-Driven Development structure: discuss
requirements with the coordinator (the main Claude Code session), delegate
implementation to subagents, then validate, review, and document the results.
The scaffold does not choose a product, technology stack, or architecture on the
user's behalf.

## What it creates

- `CLAUDE.md` with coordinator rules and shared executor constraints.
- `.claude/agents/` with four subagents: `documenter`, `test-analyst`,
  `test-writer`, and `reviewer`. Model, effort, and tools are set in the
  frontmatter and applied by Claude Code.
- `docs/architecture/` for overall architecture and individual components.
- `docs/specs/` and `docs/tasks/` for specifications and assignments.
- `docs/tests/` for test cases and automated test requirements.
- `docs/changelog/` for reports, review issues, questions for the user, and summaries.
- `docs/commits/` for requested commit messages and `docs/sdd/` with eight templates
  (including a template for new project subagents).

See the [skill instructions](skills/sdd-scaffold/SKILL.md) and the
[workflow](skills/sdd-scaffold/assets/scaffold/docs/sdd/README.md).

## Installing

### As a plugin (recommended)

In Claude Code:

```text
/plugin marketplace add IvanDuvanOFF/sdd-scaffold
/plugin install sdd-scaffold@sdd-scaffold
```

A private repository requires GitHub access from the device performing the
installation. The skill is then available as `/sdd-scaffold:sdd-scaffold`.

### Manually

Clone the repository and copy the `skills/sdd-scaffold` directory into your
user skills directory, `~/.claude/skills/sdd-scaffold` (all projects), or into
a project's `.claude/skills/sdd-scaffold` (that project only):

```bash
git clone https://github.com/IvanDuvanOFF/sdd-scaffold.git
```

```bash
cp -r sdd-scaffold/skills/sdd-scaffold ~/.claude/skills/
```

Check first that the destination directory does not exist. Back up an existing
skill separately and explicitly decide which version to keep; do not merge files
into an older version by overwriting them. On Windows, `~` is your user home
directory. Start a new Claude Code session so the skill is loaded.

## Usage

Ask:

```text
Create an SDD structure in this project.
```

Or invoke the skill explicitly: `/sdd-scaffold` (manual install) or
`/sdd-scaffold:sdd-scaffold` (plugin).

After the scaffold is created, restart Claude Code (or open `/agents`) so the new
subagents are registered.

The generator supports a preview and requires Python 3:

```bash
python3 skills/sdd-scaffold/scripts/scaffold.py --target /path/to/project --dry-run
```

After checking the paths, remove `--dry-run` to create missing files. The
generator does not overwrite existing files with different contents. If
conflicts occur (for example, the project already has a `CLAUDE.md`), Claude
first examines the current rules and adds compatible content. Conflicting
requirements are referred to the user.

## Models and effort

| Role | Model | Effort |
| --- | --- | --- |
| documenter | `sonnet` | `xhigh` |
| test-analyst | `sonnet` | `medium` |
| test-writer | `opus` | `max` |
| reviewer | `inherit` (coordinator's model) | default |

Aliases always point to the latest model of the family. Change them in the
frontmatter of `.claude/agents/*.md` in the target project. Availability depends
on the plan, provider (Anthropic API, Bedrock, Vertex), and Claude Code version. An unavailable configuration is not
silently substituted: it becomes a flag for the user, and the affected role is
not started until it is resolved. `max` effort uses the most tokens; lower it if
that is too expensive.

## Environment capabilities

Unlike the Markdown-only roles of the Codex version, `.claude/agents/` files are
real Claude Code runtime configuration: they register subagents and apply the
model, effort, and tool list. Path boundaries in assignments are still
instructions; Claude Code permissions and the sandbox enforce what is technically
possible. Subagents start with a fresh context and do not launch other subagents.
Report timestamps default to Asia/Novokuznetsk (UTC+07:00); this can be
explicitly changed before records begin.

Installing this skill does not itself create commits, publish a project,
or import another project's tasks or reports.
