# Daily GPT Work Log

一个面向 Codex / ChatGPT 工作记录的个人 Skill。它能够根据可访问的聊天、任务、文件和导出数据，生成基于证据、带可视化摘要的日报、周报和月报。

## 功能特点

- 生成每日、每周和每月工作日志
- 自动识别已完成、进行中、暂停和阻塞任务
- 合并重复任务，避免重复计数
- 整理已创建或更新的交付物
- 总结当天使用和练习的技能
- 生成状态分布、分类占比和工作趋势图
- 从历史日志中提炼简历、作品集和面试素材
- 严格区分已完成工作、实际进展和单纯讨论
- 不虚构文件、数据、效果、工时或业务影响

## 安装

将仓库克隆到 Codex 的个人 skills 目录：

```bash
git clone https://github.com/ZoeySun233/daily-gpt-work-log.git \
  ~/.codex/skills/daily-gpt-work-log
```

安装后重新打开 Codex，或开始一个新对话。

也可以将它作为项目级 Skill 使用：

```text
your-project/
└── .codex/
    └── skills/
        └── daily-gpt-work-log/
```

## 本地时间支持

Skill 会优先使用 Codex 客户端提供的本地时区。

时区解析顺序：

1. 用户明确指定的时区
2. Codex 客户端提供的本地时区
3. 设备或运行环境的本地时区
4. 无法确定时才使用 UTC

所有聊天时间都会先转换到本地时区，再进行今日、昨日、周和月的筛选。

报告会显示实际使用的 IANA 时区和 UTC 偏移，例如：

```text
Timezone: Asia/Singapore (UTC+08:00)
```

## 可视化能力

日志默认使用便于阅读和归档的 Markdown 表格及 Unicode 图表：

```text
Status mix · 3 tasks
✅ Completed    ████████░░░░  2 (67%)
🟡 In Progress ████░░░░░░░░  1 (33%)
```

支持的可视化包括：

- 任务状态分布
- 工作分类占比
- 本地时间活动时段
- 每周每日趋势
- 月度分周趋势
- 项目进度表
- 成就证据置信度矩阵

图表与正文使用同一份去重后的任务数据，不会根据消息数量推测生产力或工作时长。


## 使用方法

在 Codex 中输入：

```text
$daily-gpt-work-log daily-log today
```

其他示例：

```text
$daily-gpt-work-log daily-log yesterday
$daily-gpt-work-log daily-log 2026-10-22
$daily-gpt-work-log daily-log week
$daily-gpt-work-log daily-log month
$daily-gpt-work-log daily-log month 2026-10
$daily-gpt-work-log daily-log achievements
```

也可以直接使用自然语言：

```text
帮我生成今天的工作日志。
```

```text
总结本周完成的工作，并显示工作趋势。
```

```text
从历史工作日志中提炼适合写进简历的成果。
```

## ChatGPT 导出数据

当无法直接访问完整聊天历史时，可以分析 ChatGPT 导出的 ZIP 或 `conversations.json`：

```bash
python3 scripts/parse_chatgpt_export.py export.zip today \
  --timezone Asia/Singapore
```

不指定 `--timezone` 时，脚本会尝试使用设备的本地时区。

支持的时间范围：

```text
today
yesterday
week
month
YYYY-MM-DD
YYYY-MM
```

解析脚本要求 Python 3.9 或更高版本，并且只使用 Python 标准库。

## 文件结构

```text
daily-gpt-work-log/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── data-sources.md
│   ├── evidence-and-dedup.md
│   ├── example-daily-log.md
│   ├── report-formats.md
│   └── visualizations.md
└── scripts/
    └── parse_chatgpt_export.py
```


## 输出原则

本 Skill 遵循以下原则：

- 只记录证据能够支持的工作
- 一个任务代表一个连贯成果，而不是一条消息
- 同一任务出现在多个来源时只计算一次
- 计划和建议不等于已经完成
- 没有完成证据时标记为进行中
- 不根据聊天数量估算工作时间
- 不把讨论过的想法写成实际成果
