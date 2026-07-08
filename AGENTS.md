# Agent Instructions

## Tasks drive all work

- Every change maps to exactly one task in the Backlog.md system
  (backlog/). No task, no edits.
- Asked to change something without a task: create one first
  (`backlog task create "Title" -d "..." --ac "..."`), then work it.
- Implement exactly what the task states. Discovered work and new ideas
  become new tasks, not scope expansion.
- If a task is ambiguous or conflicts with the code, stop and report; do
  not guess.

## Task workflow

1. Read: `backlog task <id> --plain`
2. Claim: `backlog task edit <id> -s "In Progress" -a @<your-name>`
3. Implement.
4. Verify each acceptance criterion: `backlog task edit <id> --check-ac <n>`
5. Summarize changes: `backlog task edit <id> --notes "..."`
6. Close: `backlog task edit <id> -s Done`

Select work with `backlog task list -s "To Do" --plain`. Skip tasks whose
dependencies are not Done; never select Deferred tasks. Blocked mid-task:
record the blocker in a comment, return the task to To Do, report; only
the owner sets Deferred. Never edit files under backlog/ by hand; use the
CLI. Detailed guidance: `backlog instructions overview`.

## Decisions

- Architectural and design decisions are recorded with
  `backlog decision create`, one per decision. Do not encode them in this
  file, CLAUDE.md, README, or documents; those link to the decision by id.
- A decision is never rewritten to reverse it: supersede it with a new
  record that references the old one. See docs/decision-records.md.

## Editing code

- When replacing working logic, keep the old code commented out, marked
  with the task id (`// task-42: superseded`). Use judgment: dead code,
  typos, renames, and generated files are edited normally. Commented-out
  blocks are removed only by a dedicated cleanup task.
- Match the style, naming, and structure of the surrounding code.
- No new dependencies and no new top-level files or directories unless the
  task states them.
- Commits: Conventional Commits `type(scope): <imperative summary>
  (task-<id>)`; types feat, fix, refactor, docs, test, chore, perf.
  Exactly one commit per task. Do not push.

## Language

- Everything in English: code, comments, commits, tasks, documentation.
- Documentation reads as a technical specification: concise, factual, no
  emoji, no marketing, no first person, no attribution of decisions to
  people.
- Neutral wording only: describe technical behavior; never reference
  countries, jurisdictions, politics, or the motivations of users.

## Boundaries

- local/ is untracked scratch space; secrets live only there. Never commit
  it or reference it from tracked files.
- Do not modify the agent instruction file (AGENTS.md or CLAUDE.md),
  .gitignore, or backlog/config.yml unless the task requires it.
