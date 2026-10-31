# SDD Scaffold

A Codex skill for creating a Spec-Driven Development structure: discuss requirements
with a coordinator, delegate implementation to subagents, then validate, review,
and document the results. The scaffold does not choose a product, technology stack,
or architecture on the user's behalf.

## What it creates

- `AGENTS.md` with shared rules and the `documenter`, `test-analyst`, `test-writer`, and `reviewer` roles.
- `docs/architecture/` for overall architecture and individual components.
- `docs/agents/`, `docs/specs/`, and `docs/tasks/` for project roles, specifications, and assignments.
- `docs/tests/` for test cases and automated test requirements.
- `docs/changelog/` for reports, review issues, questions for the user, and summaries.
- `docs/commits/` for requested commit messages and `docs/sdd/` with eight templates.

See the [skill instructions](skills/sdd-scaffold/SKILL.md) and the
[workflow template](skills/sdd-scaffold/assets/scaffold/docs/sdd/README.md).
The source project's history is not included in this package.

## Installing on another device

This repository is currently local; no remote repository has been published.
To share it with someone or transfer it to another device, copy the repository
directory or create a Git bundle after the first commit. From the repository root:

```text
git bundle create ../sdd-scaffold.bundle --all
```

Send `sdd-scaffold.bundle` to the recipient. On another device with Git installed,
clone it into a directory that does not already exist:

```text
git clone /path/to/sdd-scaffold.bundle sdd-scaffold
```

Replace `/path/to/sdd-scaffold.bundle` with the actual path to the transferred file.
Then copy the entire `skills/sdd-scaffold` directory into your user skills directory:
`$CODEX_HOME/skills/sdd-scaffold` if `CODEX_HOME` is set, or otherwise
`~/.codex/skills/sdd-scaffold`. On Windows, `~` refers to your user home directory.
Before copying, check that the destination directory does not exist. Back up an
existing skill separately and explicitly decide which version to keep. Do not
merge files into an older version by overwriting them. The repository itself can
be stored anywhere.

Open a new Codex conversation in the target project so the skill is available
for selection.

## Installing after publication on GitHub

If the repository is published, ask Codex to install the skill using its URL:

```text
Use $skill-installer to install the skill from
https://github.com/OWNER/sdd-scaffold/tree/main/skills/sdd-scaffold
```

`OWNER` is the future repository owner's account name. This is an example URL,
not a published repository address. A private repository requires access from
the device performing the installation. The installer does not replace an
existing skill with the same name. For manual installation after publication,
clone the repository and copy the skill directory as described above:

```text
git clone https://github.com/OWNER/sdd-scaffold.git
```

## Usage

Ask:

```text
Create an SDD structure in this project.
```

Or invoke the skill explicitly:

```text
Use $sdd-scaffold to set up this project.
```

The generator supports a preview and requires Python 3:

```text
python3 skills/sdd-scaffold/scripts/scaffold.py --target /path/to/project --dry-run
```

After checking the paths, remove `--dry-run` to create missing files. This command
assumes the repository root is the working directory; use the Python command
available on your system and the actual target project path. The generator does
not overwrite existing files with different contents. If conflicts occur, Codex
first examines the current rules and adds compatible documentation. Conflicting
requirements are referred to the user.

## Environment capabilities

The scaffold preserves these model preferences: Terra 6.1 / xhigh for the
documenter, Sol 6.1 / medium for the analyst, and Luna 6 / ultra for the test writer;
the reviewer inherits the coordinator's model. Check each combination in the
target environment. An unavailable configuration is not silently substituted:
it becomes a question for the user, and the affected role is not started until
that question is resolved.

Markdown files describe agent behavior. They do not register tools, configure
models automatically, or enforce filesystem isolation. Subagent support and
access permissions depend on the environment. Report timestamps default to
Asia/Novokuznetsk (UTC+07:00); this can be explicitly changed before records begin.

Installing this skill does not itself create commits, publish a project,
or import another project's tasks or reports.
