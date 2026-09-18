#!/usr/bin/env python3
"""granth — the whole toolchain for this curriculum repository, in one file.

    python granth.py status | brief N | start N | parts N | new N [slug]
                     depth [N] [--list] | index [--check] | check | done N | doctor

Stdlib only, Python 3.11+ (tomllib). A repository that teaches you something should not need a
package install before it can check itself.

The master plan is the single source of truth for *what the curriculum is*: tracks, phases and the
day map live there between `<!-- granth:...:start -->` markers, so a person reading the plan and
this script parsing it cannot disagree. granth.toml holds only what the plan cannot express.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

if sys.version_info < (3, 11):  # pragma: no cover
    sys.exit("granth: needs Python 3.11 or newer (tomllib is stdlib from 3.11).")

import tomllib

ROOT = Path(__file__).resolve().parent

# Day titles carry em dashes and non-Latin words, and a Windows console still defaults to a legacy
# code page. Line buffering keeps this script's own output in order with its subprocesses'.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", line_buffering=True)
        except (ValueError, OSError):  # pragma: no cover
            pass

# =============================================================================================
# Configuration
# =============================================================================================

# The eleven part sections. The order is the pedagogy — scene before definition, definition before
# mechanism, mechanism before failure, failure before production. Changing it is a plan amendment.
PART_SECTIONS = [
    "one-line answer",
    "the story",
    "the idea in plain language",
    "why this project needs it",
    "the source behind it",
    "the mechanism",
    "line by line",
    "the source in one demo",
    "when it breaks",
    "in production",
    "check yourself",
]
SECTION_PATTERNS = {
    "one-line answer": r"one[- ]line answer",
    "the story": r"the story",
    "the idea in plain language": r"idea in plain language",
    "why this project needs it": r"why .{0,40}needs? it",
    "the source behind it": r"the (source|paper|spec) behind it",
    "the mechanism": r"mechanism",
    "line by line": r"line by line",
    "the source in one demo": r"(source|paper|spec) in one demo",
    "when it breaks": r"when it breaks",
    "in production": r"in production",
    "check yourself": r"check yourself",
}
# "Line by line" is a bolded lead-in after each code block, not a heading in a fixed place, so it
# is excluded from the order comparison; unexplained_code_blocks() enforces it per fence instead.
ORDER_EXEMPT = {"line by line"}
CONDITIONAL = {"the source behind it", "line by line", "the source in one demo"}

HUB_SECTIONS = [
    "Where we are", "The map", "Setup", "Build brief",
    "The check that must be able to fail", "Budget", "Traps", "Verify before you build",
    "Say it out loud", "Done when", "Ledger & commit",
]
LEVELS = ["foundation", "working", "production"]
NO_WALKTHROUGH_LANGS = ["", "text", "console", "output", "traceback", "mermaid", "diff",
                        "json", "toml", "yaml", "ini", "csv"]
EXEMPT_HEADINGS = r"when it breaks|check yourself|verify|budget|ledger|the map|setup"

# A day is a unit of subject, not of time. A duration field silently authorises the worst edit in
# technical writing: cutting an explanation because the day is running long.
TIME_BANS = [
    (r"^\s*(reading_minutes|duration|time_estimate|minutes|est_time|estimated_hours"
     r"|estimated hours|effort|pace)\s*:", "a duration field in frontmatter"),
    (r"\b\d+\s*[-–]?\s*\d*\s*(minutes?|mins?|hours?|hrs?)\b(?!\s*(of |the |per ))",
     "a time estimate in the prose"),
    (r"\*\*(Time|Duration|Estimated hours):?\*\*", "a bolded time line"),
    (r"should take (about |around |roughly )?\w+", "a 'should take ...' pace"),
]

PART_KEYS = ["day", "part", "title", "ids", "level", "prerequisites", "prev", "next"]
# A source document has no `part` — it is not a subtopic of anything — and adds `source`.
SOURCE_KEYS = ["day", "source", "title", "ids", "level", "prerequisites", "prev", "next"]
HUB_KEYS = ["day", "phase", "title", "ids", "kind", "plan_version", "parts", "generated", "status"]

# A citation is an identifier, never a person: an identifier resolves to exactly one document and
# is what a reader types.
SOURCE_ID_RE = re.compile(
    r"arXiv:\d{4}\.\d{4,5}(?:v\d+)?"
    r"|arXiv:[a-z-]+(?:\.[A-Z]{2})?/\d{7}"
    r"|doi:10\.\d{4,9}/[^\s)\]|,;\"'`>*<]+"
    r"|RFC\s?\d{3,5}"
    r"|ISO[/ ]?(?:IEC[/ ]?)?\d{3,5}(?:-\d+)?(?::\d{4})?"
    r"|spec:[a-z0-9][a-z0-9.\-/]*", re.I)
# Only the two colon-prefixed forms: `spec:` and `iso:` collide with ordinary English, and these
# are the forms where a malformed identifier is both likely and silent.
SOURCE_ID_LOOSE_RE = re.compile(r"\b(?:arxiv|doi)\s*:\s*\S+", re.I)

PART_NAME_RE = re.compile(r"^(\d+)\.(\d+)-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
SECTION_DIR_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
SOURCE_NAME_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
DAY_DIR_RE = re.compile(r"^day-(\d{2,3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
ANY_DAY_DIR_RE = re.compile(r"^day-(\d{2,3})(?:-([a-z0-9-]*))?$")
ID_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,7})-(\d{2,3})\b")


@dataclass
class Config:
    name: str = "Project"
    slug: str = "project"
    topic: str = "the subject"
    plan_version: str = "v1.0.0"
    driver: str = "python granth.py"
    plan: Path = field(default_factory=lambda: ROOT / "docs" / "00_MASTER_PLAN.md")
    docs: Path = field(default_factory=lambda: ROOT / "docs")
    days: Path = field(default_factory=lambda: ROOT / "days")
    sources_dir: str = "sources"
    parts_dir: str = "parts"
    levels: list[str] = field(default_factory=lambda: list(LEVELS))
    part_sections: list[str] = field(default_factory=lambda: list(PART_SECTIONS))
    section_patterns: dict[str, str] = field(default_factory=lambda: dict(SECTION_PATTERNS))
    hub_sections: list[str] = field(default_factory=lambda: list(HUB_SECTIONS))
    no_walkthrough_langs: list[str] = field(default_factory=lambda: list(NO_WALKTHROUGH_LANGS))
    exempt_headings: str = EXEMPT_HEADINGS
    require_failure_part: bool = True
    require_sources: bool = True
    lint: str = ""
    format_check: str = ""
    test: str = ""

    @property
    def sources_ledger(self) -> Path:
        return self.docs / "SOURCES.md"

    @property
    def progress(self) -> Path:
        return self.docs / "PROGRESS.md"

    def rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(ROOT).as_posix()
        except ValueError:
            return path.as_posix()


def load_config() -> Config:
    """Read granth.toml. Every key is optional; the constants above are the standing contract."""
    cfg = Config()
    path = ROOT / "granth.toml"
    if not path.exists():
        return cfg
    with path.open("rb") as handle:
        raw = tomllib.load(handle)
    p, paths = raw.get("project", {}), raw.get("paths", {})
    c, t = raw.get("contract", {}), raw.get("toolchain", {})
    for key in ("name", "slug", "topic", "plan_version", "driver"):
        setattr(cfg, key, p.get(key, getattr(cfg, key)))
    for key, default in (("plan", "docs/00_MASTER_PLAN.md"), ("docs", "docs"), ("days", "days")):
        value = Path(paths.get(key, default))
        setattr(cfg, key, value if value.is_absolute() else ROOT / value)
    for key in ("sources_dir", "parts_dir", "levels", "part_sections", "hub_sections",
                "no_walkthrough_langs", "exempt_headings", "require_failure_part",
                "require_sources"):
        setattr(cfg, key, c.get(key, getattr(cfg, key)))
    cfg.section_patterns = {**cfg.section_patterns, **c.get("section_patterns", {})}
    for key in ("lint", "format_check", "test"):
        setattr(cfg, key, t.get(key, ""))
    return cfg


# =============================================================================================
# Reading the plan and the days
# =============================================================================================

def marked_block(text: str, marker: str) -> str:
    """Text between `<!-- granth:<marker>:start -->` and its `:end`.

    Markers rather than heading names: a heading can be reworded freely, a marker cannot be
    reworded by accident.
    """
    name = re.escape(marker)
    hit = re.search(rf"<!--\s*granth:{name}:start\s*-->(.*?)<!--\s*granth:{name}:end\s*-->",
                    text, re.S)
    return hit.group(1) if hit else ""


def _sep(cells: list[str]) -> bool:
    real = [c for c in cells if c.strip()]
    return bool(real) and all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in real)


def table_rows(block: str) -> list[list[str]]:
    """Data rows of every Markdown table in `block`. A header is the row a separator follows."""
    rows, lines = [], [ln.strip() for ln in block.splitlines()]
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if _sep(cells):
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if nxt.startswith("|") and _sep([c.strip() for c in nxt.strip("|").split("|")]):
            continue
        rows.append(cells)
    return rows


def ids_in(text: str) -> list[str]:
    seen: dict[str, None] = {}
    for m in ID_RE.finditer(text or ""):
        seen.setdefault(f"{m.group(1)}-{m.group(2)}", None)
    return list(seen)


@dataclass
class PlanDay:
    number: int
    title: str
    ids: list[str]


@dataclass
class Track:
    prefix: str
    name: str
    count: int | None


@dataclass
class Phase:
    number: str
    days: str
    theme: str
    gate: str
    first: int | None
    last: int | None


def read_plan(cfg: Config) -> str:
    if not cfg.plan.exists():
        sys.exit(f"granth: no plan at {cfg.rel(cfg.plan)} — run the initiate step first.")
    return cfg.plan.read_text(encoding="utf-8")


def plan_days(cfg: Config) -> dict[int, PlanDay]:
    block = marked_block(read_plan(cfg), "day-map")
    if not block:
        sys.exit("granth: the plan carries no <!-- granth:day-map:start --> block.\n"
                 "        Every day document is checked against it — add the markers and re-run.")
    days: dict[int, PlanDay] = {}
    for cells in table_rows(block):
        if len(cells) < 2 or not re.fullmatch(r"\d{1,3}", cells[0]):
            continue
        days[int(cells[0])] = PlanDay(int(cells[0]), cells[1],
                                      ids_in(cells[2]) if len(cells) > 2 else [])
    return days


def plan_tracks(cfg: Config) -> list[Track]:
    tracks = []
    for cells in table_rows(marked_block(read_plan(cfg), "tracks")):
        if len(cells) < 2:
            continue
        prefix = re.sub(r"[`*]", "", cells[1]).strip()
        if not re.fullmatch(r"[A-Z][A-Z0-9]{1,7}", prefix):
            continue
        count = int(cells[2]) if len(cells) > 2 and re.fullmatch(r"\d+", cells[2].strip()) else None
        tracks.append(Track(prefix, cells[0].strip("* "), count))
    return tracks


def plan_phases(cfg: Config) -> list[Phase]:
    phases = []
    for cells in table_rows(marked_block(read_plan(cfg), "phases")):
        if len(cells) < 2:
            continue
        span = re.sub(r"[`*]", "", cells[1]).strip()
        b = re.findall(r"\d+", span)
        phases.append(Phase(re.sub(r"[`*]", "", cells[0]).strip(), span,
                            cells[2] if len(cells) > 2 else "",
                            cells[3] if len(cells) > 3 else "",
                            int(b[0]) if b else None, int(b[-1]) if b else None))
    return phases


def phase_of(day: int, phases: list[Phase]) -> Phase | None:
    return next((p for p in phases
                 if p.first is not None and p.last is not None and p.first <= day <= p.last), None)


def day_dirs(cfg: Config) -> dict[int, Path]:
    """Every days/day-NN-<slug>/ keyed by number.

    The number is the identity and the slug a label on it, so a folder can be renamed to a better
    slug at any time without breaking a single tool.
    """
    found: dict[int, Path] = {}
    if cfg.days.exists():
        for entry in sorted(cfg.days.iterdir()):
            m = ANY_DAY_DIR_RE.match(entry.name) if entry.is_dir() else None
            if m:
                found[int(m.group(1))] = entry
    return found


def find_day(cfg: Config, number: int) -> Path | None:
    return day_dirs(cfg).get(number)


def part_files(folder: Path, cfg: Config) -> list[Path]:
    d = folder / cfg.parts_dir
    return sorted(d.rglob("*.md")) if d.is_dir() else []


def source_files(folder: Path, cfg: Config) -> list[Path]:
    d = folder / cfg.sources_dir
    return sorted(d.glob("*.md")) if d.is_dir() else []


def is_written(folder: Path, cfg: Config) -> bool:
    """A day is *written* only when it has a hub and a non-empty parts directory."""
    return (folder / "LESSON.md").exists() and bool(part_files(folder, cfg))


def frontmatter(text: str) -> dict[str, str] | None:
    """The leading `---` block as flat key to value. Not a YAML parser, and does not need to be."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    meta = {}
    for line in text[3:end].splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            key, sep, value = line.partition(":")
            if sep:
                meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def body(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    return text if end == -1 else text[end + 4:]


def progress_days(cfg: Config) -> list[int]:
    """Day numbers with a row in the progress ledger — the ledger is what 'complete' means."""
    if not cfg.progress.exists():
        return []
    done = []
    for line in cfg.progress.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("|"):
            first = s.strip("|").split("|")[0].strip()
            if re.fullmatch(r"\d{1,3}", first):
                done.append(int(first))
    return sorted(set(done))


# =============================================================================================
# The depth contract, checked by a machine
# =============================================================================================

@dataclass
class Report:
    day: int
    failures: list[str] = field(default_factory=list)
    parts: int = 0
    sources: int = 0

    def fail(self, where: str, message: str) -> None:
        self.failures.append(f"{where}: {message}")

    @property
    def ok(self) -> bool:
        return not self.failures


def source_ids(value: str) -> list[str]:
    return [h.group(0) for h in SOURCE_ID_RE.finditer(value or "")]


def malformed_source_ids(text: str) -> list[str]:
    """Citation-shaped strings no accepted form matches.

    Compares by start position rather than trimming punctuation: a real citation in prose is
    followed by a backtick or a bracket, and guessing what to strip is how this produces false
    failures.
    """
    valid = {h.start() for h in SOURCE_ID_RE.finditer(text)}
    return [h.group(0).strip() for h in SOURCE_ID_LOOSE_RE.finditer(text) if h.start() not in valid]


def ledger_ids(cfg: Config) -> frozenset[str]:
    if not cfg.sources_ledger.exists():
        return frozenset()
    text = cfg.sources_ledger.read_text(encoding="utf-8")
    return frozenset(m.group(0).lower() for m in SOURCE_ID_RE.finditer(text))


def sources_taught(cfg: Config) -> dict[str, list[str]]:
    """identifier -> documents declaring it. A source is taught once and cited thereafter."""
    taught: dict[str, list[str]] = {}
    for number, folder in day_dirs(cfg).items():
        for path in source_files(folder, cfg):
            meta = frontmatter(path.read_text(encoding="utf-8")) or {}
            for i in source_ids(meta.get("source", "")):
                taught.setdefault(i.lower(), []).append(f"day {number} {path.name}")
    return taught


def _fences(cfg: Config, text: str):
    """Yield (start, lang, heading, end) per fence.

    A fence may be longer than three backticks so it can contain a shorter one — which is how a
    lesson shows the contents of a Markdown file.
    """
    lines, heading, i = text.splitlines(), "", 0
    while i < len(lines):
        if lines[i].startswith("#"):
            heading, i = lines[i], i + 1
            continue
        fence = re.match(r"^(`{3,})([\w+-]*)\s*$", lines[i])
        if not fence:
            i += 1
            continue
        closing = re.compile(rf"^`{{{len(fence.group(1))},}}\s*$")
        start, i = i, i + 1
        while i < len(lines) and not closing.match(lines[i]):
            i += 1
        i += 1
        yield start, fence.group(2).lower(), heading, i


def _needs_walkthrough(cfg: Config, lang: str, heading: str) -> bool:
    return lang not in cfg.no_walkthrough_langs and not re.search(
        cfg.exempt_headings, heading, re.I)


def unexplained_code_blocks(cfg: Config, text: str) -> list[int]:
    """Fences no walkthrough follows. An unexplained line is a bug in the document: the reader
    can copy it but cannot change it."""
    lines, out = text.splitlines(), []
    for start, lang, heading, after in _fences(cfg, text):
        if not _needs_walkthrough(cfg, lang, heading):
            continue
        j, explained = after, False
        while j < len(lines):
            if re.search(r"line by line", lines[j], re.I):
                explained = True
                break
            if re.match(r"^`{3,}[\w+-]", lines[j]) or lines[j].startswith("## "):
                break
            j += 1
        if not explained:
            out.append(start + 1)
    return out


def has_explainable_code(cfg: Config, text: str) -> bool:
    return any(_needs_walkthrough(cfg, lg, h) for _, lg, h, _ in _fences(cfg, text))


def check_no_clocks(cfg: Config, text: str, where: str, report: Report) -> None:
    prose = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    for pattern, description in TIME_BANS:
        hit = re.search(pattern, prose, re.I | re.M)
        if hit:
            snippet = hit.group(0).strip().replace("\n", " ")
            report.fail(where, f"{description} ({snippet!r}) — a day carries no clock")


def section_regex(cfg: Config, name: str) -> re.Pattern[str]:
    pattern = cfg.section_patterns.get(name, re.escape(name))
    if name == "line by line":
        return re.compile(rf"^#{{2,4}}\s.*{pattern}|^\*\*Line by line:?\*\*", re.I | re.M)
    return re.compile(rf"^#{{2,4}}\s.*{pattern}", re.I | re.M)


def check_sections(cfg: Config, content: str, meta: dict[str, str], where: str,
                   report: Report, is_source: bool) -> None:
    """Required sections present, unconditional ones in the contract's order.

    Three are conditional — each required exactly when its trigger is present. No script can
    decide whether an idea has a citable origin, so the writer declares it and the script checks
    that the declaration and the section agree.
    """
    triggers = {
        "the source behind it": bool(source_ids(meta.get("sources", ""))),
        "line by line": has_explainable_code(cfg, content),
        "the source in one demo": is_source,
    }
    positions: list[tuple[int, str]] = []
    for name in cfg.part_sections:
        hit = section_regex(cfg, name).search(content)
        required = triggers.get(name, True)
        if hit is None:
            if required:
                report.fail(where, f"missing section '{name}'")
            continue
        if name == "the source behind it" and not required:
            report.fail(where, "carries 'the source behind it' but declares no 'sources' — the "
                               "section and the key are required exactly when the other is present")
        if name not in ORDER_EXEMPT:
            positions.append((hit.start(), name))
    found = {n for _, n in positions}
    ordered = [n for _, n in sorted(positions)]
    expected = [n for n in cfg.part_sections if n in found]
    if ordered != expected:
        report.fail(where, "sections are out of order — the sequence is the pedagogy. "
                           f"found {ordered}, expected {expected}")
    for token in malformed_source_ids(content):
        report.fail(where, f"{token!r} is citation-shaped but matches no accepted identifier form")


def check_citations(cfg: Config, meta: dict[str, str], where: str, report: Report) -> None:
    if not cfg.require_sources:
        return
    known = ledger_ids(cfg)
    for i in source_ids(meta.get("sources", "")) + source_ids(meta.get("source", "")):
        if i.lower() not in known:
            report.fail(where, f"{i} is not in {cfg.rel(cfg.sources_ledger)} — look the record up "
                               "live and add a dated row before citing it")


@dataclass
class PartResult:
    section: int
    subtopic: int
    declares_failure: bool = False


def check_part(cfg: Config, path: Path, day: int, report: Report) -> PartResult | None:
    where = cfg.rel(path)
    name = PART_NAME_RE.match(path.name)
    if not name:
        report.fail(where, "filename must be <section>.<subtopic>-<kebab-slug>.md")
        return None
    section, subtopic = int(name.group(1)), int(name.group(2))
    folder = SECTION_DIR_RE.match(path.parent.name)
    if not folder:
        report.fail(cfg.rel(path.parent),
                    "a section folder is NN-<kebab-slug> — a bare number is an address, "
                    "not an answer")
    elif int(folder.group(1)) != section:
        report.fail(where, f"sits in {path.parent.name} but its number says section {section}")

    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail(where, "no YAML frontmatter")
        return PartResult(section, subtopic)
    for key in PART_KEYS:
        if key not in meta:
            report.fail(where, f"frontmatter is missing '{key}'")
    if meta.get("level") and meta["level"] not in cfg.levels:
        report.fail(where, f"level {meta['level']!r} is not one of {cfg.levels}")
    if meta.get("day") and meta["day"].strip() != str(day):
        report.fail(where, f"frontmatter says day {meta['day']} but it sits in day {day}")

    content = body(text)
    check_sections(cfg, content, meta, where, report, is_source=False)
    check_citations(cfg, meta, where, report)
    check_no_clocks(cfg, text, where, report)
    for line in unexplained_code_blocks(cfg, content):
        report.fail(where, f"code block at line {line} has no 'Line by line' walkthrough after it")
    return PartResult(section, subtopic,
                      meta.get("failure", "").strip().lower() in {"true", "yes"})


def check_source(cfg: Config, path: Path, day: int, report: Report) -> int | None:
    where = cfg.rel(path)
    name = SOURCE_NAME_RE.match(path.name)
    if not name:
        report.fail(where, "a source document is NN-<kebab-slug>.md, numbered from 01")
        return None
    text = path.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail(where, "no YAML frontmatter")
        return int(name.group(1))
    for key in SOURCE_KEYS:
        if key not in meta:
            report.fail(where, f"frontmatter is missing '{key}'")
    if "part" in meta:
        report.fail(where, "a source document has no 'part' — it is not a subtopic of anything")
    declared = source_ids(meta.get("source", ""))
    if not declared:
        report.fail(where, "frontmatter 'source' must carry exactly one resolvable identifier")
    elif len(declared) > 1:
        report.fail(where, f"'source' declares {len(declared)} identifiers — one document, "
                           "one source")
    if meta.get("level") and meta["level"] not in cfg.levels:
        report.fail(where, f"level {meta['level']!r} is not one of {cfg.levels}")

    content = body(text)
    check_sections(cfg, content, meta, where, report, is_source=True)
    check_citations(cfg, meta, where, report)
    check_no_clocks(cfg, text, where, report)
    for line in unexplained_code_blocks(cfg, content):
        report.fail(where, f"code block at line {line} has no 'Line by line' walkthrough after it")
    return int(name.group(1))


def check_hub(cfg: Config, folder: Path, part_count: int, report: Report) -> None:
    hub = folder / "LESSON.md"
    where = cfg.rel(hub)
    if not hub.exists():
        report.fail(cfg.rel(folder), "no LESSON.md — the hub is what assembles the day")
        return
    text = hub.read_text(encoding="utf-8")
    meta = frontmatter(text)
    if meta is None:
        report.fail(where, "no YAML frontmatter")
        return
    for key in HUB_KEYS:
        if key not in meta:
            report.fail(where, f"frontmatter is missing '{key}'")
    if meta.get("plan_version") and meta["plan_version"] != cfg.plan_version:
        report.fail(where, f"plan_version {meta['plan_version']!r} but granth.toml says "
                           f"{cfg.plan_version!r}")
    if meta.get("parts", "").strip().isdigit() and int(meta["parts"]) != part_count:
        report.fail(where, f"frontmatter claims {meta['parts']} parts; {part_count} are on disk")

    content = body(text)
    if not re.search(r"^>\s", content, re.M):
        report.fail(where, "no yesterday / today / tomorrow blockquote")
    positions = []
    for index, title in enumerate(cfg.hub_sections, start=1):
        hit = re.search(rf"^#{{2,3}}\s*(?:§\s*)?{index}\b.*", content, re.M)
        if hit is None:
            report.fail(where, f"missing hub section {index} — {title}")
        else:
            positions.append((hit.start(), index))
    if [n for _, n in sorted(positions)] != [n for _, n in positions]:
        report.fail(where, "hub sections are out of order")
    # The hub orients and assembles; the parts teach.
    if re.search(r"\*\*Line by line:?\*\*", content, re.I):
        report.fail(where, "the hub carries a 'Line by line' walkthrough — teaching belongs "
                           "in a part")
    check_no_clocks(cfg, text, where, report)
    if not (folder / "CHECKLIST.md").exists():
        report.fail(cfg.rel(folder), "no CHECKLIST.md — a day has no definition of done without it")


def check_numbering(numbers: list[tuple[int, int]], where: str, report: Report) -> None:
    """Sections run 1..N with no gaps, and so do subtopics inside each.

    A gap means a document was deleted or never written, and nothing else in the repository would
    say so — the reader would simply never learn that 2.3 was meant to exist.
    """
    if not numbers:
        return
    sections = sorted({s for s, _ in numbers})
    if sections != list(range(1, len(sections) + 1)):
        report.fail(where, f"section numbers {sections} — they must run 1..N with no gaps")
    for section in sections:
        subs = sorted(sub for sec, sub in numbers if sec == section)
        if subs != list(range(1, len(subs) + 1)):
            report.fail(where, f"section {section} subtopics {subs} — must run 1..N with no gaps")


def check_day(cfg: Config, number: int) -> Report:
    report = Report(day=number)
    folder = find_day(cfg, number)
    if folder is None:
        report.fail(f"day {number}", f"no folder in {cfg.rel(cfg.days)}")
        return report
    where = cfg.rel(folder)
    if not DAY_DIR_RE.match(folder.name):
        report.fail(where, "a day folder is day-NN-<kebab-slug> — a number alone is "
                           "indistinguishable from every other day in a file tree or a git log")
    parts_dir = folder / cfg.parts_dir
    if not parts_dir.is_dir():
        report.fail(where, f"no {cfg.parts_dir}/ — a day without it is not written")
        return report
    for path in sorted(parts_dir.glob("*.md")):
        report.fail(cfg.rel(path),
                    f"loose in {cfg.parts_dir}/ — every part lives in its section folder")

    numbers, failure_declared = [], False
    for path in sorted(parts_dir.rglob("*.md")):
        if path.parent == parts_dir:
            continue
        result = check_part(cfg, path, number, report)
        if result:
            numbers.append((result.section, result.subtopic))
            failure_declared = failure_declared or result.declares_failure
    report.parts = len(numbers)
    check_numbering(numbers, where, report)
    if report.parts == 0:
        report.fail(where, f"{cfg.parts_dir}/ holds no part documents")

    source_numbers = []
    for path in source_files(folder, cfg):
        result = check_source(cfg, path, number, report)
        if result is not None:
            source_numbers.append(result)
    report.sources = len(source_numbers)
    if source_numbers and sorted(source_numbers) != list(range(1, len(source_numbers) + 1)):
        report.fail(where, f"source numbers {sorted(source_numbers)} — must run 01..NN, no gaps")

    if cfg.require_failure_part and not failure_declared:
        report.fail(where, "no part declares 'failure: true' — every day carries at least one "
                           "part whose subject is a deliberate failure")
    check_hub(cfg, folder, report.parts, report)

    plan, hub = plan_days(cfg), folder / "LESSON.md"
    if hub.exists() and number in plan:
        meta = frontmatter(hub.read_text(encoding="utf-8")) or {}
        claimed, assigned = set(ids_in(meta.get("ids", ""))), set(plan[number].ids)
        for extra in sorted(claimed - assigned):
            report.fail(cfg.rel(hub), f"claims {extra}, which the plan does not assign to this day")
        for missing in sorted(assigned - claimed):
            report.fail(cfg.rel(hub), f"the plan assigns {missing} to this day; the hub omits it")
    return report


def cmd_depth(cfg: Config, args: list[str]) -> int:
    if "--list" in args:
        print(f"granth depth contract for {cfg.name} ({cfg.plan_version})\n")
        print("A part document carries, in order:")
        for n in cfg.part_sections:
            print(f"  - {n}{' (conditional)' if n in CONDITIONAL else ''}")
        print("\nA hub carries, in order:")
        for i, t in enumerate(cfg.hub_sections, start=1):
            print(f"  {i:>2}. {t}")
        print(f"\nLevels: {', '.join(cfg.levels)}")
        print(f"Sources: {cfg.sources_dir}/   Parts: {cfg.parts_dir}/")
        return 0

    targets = [int(a) for a in args if a.isdigit()] or sorted(
        n for n, f in day_dirs(cfg).items() if is_written(f, cfg))
    if not targets:
        print("granth: no written days yet — nothing to check.")
        return 0
    reports = [check_day(cfg, n) for n in targets]
    # A source is taught once in the whole curriculum, so this check spans days.
    cross = [f"{i} is taught in {len(p)} places ({', '.join(p)}) — a source is taught once "
             "and cited thereafter" for i, p in sorted(sources_taught(cfg).items()) if len(p) > 1]

    failed = 0
    for r in reports:
        head = f"day {r.day:>2}  {r.parts} parts" + (f" + {r.sources} sources" if r.sources else "")
        if r.ok:
            print(f"OK    {head}")
        else:
            failed += 1
            print(f"FAIL  {head}")
            for line in r.failures:
                print(f"        {line}")
    if cross:
        print("FAIL  curriculum")
        for line in cross:
            print(f"        {line}")
    if failed or cross:
        print(f"\n{failed} of {len(reports)} day(s) fail the depth contract.")
        return 1
    print(f"\nOK all {len(reports)} day(s) meet the depth contract.")
    return 0


# =============================================================================================
# The generated indexes
# =============================================================================================

BANNER = "> **Do not edit this file by hand.** It is regenerated by `{d} index`."


def truncate(text: str, width: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= width else text[:width - 1].rstrip() + "…"


def one_line_answer(text: str) -> str:
    """The first paragraph under the one-line-answer heading, flattened.

    Reads the paragraph rather than the first line: day documents are hard-wrapped, so stopping at
    the newline cuts most answers mid-sentence.
    """
    hit = re.search(r"^#{2,4}\s.*one[- ]line answer.*$", text, re.I | re.M)
    if not hit:
        return ""
    out: list[str] = []
    for line in text[hit.end():].splitlines():
        s = line.strip().lstrip("> ").strip()
        if s.startswith("#") or s.startswith("```"):
            break
        if not s:
            if out:
                break
            continue
        out.append(s)
    return re.sub(r"\s+", " ", " ".join(out))


class DayFacts:
    def __init__(self, cfg: Config, number: int, folder: Path) -> None:
        self.number, self.folder = number, folder
        self.written = is_written(folder, cfg)
        self.hub = frontmatter((folder / "LESSON.md").read_text(encoding="utf-8")) or {}
        self.title = self.hub.get("title", "")
        self.ids = ids_in(self.hub.get("ids", ""))
        self.parts, self.sources = [], []
        for path in part_files(folder, cfg):
            if path.parent == folder / cfg.parts_dir:
                continue
            text = path.read_text(encoding="utf-8")
            meta = frontmatter(text) or {}
            self.parts.append({"part": meta.get("part", ""),
                               "title": meta.get("title", path.stem),
                               "level": meta.get("level", ""),
                               "answer": one_line_answer(body(text)),
                               "path": f"{cfg.parts_dir}/{path.parent.name}/{path.name}"})
        for path in source_files(folder, cfg):
            meta = frontmatter(path.read_text(encoding="utf-8")) or {}
            self.sources.append({"source": meta.get("source", ""),
                                 "title": meta.get("title", path.stem),
                                 "path": f"{cfg.sources_dir}/{path.name}"})

    @staticmethod
    def key(part: dict[str, str]) -> tuple[float, float]:
        bits = re.findall(r"\d+", part["part"])
        return (float(bits[0]) if bits else 0.0, float(bits[1]) if len(bits) > 1 else 0.0)


def day_link(cfg: Config, number: int, facts: dict[int, DayFacts]) -> str:
    """A link that still points somewhere sensible before the day exists."""
    name = facts[number].folder.name if number in facts else f"day-{number:02d}"
    return f"../days/{name}/LESSON.md"


def build_all(cfg: Config) -> dict[Path, str]:
    read_plan(cfg)
    plan, phases, tracks = plan_days(cfg), plan_phases(cfg), plan_tracks(cfg)
    complete = set(progress_days(cfg))
    facts = {n: DayFacts(cfg, n, f) for n, f in sorted(day_dirs(cfg).items())
             if (f / "LESSON.md").exists()}
    today, d = date.today().isoformat(), cfg.driver
    head = [f"_Generated {today} by `granth.py`._", BANNER.format(d=d), ""]

    # --- traceability -----------------------------------------------------------------------
    track_of = {t.prefix: t.name for t in tracks}
    rows, open_count = [], 0
    for number, day in sorted(plan.items()):
        ph = phase_of(number, phases)
        for i in day.ids:
            claimed = number in facts and i in facts[number].ids
            if number in complete and claimed:
                mark, status = "[x]", f"closed day {number}"
            elif claimed:
                mark, status, open_count = "[~]", f"written day {number}, not in the ledger", open_count + 1
            else:
                mark, status, open_count = "[ ]", "open", open_count + 1
            rows.append(f"| `{i}` | {track_of.get(i.split('-')[0], i.split('-')[0])} "
                        f"| {ph.number if ph else '-'} | {number} | {mark} {status} |")
    trace = "\n".join([f"# Traceability — {cfg.name}", "", *head,
        "An ID counts as **closed** only when its day has a row in `docs/PROGRESS.md` *and* its",
        "hub's frontmatter claims the ID. **An open ID from a completed phase is a bug**, not a",
        "backlog item.", "", f"**{len(rows) - open_count} of {len(rows)} closed.**", "",
        "| ID | Track | Phase | Planned day | Status |", "| --- | --- | --- | --- | --- |",
        *rows, ""])

    # --- curriculum index -------------------------------------------------------------------
    where = {i: (n, d_.title) for n, d_ in sorted(plan.items()) for i in d_.ids}
    lines = [f"# Curriculum index — {cfg.name}", "", *head,
             "The day map answers *what does day 43 teach?* This answers the reverse — *where do I",
             "learn `XX-14`?* Every ID appears exactly once; a duplicate or a missing ID is a plan",
             "bug.", ""]
    seen = set()
    for track in tracks:
        owned = sorted((i for i in where if i.startswith(f"{track.prefix}-")),
                       key=lambda i: int(i.split("-")[1]))
        seen.update(owned)
        lines += [f"## {track.name} (`{track.prefix}-`) — {len(owned) or 'no'} IDs", "",
                  "| ID | Day | Day title |", "| --- | --- | --- |"]
        lines += [f"| `{i}` | [{where[i][0]}]({day_link(cfg, where[i][0], facts)}) "
                  f"| {truncate(where[i][1], 96)} |" for i in owned]
        lines.append("")
        if track.count is not None and owned and len(owned) != track.count:
            lines += [f"> **Mismatch.** The plan's track table says {track.count} IDs; the day map "
                      f"assigns {len(owned)}. Fix the plan, then regenerate.", ""]
    if sorted(set(where) - seen):
        lines += ["## Unclaimed prefixes", "",
                  "Assigned in the day map, but the prefix has no row in the track table.", "",
                  "| ID | Day |", "| --- | --- |"]
        lines += [f"| `{i}` | {where[i][0]} |" for i in sorted(set(where) - seen)] + [""]
    index = "\n".join(lines)

    # --- tracker ----------------------------------------------------------------------------
    written = [n for n, f in facts.items() if f.written]
    total = len(plan)
    pct = lambda c: f"{(100 * c / total):.1f}%" if total else "-"  # noqa: E731
    lines = [f"# Tracker — {cfg.name}", "", *head,
             "A day is **written** with a hub and a non-empty parts directory, and **complete**",
             "only when it also has a ledger row. A thin day is visible from the parts column.", "",
             "| | Count | Of plan |", "| --- | --- | --- |",
             f"| Days in the plan | **{total}** | 100% |",
             f"| Days written | **{len(written)}** | {pct(len(written))} |",
             f"| Days complete | **{len(complete & set(plan))}** | {pct(len(complete & set(plan)))} |",
             f"| Subtopic documents | **{sum(len(f.parts) for f in facts.values())}** | — |",
             f"| Source documents | **{sum(len(f.sources) for f in facts.values())}** | — |", "",
             "## Every day", "", "| Day | Phase | Title | Status | Parts | Sources | IDs |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for number, day in sorted(plan.items()):
        f_, ph = facts.get(number), phase_of(number, phases)
        status = ("complete" if number in complete and f_ and f_.written
                  else "written" if f_ and f_.written else "hub only" if f_ else "not started")
        title = truncate(f_.title if f_ and f_.title else day.title, 72)
        cell = f"[{title}]({day_link(cfg, number, facts)})" if f_ else title
        lines.append(f"| {number} | {ph.number if ph else '-'} | {cell} | {status} "
                     f"| {len(f_.parts) if f_ else 0} | {len(f_.sources) if f_ else 0} "
                     f"| {', '.join(f'`{i}`' for i in day.ids) or '—'} |")
    lines += ["", "## Phases", "", "| Phase | Days | Theme | Written | Complete | Gate |",
              "| --- | --- | --- | --- | --- | --- |"]
    for ph in phases:
        if ph.first is None or ph.last is None:
            continue
        span = [n for n in plan if ph.first <= n <= ph.last]
        lines.append(f"| {ph.number} | {ph.days} | {truncate(ph.theme, 48)} "
                     f"| {len([n for n in span if n in facts and facts[n].written])}/{len(span)} "
                     f"| {len([n for n in span if n in complete])}/{len(span)} "
                     f"| {truncate(ph.gate, 56)} |")
    tracker = "\n".join(lines + [""])

    # --- wiki -------------------------------------------------------------------------------
    lines = [f"# {cfg.name} wiki — one row per day", "", *head,
             "For a day's parts open `wiki/day-NN.md`; open the day folder itself only to write",
             "it. Cross-day lookups live in `wiki/ENTITIES.md`.", "",
             "| Day | Subject | IDs closed | Parts | Sources |", "| --- | --- | --- | --- | --- |"]
    for number, f_ in sorted(facts.items()):
        srcs = ", ".join(s["source"] for s in f_.sources if s["source"]) or "—"
        lines.append(f"| [{number:02d}](wiki/day-{number:02d}.md) | {truncate(f_.title, 84)} "
                     f"| {', '.join(f_.ids) or '—'} | {len(f_.parts)} | {srcs} |")
    wiki = "\n".join(lines + [""])

    out = {cfg.docs / "TRACEABILITY.md": trace, cfg.docs / "CURRICULUM_INDEX.md": index,
           cfg.docs / "TRACKER.md": tracker, cfg.docs / "WIKI.md": wiki}

    # --- one page per day, plus the entity index ---------------------------------------------
    for number, f_ in facts.items():
        rel = f"../../days/{f_.folder.name}"
        lines = [f"# Day {number:02d} — {f_.title}", "", *head,
                 f"Hub: [`LESSON.md`]({rel}/LESSON.md) — IDs closed: {', '.join(f_.ids) or 'none'}",
                 "", "| Part | Title | Level | One-line answer |", "| --- | --- | --- | --- |"]
        for p in sorted(f_.parts, key=DayFacts.key):
            lines.append(f"| {p['part']} | [{truncate(p['title'], 60)}]({rel}/{p['path']}) "
                         f"| {p['level']} | {truncate(p['answer'], 120)} |")
        if f_.sources:
            lines += ["", "## Sources taught on this day", "", "| Identifier | Document |",
                      "| --- | --- |"]
            lines += [f"| {s['source']} | [{truncate(s['title'], 72)}]({rel}/{s['path']}) |"
                      for s in f_.sources]
        out[cfg.docs / "wiki" / f"day-{number:02d}.md"] = "\n".join(lines + [""])

    lines = [f"# Entities — {cfg.name}", "", *head,
             "The answer to *which day taught X?* and *is this source already taught?* — the two",
             "questions a long curriculum makes expensive to answer by reading.", "",
             "## Sources", "", "| Identifier | Taught on | Document |", "| --- | --- | --- |"]
    srows = sorted((s["source"], n, s["title"]) for n, f_ in facts.items()
                   for s in f_.sources if s["source"])
    lines += ([f"| {i} | [day {n}](day-{n:02d}.md) | {truncate(t, 72)} |" for i, n, t in srows]
              or ["| — | — | no source documents yet |"])
    lines += ["", "## Curriculum IDs", "", "| ID | Closed on |", "| --- | --- |"]
    irows = sorted(((i, n) for n, f_ in facts.items() for i in f_.ids),
                   key=lambda r: (r[0].split("-")[0], int(r[0].split("-")[1])))
    lines += ([f"| `{i}` | [day {n}](day-{n:02d}.md) |" for i, n in irows]
              or ["| — | no IDs claimed yet |"])
    out[cfg.docs / "wiki" / "ENTITIES.md"] = "\n".join(lines + [""])
    return out


def cmd_index(cfg: Config, args: list[str]) -> int:
    docs = build_all(cfg)
    if "--check" in args:
        stale = [cfg.rel(p) for p, t in docs.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != t]
        if stale:
            print("granth: these generated documents are stale —")
            for name in stale:
                print(f"        {name}")
            print(f"        run `{cfg.driver} index`.")
            return 1
        print(f"OK {len(docs)} generated document(s) are current.")
        return 0
    for path, text in docs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(f"OK wrote {len(docs)} generated document(s) under {cfg.rel(cfg.docs)}/.")
    return 0


# =============================================================================================
# The day brief, and the order guard
# =============================================================================================

def cmd_brief(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "brief")
    plan, phases = plan_days(cfg), plan_phases(cfg)
    complete, on_disk = progress_days(cfg), day_dirs(cfg)
    out: list[str] = [f"# {cfg.name} — brief for day {day}", ""]
    status = 0

    if day not in plan:
        first, last = (min(plan), max(plan)) if plan else (0, 0)
        print("\n".join(out + [f"**STOP.** The plan has no day {day}. It runs {first} to {last}.",
              "Adding, merging or reordering a day is a plan amendment: write the ADR first."]))
        return 1
    entry, ph = plan[day], phase_of(day, phases)

    expected = (max(complete) + 1) if complete else min(plan)
    if day != expected:
        status = 1
        if day in complete:
            out += [f"**STOP.** Day {day} already has a row in the progress ledger.",
                    f"The next unwritten day is **{expected}**."]
        elif day < expected:
            out.append(f"**STOP.** Day {day} is behind the ledger. The next day is **{expected}**.")
        else:
            missing = ", ".join(str(n) for n in range(expected, day) if n not in complete)
            out += [f"**STOP.** Day {day} is out of order — day **{expected}** is next.", "",
                    f"Not yet in the ledger: {missing}.",
                    "Never skip a day, merge two days, or reorder days without an ADR."]
        out += ["", "---", ""]

    out += ["## The assignment", "", f"**Title (from the plan):** {entry.title}", ""]
    out.append(f"**Close exactly these IDs — no more, no fewer:** {', '.join(entry.ids)}"
               if entry.ids else
               "**Closes no IDs.** State why in the hub, so traceability stays honest.")
    out.append("")
    if ph:
        out += [f"**Phase {ph.number} — {ph.theme}**", "", f"- Days in the phase: {ph.days}",
                f"- The gate this day feeds: {ph.gate}", ""]

    claimed: set[str] = set()
    for number, folder in on_disk.items():
        hub = folder / "LESSON.md"
        if number in complete and hub.exists():
            claimed |= set(ids_in((frontmatter(hub.read_text(encoding="utf-8")) or {}).get("ids", "")))
    debt = [(n, i) for n, p in sorted(plan.items()) if n < day for i in p.ids if i not in claimed]
    if debt:
        out += ["## Open IDs from earlier days", "",
                "An open ID from a day already behind you is a bug, not a backlog item.", ""]
        out += [f"- `{i}` was assigned to day {n} and is not closed." for n, i in debt] + [""]

    previous = max((n for n in plan if n < day), default=None)
    if previous is not None:
        folder = find_day(cfg, previous)
        out += [f"## Where day {previous} left off", ""]
        if folder is None:
            out.append(f"No folder for day {previous} — it was never written.")
        else:
            hub = folder / "LESSON.md"
            meta = frontmatter(hub.read_text(encoding="utf-8")) if hub.exists() else None
            if meta:
                out += [f"- Hub: `{cfg.rel(hub)}`", f"- Title: {meta.get('title', '?')}",
                        f"- Status: {meta.get('status', '?')}"]
            checklist = folder / "CHECKLIST.md"
            boxes = ([ln.strip() for ln in checklist.read_text(encoding="utf-8").splitlines()
                      if ln.strip().startswith("- [ ]")] if checklist.exists() else [])
            if boxes:
                out.append(f"- **{len(boxes)} unticked checklist box(es)** — ask before moving on:")
                out += [f"    {b}" for b in boxes[:8]]
                if len(boxes) > 8:
                    out.append(f"    ... and {len(boxes) - 8} more")
            elif checklist.exists():
                out.append("- Checklist: fully ticked.")
            if is_written(folder, cfg):
                out.append(f"- Read its parts before writing day {day}; build on them, never "
                           "repeat them.")
        out.append("")

    taught = sorted((meta["source"], n, meta.get("title", p.stem))
                    for n, f_ in sorted(on_disk.items()) for p in source_files(f_, cfg)
                    if (meta := frontmatter(p.read_text(encoding="utf-8")) or {}).get("source"))
    if taught:
        out += ["## Sources already taught (cite and link these — never teach one twice)", "",
                "| Identifier | Day | Document |", "| --- | --- | --- |"]
        out += [f"| {i} | {n} | {t} |" for i, n, t in taught] + [""]

    out += ["## Before you write a line", "",
            f"1. `{cfg.rel(cfg.plan)}` — the depth contract section, in full. It is the standard.",
            "2. The style guide section of the same plan — the register and the story rules.",
            f"3. `{cfg.rel(cfg.docs / 'GLOSSARY.md')}` — so a term defined on day 3 is defined the "
            "same way today.",
            "4. Verify every fact live. A version, an interface, a citation: look it up today, or",
            "   leave a TODO carrying the exact lookup command. Never a remembered answer.", ""]
    if status == 0:
        out.append(f"**Day {day} is next. Go.**")
    print("\n".join(out))
    return status


# =============================================================================================
# The rest of the driver
# =============================================================================================

def need_day(cfg: Config, args: list[str], command: str) -> int:
    if not args or not re.fullmatch(r"\d{1,3}", args[0]):
        sys.exit(f"usage: {cfg.driver} {command} <day-number>")
    return int(args[0])


def slugify(text: str) -> str:
    """A 1-4 word kebab-case label from the plan's title.

    Titles read `<subject> — <the elaboration>`, so the slug comes from the head phrase: truncating
    the whole title at four words lands mid-clause.
    """
    head = re.split(r"\s+[-–—:]\s+", text.strip(), maxsplit=1)[0]
    words = re.sub(r"[^a-z0-9]+", " ", head.lower()).split()
    dropped = {"a", "an", "the", "and", "of", "to", "in", "for", "with", "on", "by", "its"}
    return "-".join(([w for w in words if w not in dropped] or words)[:4]) or "day"


def cmd_status(cfg: Config, args: list[str]) -> int:
    plan = plan_days(cfg)
    written = [n for n, f in day_dirs(cfg).items() if is_written(f, cfg)]
    complete = [n for n in progress_days(cfg) if n in plan]
    nxt = (max(complete) + 1) if complete else (min(plan) if plan else 0)
    print(f"{cfg.name} ({cfg.plan_version}): {len(complete)}/{len(plan)} days complete, "
          f"{len(written)} written. Next: day {nxt}.")
    return 0


def cmd_start(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "start")
    folder = find_day(cfg, day)
    if folder is None:
        print(f"no day {day} on disk yet — `{cfg.driver} brief {day}` says what it must cover.")
        return 1
    if not is_written(folder, cfg):
        print(f"day {day} has a folder but no parts — it is not written.")
        return 1
    print(f"-> open {cfg.rel(folder / 'LESSON.md')}   (read its map, then the parts in order)")
    for path in part_files(folder, cfg):
        print(f"     {path.relative_to(folder).as_posix()}")
    for path in source_files(folder, cfg):
        print(f"     {path.relative_to(folder).as_posix()}   (read after the parts)")
    return 0


def cmd_parts(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "parts")
    folder = find_day(cfg, day)
    if folder is None or not (folder / cfg.parts_dir).is_dir():
        print(f"day {day} has no {cfg.parts_dir}/ — it is not written.")
        return 1
    for path in part_files(folder, cfg):
        print(path.relative_to(folder / cfg.parts_dir).as_posix())
    return 0


def cmd_new(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "new")
    plan = plan_days(cfg)
    if day not in plan:
        print(f"the plan has no day {day} — amend the plan first.")
        return 1
    if find_day(cfg, day):
        print(f"day {day} already exists at {cfg.rel(find_day(cfg, day))}.")
        return 1
    templates = cfg.days / "_TEMPLATES"
    if not templates.is_dir():
        print(f"no templates at {cfg.rel(templates)} — nothing to scaffold from.")
        return 1
    slug = slugify(args[1]) if len(args) > 1 else slugify(plan[day].title)
    folder = cfg.days / f"day-{day:02d}-{slug}"
    (folder / cfg.parts_dir / "01-rename-me").mkdir(parents=True, exist_ok=True)
    (folder / "lab").mkdir(exist_ok=True)
    for name in ("LESSON.md", "CHECKLIST.md"):
        if (templates / name).exists():
            shutil.copy(templates / name, folder / name)
    if (templates / "PART.md").exists():
        shutil.copy(templates / "PART.md",
                    folder / cfg.parts_dir / "01-rename-me" / "1.1-rename-me.md")
    print(f"-> {cfg.rel(folder)}")
    print(f"   the plan assigns: {plan[day].title}")
    print(f"   IDs to close: {', '.join(plan[day].ids) or 'none'}")
    print("   rename the section folder and the part file to say what they teach, then write.")
    return 0


def cmd_check(cfg: Config, args: list[str]) -> int:
    for command, label in ((cfg.lint, "lint"), (cfg.format_check, "format"), (cfg.test, "tests")):
        if command:
            print(f"--- {label}: {command}", flush=True)
            if subprocess.call(command, shell=True, cwd=ROOT) != 0:
                print(f"FAIL {label}")
                return 1
    print("--- depth contract", flush=True)
    if cmd_depth(cfg, []) != 0:
        return 1
    print("--- generated documents", flush=True)
    if cmd_index(cfg, ["--check"]) != 0:
        return 1
    print("\nOK all green")
    return 0


def cmd_done(cfg: Config, args: list[str]) -> int:
    day = need_day(cfg, args, "done")
    folder = find_day(cfg, day)
    if folder is None:
        print(f"no folder for day {day}.")
        return 1
    checklist = folder / "CHECKLIST.md"
    if not checklist.exists():
        print(f"FAIL no {cfg.rel(checklist)} — a day has no definition of done without it.")
        return 1
    boxes = [ln for ln in checklist.read_text(encoding="utf-8").splitlines()
             if ln.strip().startswith("- [ ]")]
    if boxes:
        print(f"FAIL {len(boxes)} unticked box(es) in {cfg.rel(checklist)}:")
        for line in boxes:
            print(f"      {line.strip()}")
        return 1
    if day not in progress_days(cfg):
        print(f"FAIL day {day} has no row in {cfg.rel(cfg.progress)}.")
        print("      Paste the row from the hub's ledger section first — the ledger is the record,")
        print("      and a commit is not one.")
        return 1
    # Regenerate BEFORE checking: the ledger row this command just insisted on is itself an input
    # to the indexes, so checking first would fail on a staleness the day created.
    if cmd_index(cfg, []) != 0 or cmd_check(cfg, []) != 0:
        return 1
    meta = frontmatter((folder / "LESSON.md").read_text(encoding="utf-8")) or {}
    ids = ids_in(meta.get("ids", ""))
    message = f"day {day:02d}: {meta.get('title', folder.name)}"
    if ids:
        message += f" — closes {', '.join(ids)}"
    if subprocess.call(["git", "add", "-A"], cwd=ROOT) != 0:
        return 1
    if subprocess.call(["git", "commit", "-m", message], cwd=ROOT) != 0:
        return 1
    print(f"OK day {day} committed.")
    return 0


def cmd_doctor(cfg: Config, args: list[str]) -> int:
    """The repository's own wiring, checked before blaming a day for a tool's failure."""
    problems = []
    if not (ROOT / "granth.toml").exists():
        problems.append("no granth.toml at the repository root")
    if not cfg.plan.exists():
        problems.append(f"no plan at {cfg.rel(cfg.plan)}")
    else:
        text = cfg.plan.read_text(encoding="utf-8")
        problems += [f"the plan has no <!-- granth:{m}:start --> block"
                     for m in ("tracks", "phases", "day-map") if not marked_block(text, m)]
    problems += [f"no {cfg.rel(cfg.docs / n)}" for n in
                 ("PROGRESS.md", "CHANGELOG_PLAN.md", "GLOSSARY.md", "SOURCES.md")
                 if not (cfg.docs / n).exists()]
    if not (cfg.docs / "adr").is_dir():
        problems.append(f"no {cfg.rel(cfg.docs / 'adr')}/")
    if not cfg.days.is_dir():
        problems.append(f"no {cfg.rel(cfg.days)}/")
    if not (ROOT / ".gitignore").exists():
        problems.append("no .gitignore — secrets discipline starts with the file that enforces it")

    plan = plan_days(cfg) if cfg.plan.exists() else {}
    seen: dict[str, int] = {}
    for number, day in plan.items():
        for i in day.ids:
            if i in seen:
                problems.append(f"{i} is assigned to both day {seen[i]} and day {number}")
            seen[i] = number
    if problems:
        print("granth doctor found:")
        for line in problems:
            print(f"  - {line}")
        return 1
    print(f"OK {cfg.name}: config, plan markers, ledgers and day map all present.")
    print(f"   {len(plan)} days planned, {len(seen)} IDs assigned, each to exactly one day.")
    return 0


COMMANDS = {"status": cmd_status, "brief": cmd_brief, "start": cmd_start, "parts": cmd_parts,
            "new": cmd_new, "depth": cmd_depth, "index": cmd_index, "check": cmd_check,
            "done": cmd_done, "doctor": cmd_doctor}

USAGE = """usage: {d} <command> [args]

  status          how many days are written, how many complete, what is next
  brief N         what day N must close, its gate, and whether N is allowed yet
  start N         point at day N's hub and list its documents in reading order
  parts N         list day N's subtopic documents
  new N [slug]    scaffold an empty day folder from days/_TEMPLATES/
  depth [N]       check day N (or every written day) against the depth contract
  depth --list    print the contract as configured
  index [--check] regenerate the derived documents in docs/ (or fail if stale)
  check           lint + format + tests + depth contract + generated documents
  done N          refuse unless the checklist is ticked and the ledger row exists, then commit
  doctor          this repository's own wiring: config, plan markers, ledgers, day map
"""


def main(argv: list[str]) -> int:
    cfg = load_config()
    command = argv[0] if argv else "help"
    handler = COMMANDS.get(command)
    if handler is None:
        print(USAGE.format(d=cfg.driver))
        return 0 if command in {"help", "-h", "--help"} else 2
    return handler(cfg, argv[1:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
