from __future__ import annotations

import hashlib
import json
import sys
import unittest
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest import mock

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_gateway_container import (  # noqa: E402
    _freshness_time,
    assert_catalogue_freshness,
    image_catalogue_freshness,
)


STALE_AFTER = "2026-11-20T00:00:00Z"
BUNDLE_BYTES = json.dumps(
    {"staleAfter": STALE_AFTER}, sort_keys=True, separators=(",", ":")
).encode("utf-8")
BUNDLE_SHA256 = hashlib.sha256(BUNDLE_BYTES).hexdigest()
DEADLINE = datetime.fromisoformat(STALE_AFTER.replace("Z", "+00:00"))


def health_for(stale: bool, stale_after: str = STALE_AFTER) -> dict[str, object]:
    warnings = (
        [
            "Catalogue freshness review expired at "
            f"{stale_after}; results are a governed snapshot, not current source authority."
        ]
        if stale
        else []
    )
    return {"catalogue": {"stale": stale, "warnings": warnings}}


class GatewayCatalogueFreshnessTests(unittest.TestCase):
    def test_exact_image_bundle_identity_is_read_from_container(self) -> None:
        with mock.patch(
            "check_gateway_container.json_from_exec",
            return_value={"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256},
        ) as read_image:
            value = image_catalogue_freshness("container-id")

        self.assertEqual(value, {
            "stale_after": STALE_AFTER,
            "bundle_sha256": BUNDLE_SHA256,
        })
        read_image.assert_called_once()
        self.assertEqual(read_image.call_args.args[0], "container-id")
        self.assertIn("/app/artifacts/okf/okf-bundle.json", read_image.call_args.args[1])

    def test_image_identity_rejects_malformed_time_digest_and_extra_fields(self) -> None:
        for value in (
            {"stale_after": "2026-02-30T00:00:00Z", "bundle_sha256": BUNDLE_SHA256},
            {"stale_after": STALE_AFTER, "bundle_sha256": "not-a-digest"},
            {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256, "extra": "x"},
        ):
            with (
                self.subTest(value=value),
                mock.patch("check_gateway_container.json_from_exec", return_value=value),
                self.assertRaises(AssertionError),
            ):
                image_catalogue_freshness("container-id")

    def test_schema_accepts_only_coupled_fresh_and_expired_health_states(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "gateway-container-acceptance.schema.json").read_text(
                encoding="utf-8"
            )
        )
        boundary_schema = deepcopy(schema["$defs"]["boundary"])
        boundary_schema["required"] = ["catalogue_freshness", "health"]
        boundary_schema["properties"] = {
            "catalogue_freshness": boundary_schema["properties"]["catalogue_freshness"],
            "health": boundary_schema["properties"]["health"],
        }
        schema["required"] = ["boundary"]
        schema["properties"] = {"boundary": {"$ref": "#/$defs/boundary"}}
        schema["$defs"]["boundary"] = boundary_schema
        validator = Draft202012Validator(schema, format_checker=FormatChecker())

        def instance(stale: bool, warnings: list[str]) -> dict[str, object]:
            started = (
                DEADLINE + timedelta(seconds=1)
                if stale
                else DEADLINE - timedelta(seconds=1)
            )
            return {
                "boundary": {
                    "catalogue_freshness": {
                        "bundle_sha256": BUNDLE_SHA256,
                        "stale_after": STALE_AFTER,
                        "load_window_started_at": started.isoformat(timespec="seconds").replace(
                            "+00:00", "Z"
                        ),
                        "observed_at": (started + timedelta(milliseconds=10)).isoformat(
                            timespec="milliseconds"
                        ).replace("+00:00", "Z"),
                        "stale": stale,
                    },
                    "health": {
                        "status": "ok",
                        "product": "GIS AI GO",
                        "lifecycle": "candidate-unregistered",
                        "production_registration": False,
                        "catalogue": {
                            "revision": "a" * 40,
                            "version": "0.1.0",
                            "content_root_sha256": "b" * 64,
                            "record_count": 1,
                            "stale": stale,
                            "warnings": warnings,
                        },
                    },
                }
            }

        warning = (
            "Catalogue freshness review expired at "
            f"{STALE_AFTER}; results are a governed snapshot, not current source authority."
        )
        validator.validate(instance(False, []))
        validator.validate(instance(True, [warning]))
        for mismatch in (
            instance(False, [warning]),
            instance(True, []),
            {
                **instance(False, []),
                "boundary": {
                    **instance(False, [])["boundary"],
                    "catalogue_freshness": {
                        **instance(False, [])["boundary"]["catalogue_freshness"],
                        "stale": True,
                    },
                },
            },
            instance(True, ["Catalogue remains current."]),
        ):
            with self.subTest(mismatch=mismatch), self.assertRaises(ValidationError):
                validator.validate(mismatch)

    def test_fresh_before_deadline_and_expired_at_and_after_deadline(self) -> None:
        cases = (
            (DEADLINE - timedelta(seconds=1), False),
            (DEADLINE, True),
            (DEADLINE + timedelta(days=3), True),
        )
        image = {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256}
        for started, expected_stale in cases:
            with self.subTest(started=started.isoformat()):
                observed = started + timedelta(milliseconds=100)
                result = assert_catalogue_freshness(
                    health_for(expected_stale), image,
                    started.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
                    observed.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
                )
                self.assertIs(result["stale"], expected_stale)
                self.assertEqual(result["stale_after"], STALE_AFTER)
                self.assertEqual(result["bundle_sha256"], BUNDLE_SHA256)

    def test_fractional_deadline_uses_gateway_millisecond_precision(self) -> None:
        fractional_deadline = "2026-11-20T00:00:00.000001Z"
        started = "2026-11-20T00:00:00.000Z"
        health = {
            "catalogue": {
                "stale": True,
                "warnings": [
                    "Catalogue freshness review expired at "
                    f"{fractional_deadline}; results are a governed snapshot, "
                    "not current source authority."
                ],
            }
        }
        result = assert_catalogue_freshness(
            health,
            {"stale_after": fractional_deadline, "bundle_sha256": BUNDLE_SHA256},
            started,
            started,
        )
        self.assertIs(result["stale"], True)
        self.assertEqual(result["stale_after"], fractional_deadline)

    def test_image_staleness_is_not_faked_fresh_at_expiry(self) -> None:
        started = DEADLINE
        iso = started.isoformat(timespec="seconds").replace("+00:00", "Z")
        with self.assertRaisesRegex(AssertionError, "freshness differs"):
            assert_catalogue_freshness(
                health_for(False),
                {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256},
                iso,
                (started + timedelta(milliseconds=100)).isoformat(
                    timespec="milliseconds"
                ).replace("+00:00", "Z"),
            )

    def test_stale_state_requires_exact_expiry_warning(self) -> None:
        started = DEADLINE + timedelta(seconds=1)
        start_text = started.isoformat(timespec="seconds").replace("+00:00", "Z")
        observed_text = (started + timedelta(seconds=1)).isoformat(
            timespec="seconds"
        ).replace("+00:00", "Z")
        expected = health_for(True)

        suppressed = health_for(True)
        suppressed["catalogue"]["warnings"] = []  # type: ignore[index]
        changed = health_for(True)
        changed["catalogue"]["warnings"] = ["Catalogue remains current."]  # type: ignore[index]
        wrong_type = health_for(True)
        wrong_type["catalogue"]["stale"] = 1  # type: ignore[index]
        for health in (suppressed, changed, wrong_type):
            with self.subTest(health=health), self.assertRaises(AssertionError):
                assert_catalogue_freshness(
                    health,
                    {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256},
                    start_text,
                    observed_text,
                )

        exact = assert_catalogue_freshness(
            expected,
            {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256},
            start_text,
            observed_text,
        )
        self.assertIs(exact["stale"], True)

    def test_fresh_state_rejects_a_warning(self) -> None:
        started = DEADLINE - timedelta(seconds=1)
        health = health_for(False)
        health["catalogue"]["warnings"] = [  # type: ignore[index]
            "Catalogue freshness review expired at "
            f"{STALE_AFTER}; results are a governed snapshot, not current source authority."
        ]
        with self.assertRaises(AssertionError):
            assert_catalogue_freshness(
                health,
                {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256},
                started.isoformat(timespec="seconds").replace("+00:00", "Z"),
                (started + timedelta(milliseconds=100)).isoformat(
                    timespec="milliseconds"
                ).replace("+00:00", "Z"),
            )

    def test_crossed_startup_deadline_is_rejected(self) -> None:
        started = DEADLINE - timedelta(milliseconds=1)
        observed = DEADLINE
        with self.assertRaisesRegex(AssertionError, "crossed a time boundary"):
            assert_catalogue_freshness(
                health_for(False),
                {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256},
                started.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
                observed.isoformat(timespec="seconds").replace("+00:00", "Z"),
            )

    def test_reversed_observation_interval_is_rejected(self) -> None:
        started = DEADLINE + timedelta(seconds=1)
        observed = started - timedelta(milliseconds=1)
        with self.assertRaisesRegex(AssertionError, "crossed a time boundary"):
            assert_catalogue_freshness(
                health_for(True),
                {"stale_after": STALE_AFTER, "bundle_sha256": BUNDLE_SHA256},
                started.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
                observed.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            )

    def test_invalid_dates_and_malformed_image_identity_fail_closed(self) -> None:
        for value in (
            "2026-02-30T00:00:00Z",
            "2026-11-20T00:00:00+00:00",
            "2026-11-20T00:00:00.1234567Z",
            None,
        ):
            with self.subTest(value=value), self.assertRaises(AssertionError):
                _freshness_time(value)

if __name__ == "__main__":
    unittest.main()
