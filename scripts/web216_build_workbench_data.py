"""Generate the minimal, contact-free WEB-216 browser discovery projection."""
from pathlib import Path

from web216_corpus import canonical, load_corpus
from web216_experiments import build

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    state = build(load_corpus(ROOT / "tests/fixtures/web216/story-corpus.json"))
    target = ROOT / "apps/public-data-workbench/src/generated/discovery.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(canonical(state) + b"\n")
    print(f"Generated {len(state['entries'])} metadata records; no observations or contacts")


if __name__ == "__main__":
    main()
