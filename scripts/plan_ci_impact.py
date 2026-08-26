#!/usr/bin/env python3
"""Produce a deterministic, fail-closed CI impact plan without skipping checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = Path(".github/ci/verification-impact-map.v2.json")
MAP_SCHEMA = "gis-ai-go.ci-impact-map.v2"
PLAN_SCHEMA = "gis-ai-go.ci-impact-plan.v2"
GATEWAY_IMAGE_LANE = "gateway_image"
COMMIT = re.compile(r"^[0-9a-f]{40}$")
LANE_ID = re.compile(r"^[a-z][a-z0-9_-]*$")
RULE_ID = re.compile(r"^[a-z][a-z0-9-]*$")
MAX_MAP_BYTES = 1024 * 1024
MAX_CHANGED_PATHS = 20_000
MAX_DIFF_BYTES = 64 * 1024 * 1024
MAX_PATH_BYTES = 4_096
ALLOWED_EVENTS = frozenset({"pull_request", "push_main"})


class ImpactPlanError(ValueError):
    """Raised when an impact plan cannot be produced safely."""


@dataclass(frozen=True)
class Lane:
    lane_id: str
    description: str
    events: tuple[str, ...]
    depends_on: tuple[str, ...]


@dataclass(frozen=True)
class Rule:
    rule_id: str
    description: str
    patterns: tuple[str, ...]
    lanes: tuple[str, ...]
    force_full: bool
    matchers: tuple[re.Pattern[str], ...]


@dataclass(frozen=True)
class ImpactMap:
    digest: str
    always_run: tuple[str, ...]
    lanes: tuple[Lane, ...]
    full_lanes: tuple[str, ...]
    push_main_policy: str
    rules: tuple[Rule, ...]


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ImpactPlanError(f"impact map contains duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_json_constant(value: str) -> object:
    raise ImpactPlanError(f"impact map contains non-standard JSON constant: {value}")


def _closed_object(value: object, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ImpactPlanError(f"{label} must be an object")
    observed = set(value)
    if observed != keys:
        missing = sorted(keys - observed)
        extra = sorted(observed - keys)
        raise ImpactPlanError(f"{label} keys are not closed; missing={missing}, extra={extra}")
    return value


def _string(value: object, label: str, *, maximum: int = 240) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        raise ImpactPlanError(f"{label} must be a non-empty string of at most {maximum} characters")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ImpactPlanError(f"{label} contains a control character")
    return value


def _string_list(value: object, label: str, *, maximum: int = 256) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or len(value) > maximum:
        raise ImpactPlanError(f"{label} must be a non-empty bounded array")
    items = tuple(_string(item, f"{label} item", maximum=MAX_PATH_BYTES) for item in value)
    if len(items) != len(set(items)):
        raise ImpactPlanError(f"{label} contains a duplicate")
    if items != tuple(sorted(items)):
        raise ImpactPlanError(f"{label} must be sorted")
    return items


def _validate_repository_path(value: str, label: str = "changed path") -> str:
    encoded = value.encode("utf-8")
    if not encoded or len(encoded) > MAX_PATH_BYTES:
        raise ImpactPlanError(f"{label} has an invalid byte length")
    if value.startswith("/") or value.endswith("/") or "\\" in value:
        raise ImpactPlanError(f"{label} is not a canonical repository-relative path")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ImpactPlanError(f"{label} contains a control character")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ImpactPlanError(f"{label} contains an unsafe path component")
    return value


def _validate_pattern(value: str) -> str:
    _validate_repository_path(value, "impact pattern")
    if any(character in value for character in "?[]{}") or "***" in value:
        raise ImpactPlanError(f"impact pattern uses unsupported syntax: {value}")
    for part in value.split("/"):
        if "**" in part and part != "**":
            raise ImpactPlanError(f"recursive wildcard must occupy one path component: {value}")
    return value


def _compile_pattern(pattern: str) -> re.Pattern[str]:
    fragments: list[str] = ["^"]
    index = 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            fragments.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            fragments.append(".*")
            index += 2
        elif pattern[index] == "*":
            fragments.append("[^/]*")
            index += 1
        else:
            fragments.append(re.escape(pattern[index]))
            index += 1
    fragments.append("$")
    return re.compile("".join(fragments))


def _validate_dependency_graph(lanes: tuple[Lane, ...]) -> None:
    by_id = {lane.lane_id: lane for lane in lanes}
    for lane in lanes:
        for dependency in lane.depends_on:
            if dependency not in by_id:
                raise ImpactPlanError(
                    f"lane {lane.lane_id} has unknown dependency {dependency}"
                )
            if dependency == lane.lane_id:
                raise ImpactPlanError(f"lane {lane.lane_id} depends on itself")
            if not set(lane.events).issubset(by_id[dependency].events):
                raise ImpactPlanError(
                    f"lane {lane.lane_id} dependency {dependency} is not available "
                    "for every consumer event"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(lane_id: str) -> None:
        if lane_id in visiting:
            raise ImpactPlanError("lane dependency graph contains a cycle")
        if lane_id in visited:
            return
        visiting.add(lane_id)
        for dependency in by_id[lane_id].depends_on:
            visit(dependency)
        visiting.remove(lane_id)
        visited.add(lane_id)

    for lane_id in sorted(by_id):
        visit(lane_id)


def _read_bounded_regular_file(path: Path) -> bytes:
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise ImpactPlanError(f"impact map is missing: {path}") from error
    if not stat.S_ISREG(metadata.st_mode) or path.is_symlink():
        raise ImpactPlanError("impact map must be a regular file, not a link")
    if metadata.st_size > MAX_MAP_BYTES:
        raise ImpactPlanError("impact map exceeds the byte limit")
    return path.read_bytes()


def load_impact_map(path: Path) -> ImpactMap:
    raw = _read_bounded_regular_file(path)
    try:
        document = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ImpactPlanError("impact map is not valid UTF-8 JSON") from error
    root = _closed_object(
        document,
        {
            "schema",
            "mode",
            "unknown_path_policy",
            "push_main_policy",
            "always_run",
            "lanes",
            "full_lanes",
            "rules",
        },
        "impact map",
    )
    if root["schema"] != MAP_SCHEMA:
        raise ImpactPlanError(f"unsupported impact map schema: {root['schema']!r}")
    if root["mode"] != "shadow":
        raise ImpactPlanError("the impact map must remain in shadow mode until separately promoted")
    if root["unknown_path_policy"] != "full":
        raise ImpactPlanError("unknown paths must select full assurance")
    if root["push_main_policy"] != "full_exact_commit":
        raise ImpactPlanError("protected-main changes must select exact-commit full assurance")

    always_run = _string_list(root["always_run"], "always_run", maximum=32)
    if any(LANE_ID.fullmatch(item) is None for item in always_run):
        raise ImpactPlanError("always_run contains an invalid job identifier")

    lane_values = root["lanes"]
    if not isinstance(lane_values, list) or not lane_values or len(lane_values) > 32:
        raise ImpactPlanError("lanes must be a non-empty bounded array")
    lanes: list[Lane] = []
    for index, value in enumerate(lane_values):
        lane = _closed_object(
            value,
            {"id", "description", "events", "depends_on"},
            f"lane {index}",
        )
        lane_id = _string(lane["id"], f"lane {index} id", maximum=80)
        if LANE_ID.fullmatch(lane_id) is None:
            raise ImpactPlanError(f"invalid lane identifier: {lane_id}")
        description = _string(lane["description"], f"lane {lane_id} description")
        events = _string_list(lane["events"], f"lane {lane_id} events", maximum=4)
        if not set(events).issubset(ALLOWED_EVENTS):
            raise ImpactPlanError(f"lane {lane_id} contains an unsupported event")
        dependencies_value = lane["depends_on"]
        if not isinstance(dependencies_value, list) or len(dependencies_value) > 32:
            raise ImpactPlanError(f"lane {lane_id} dependencies must be a bounded array")
        dependencies = tuple(
            _string(item, f"lane {lane_id} dependency", maximum=80)
            for item in dependencies_value
        )
        if len(dependencies) != len(set(dependencies)) or dependencies != tuple(
            sorted(dependencies)
        ):
            raise ImpactPlanError(f"lane {lane_id} dependencies must be unique and sorted")
        if any(LANE_ID.fullmatch(item) is None for item in dependencies):
            raise ImpactPlanError(f"lane {lane_id} contains an invalid dependency")
        lanes.append(Lane(lane_id, description, events, dependencies))

    lane_tuple = tuple(sorted(lanes, key=lambda item: item.lane_id))
    lane_ids = tuple(lane.lane_id for lane in lane_tuple)
    if len(lane_ids) != len(set(lane_ids)):
        raise ImpactPlanError("lane identifiers must be unique")
    _validate_dependency_graph(lane_tuple)
    gateway_image_lane = next(
        (lane for lane in lane_tuple if lane.lane_id == GATEWAY_IMAGE_LANE), None
    )
    if gateway_image_lane is None:
        raise ImpactPlanError("the gateway_image lane is required")
    if set(gateway_image_lane.events) != ALLOWED_EVENTS:
        raise ImpactPlanError(
            "the gateway_image lane must be available for pull requests and protected main"
        )

    full_lanes = _string_list(root["full_lanes"], "full_lanes", maximum=32)
    if full_lanes != lane_ids:
        raise ImpactPlanError("full_lanes must contain every lane exactly once")

    rule_values = root["rules"]
    if not isinstance(rule_values, list) or not rule_values or len(rule_values) > 256:
        raise ImpactPlanError("rules must be a non-empty bounded array")
    rules: list[Rule] = []
    for index, value in enumerate(rule_values):
        rule = _closed_object(
            value,
            {"id", "description", "patterns", "lanes", "force_full"},
            f"rule {index}",
        )
        rule_id = _string(rule["id"], f"rule {index} id", maximum=80)
        if RULE_ID.fullmatch(rule_id) is None:
            raise ImpactPlanError(f"invalid rule identifier: {rule_id}")
        description = _string(rule["description"], f"rule {rule_id} description")
        patterns = _string_list(rule["patterns"], f"rule {rule_id} patterns")
        patterns = tuple(_validate_pattern(pattern) for pattern in patterns)
        selected_lanes = _string_list(rule["lanes"], f"rule {rule_id} lanes", maximum=32)
        if not set(selected_lanes).issubset(lane_ids):
            raise ImpactPlanError(f"rule {rule_id} selects an unknown lane")
        force_full = rule["force_full"]
        if not isinstance(force_full, bool):
            raise ImpactPlanError(f"rule {rule_id} force_full must be a boolean")
        if force_full and selected_lanes != full_lanes:
            raise ImpactPlanError(f"force-full rule {rule_id} must select every lane")
        rules.append(
            Rule(
                rule_id,
                description,
                patterns,
                selected_lanes,
                force_full,
                tuple(_compile_pattern(pattern) for pattern in patterns),
            )
        )

    rule_ids = tuple(rule.rule_id for rule in rules)
    if len(rule_ids) != len(set(rule_ids)):
        raise ImpactPlanError("rule identifiers must be unique")
    return ImpactMap(
        digest=hashlib.sha256(raw).hexdigest(),
        always_run=always_run,
        lanes=lane_tuple,
        full_lanes=full_lanes,
        push_main_policy=root["push_main_policy"],
        rules=tuple(rules),
    )


def _validate_commit(value: str, label: str) -> str:
    if COMMIT.fullmatch(value) is None or value == "0" * 40:
        raise ImpactPlanError(f"{label} must be a non-zero full lowercase Git commit")
    return value


def _expand_dependencies(impact_map: ImpactMap, selected: set[str]) -> tuple[str, ...]:
    by_id = {lane.lane_id: lane for lane in impact_map.lanes}
    pending = list(selected)
    while pending:
        lane_id = pending.pop()
        for dependency in by_id[lane_id].depends_on:
            if dependency not in selected:
                selected.add(dependency)
                pending.append(dependency)
    return tuple(sorted(selected))


def plan_for_paths(
    impact_map: ImpactMap,
    paths: Sequence[str],
    *,
    base_commit: str,
    head_commit: str,
    event: str,
) -> dict[str, object]:
    base_commit = _validate_commit(base_commit, "base commit")
    head_commit = _validate_commit(head_commit, "head commit")
    if event not in ALLOWED_EVENTS:
        raise ImpactPlanError(f"unsupported planning event: {event}")
    if len(paths) > MAX_CHANGED_PATHS:
        raise ImpactPlanError("changed-path count exceeds the planner limit")
    changed_paths = tuple(sorted({_validate_repository_path(path) for path in paths}))
    applicable_lanes = tuple(
        lane.lane_id for lane in impact_map.lanes if event in lane.events
    )

    matched_rule_ids: set[str] = set()
    selected: set[str] = set()
    unmatched: list[str] = []
    matches: list[dict[str, object]] = []
    force_full_rules: set[str] = set()
    for path in changed_paths:
        path_rules: list[str] = []
        for rule in impact_map.rules:
            if any(matcher.fullmatch(path) is not None for matcher in rule.matchers):
                path_rules.append(rule.rule_id)
                matched_rule_ids.add(rule.rule_id)
                selected.update(rule.lanes)
                if rule.force_full:
                    force_full_rules.add(rule.rule_id)
        if not path_rules:
            unmatched.append(path)
        matches.append({"path": path, "rule_ids": sorted(path_rules)})

    if not changed_paths:
        reason = "empty-change-set"
        force_full = True
    elif unmatched:
        reason = "unmatched-path"
        force_full = True
    elif force_full_rules:
        reason = "force-full-rule"
        force_full = True
    else:
        reason = "matched-rules"
        force_full = False

    if event == "push_main" and changed_paths:
        reason = "protected-main-exact-commit"
        force_full = True

    expanded_lanes = _expand_dependencies(impact_map, selected)
    selected_lanes = tuple(
        lane_id
        for lane_id in (impact_map.full_lanes if force_full else expanded_lanes)
        if lane_id in applicable_lanes
    )
    if not force_full and not selected_lanes:
        reason = "no-applicable-lane"
        force_full = True
        selected_lanes = applicable_lanes
    lane_decisions = {
        lane.lane_id: lane.lane_id in selected_lanes for lane in impact_map.lanes
    }
    gateway_image_required = GATEWAY_IMAGE_LANE in selected_lanes
    return {
        "schema": PLAN_SCHEMA,
        "mode": "shadow",
        "enforced": False,
        "event": event,
        "reason": reason,
        "force_full": force_full,
        "base_commit": base_commit,
        "head_commit": head_commit,
        "map_sha256": impact_map.digest,
        "changed_path_count": len(changed_paths),
        "changed_paths": list(changed_paths),
        "matches": matches,
        "matched_rule_ids": sorted(matched_rule_ids),
        "force_full_rule_ids": sorted(force_full_rules),
        "unmatched_paths": unmatched,
        "always_run": list(impact_map.always_run),
        "applicable_lanes": list(applicable_lanes),
        "selected_lanes": list(selected_lanes),
        "lane_decisions": lane_decisions,
        "gateway_image_required": gateway_image_required,
    }


def _run_git(root: Path, arguments: Sequence[str]) -> bytes:
    result = subprocess.run(
        ("git", *arguments),
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ImpactPlanError(f"Git command failed closed: git {' '.join(arguments[:2])}")
    return result.stdout


def changed_paths_between(root: Path, base_commit: str, head_commit: str) -> tuple[str, ...]:
    base_commit = _validate_commit(base_commit, "base commit")
    head_commit = _validate_commit(head_commit, "head commit")
    for commit in (base_commit, head_commit):
        _run_git(root, ("cat-file", "-e", f"{commit}^{{commit}}"))
    checked_out = _run_git(root, ("rev-parse", "HEAD")).decode("ascii").strip()
    if checked_out != head_commit:
        raise ImpactPlanError("head commit does not match the checked-out worktree")

    raw = _run_git(
        root,
        (
            "diff",
            "--name-status",
            "-z",
            "--find-renames=50%",
            base_commit,
            head_commit,
            "--",
        ),
    )
    if len(raw) > MAX_DIFF_BYTES:
        raise ImpactPlanError("Git change inventory exceeds the planner byte limit")
    tokens = raw.split(b"\0")
    if tokens and tokens[-1] == b"":
        tokens.pop()
    paths: list[str] = []
    index = 0
    while index < len(tokens):
        try:
            status_text = tokens[index].decode("ascii")
        except UnicodeDecodeError as error:
            raise ImpactPlanError("Git change status is not ASCII") from error
        index += 1
        status = status_text[:1]
        path_count = 2 if status in {"C", "R"} else 1
        if status not in {"A", "C", "D", "M", "R", "T"}:
            raise ImpactPlanError(f"unsupported Git change status: {status_text}")
        if index + path_count > len(tokens):
            raise ImpactPlanError("Git change inventory is truncated")
        for raw_path in tokens[index : index + path_count]:
            try:
                path = raw_path.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ImpactPlanError("Git changed path is not UTF-8") from error
            paths.append(_validate_repository_path(path))
        index += path_count
        if len(paths) > MAX_CHANGED_PATHS:
            raise ImpactPlanError("changed-path count exceeds the planner limit")
    return tuple(sorted(set(paths)))


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _repository_file(root: Path, relative: Path, label: str) -> Path:
    if relative.is_absolute():
        raise ImpactPlanError(f"{label} must be repository relative")
    logical = _validate_repository_path(relative.as_posix(), label)
    target = root / logical
    resolved_root = root.resolve()
    resolved_target = target.resolve(strict=False)
    if not resolved_target.is_relative_to(resolved_root):
        raise ImpactPlanError(f"{label} escapes the repository")
    return target


def resolve_repository_root(path: Path) -> Path:
    """Resolve one explicit, real Git worktree root for planning."""

    logical = Path(os.path.abspath(path))
    try:
        metadata = logical.lstat()
    except FileNotFoundError as error:
        raise ImpactPlanError("repository root is missing") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ImpactPlanError("repository root must be a real directory, not a link")
    root = logical.resolve()
    if root != logical:
        raise ImpactPlanError("repository root must not use a symbolic-link alias")
    try:
        raw_top_level = _run_git(root, ("rev-parse", "--show-toplevel"))
        top_level = Path(raw_top_level.decode("utf-8").strip()).resolve()
    except (UnicodeDecodeError, OSError) as error:
        raise ImpactPlanError("repository root could not be resolved as UTF-8") from error
    if top_level != root:
        raise ImpactPlanError("repository root must be the exact Git worktree root")
    return root


def write_new_output(root: Path, relative: Path, payload: bytes) -> Path:
    target = _repository_file(root, relative, "output path")
    relative_parent = target.parent.relative_to(root)
    current = root
    for component in relative_parent.parts:
        current = current / component
        if current.exists() or current.is_symlink():
            metadata = current.lstat()
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                raise ImpactPlanError("output parent must be a real directory")
        else:
            current.mkdir(mode=0o755)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(target, flags, 0o600)
    except FileExistsError as error:
        raise ImpactPlanError("output path already exists") from error
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return target


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Plan CI impact in fail-closed shadow mode without skipping checks."
    )
    parser.add_argument("--base", required=True, help="full event base commit")
    parser.add_argument("--head", required=True, help="full checked-out head commit")
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=ROOT,
        help="explicit Git worktree root whose base-to-head change is planned",
    )
    parser.add_argument(
        "--event",
        required=True,
        choices=sorted(ALLOWED_EVENTS),
        help="normalised workflow event",
    )
    parser.add_argument(
        "--map",
        type=Path,
        default=DEFAULT_MAP,
        help="repository-relative versioned impact map",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="new repository-relative machine-readable plan path",
    )
    arguments = parser.parse_args(argv)

    try:
        repository_root = resolve_repository_root(arguments.repository_root)
        map_path = _repository_file(repository_root, arguments.map, "impact map path")
        impact_map = load_impact_map(map_path)
        paths = changed_paths_between(repository_root, arguments.base, arguments.head)
        plan = plan_for_paths(
            impact_map,
            paths,
            base_commit=arguments.base,
            head_commit=arguments.head,
            event=arguments.event,
        )
        payload = canonical_json_bytes(plan)
        write_new_output(repository_root, arguments.output, payload)
    except (ImpactPlanError, OSError) as error:
        raise SystemExit(f"CI impact planning failed closed: {error}") from error
    print(payload.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
