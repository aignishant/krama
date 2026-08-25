"""The repo checks itself: the syllabus, the folders and the index must not drift apart."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_skeleton import short_slug  # noqa: E402
from curriculum import DSA_PHASES, SD_PHASES, load  # noqa: E402

DAYS = load()
DAYS_DIR = ROOT / "days"


def test_exactly_one_hundred_and_eighty_days() -> None:
    assert [d.n for d in DAYS] == list(range(1, 181))


def test_every_day_has_both_tracks() -> None:
    for day in DAYS:
        assert day.dsa.title.strip(), f"day {day.n} has no DSA topic"
        assert day.sd.title.strip(), f"day {day.n} has no system design topic"


def test_phases_tile_the_whole_course_without_gaps() -> None:
    for phases in (DSA_PHASES, SD_PHASES):
        covered: list[int] = []
        for _, lo, hi in phases:
            covered += list(range(lo, hi + 1))
        assert covered == list(range(1, 181)), "phases overlap or leave a gap"


def test_day_slugs_are_unique_and_readable() -> None:
    slugs = [d.slug for d in DAYS]
    assert len(slugs) == len(set(slugs)), "two days share a slug"
    for slug in slugs:
        assert slug == slug.lower()
        assert " " not in slug and "_" not in slug


def test_every_day_folder_exists_with_its_four_files() -> None:
    for day in DAYS:
        folder = DAYS_DIR / day.folder
        assert folder.is_dir(), f"missing days/{day.folder} — run scripts/build_skeleton.py"
        assert (folder / "README.md").exists()
        assert (folder / "03-practice.md").exists()
        assert (folder / f"01-dsa-{short_slug(day.dsa.title)}.md").exists()
        assert (folder / f"02-system-design-{short_slug(day.sd.title)}.md").exists()


def test_no_day_has_a_lab_folder() -> None:
    """Rule 10. The lab was removed on purpose."""
    assert not list(DAYS_DIR.glob("*/lab")), "a lab/ folder came back"


def test_generated_index_is_current() -> None:
    from build_skeleton import curriculum_index

    on_disk = (ROOT / "docs" / "CURRICULUM_INDEX.md").read_text(encoding="utf-8")
    assert on_disk == curriculum_index(DAYS), "index is stale — run scripts/build_skeleton.py"
