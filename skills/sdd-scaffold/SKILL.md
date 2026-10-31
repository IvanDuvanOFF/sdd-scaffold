---
name: sdd-scaffold
description: "Create a universal SDD / Spec-Driven Development structure in a new or existing project: coordinator and subagent rules, architecture documentation, assignments, reports, test cases, and templates. Use for requests such as create an SDD structure, set up SDD in this project, create an SDD scaffold, or initialize an SDD scaffold. Not needed for ordinary execution of an already configured SDD workflow."
---

# Creating an SDD structure

Create a documentation scaffold from [assets/scaffold](assets/scaffold/).
It is self-contained: the source project and its history are not required.
Explicit user instructions and existing target project rules take precedence.

## Applying the skill

1. Determine the target root from the request or current working directory.
   Read applicable AGENTS.md files and existing documentation without accessing
   secrets. Do not choose a stack or invent a product, architecture, or approval
   of requirements.
2. Preview the changes using the absolute path to this skill:

   ```text
   python3 <skill-dir>/scripts/scaffold.py --target <project-dir> --dry-run
   ```

   The generator lists paths to create, identical files, and conflicts. It does
   not write when conflicts exist or traverse symbolic links. It never overwrites
   existing files; running it again does not clear history.
3. If there are no conflicts, run the same command without `--dry-run`. When
   subagents are available, delegate creation to an executor with an explicit
   scope: provide this skill, the target root, allowed files, and expected result.
   If subagent tools are unavailable, disclose that limitation. The documentation
   scaffold may be prepared directly; this does not authorize direct product
   implementation.
4. If existing AGENTS.md or other documents differ, inspect the differences first.
   Preserve all project rules and data. Add compatible content manually within
   the request's scope instead of replacing entire documents. Refer substantive
   requirement conflicts to the user when context does not resolve them. Routine
   creation of missing files needs no separate confirmation. Environment
   permissions still apply; this skill does not bypass sandbox or access approvals.
5. Check the models and reasoning levels selected in AGENTS.md against the target
   environment's tools. These are user preferences, not applied runtime settings.
   Do not substitute an unavailable configuration. If a combination is known to
   be unsupported, create a new flag with an ID, source, consequences, and closure
   condition in `docs/changelog/flags.md`, notify the user, and do not start that
   role. If availability cannot be checked, state that limitation rather than
   claiming support. Do not import other projects' flags or environment claims.
6. Check local links in generated documents, preservation of existing files, and
   absence of another project's history. Briefly report created paths, validation
   results, and limitations.

## Output boundaries

The scaffold contains AGENTS.md and docs/{architecture,agents,specs,tasks,tests,
changelog,commits,sdd}. Complete rules for documenter, test-analyst, test-writer,
and reviewer are in the root AGENTS.md; new project roles belong in docs/agents/.
Eight templates and the detailed workflow are in docs/sdd/.

The issues/flags lists initially contain only a heading and purpose description.
Real assignments, specifications, reports, summaries, and commit messages are
created only for current work. A template does not imply completion or approval.
The scaffold request already authorizes its creation; a separate product
specification is not needed for this step. Do not start test-writer just to create
documentation. Do not install dependencies. Do not commit, publish, clear existing
assignments, or change model settings. Files provide instructions; the environment
enforces technical permissions.
