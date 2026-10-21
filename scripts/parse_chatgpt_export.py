#!/usr/bin/env python3
"""Normalize and date-filter ChatGPT conversation exports.

Accept a ChatGPT export ZIP, a conversations JSON file, or a directory that
contains conversations*.json. Emit compact JSON evidence for the requested
local-time period. Semantic task classification remains the skill's job.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter ChatGPT export conversations by a local date period."
    )
    parser.add_argument("source", type=Path, help="Export ZIP, JSON file, or directory")
    parser.add_argument(
        "period", help="today, yesterday, week, month, YYYY-MM-DD, or YYYY-MM"
    )
    parser.add_argument(
        "--timezone",
        help="IANA timezone (default: device local timezone)",
    )
    parser.add_argument("--month", help="Explicit YYYY-MM for period=month")
    parser.add_argument("--now", help="Testing override: ISO-8601 current time")
    parser.add_argument("--output", type=Path, help="Write JSON here instead of stdout")
    return parser.parse_args()


def detect_local_timezone() -> tuple[tzinfo, str]:
    """Return the best available local timezone and a display label."""
    candidates: list[str] = []
    env_tz = os.environ.get("TZ", "").lstrip(":")
    if env_tz:
        candidates.append(env_tz)

    localtime = Path("/etc/localtime")
    try:
        resolved = localtime.resolve()
        marker = "/zoneinfo/"
        if marker in str(resolved):
            candidates.append(str(resolved).split(marker, 1)[1])
    except OSError:
        pass

    timezone_file = Path("/etc/timezone")
    try:
        candidates.append(timezone_file.read_text(encoding="utf-8").strip())
    except OSError:
        pass

    for name in candidates:
        if not name:
            continue
        try:
            return ZoneInfo(name), name
        except (ZoneInfoNotFoundError, ValueError):
            continue

    fallback = datetime.now().astimezone().tzinfo or timezone.utc
    label = getattr(fallback, "key", None) or datetime.now(fallback).tzname() or "UTC"
    return fallback, label


def parse_now(value: str | None, tz: tzinfo) -> datetime:
    if not value:
        return datetime.now(tz)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def month_bounds(year: int, month: int, tz: tzinfo) -> tuple[datetime, datetime]:
    start = datetime.combine(date(year, month, 1), time.min, tzinfo=tz)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return start, datetime.combine(end_date, time.min, tzinfo=tz)


def resolve_period(
    period: str, now: datetime, tz: tzinfo, explicit_month: str | None
) -> tuple[datetime, datetime, str]:
    token = period.strip().lower()
    today = now.date()

    if token == "today":
        start_date, end_date = today, today + timedelta(days=1)
    elif token == "yesterday":
        start_date, end_date = today - timedelta(days=1), today
    elif token in {"week", "weekly"}:
        start_date, end_date = today - timedelta(days=6), today + timedelta(days=1)
    elif token in {"month", "monthly"}:
        month_token = explicit_month or today.strftime("%Y-%m")
        try:
            year, month = map(int, month_token.split("-"))
            start, end = month_bounds(year, month, tz)
        except (ValueError, TypeError) as exc:
            raise ValueError("--month must be YYYY-MM") from exc
        return start, end, month_token
    else:
        try:
            if len(token) == 7:
                year, month = map(int, token.split("-"))
                start, end = month_bounds(year, month, tz)
                return start, end, token
            start_date = date.fromisoformat(token)
            end_date = start_date + timedelta(days=1)
        except ValueError as exc:
            raise ValueError(
                "period must be today, yesterday, week, month, YYYY-MM-DD, or YYYY-MM"
            ) from exc

    start = datetime.combine(start_date, time.min, tzinfo=tz)
    end = datetime.combine(end_date, time.min, tzinfo=tz)
    label = (
        start_date.isoformat()
        if end_date - start_date == timedelta(days=1)
        else f"{start_date.isoformat()} to {(end_date - timedelta(days=1)).isoformat()}"
    )
    return start, end, label


def load_json_bytes(raw: bytes, origin: str) -> list[dict[str, Any]]:
    try:
        value = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not parse {origin}: {exc}") from exc

    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        for key in ("conversations", "items", "data"):
            child = value.get(key)
            if isinstance(child, list):
                return [item for item in child if isinstance(item, dict)]
    raise ValueError(f"Unsupported conversation JSON shape in {origin}")


def load_conversations(source: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    origins: list[str] = []
    if source.is_dir():
        paths = sorted(source.glob("conversations*.json"))
        if not paths:
            raise ValueError(f"No conversations*.json files found in {source}")
        for path in paths:
            records.extend(load_json_bytes(path.read_bytes(), str(path)))
            origins.append(str(path))
        return records, origins

    if not source.exists():
        raise ValueError(f"Source does not exist: {source}")

    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            names = sorted(
                name
                for name in archive.namelist()
                if Path(name).name.startswith("conversations")
                and name.lower().endswith(".json")
            )
            if not names:
                raise ValueError("ZIP contains no conversations*.json files")
            for name in names:
                records.extend(load_json_bytes(archive.read(name), f"{source}!{name}"))
                origins.append(f"{source}!{name}")
        return records, origins

    records.extend(load_json_bytes(source.read_bytes(), str(source)))
    origins.append(str(source))
    return records, origins


def as_epoch(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                return parsed.timestamp()
            except ValueError:
                return None
    return None


def event_time(value: Any, tz: tzinfo) -> datetime | None:
    epoch = as_epoch(value)
    if epoch is None:
        return None
    try:
        return datetime.fromtimestamp(epoch, timezone.utc).astimezone(tz)
    except (OverflowError, OSError, ValueError):
        return None


def stringify_part(part: Any) -> str:
    if isinstance(part, str):
        return part
    if isinstance(part, dict):
        for key in ("text", "caption", "name", "url", "asset_pointer"):
            value = part.get(key)
            if isinstance(value, str) and value.strip():
                return value
        return json.dumps(part, ensure_ascii=False, sort_keys=True)
    return str(part)


def message_text(message: dict[str, Any]) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, dict):
        return ""
    parts = content.get("parts")
    if isinstance(parts, list):
        return "\n".join(filter(None, (stringify_part(part).strip() for part in parts)))
    text = content.get("text")
    return text.strip() if isinstance(text, str) else ""


def iter_messages(conversation: dict[str, Any]) -> Iterable[dict[str, Any]]:
    mapping = conversation.get("mapping")
    if isinstance(mapping, dict):
        nodes: Iterable[Any] = mapping.values()
    else:
        messages = conversation.get("messages")
        nodes = messages if isinstance(messages, list) else []

    for node in nodes:
        if not isinstance(node, dict):
            continue
        message = node.get("message") if "message" in node else node
        if isinstance(message, dict):
            yield message


def normalize_conversation(
    conversation: dict[str, Any], start: datetime, end: datetime, tz: tzinfo
) -> dict[str, Any] | None:
    selected: list[dict[str, Any]] = []
    for message in iter_messages(conversation):
        timestamp = event_time(message.get("create_time") or message.get("update_time"), tz)
        if timestamp is None or not (start <= timestamp < end):
            continue
        author = message.get("author")
        role = author.get("role") if isinstance(author, dict) else message.get("role")
        text = message_text(message)
        if not text and role not in {"tool", "assistant", "user"}:
            continue
        content = message.get("content")
        selected.append(
            {
                "timestamp": timestamp.isoformat(),
                "role": role or "unknown",
                "text": text,
                "content_type": (
                    content.get("content_type") if isinstance(content, dict) else None
                ),
            }
        )

    if not selected:
        return None
    selected.sort(key=lambda item: item["timestamp"])
    return {
        "id": conversation.get("id") or conversation.get("conversation_id"),
        "title": conversation.get("title") or "Untitled conversation",
        "messages": selected,
    }


def main() -> int:
    args = parse_args()
    try:
        if args.timezone:
            tz: tzinfo = ZoneInfo(args.timezone)
            timezone_label = args.timezone
        else:
            tz, timezone_label = detect_local_timezone()
        now = parse_now(args.now, tz)
        start, end, label = resolve_period(args.period, now, tz, args.month)
        raw_records, origins = load_conversations(args.source)
        normalized = [
            item
            for item in (
                normalize_conversation(record, start, end, tz) for record in raw_records
            )
            if item is not None
        ]
    except (ValueError, OSError, zipfile.BadZipFile, ZoneInfoNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    normalized.sort(key=lambda item: item["messages"][0]["timestamp"])
    result = {
        "schema_version": 1,
        "timezone": timezone_label,
        "period": label,
        "start_inclusive": start.isoformat(),
        "end_exclusive": end.isoformat(),
        "source_files": origins,
        "source_conversation_count": len(raw_records),
        "matched_conversation_count": len(normalized),
        "conversations": normalized,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
