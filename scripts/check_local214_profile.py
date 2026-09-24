"""Check the separate local profile and, optionally, an exact-artefact gate record.

Validation proves structure and gate completeness, not the truth of observations.
Release operators must also verify the linked evidence and matching artefact bytes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluation/local-edition-profile.v1.json"
SCHEMA = ROOT / "schemas/local-edition-acceptance.v1.schema.json"


def validate_record(record: dict, profile: dict, *, require_pass: bool = False) -> None:
    schema = json.loads(SCHEMA.read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(record)
    identifiers = [check["id"] for check in record["checks"]]
    if len(set(identifiers)) != len(identifiers) or set(identifiers) != set(profile["required_gates"]):
        raise ValueError("Every local gate must appear exactly once")
    if require_pass and any(check["status"] != "passed" for check in record["checks"]):
        raise ValueError("Local publication is blocked: not every required gate passed")


def validate_profile(profile: dict) -> None:
    if profile["software_version"] != (ROOT / "VERSION").read_text().strip():
        raise ValueError("Local software version differs from repository version")
    if profile["edition"] != "0.2.0-local.1" or profile["target_release"] != "0.2.0":
        raise ValueError("A changed edition requires reviewed profile/schema changes")
    if profile["latest_supported_release"] != "0.1.0":
        raise ValueError("Local evaluation does not promote the supported public release")
    publication = profile["publication"]
    if (set(publication) != {"prerelease", "make_latest", "requires_all_gates"}
            or publication["prerelease"] is not True
            or publication["make_latest"] is not False
            or publication["requires_all_gates"] is not True):
        raise ValueError("Local edition cannot claim the latest supported public release")
    if profile["provider_egress"] is not False or (profile["provider_egress"], profile["host"], profile["port"], profile["evidence_retention"]) != (
        False, "127.0.0.1", 8787, "current-session-only"
    ):
        raise ValueError("Local runtime boundary changed")
    cache = json.loads((ROOT / "providers/ons/data-query-approved-cache.v1.json").read_text())
    if profile["approved_cache_expires_at"] != cache["freshness"]["stale_after"]:
        raise ValueError("Profile must expose the actual immutable cache expiry")
    gate_ids = json.loads(SCHEMA.read_text())["properties"]["checks"]["items"]["properties"]["id"]["enum"]
    if profile["required_gates"] != gate_ids:
        raise ValueError("Profile and acceptance schema disagree")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path)
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()
    profile = json.loads(PROFILE.read_text())
    validate_profile(profile)
    if args.require_pass and args.record is None:
        parser.error("--require-pass requires --record")
    if args.record:
        validate_record(json.loads(args.record.read_text()), profile, require_pass=args.require_pass)
    print("Local profile valid" + ("; every recorded gate passed (evidence review still required)" if args.require_pass else "; no publication acceptance implied"))


if __name__ == "__main__":
    main()
