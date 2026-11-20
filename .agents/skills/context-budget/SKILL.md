---
name: context-budget
description: Use when a Codex task has high token consumption, repeated file scans, many subagents, long tool outputs, or a request to optimize coding-agent context, cost, and delegation.
---
# Context budget — fast, balanced, deep

1. Start from the goal and observable acceptance criteria. Avoid re-reading project files already summarized with evidence.
2. Pick FAST (main agent only) for localized edits; BALANCED (1–2 subagents) for independent specialist checks; DEEP (up to 3 concurrent) for multi-area or high-risk work. Do not launch agents purely to simulate organizational roles.
3. Delegate with a bounded question, directories/files, non-goals, and response cap: **max 8 bullets, path:line for findings, test evidence**.
4. Inspect file names first, then focused symbols/sections (`rg`, `git diff --stat`, file-range reads), not entire repositories or unfiltered logs.
5. Prefer executable tests, static checks and concise diffs to long narrative reports.
6. If a thread is bloated, write `HANDOFF.md` with goal, current branch, changed paths, passing/failing commands, known blockers, remaining next actions. Resume with fresh focused context.
7. Never promise a fixed percentage of token reduction. Record input/output tokens when the runtime exposes them, as well as duration and outcome; compare equivalent tasks.

**Output:** mode chosen; active agents; context risk; tests run; next action.
