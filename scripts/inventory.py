#!/usr/bin/env python3
"""
inventory.py — ChatGPT conversation export inventory script.

Discovers all conversations-*.json files in a given export directory,
aggregates statistics across all chunks, and writes a Markdown report
to the repo root.

Schema confirmed (2026-05-19):
  - conversation.create_time       → Unix timestamp (float)
  - conversation.default_model_slug → model name string or None
  - mapping node.message           → None (root nodes) or message dict
  - message.author.role            → "user" | "assistant" | "system" | "tool"
  - message.metadata.model_slug    → model name string or None

Usage:
    python scripts/inventory.py --export-dir /path/to/chatgpt/export

Output:
    inventory_report.md at the repo root
    Progress printed to stdout per file processed
"""

import argparse
import json
import sys
import warnings
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = REPO_ROOT / "inventory_report.md"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory a ChatGPT conversation export directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--export-dir",
        required=True,
        type=Path,
        metavar="DIR",
        help="Absolute path to the folder containing conversations-*.json files",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Schema traversal
# ---------------------------------------------------------------------------

def iter_messages(mapping: dict) -> Iterator[dict]:
    """Yield non-null message dicts from a conversation's mapping tree."""
    for node in mapping.values():
        msg = node.get("message")
        if msg is not None:
            yield msg


def get_conversation_model(conv: dict) -> str:
    """
    Determine the primary model for a conversation.

    Uses default_model_slug from the conversation object when available.
    Falls back to the most common non-null model_slug across assistant
    messages in the mapping tree. Returns "unknown" if neither is found.
    """
    slug = conv.get("default_model_slug")
    if slug:
        return slug

    mapping = conv.get("mapping")
    if not isinstance(mapping, dict):
        return "unknown"

    slug_counts: Counter = Counter()
    for msg in iter_messages(mapping):
        try:
            role = msg["author"]["role"]
            msg_slug = msg["metadata"]["model_slug"]
            if role == "assistant" and msg_slug:
                slug_counts[msg_slug] += 1
        except (KeyError, TypeError):
            pass

    return slug_counts.most_common(1)[0][0] if slug_counts else "unknown"


def process_conversation(conv: dict, source_file: str) -> Optional[dict]:
    """
    Extract per-conversation statistics from a single conversation object.

    Returns a dict with aggregated counts, or None if the conversation
    is structurally invalid (a warning is emitted in that case).

    Return schema:
        message_count  : int
        roles          : Counter[str, int]
        create_time    : float | None
        model          : str
    """
    conv_id = conv.get("id", "<no-id>")
    mapping = conv.get("mapping")

    if not isinstance(mapping, dict):
        warnings.warn(
            f"[{source_file}] Conversation {conv_id!r} has no valid mapping — skipped."
        )
        return None

    roles: Counter = Counter()
    message_count = 0

    for msg in iter_messages(mapping):
        message_count += 1
        try:
            role = msg["author"]["role"]
            roles[role] += 1
        except (KeyError, TypeError):
            roles["unknown"] += 1

    return {
        "message_count": message_count,
        "roles": roles,
        "create_time": conv.get("create_time"),
        "model": get_conversation_model(conv),
    }


# ---------------------------------------------------------------------------
# File-level processing
# ---------------------------------------------------------------------------

def process_file(path: Path) -> dict:
    """
    Load and process one conversations-*.json chunk.

    Returns a summary dict:
        conv_count    : int
        msg_count     : int
        roles         : Counter[str, int]
        models        : Counter[str, int]   (one entry per conversation)
        timestamps    : list[float]         (create_time values, non-null only)
        skipped       : int                 (conversations with invalid structure)
    """
    summary = {
        "conv_count": 0,
        "msg_count": 0,
        "roles": Counter(),
        "models": Counter(),
        "timestamps": [],
        "skipped": 0,
    }

    with path.open(encoding="utf-8") as fh:
        try:
            conversations = json.load(fh)
        except json.JSONDecodeError as exc:
            warnings.warn(f"[{path.name}] JSON parse error — file skipped. {exc}")
            return summary

    if not isinstance(conversations, list):
        warnings.warn(f"[{path.name}] Expected a JSON array at top level — file skipped.")
        return summary

    for conv in conversations:
        stats = process_conversation(conv, path.name)
        if stats is None:
            summary["skipped"] += 1
            continue

        summary["conv_count"] += 1
        summary["msg_count"] += stats["message_count"]
        summary["roles"] += stats["roles"]
        summary["models"][stats["model"]] += 1

        if stats["create_time"] is not None:
            summary["timestamps"].append(stats["create_time"])

    return summary


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def ts_to_date(ts: float) -> str:
    """Convert a Unix timestamp to a human-readable UTC date string."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def format_number(n: int) -> str:
    return f"{n:,}"


def build_report(
    file_results: list[tuple[str, dict]],
    total_files: int,
    total_convs: int,
    total_msgs: int,
    all_roles: Counter,
    all_models: Counter,
    all_timestamps: list[float],
) -> str:
    """Render the full Markdown inventory report as a string."""
    lines: list[str] = []

    lines.append("# ChatGPT Export — Inventory Report")
    lines.append("")
    lines.append(
        f"Generated: {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
    )
    lines.append("")

    # --- Overall summary ---
    lines.append("## Overall Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Conversation files processed | {format_number(total_files)} |")
    lines.append(f"| Total conversations | {format_number(total_convs)} |")
    lines.append(f"| Total messages | {format_number(total_msgs)} |")

    avg = round(total_msgs / total_convs, 1) if total_convs else 0
    lines.append(f"| Average messages per conversation | {avg} |")

    if all_timestamps:
        lines.append(f"| Earliest conversation | {ts_to_date(min(all_timestamps))} |")
        lines.append(f"| Latest conversation | {ts_to_date(max(all_timestamps))} |")
    else:
        lines.append(f"| Earliest conversation | N/A |")
        lines.append(f"| Latest conversation | N/A |")

    lines.append("")

    # --- Conversations per model ---
    lines.append("## Conversations per Model")
    lines.append("")
    lines.append("| Model | Conversations | % |")
    lines.append("|-------|--------------|---|")
    for model, count in all_models.most_common():
        pct = round(count / total_convs * 100, 1) if total_convs else 0
        lines.append(f"| {model} | {format_number(count)} | {pct}% |")
    lines.append("")

    # --- Messages by author role ---
    lines.append("## Messages by Author Role")
    lines.append("")
    lines.append("| Role | Messages | % |")
    lines.append("|------|---------|---|")
    total_role_msgs = sum(all_roles.values())
    for role, count in all_roles.most_common():
        pct = round(count / total_role_msgs * 100, 1) if total_role_msgs else 0
        lines.append(f"| {role} | {format_number(count)} | {pct}% |")
    lines.append("")

    # --- Per-file breakdown ---
    lines.append("## Per-File Breakdown")
    lines.append("")
    lines.append("| File | Conversations | Messages | Avg Msg/Conv |")
    lines.append("|------|--------------|---------|--------------|")
    for fname, result in file_results:
        c = result["conv_count"]
        m = result["msg_count"]
        a = round(m / c, 1) if c else 0
        lines.append(f"| {fname} | {format_number(c)} | {format_number(m)} | {a} |")
    lines.append("")

    lines.append("---")
    lines.append("*Generated by `scripts/inventory.py` from the ai-human-observatory.*")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    export_dir = args.export_dir.resolve()

    if not export_dir.is_dir():
        print(f"Error: export directory does not exist: {export_dir}", file=sys.stderr)
        sys.exit(1)

    chunk_files = sorted(export_dir.glob("conversations-*.json"))

    if not chunk_files:
        print(
            f"No files matching conversations-*.json found in {export_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Found {len(chunk_files)} conversation file(s) in {export_dir}")
    print()

    # Aggregate across all files
    file_results: list[tuple[str, dict]] = []
    total_convs = 0
    total_msgs = 0
    all_roles: Counter = Counter()
    all_models: Counter = Counter()
    all_timestamps: list[float] = []

    for chunk_path in chunk_files:
        result = process_file(chunk_path)
        file_results.append((chunk_path.name, result))

        total_convs += result["conv_count"]
        total_msgs += result["msg_count"]
        all_roles += result["roles"]
        all_models += result["models"]
        all_timestamps.extend(result["timestamps"])

        print(
            f"  Processing {chunk_path.name}... "
            f"{format_number(result['conv_count'])} conversations, "
            f"{format_number(result['msg_count'])} messages"
        )

    print()
    print(f"Total: {format_number(total_convs)} conversations, {format_number(total_msgs)} messages")
    print()

    report = build_report(
        file_results=file_results,
        total_files=len(chunk_files),
        total_convs=total_convs,
        total_msgs=total_msgs,
        all_roles=all_roles,
        all_models=all_models,
        all_timestamps=all_timestamps,
    )

    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
