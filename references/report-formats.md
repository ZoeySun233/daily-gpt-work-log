# Report formats

## Daily

Use this structure. Replace bracketed text with evidence; never leave placeholders.

```markdown
# Daily GPT Work Log — YYYY-MM-DD

**Timezone:** [IANA timezone and UTC offset at the report interval]

## Overview

Today I completed:

- X completed tasks
- X ongoing tasks
- X major outputs

Main areas:

- [Primary areas actually observed]

## Visual Snapshot

[Compact status mix. Add category mix or an activity timeline only when it reveals a useful pattern.]

## Completed Work

### 1. [Outcome-oriented task name]

**Category:** [one primary category]

**What I did:** [2–4 concise sentences focused on actions and outcome.]

**Output:**

- [Verified file or descriptive deliverable]

**Skills used:**

- [Verified skill]

**Status:** ✅ Completed

## In Progress

- **[Task]** — [Current verified state and remaining gap.] **Status:** 🟡 In Progress

## Paused / Blocked

- **[Task]** — [Why it was paused or the specific blocker.] **Status:** ⏸ Paused / ❌ Blocked

## Deliverables Created

| Deliverable | Type | Related Project |
|---|---|---|
| [Exact filename or accurate description] | [Type] | [Project] |

## Skills Practiced Today

**[Skill family]**

- [Skill]

## Productivity Summary

Tasks completed: X  
Tasks ongoing: X  
Tasks paused: X  
Tasks blocked: X  
[Observed primary category]: X

## Key Achievements

- [3–5 specific outcomes or advances; use fewer if evidence is sparse.]

## Suggested Next Actions

1. [Evidence-based next step from unfinished work.]

## One-line Daily Summary

> [One concrete sentence.]
```

If there are no verified completed tasks, write `None verified` under Completed Work and do not force a Key Achievement. If no tasks are paused or blocked, omit that subsection. If no deliverables are verified, keep the table headers and add `| None verified | — | — |`.

## Weekly

Title: `# Weekly GPT Work Log — YYYY-MM-DD to YYYY-MM-DD`

Include:

Show the report timezone directly below the title.

1. Overview with deduplicated completed, ongoing, paused, blocked, and major-output counts.
2. Visual Snapshot with status mix and a daily trend when at least two dates contain verified activity.
3. Category Breakdown table: `Category | Completed | Ongoing | Total`.
4. Completed Tasks, grouped by project or category.
5. Main Projects with progress and current state.
6. Deliverables table.
7. Skills Practiced, grouped by family.
8. Unfinished Tasks, including blockers or pause reasons.
9. Key Achievements (up to seven).
10. Suggested Next Actions (up to five).
11. One-line Weekly Summary.
12. Data Coverage only when needed.

Deduplicate across all seven days. A task worked on repeatedly is one task with a compact progression summary. Attribute a completion to the day it was evidenced as complete.

## Monthly

Title: `# Monthly GPT Work Log — YYYY-MM`

Include:

Show the report timezone directly below the title.

1. Executive Summary.
2. Visual Snapshot with status mix, weekly trend, and category mix when supported by the data.
3. Category Breakdown table.
4. Major Projects and milestones.
5. Completed Tasks.
6. Deliverables and reusable assets.
7. Skills Practiced and learned.
8. Coursework / Research / Career Progress, including only observed sections.
9. Unfinished, Paused, and Blocked Work.
10. Resume / Portfolio Candidates, clearly separated from confirmed claims.
11. Next-Month Carryover (up to seven evidence-based items).
12. One-line Monthly Summary.
13. Data Coverage only when needed.

Prefer archived daily logs as the monthly source. Use raw history to fill gaps, not to double-count.

## Achievements

Title: `# Achievement Mining — [date range or source]`

For each candidate include:

```markdown
### [Achievement name]

**Source:** [log date(s) and project]  
**Best fit:** Resume / Portfolio / Application / Interview story  
**Evidence:** [What the logs directly establish]  
**Draft statement:** [Action + method + deliverable/outcome]  
**Confidence:** Strong / Moderate / Needs evidence  
**Missing evidence:** [Only when applicable]
```

Then include:

- Top Resume Candidates
- Portfolio Candidates
- Interview Story Seeds using Situation / Task / Action / Result, leaving `Result not recorded` when necessary
- Evidence Gaps to Collect

Do not transform a vague log into a stronger factual claim than its evidence supports.
