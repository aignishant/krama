---
day: 14
track: lang-python
title: "uv, venv, pyproject.toml, ruff"
theme: "Formatters, linters, and a real project layout"
phase: "Languages: every language, every basic"
status: written
---

# Day 014 · Python — uv, venv, pyproject.toml, ruff

**Today's theme:** Formatters, linters, and a real project layout

**After today you can:** You can start a new project in each language from an empty folder, with formatting and dependencies working.

**The interviewer asks it as:** *How do you set up a new project so a teammate can build it on day one?*

---

## 1. What this is, and why it matters

A **virtual environment** gives a project its own installed Python packages. `venv` is Python's built-in environment tool; `uv` can manage environments and project dependencies. `pyproject.toml` records project metadata and tool settings. A lockfile records a resolved dependency set for repeatable application environments.

Today you use formatters, linters, and a real project layout to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Farah invites her cousin to help bake a cake. She sends a photo of the finished cake and says it is easy. Her cousin arrives with flour, but the recipe needs a different kind. The measuring cup has no markings. The oven dial has a worn patch where the temperature should be. Farah knows what all these things mean because she uses them every week. Her cousin does not.

The following Saturday, Farah prepares differently. She saves a shopping list on her phone, including the exact sizes of the packets. She puts the bowls together and checks that the scales turn on. She explains which oven setting she uses and where the cake goes after baking. Her cousin can now repeat the work without asking a question at every step.

They also agree on a few small habits. Wash a spoon before using it for another ingredient. Put lids back immediately. Wipe the counter before measuring the next thing. These habits do not guarantee a good cake. They remove preventable confusion so both people can pay attention to the mixture.

At the end, Farah keeps the recipe and shopping list, but throws away the used packaging. Next week she wants the instructions and ingredients, not yesterday's mess. She asks her cousin to try again without help. If the cake only works when Farah stands beside the oven, the instructions are still missing something important.

## 3. The idea in plain English

A **virtual environment** gives a project its own installed Python packages. `venv` is Python's built-in environment tool; `uv` can manage environments and project dependencies. `pyproject.toml` records project metadata and tool settings. A lockfile records a resolved dependency set for repeatable application environments.

Farah's ingredient list becomes declared dependencies; her personal kitchen becomes your local environment. Do not require teammates to guess which packages happen to be installed globally. `uv add --dev ruff` declares a development tool and updates the lockfile. `uv run` runs a command in the project's environment.

Ruff has separate formatting and linting commands. A **formatter** standardises layout. A **linter** checks configured rules for suspicious or unwanted code patterns. Neither proves your program computes the right result. Keep the application small enough to run directly before adding packaging machinery you do not need.

## 4. The picture

```text
source + declared requirements + tool settings
                       |
                       v
              fresh project environment
                /       |         \
               v        v          v
           format     checks     build/run
                       |            |
                       v            v
                  diagnostics   observed result
```

A fresh environment should reproduce the workflow from committed inputs. Formatting, diagnostics, and running the program answer different questions.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
def add(left: int, right: int) -> int:
    return left + right
```

Keep the behaviour independent of the entry point so running it is straightforward. The tooling commands below operate on this same source: format controls layout, check reports configured lint problems, and run executes the program.

With uv installed, create an empty folder and run `uv init`, then `uv add --dev ruff`. Replace its `main.py` with the program below. Commit the generated metadata and lockfile. See [uv projects](https://docs.astral.sh/uv/guides/projects/) and [Ruff's tutorial](https://docs.astral.sh/ruff/tutorial/) for these workflows.

The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
def add(left: int, right: int) -> int:
    return left + right

def main() -> None:
    total = add(2, 3)
    print(total)

if __name__ == "__main__":
    main()
```

**Check the result:** `uv run main.py` prints `5`. `uv run ruff format --check .` checks layout; `uv run ruff check .` runs lint rules. Format first with `uv run ruff format .` if needed.

## 6. How the other two languages do it

- **Python** — Declare project metadata and dependencies in pyproject.toml.
- **Go** — go.mod identifies a module and its requirements.
- **C++** — CMake describes targets and their requirements.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** install Ruff globally but omit it from the project. Your command works while a teammate's fresh environment lacks it. Declare development dependencies and commit `pyproject.toml` and `uv.lock`; do not commit `.venv`.

**Failure to reproduce:** add `import os` without using it, then run `uv run ruff check .`. The report includes `F401` and `` `os` imported but unused ``. Formatting will not fix that mistake. Remove the import or use it intentionally, then rerun both checks.

## 8. Say it out loud

**How it gets asked:** “How do you set up a new project so a teammate can build it on day one?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I declare the Python requirement and dependencies in pyproject.toml, keep an isolated environment, and commit the application's lockfile. I provide one command to run it and separate formatting and lint checks. I then try those commands from a fresh checkout. A successful formatter says the layout is consistent, not that the program is correct.

**Follow-ups**

1. **What is the standard-library alternative to uv?** Use python -m venv .venv, activate it, and install declared dependencies with pip.

2. **Should .venv be committed?** No. Recreate it from project declarations.

3. **What validates behaviour?** Running examples and meaningful tests; a linter cannot replace those.

**Model answer:** Keep the behaviour independent of the entry point so running it is straightforward. The tooling commands below operate on this same source: format controls layout, check reports configured lint problems, and run executes the program. Verify the documented command in a fresh environment.

## 9. Recall card

- Declare project metadata and dependencies in pyproject.toml.
- Use a project-specific environment.
- Run formatting and lint checks separately.
- Commit an application lockfile; exclude .venv.
- Verify the documented command in a fresh environment.
