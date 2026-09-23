"""The repo checks itself: the plan and the index must not drift apart."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "docs" / "CURRICULUM_INDEX.md"
PLAN = ROOT / "docs" / "00_MASTER_PLAN_DSA.md"
ID_RE = re.compile(r"\b[A-Z]{3}-\d{2}\b")


def index_rows() -> list[tuple[int, str]]:
    rows = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0].isdigit():
            rows.append((int(cells[0]), cells[2]))
    return rows


def test_every_day_slot_present_exactly_once() -> None:
    days = [d for d, _ in index_rows()]
    assert days == sorted(days), "index days are out of order"
    assert len(days) == len(set(days)), "a day appears twice in the index"
    assert days == list(range(0, 309)), "index must cover day 0 through day 308"


def test_no_concept_id_is_owned_twice() -> None:
    owner: dict[str, int] = {}
    for day, ids in index_rows():
        for cid in ID_RE.findall(ids):
            assert cid not in owner, f"{cid} owned by both day {owner[cid]} and day {day}"
            owner[cid] = day


def test_plan_id_count_matches_index() -> None:
    total = sum(len(ID_RE.findall(ids)) for _, ids in index_rows())
    claimed = re.search(r"\*\*(\d+) concept IDs\*\*", PLAN.read_text(encoding="utf-8"))
    assert claimed, "plan does not state a concept ID count"
    assert int(claimed.group(1)) == total, (
        f"plan claims {claimed.group(1)} IDs, index has {total} — amend the plan"
    )


def test_no_time_estimates_in_days() -> None:
    bad = re.compile(r"\b\d+\s*(?:-\s*\d+\s*)?(?:min(?:ute)?s?|hours?|hrs?)\b", re.IGNORECASE)
    for md in (ROOT / "days").rglob("*.md"):
        hit = bad.search(md.read_text(encoding="utf-8"))
        assert not hit, f"{md.relative_to(ROOT)} contains a time estimate: {hit.group(0)!r}"


PROBLEMS = ROOT / "docs" / "PROBLEM_INDEX.md"


def catalogue_rows() -> list[list[str]]:
    rows = []
    for line in PROBLEMS.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 5 and ID_RE.fullmatch(cells[3]):
            rows.append(cells)
    return rows


def test_every_catalogued_problem_targets_a_real_concept_id() -> None:
    known = {cid for _, ids in index_rows() for cid in ID_RE.findall(ids)}
    for name, _src, _lv, cid, _testing in catalogue_rows():
        assert cid in known, f"{name!r} targets {cid}, which no day owns"


def test_every_catalogued_problem_has_a_testing_line() -> None:
    for name, _src, _lv, _cid, testing in catalogue_rows():
        assert len(testing.split()) >= 4, f"{name!r} has no real 'really testing' line"


def test_catalogue_has_no_duplicate_primary_entries() -> None:
    seen: dict[tuple[str, str], str] = {}
    for name, src, _lv, cid, testing in catalogue_rows():
        if "\u21ba" in testing:
            continue  # an explicit cross-listing, which the catalogue allows
        key = (name.lower(), src.lower())
        assert key not in seen, f"{name!r} ({src}) is listed twice as primary ({seen[key]}, {cid})"
        seen[key] = cid
