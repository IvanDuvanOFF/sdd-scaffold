---
name: sdd-scaffold
description: "Create a universal SDD / Spec-Driven Development structure for Claude Code in a new or existing project: CLAUDE.md coordinator rules, subagents in .claude/agents (documenter, test-analyst, test-writer, reviewer), architecture documentation, assignments, reports, test cases, and templates. Use for requests such as create an SDD structure, set up SDD in this project, create an SDD scaffold, or initialize an SDD scaffold. Not needed for ordinary execution of an already configured SDD workflow."
---

# Creating an SDD structure

Create a documentation scaffold from [assets/scaffold](assets/scaffold/).
It is self-contained: the source project and its history are not required.
Explicit user instructions and existing target project rules take precedence.

## Applying the skill

1. Determine the target root from the request or current working directory.
   Read the applicable CLAUDE.md files (also AGENTS.md if present), existing
   `.claude/agents/`, and existing documentation without accessing secrets.
   Do not choose a stack or invent a product, architecture, or approval of
   requirements.
2. Preview the changes using the absolute path to this skill's directory:

   ```text
   python3 <skill-dir>/scripts/scaffold.py --target <project-dir> --dry-run
   ```

   The generator lists paths to create, identical files, and conflicts. It does
   not write when conflicts exist or traverse symbolic links. It never overwrites
   existing files; running it again does not clear history.
3. If there are no conflicts, run the same command without `--dry-run`. Creating
   the documentation scaffold may be done directly in the main session; this does
   not authorize direct product implementation later.
4. If an existing CLAUDE.md, agent file, or other document differs, inspect the
   differences first. Preserve all project rules and data. Add compatible content
   manually within the request's scope instead of replacing entire documents:
   for example, append the SDD sections to the existing CLAUDE.md, or keep the
   project's CLAUDE.md and import the rules with an `@path` line. If the project
   already has an agent with the same name but a different purpose, ask the user
   rather than overwriting it. Refer substantive requirement conflicts to the user
   when context does not resolve them. Routine creation of missing files needs no
   separate confirmation. Claude Code permissions still apply; this skill does
   not bypass them.
5. Check the `model` and `effort` values in `.claude/agents/*.md` against the
   environment (plan, provider such as Bedrock/Vertex, Claude Code version).
   These are the user's preferences. Do not substitute an unavailable
   configuration. If a combination is known to be unsupported, create a new flag
   with an ID, source, consequences, and closure condition in
   `docs/changelog/flags.md`, notify the user, and do not start that role. If
   availability cannot be checked, state that limitation rather than claiming
   support. Do not import other projects' flags or environment claims.
6. Check local links in generated documents, preservation of existing files, and
   absence of another project's history. Briefly report created paths, validation
   results, and limitations. Remind the user that new subagents become available
   after restarting Claude Code (or via `/agents`).

## Output boundaries

The scaffold contains CLAUDE.md, `.claude/agents/` with documenter, test-analyst,
test-writer, and reviewer, and docs/{architecture,specs,tasks,tests,changelog,
commits,sdd}. Project roles are added as new subagent files using
`docs/sdd/agent-template.md`. Eight templates and the detailed workflow are in
docs/sdd/.

The issues/flags lists initially contain only a heading and purpose description.
Real assignments, specifications, reports, summaries, and commit messages are
created only for current work. A template does not imply completion or approval.
The scaffold request already authorizes its creation; a separate product
specification is not needed for this step. Do not start test-writer just to create
documentation. Do not install dependencies. Do not commit, publish, clear existing
assignments, create or change `.claude/settings*.json`, or change model settings.
Files provide instructions; Claude Code permissions enforce technical limits.
