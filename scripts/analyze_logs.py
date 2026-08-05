#!/usr/bin/env python3
"""Analyze Java simulation server logs for runtime warning patterns.

Usage:
    python scripts/analyze_logs.py logs --out data/generated

The script extracts counts from text logs. Spark TPS/MSPT values are not decoded
from .sparkprofile binaries here; use data/spark_metrics.csv for
the retained screenshot-based Spark metrics.
"""
from pathlib import Path
import argparse, csv, re

def read(path):
    return Path(path).read_text(encoding="utf-8", errors="ignore")

def count(pattern, text, flags=re.I):
    return len(re.findall(pattern, text, flags))

def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    fields = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def parse_log(path):
    text = read(path)
    overloads = re.findall(
        r"\[(\d{2}:\d{2}:\d{2})\].*?Can't keep up! Is the server overloaded\? Running\s+(\d+)ms\s+or\s+(\d+)\s+ticks behind",
        text,
        flags=re.I
    )
    delays = [int(ms) for _, ms, _ in overloads]
    ticks = [int(t) for _, _, t in overloads]

    return {
        "file": str(path),
        "overload_warning_count": len(overloads),
        "max_tick_delay_ms": max(delays) if delays else "",
        "total_tick_delay_ms": sum(delays) if delays else 0,
        "max_ticks_behind": max(ticks) if ticks else "",
        "total_ticks_behind": sum(ticks) if ticks else 0,
        "template_pool_warning_count": count(r"Non-existent template pool reference", text),
        "view_range_warning_count": count(r"Ignoring chunk since it's not in the view range", text),
        "sound_openal_error_count": count(r"OpenAL error AL_INVALID_VALUE|Sound engine/ERROR", text),
        "dimension_save_mention_count": count(r"Saving chunks for level", text),
        "structure_search_mention_count": count(r"Found Structure:|Searching for closest structure|worldgen/structure", text),
        "block_entity_warning_count": count(r"Tried to access a block entity before it was created", text),
        "maplike_selector_error_count": count(r"No key selector in MapLike", text),
        "exception_or_error_count": count(r"\bException\b|\bERROR\b|Crash Report", text),
    }

def parse_overload_events(path):
    text = read(path)
    rows = []
    events = re.findall(
        r"\[(\d{2}:\d{2}:\d{2})\].*?Can't keep up! Is the server overloaded\? Running\s+(\d+)ms\s+or\s+(\d+)\s+ticks behind",
        text,
        flags=re.I
    )
    for i, (event_time, delay_ms, ticks_behind) in enumerate(events, start=1):
        rows.append({
            "file": str(path),
            "event_index": i,
            "event_time": event_time,
            "delay_ms": int(delay_ms),
            "ticks_behind": int(ticks_behind),
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log_dir", type=Path)
    ap.add_argument("--out", type=Path, default=Path("data/generated_from_script"))
    args = ap.parse_args()

    logs = sorted([p for p in args.log_dir.rglob("*.txt") if p.is_file()])
    summaries = [parse_log(p) for p in logs]
    events = []
    for p in logs:
        events.extend(parse_overload_events(p))

    write_csv(args.out / "log_summary.csv", summaries)
    write_csv(args.out / "overload_events.csv", events)
    print(f"Analyzed {len(logs)} log files")
    print(f"Wrote {args.out / 'log_summary.csv'}")
    print(f"Wrote {args.out / 'overload_events.csv'}")

if __name__ == "__main__":
    main()
