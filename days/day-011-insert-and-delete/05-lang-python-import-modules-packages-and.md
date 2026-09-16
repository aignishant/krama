---
day: 11
track: lang-python
title: "import, modules, packages, and the main guard"
theme: "Splitting code across files"
phase: "Languages: every language, every basic"
status: written
---

# Day 011 · Python — import, modules, packages, and the main guard

**Today's theme:** Splitting code across files

**After today you can:** You can split a program into three files in each language and explain what is visible from where.

**The interviewer asks it as:** *What makes a name visible to another file?*

---

## 1. What this is, and why it matters

A **module** is a Python file you can import. A **package** groups modules under a shared name, commonly using a directory containing `__init__.py`. `import arithmetic` binds the module name; `arithmetic.add(2, 3)` asks that module for its function.

Today you use splitting code across files to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Meera is arranging dinner for six friends. Until yesterday, everyone asked her everything. Where are the plates? When should the rice go on? Who is buying milk? Her phone kept buzzing while she tried to cook, and she answered the same question three times.

Tonight she divides the work. Arun handles food, Leela handles drinks, and Meera handles the table. Everyone knows who to ask. Arun tells the group when dinner will be ready, but he does not send them every small decision he makes in the kitchen. Leela needs the serving time, not the order in which he washes vegetables.

At seven, a guest asks Leela whether the rice is ready. She asks Arun rather than inventing an answer. Arun remains responsible for that one piece of information. If he changes the meal, he tells the group what has changed at the boundary: dinner is now at eight. The others can adjust without learning his whole recipe.

There is one final rule. Asking Arun about dinner must not cause him to start cooking a second meal. A question and the instruction to begin are different things. Meera sends the instruction once, after everyone arrives.

The arrangement works because each person has a clear job, a clear way to be reached, and a clear distinction between answering a question and starting the evening. Splitting the work helps only when those boundaries remain understandable.

## 3. The idea in plain English

A **module** is a Python file you can import. A **package** groups modules under a shared name, commonly using a directory containing `__init__.py`. `import arithmetic` binds the module name; `arithmetic.add(2, 3)` asks that module for its function.

Meera's separate responsibilities become separate files. Keep calculation independent of presentation. Python executes a module's top-level statements when it first imports it in a process, then normally reuses the module from its import cache. A leading underscore marks an internal name by convention; it is not an access restriction.

The **main guard**, `if __name__ == "__main__":`, runs its body when the file is the entry point. When the file is imported, `__name__` is its module name instead. Put command-line work behind the guard so importing a helper does not start the application.

## 4. The picture

```text
main (entry point)
  | calls add(2, 3)       | formats result
  v                       v
calculation component    presentation component
  | returns 5             | returns total=5
  +-----------------------+
              |
              v
         terminal output
```

The entry point coordinates two responsibilities. The calculation component does not need to know how the result will be displayed.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
if __name__ == "__main__":
    main()
```

The guard belongs in the entry file. Running that file calls main; importing it creates reusable definitions without starting the command. The two helper files each own one function, so the call path is main → add → label → print.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
# arithmetic.py
def add(left: int, right: int) -> int:
    return left + right

# display.py
def label(total: int) -> str:
    return f"total={total}"

# main.py
import arithmetic
from display import label

def main() -> None:
    print(label(arithmetic.add(2, 3)))

if __name__ == "__main__":
    main()
```

**Check the result:** Run `python main.py` from the directory containing the three files. It prints `total=5`. Running `python -c "import main"` prints nothing.

## 6. How the other two languages do it

- **Python** — A module owns a collection of names.
- **Go** — Packages, not files, control Go name visibility.
- **C++** — Headers publish declarations to callers.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** put `main()` outside the guard, then import `main` from another file. The demonstration runs during import. Restore the guard; reusable code should not unexpectedly read input or print output.

**Failure to reproduce:** in an otherwise empty directory run `python -c "import missing_krama_module"`. The final error line is `ModuleNotFoundError: No module named 'missing_krama_module'`. Check the spelling and where Python is searching before changing the code. Also avoid naming a file `json.py`: it can shadow the standard library module.

## 8. Say it out loud

**How it gets asked:** “What makes a name visible to another file?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I split code by responsibility and import the module that owns a name. Importing is an execution step, not a textual paste. I keep the entry-point call behind the main guard and keep reusable modules free of command-line side effects. Packages give related modules a shared namespace.

**Follow-ups**

1. **Does an underscore make a name private?** No. It communicates intent; normal attribute access can still reach it.

2. **What about circular imports?** Two modules can observe partially initialised state. Move their shared dependency into a third module.

3. **When should I use `python -m package.module`?** When running a module in its package context, especially when it uses relative imports.

**Model answer:** The guard belongs in the entry file. Running that file calls main; importing it creates reusable definitions without starting the command. The two helper files each own one function, so the call path is main → add → label → print. Keep dependencies pointing in a clear direction.

## 9. Recall card

- A module owns a collection of names.
- Import runs top-level code on first loading.
- The main guard separates reuse from entry-point work.
- Packages group modules; underscores express intent.
- Keep dependencies pointing in a clear direction.
