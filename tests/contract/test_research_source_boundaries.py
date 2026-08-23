from __future__ import annotations

import hashlib
from pathlib import Path
import re
import subprocess
import unittest
import zipfile
from xml.etree import ElementTree


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
RESEARCH_SOURCE_ROOT = Path(
    "docs/research/2026-08-23/agentic-ai-governance-review/sources"
)
LOCAL_ONLY_SOURCES = {
    RESEARCH_SOURCE_ROOT / "AI-Report-eBook-2026.pdf": (
        "99897f2f12aacecfdc5dd50b3409821df68c307d4c5d3cd289419c05a41658bb"
    ),
    RESEARCH_SOURCE_ROOT / "UNOFFICIAL-DRAFT Agentic AI Governance UK MCP.docx": (
        "79941e9941e88bbac6b8fc49f470f2e07c36666314fca31899bebad33efb65f4"
    ),
}
PRIVACY_SCRUBBED_DERIVATIVE = RESEARCH_SOURCE_ROOT / (
    "UNOFFICIAL-DRAFT Agentic AI Governance UK MCP — privacy-scrubbed.docx"
)
PRIVACY_SCRUBBED_SHA256 = (
    "49f6152ec983bc24cf8b3c3473bd263e122a3c199d5fb723970b247cfe713bda"
)
SUPPLIED_MARKDOWN = RESEARCH_SOURCE_ROOT / (
    "Agentic AI Governance, MCP and GIS AI GO — Updated Research Report "
    "incorporating The State of AI 2026.md"
)
SUPPLIED_MARKDOWN_SHA256 = (
    "a02f5f33b84d47b25506d400beff7993c606e3ec834d8f7feae97022b493df4c"
)
EMAIL_PATTERN = re.compile(rb"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
GUID_PATTERN = re.compile(
    rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.I,
)
SYNTHETIC_EMAIL = b"jane.okafor@example.com"
RELATIONSHIP_NAMESPACE = (
    "http://schemas.openxmlformats.org/package/2006/relationships"
)
CONTENT_TYPE_NAMESPACE = (
    "http://schemas.openxmlformats.org/package/2006/content-types"
)
DRAWINGML_NAMESPACE = "http://schemas.openxmlformats.org/drawingml/2006/main"


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
    )
    return [Path(value) for value in result.stdout.decode("utf-8").split("\0") if value]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


class ResearchSourceBoundaryTests(unittest.TestCase):
    def test_local_only_sources_are_not_tracked_by_name_or_content(self) -> None:
        tracked = tracked_paths()

        local_only_names = {path.name for path in LOCAL_ONLY_SOURCES}
        tracked_names = [str(path) for path in tracked if path.name in local_only_names]
        self.assertEqual(tracked_names, [])

        local_only_hashes = set(LOCAL_ONLY_SOURCES.values())
        matching_content: list[str] = []
        for relative_path in tracked:
            candidate = REPOSITORY_ROOT / relative_path
            if candidate.is_symlink() or not candidate.is_file():
                continue
            if sha256_file(candidate) in local_only_hashes:
                matching_content.append(str(relative_path))
        self.assertEqual(matching_content, [])

    def test_local_only_sources_have_exact_ignore_rules(self) -> None:
        ignore_rules = (REPOSITORY_ROOT / ".gitignore").read_text(
            encoding="utf-8"
        ).splitlines()
        for local_only_source in LOCAL_ONLY_SOURCES:
            with self.subTest(source=local_only_source.name):
                self.assertIn(f"/{local_only_source.as_posix()}", ignore_rules)
                result = subprocess.run(
                    [
                        "git",
                        "check-ignore",
                        "--no-index",
                        "--quiet",
                        str(local_only_source),
                    ],
                    cwd=REPOSITORY_ROOT,
                    check=False,
                )
                self.assertEqual(result.returncode, 0)

    def test_tracked_review_sources_have_exact_hashes(self) -> None:
        tracked = set(tracked_paths())
        self.assertIn(PRIVACY_SCRUBBED_DERIVATIVE, tracked)
        self.assertIn(SUPPLIED_MARKDOWN, tracked)
        self.assertEqual(
            sha256_file(REPOSITORY_ROOT / PRIVACY_SCRUBBED_DERIVATIVE),
            PRIVACY_SCRUBBED_SHA256,
        )
        self.assertEqual(
            sha256_file(REPOSITORY_ROOT / SUPPLIED_MARKDOWN),
            SUPPLIED_MARKDOWN_SHA256,
        )

    def test_privacy_scrubbed_derivative_has_no_collaboration_metadata(self) -> None:
        derivative = REPOSITORY_ROOT / PRIVACY_SCRUBBED_DERIVATIVE
        with zipfile.ZipFile(derivative, "r") as archive:
            parts = {name: archive.read(name) for name in archive.namelist()}

        self.assertNotIn("docProps/custom.xml", parts)
        self.assertNotIn("word/people.xml", parts)
        self.assertFalse(any(name.startswith("customXml/") for name in parts))

        all_bytes = b"\n".join(parts[name] for name in sorted(parts))
        emails = [match.lower() for match in EMAIL_PATTERN.findall(all_bytes)]
        self.assertEqual(emails, [SYNTHETIC_EMAIL])
        self.assertNotIn(b"@hmrc.gov.uk", all_bytes.lower())
        self.assertNotIn(b"msip_label_", all_bytes.lower())
        self.assertNotIn(b"classificationcontentmarkingfooter", all_bytes.lower())
        self.assertIn(b"official", all_bytes.lower())

        unexpected_guids: list[tuple[str, str]] = []
        for name, payload in parts.items():
            if not (name.endswith(".xml") or name.endswith(".rels")):
                self.assertEqual(GUID_PATTERN.findall(payload), [])
                continue

            root = ElementTree.fromstring(payload)
            for element in root.iter():
                element_name = element.tag.rsplit("}", 1)[-1]
                element_namespace = (
                    element.tag[1:].split("}", 1)[0]
                    if element.tag.startswith("{")
                    else ""
                )
                self.assertNotIn(
                    element_name,
                    {"docId", "people", "person", "presenceInfo", "rsids"},
                )
                if element_name in {"creator", "lastModifiedBy"}:
                    self.assertEqual((element.text or "").strip(), "")
                self.assertNotIn(
                    element_name,
                    {
                        "Application",
                        "AppVersion",
                        "Company",
                        "created",
                        "HyperlinkBase",
                        "lastPrinted",
                        "Manager",
                        "modified",
                        "revision",
                        "Template",
                        "TotalTime",
                    },
                )
                for attribute, value in element.attrib.items():
                    attribute_name = attribute.rsplit("}", 1)[-1]
                    self.assertFalse(attribute_name.startswith("rsid"))
                    self.assertNotIn(
                        attribute_name,
                        {"personId", "providerId", "userId"},
                    )
                    matches = GUID_PATTERN.findall(value.encode("utf-8"))
                    if matches and not (
                        element_namespace == DRAWINGML_NAMESPACE
                        and element_name == "ext"
                        and attribute_name == "uri"
                    ):
                        unexpected_guids.append((name, attribute_name))
                if element.text and GUID_PATTERN.search(element.text.encode("utf-8")):
                    unexpected_guids.append((name, "text"))

            if name.endswith(".rels"):
                for relationship in root.findall(
                    f"{{{RELATIONSHIP_NAMESPACE}}}Relationship"
                ):
                    target = (relationship.get("Target") or "").lower()
                    relationship_type = (relationship.get("Type") or "").lower()
                    self.assertNotIn("people.xml", target)
                    self.assertNotIn("customxml/", target)
                    self.assertNotIn("/people", relationship_type)
                    self.assertFalse(relationship_type.endswith("/customxml"))

            if name == "[Content_Types].xml":
                for override in root.findall(
                    f"{{{CONTENT_TYPE_NAMESPACE}}}Override"
                ):
                    part_name = (override.get("PartName") or "").lower()
                    self.assertNotIn(
                        part_name,
                        {"/docprops/custom.xml", "/word/people.xml"},
                    )
                    self.assertFalse(part_name.startswith("/customxml/"))

        self.assertEqual(unexpected_guids, [])


if __name__ == "__main__":
    unittest.main()
