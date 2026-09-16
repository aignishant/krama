"""Temporary authoring assembly for days 11–20; not a curriculum generator."""
from pathlib import Path
from build_skeleton import LANG_SECTIONS, combine_practice, lang_lesson_name
from curriculum import load

ROOT = Path(__file__).resolve().parent.parent
STORIES = {}
DATA = {}
EXERCISES = {}

def topic(day, story, exercises):
    STORIES[day] = story.strip()
    EXERCISES[day] = exercises

def lesson(day, language, idea, code, output, trap, answer, followups, recall, setup="", source=""):
    DATA[day, language] = dict(idea=idea, code=code.strip(), output=output, trap=trap,
        answer=answer, followups=followups, recall=recall, setup=setup, source=source)

def write_all():
    for day in load():
        if not 11 <= day.n <= 20:
            continue
        folder = ROOT / "days" / day.folder
        comparison = "\n".join(f"- **{lang}** — {DATA[day.n, lang]['recall'][0]}" for lang in ("Python", "Go", "C++"))
        for spec, lang in zip(day.langs.lessons, ("Python", "Go", "C++")):
            d = DATA[day.n, lang]
            path = folder / lang_lesson_name(spec)
            original = path.read_text(encoding="utf-8")
            header = original.split("## 1.")[0].split("> Not written yet.")[0].replace("status: empty", "status: written").rstrip()
            syntax = {"Python": "python", "Go": "go", "C++": "cpp"}[lang]
            paragraphs = d['idea'].split("\n\n")
            first = paragraphs[0]
            fragment = "\n".join(d['code'].splitlines()[:min(8, len(d['code'].splitlines()))])
            sections = [first + "\n\n" + f"Today you use {day.langs.theme.lower()} to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.",
                STORIES[day.n],
                d['idea'],
                "```text\n" + d['recall'][0] + "\n    |\n    v\n" + d['recall'][1] + "\n    |\n    v\n" + d['recall'][2] + "\n```\n\nRead from top to bottom. The first line states the mechanism; the next two state what you must account for when using it.",
                f"Start with this opening piece of the example:\n\n```{syntax}\n{fragment}\n```\n\n{paragraphs[-1]}\n\n{d['setup']}\n\nThe complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`, `main.go`, or `main.cpp`, matching the language.\n\n```{syntax}\n{d['code']}\n```\n\n**Check the result:** {d['output']}",
                comparison + "\n\nThe syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.",
                d['trap'],
                f"**How it gets asked:** “{day.langs.question}” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”\n\n**What to say out loud:** {d['answer']}\n\n**Follow-ups**\n\n" + "\n\n".join(f"{i}. **{q}** {a}" for i, (q,a) in enumerate(d['followups'], 1)) + f"\n\n**Model answer:** {d['answer']} Start the demonstration with the working example in §5, predict its output, and then make the change from §7. Explain the changed behaviour using the rule, rather than memorising the output. {d['recall'][-1]}",
                "\n".join("- " + r for r in d['recall'])]
            text = header + "\n\n" + "\n\n".join(f"## {i}. {heading}\n\n{body}" for i, ((heading,_), body) in enumerate(zip(LANG_SECTIONS, sections), 1)) + "\n"
            if d['source']:
                text += "\nFurther reading: " + d['source'] + "\n"
            path.write_text(text, encoding="utf-8", newline="\n")
        old = folder / "08-lang-practice.md"
        language_practice = f"**Theme:** {day.langs.theme}\n\n## Build these, in all three languages\n\nUse the same inputs in Python, Go, and C++. Predict the result before running it, then explain any difference.\n\n| # | Exercise | What it is really testing |\n|---|---|---|\n"
        language_practice += "\n".join(f"| {i} | {exercise} | {why} |" for i,(exercise,why) in enumerate(EXERCISES[day.n],1))
        language_practice += "\n\n## Compare\n\n" + comparison + "\n\n## Say these out loud\n\n"
        language_practice += f"1. {day.langs.question}\n2. Explain the failure example in each language lesson and repair it.\n3. Which behaviour is checked before the program runs, and which requires a runtime check? Give a concrete example from today.\n\n## Before you move on\n\n- [ ] I completed all three language exercises in Python, Go, and C++.\n- [ ] I can predict the working examples and explain the failure cases.\n- [ ] I answered all three questions above out loud.\n"
        practice = folder / "03-practice.md"
        practice.write_text(combine_practice(practice.read_text(encoding="utf-8"), language_practice), encoding="utf-8", newline="\n")
        old.unlink()
