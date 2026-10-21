# Evidence, task identity, status, and counting

## Evidence hierarchy

Use the strongest evidence available.

1. **Verified output:** file/artifact creation or edit, completed tool result, submitted form confirmation, executed analysis, or inspectable deliverable.
2. **Explicit completion:** the user or final response clearly states the scoped task was finished, with enough context to identify the outcome.
3. **Concrete progress:** draft, partial analysis, code change, debugging attempt, or intermediate result without completion evidence.
4. **Discussion only:** advice, brainstorming, explanation, planning, example text, or a proposed workflow.

Assistant statements such as “I will create…” are not completion evidence. A final answer that links or names a verified artifact is stronger than a generic completion claim.

## Task identity

Represent each candidate task internally as:

```text
project: normalized project/client/course/application
goal: intended outcome
output: verified or expected deliverable
date_events: evidence inside the report interval
sources: contributing task/conversation/log identifiers
```

Normalize aliases, spelling variants, languages, and abbreviations when context proves they refer to the same entity. For example, `P&G`, `宝洁`, and `Procter & Gamble` may identify one project; the name match alone is not enough.

Merge candidates when `project + goal + output` describe one continuous outcome. Two strong matching dimensions plus compatible context are normally sufficient. Keep them separate when:

- the deliverables serve different goals;
- the same course contains separate assignments;
- the same employer has different applications or interview stages;
- one task consumes another task's output but has a distinct outcome.

If one conversation contains multiple material goals, split it. If several conversations refine one deliverable, merge them.

## Status rules

- `✅ Completed`: the scoped outcome is delivered, executed, submitted, or explicitly finished. Use only evidence levels 1–2.
- `🟡 In Progress`: concrete work occurred, but the intended outcome remains unfinished or completion is unverified.
- `⏸ Paused`: the record explicitly shows the task was intentionally deferred, stopped, or deprioritized without an active blocking condition.
- `❌ Blocked`: the record shows a specific unresolved dependency, permission, missing input, external decision, or technical failure preventing progress.

Do not mark a task blocked merely because it is hard or incomplete. If a task moves from progress to completion during the interval, count it once as completed and summarize the progression. If evidence conflicts, prefer later timestamped evidence; otherwise use the more conservative status and mention the uncertainty.

## Deliverables

A deliverable can be a file or a non-file output such as an analysis, decision memo, notes set, model, query, application response, or presentation script.

- Use an exact filename only when evidenced.
- Otherwise use a precise description, such as `ATS-focused resume draft`.
- Do not count the same artifact twice because it appears in both a tool event and final message.
- Distinguish `created`, `updated`, `analyzed`, and `discussed` when material.

## Skills

List a skill only when the user practiced or applied it during the interval. Evidence can include code execution, tool usage, analysis steps, deliverable content, or explicit learning work.

Do not infer a skill from:

- a job description keyword;
- a requested example;
- a file name alone;
- an assistant recommendation not acted upon;
- background information copied into a resume.

Group skills into useful families such as Programming, Data Science, Biomedical/Research, Writing, and Career. Omit empty families.

## Counts

- Completed/ongoing/paused/blocked counts are counts of deduplicated tasks.
- Category counts use one primary category per task.
- Major outputs are unique, meaningful deliverables, not every intermediate file.
- Do not estimate time from message counts, timestamps, token volume, or tool duration.
- When source coverage is partial, counts describe the observed source set, not the user's entire day.

## Achievement value

Rank key achievements using evidenced dimensions:

- completed outcome;
- substantive deliverable;
- technical or domain complexity;
- usefulness for coursework, project progress, career, or portfolio;
- clear advancement of previously unfinished work.

Never award value based on invented impact.
