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


def test_no_day_links_to_a_folder_that_does_not_exist() -> None:
    """Slugs move when the syllabus is edited, and a stale link is silent."""
    from check_day import check_links

    broken: list[str] = []
    for path in sorted(DAYS_DIR.glob("day-*/*.md")):
        broken += check_links(path)
    assert not broken, "\n".join(broken)


def test_wiki_is_current() -> None:
    """wiki/ is a projection of the written lessons. A stale one misleads the writer."""
    from wiki import lint

    problems = lint()
    assert not problems, "\n".join(problems) + "\n(run ./k wiki)"


def test_wiki_copies_verbatim_and_never_invents() -> None:
    """Every recall card in the wiki must appear, word for word, in its lesson."""
    from wiki import load_written, phase_slug, section

    for lesson in load_written():
        card = section(lesson.text, 9)
        if not card:
            continue
        phase_file = ROOT / "wiki" / "recall" / f"{phase_slug(lesson.phase)}.md"
        text = phase_file.read_text(encoding="utf-8")
        first_line = card.splitlines()[0].strip()
        assert first_line in text, f"day {lesson.day} {lesson.track}: recall card not projected"
