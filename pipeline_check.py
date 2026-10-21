#!/usr/bin/env python3
"""Validate a batch of Python API/data-pipeline events."""
import argparse
import json
from datetime import datetime

REQUIRED = {"event_id", "source", "event_type", "occurred_at", "payload"}


def parse_time(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def validate_events(events):
    errors = []
    seen = set()
    previous_time = None
    for index, event in enumerate(events):
        missing = REQUIRED - set(event)
        if missing:
            errors.append(f"events[{index}] missing {', '.join(sorted(missing))}")
            continue
        if event["event_id"] in seen:
            errors.append(f"events[{index}] duplicate event_id {event['event_id']}")
        seen.add(event["event_id"])
        occurred = parse_time(event["occurred_at"])
        if occurred is None:
            errors.append(f"events[{index}] invalid occurred_at")
        elif previous_time and occurred < previous_time:
            errors.append(f"events[{index}] out of order")
        previous_time = occurred or previous_time
        if not isinstance(event["payload"], dict) or not event["payload"]:
            errors.append(f"events[{index}] payload must be a non-empty object")
    return errors


def summarize(events):
    by_source = {}
    for event in events:
        by_source[event.get("source", "unknown")] = by_source.get(event.get("source", "unknown"), 0) + 1
    return {"events": len(events), "sources": by_source, "errors": validate_events(events)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("events_json")
    args = parser.parse_args()
    with open(args.events_json, encoding="utf-8") as handle:
        result = summarize(json.load(handle))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
