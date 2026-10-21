# Work-log visualizations

Use visuals to expose patterns already supported by the evidence. The prose remains the authoritative explanation.

## Shared rules

- Build every chart from the final deduplicated task set and status/category assignments.
- Show exact counts beside marks. A bar without a number is insufficient.
- Use Markdown tables and Unicode text bars by default so archived logs remain portable and readable without rendering support.
- Keep a text label for every series; never encode meaning by color alone.
- Label zero as `0`; do not draw a minimum-width bar that suggests activity.
- Percentages describe observed tasks only. Round to whole percentages and allow the displayed total to differ from 100% by one point because of rounding.
- Do not visualize time spent, productivity, impact, completion percentage, or activity gaps unless the source directly records those values.
- A completed-task count belongs to the local date on which completion was evidenced. Other verified work can appear as activity or progress without being counted as a completion.
- Use no more than three compact visuals in a daily report and four in a weekly or monthly report. Omit a chart when all it adds is one number.

## Text bars

Use a consistent width of 12 cells within one chart. Scale each bar to the largest value in that chart; show the absolute value and, for distributions, the share of the total.

```text
Status mix · 6 tasks
✅ Completed    ████████████  3 (50%)
🟡 In Progress ████████░░░░  2 (33%)
❌ Blocked     ████░░░░░░░░  1 (17%)
```

For a single-item distribution, prefer a sentence or KPI table instead of a full bar chart.

## Visual selection

### Daily

Use a status mix when at least two tasks are verified. Add one of these only when useful:

- category mix for two or more categories;
- local-time activity timeline for three or more timestamped work events spanning at least two dayparts;
- project progress table when two or more active projects have distinct states.

For a timeline, aggregate into `00–05`, `06–11`, `12–17`, and `18–23` in the report timezone. Count verified work events, not messages, and state the unit as `events`.

### Weekly

Use a status mix and a seven-row daily trend. The trend should show verified completions and other progress events as separate columns. Use local calendar dates and include zero-activity dates only when source coverage for those dates is known to be complete.

### Monthly

Use a status mix, category mix, and week-by-week trend. Bucket weeks by their local-date intersections with the month and label partial weeks with explicit date ranges. Add a project milestone table only when it helps distinguish several projects.

### Achievements

Do not add decorative charts by default. A confidence matrix (`Strong`, `Moderate`, `Needs evidence`) is useful when there are at least four candidates.

## Image charts

Create PNG or SVG charts only when requested or when the report is being delivered as a visual document. Preserve the same exact counts and accompany each image with a small source table or concise textual summary. Store user-facing chart files beside the archived report when saving; do not embed private conversation text in chart metadata.
