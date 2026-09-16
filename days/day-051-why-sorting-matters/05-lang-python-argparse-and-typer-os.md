---
day: 51
track: lang-python
title: "argparse and typer, os.environ, and a settings class"
theme: "Configuration: flags, environment, files"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 051 · Python — argparse and typer, os.environ, and a settings class

**Today's theme:** Configuration: flags, environment, files

**After today you can:** You can configure a program from flags, env vars and a file, with a clear precedence order, in each language.

**The interviewer asks it as:** *Where should a database password come from, and where should it never be?*

---

## 1. What this is, and why it matters

Configuration is everything a program needs to know that is not in its code: which port to
listen on, where the database is, whether to log verbosely, and the password. It comes from
three places, a file checked into the repository with the defaults, environment variables set by
whoever runs the program, and flags typed on the command line, and the program merges them in a
fixed order into one settings object that the rest of the code reads. In Python the pieces are
`argparse` from the standard library for flags, `os.environ` for the environment, `json` or
`tomllib` for the file, and a frozen dataclass to hold the result.

At work, the first hour on any new service is spent finding out where its configuration comes
from, and the worst incidents start with a password in the wrong place. In interviews the
question is asked exactly as the header puts it, and the interviewer is listening for two things:
the word "never" attached to the right place, and a precedence order you can say without
hesitating.

## 2. The story

Lakshmi cooks for a hostel canteen, two hundred plates at lunch. Three things tell her what to
cook and how.

On the kitchen wall is the laminated card. It has been there for years. Sambar on Monday, rajma
on Tuesday, how many kilos of rice for two hundred, the time the gas goes on. Anybody who walks
into the kitchen can read it, and every new helper is told to read it first. It is the way things
are unless somebody says otherwise.

Every morning there is a note on the board by the door, written by the warden the night before.
"Only 140 today, exam batch is away." "Use the small hall." The note is for today only. It does
not change the card, and tomorrow there will be a different note or none. Lakshmi reads the note
after the card, and where they disagree, the note wins.

And then there is the warden himself, when he walks in at ten and says "make it less spicy,
the visitors are from abroad". That is for this one lunch, said out loud, and it beats both the
card and the note. Nobody writes it down.

So the order is always the same. Card, then note, then whatever is said in the room. Later beats
earlier, and Lakshmi can tell you at any moment why she is doing what she is doing, and which of
the three it came from.

One thing is on none of them. The key to the store room, where the month's rice and oil are
kept, is not written on the card, because the card is on the wall and three hundred people walk
past it. It is not on the note, because the note is on a board by the door. The warden hands it
to Lakshmi at the start of her shift, from his pocket to hers, and she gives it back at the end.
If a new helper asks where the key is written down, the answer is that it is not, anywhere, and
that is the point.

## 3. The idea in plain English

The laminated card is the **config file**: `config.json` next to the program, checked into the
repository, readable by anyone with the code. It carries the defaults and the things that rarely
change. The program reads it with `json.loads` from [day 40](../day-040-2d-prefix-sums/README.md).
The standard library also reads TOML with `tomllib`, which is what `pyproject.toml` from
[day 44](../day-044-first-and-last-occurrence/README.md) uses; the shape of the code is the same.

The note on the board is the **environment**: variables like `APP_PORT=9100` that the shell, the
container, or the deployment system sets before the program starts. `os.environ` is a dict of
them. They are per-machine and per-run, they do not live in the repository, and they are how the
same code runs on a laptop and in production with different settings.

What the warden says out loud is a **flag**: `--port 9200` typed after the program name.
`argparse` declares which flags exist, parses `sys.argv`, and gives you a namespace with one
attribute per flag. Flags are for this one run, and they also give you `--help` for free.

Card, note, room is the **precedence**: defaults, then file, then environment, then flags, each
one overriding the last. The program applies them in that order into a **settings object**, a
frozen dataclass from [day 40](../day-040-2d-prefix-sums/README.md), so the rest of the code
reads `settings.port` and never touches `os.environ` or `argparse` again. `dataclasses.replace`
returns a new frozen object with some fields changed, which is how each layer is applied.

The store room key is the **secret**. It is never in the file, because the file is in the
repository and the repository is copied, forked, backed up, and read by people who left the
company. It is never a flag, because flags show up in the process list and in shell history. It
comes from the environment, handed to the process at start by whoever runs it, or from a secrets
manager that the environment points at. And the program refuses to start without it, rather than
starting with an empty password and failing an hour later.

## 4. The picture

```text
   defaults            config.json           APP_* environment        --flags
   (in the code)       (in the repo)         (on the machine)         (this run)
   port = 8000   -->   port = 9000     -->   APP_PORT=9100     -->    --port 9200
   db_host =           db_host =                                       
     "localhost" -->     "db.internal" -->   (not set)          -->   (not given)
   db_password =                                                       
     ""          -->   (never here)    -->   APP_DB_PASSWORD   -->   (never here)
   debug = False -->   (not set)       -->   (not set)          -->   --debug

   result:  port=9200  db_host="db.internal"  db_password=***  debug=True
```

Notice that each column only changes the rows it mentions, and the password row has two cells
that say "never". Read left to right, later wins.

## 5. The code, built step by step

The settings object.

```python
@dataclass(frozen=True)
class Settings:
    port: int = 8000
    db_host: str = "localhost"
    db_password: str = ""
    debug: bool = False

    def masked(self) -> dict[str, object]:
        shown = self.__dict__.copy()
        shown["db_password"] = "***" if self.db_password else "(unset)"
        return shown
```

The defaults live here and nowhere else. `frozen=True` means nothing can assign to a field after
construction, so a settings object cannot be changed by accident halfway through the program.
`masked` exists because you will print the settings at start-up, and the password must not be
in that line.

The card.

```python
def from_file(settings: Settings, path: Path) -> Settings:
    if not path.exists():
        return settings
    data = json.loads(path.read_text(encoding="utf-8"))
    unknown = set(data) - set(settings.__dict__)
    if unknown:
        sys.exit(f"{path}: unknown keys {sorted(unknown)}")
    return replace(settings, **data)
```

A missing file is fine; the defaults stand. A key the dataclass does not have is a typo, and the
program stops and names it rather than ignoring it. `replace` builds a new `Settings` with the
file's values over the current ones.

The note.

```python
def from_env(settings: Settings) -> Settings:
    updates: dict[str, object] = {}
    if value := os.environ.get("APP_PORT"):
        updates["port"] = int(value)
    if value := os.environ.get("APP_DB_HOST"):
        updates["db_host"] = value
    if value := os.environ.get("APP_DB_PASSWORD"):
        updates["db_password"] = value
    if value := os.environ.get("APP_DEBUG"):
        updates["debug"] = value.lower() in ("1", "true", "yes")
    return replace(settings, **updates)
```

Every variable has the `APP_` prefix so they do not collide with anything else on the machine.
Environment values are always strings, so `int(value)` and the `lower() in (...)` are the
conversions. `os.environ.get` returns `None` when unset, and the walrus `:=` from
[day 23](../day-023-palindromes/README.md) assigns and tests in one line.

The room.

```python
def parse_flags(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="the users service")
    parser.add_argument("--config", type=Path, default=Path("config.json"), help="settings file")
    parser.add_argument("--port", type=int, help="port to listen on")
    parser.add_argument("--debug", action="store_true", default=None, help="verbose logging")
    return parser.parse_args(argv)
```

`type=int` converts and rejects; `action="store_true"` makes `--debug` a switch. The
`default=None` on both `--port` and `--debug` is the important detail: a flag that was not given
must be `None`, not `8000` or `False`, or it would override the file and the environment with the
default. `--help` is generated from these lines.

The order.

```python
def load(argv: list[str]) -> Settings:
    flags = parse_flags(argv)
    settings = Settings()
    settings = from_file(settings, flags.config)
    settings = from_env(settings)
    given = {name: value for name, value in vars(flags).items() if value is not None and name != "config"}
    settings = replace(settings, **given)
    if not settings.db_password:
        sys.exit("APP_DB_PASSWORD is not set; refusing to start")
    return settings
```

Defaults, file, environment, flags: four lines, in the order of the picture. `vars(flags)` is the
namespace as a dict; the comprehension keeps only flags that were actually given. The last check
is the store room key: no password, no start.

Save as `main.py` with a `config.json` beside it:

```json
{"port": 9000, "db_host": "db.internal"}
```

Then run it four ways:

```bash
python main.py
APP_DB_PASSWORD=hunter2 python main.py
APP_DB_PASSWORD=hunter2 APP_PORT=9100 python main.py
APP_DB_PASSWORD=hunter2 APP_PORT=9100 python main.py --port 9200 --debug
```

```text
APP_DB_PASSWORD is not set; refusing to start
{'port': 9000, 'db_host': 'db.internal', 'db_password': '***', 'debug': False}
{'port': 9100, 'db_host': 'db.internal', 'db_password': '***', 'debug': False}
{'port': 9200, 'db_host': 'db.internal', 'db_password': '***', 'debug': True}
```

Line one is the refusal. Line two is the file winning over the defaults. Line three is the
environment winning over the file. Line four is the flags winning over everything, and `db_host`
still coming from the file because nothing later mentioned it. On Windows, set the variables
with `set APP_DB_PASSWORD=hunter2` on the line before, or use `$env:APP_DB_PASSWORD="hunter2"` in
PowerShell.

**The same flags with typer.** `typer` is a third-party library that builds the parser from a
function's type hints, the way FastAPI builds routes from them:

```python
import typer

def main(port: int | None = None, debug: bool = False, config: Path = Path("config.json")) -> None:
    ...

if __name__ == "__main__":
    typer.run(main)
```

`--port`, `--debug` and `--config` exist because the parameters do, with `--help` and type
errors generated. It is the nicer tool for a command-line program with many commands; `argparse`
is the one that is always there, and the precedence logic is identical with either.

Here is the whole program in one piece, `main.py`:

```python
import argparse
import json
import os
import sys
from dataclasses import dataclass, replace
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    port: int = 8000
    db_host: str = "localhost"
    db_password: str = ""
    debug: bool = False

    def masked(self) -> dict[str, object]:
        shown = self.__dict__.copy()
        shown["db_password"] = "***" if self.db_password else "(unset)"
        return shown


def from_file(settings: Settings, path: Path) -> Settings:
    if not path.exists():
        return settings
    data = json.loads(path.read_text(encoding="utf-8"))
    unknown = set(data) - set(settings.__dict__)
    if unknown:
        sys.exit(f"{path}: unknown keys {sorted(unknown)}")
    return replace(settings, **data)


def from_env(settings: Settings) -> Settings:
    updates: dict[str, object] = {}
    if value := os.environ.get("APP_PORT"):
        updates["port"] = int(value)
    if value := os.environ.get("APP_DB_HOST"):
        updates["db_host"] = value
    if value := os.environ.get("APP_DB_PASSWORD"):
        updates["db_password"] = value
    if value := os.environ.get("APP_DEBUG"):
        updates["debug"] = value.lower() in ("1", "true", "yes")
    return replace(settings, **updates)


def parse_flags(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="the users service")
    parser.add_argument("--config", type=Path, default=Path("config.json"), help="settings file")
    parser.add_argument("--port", type=int, help="port to listen on")
    parser.add_argument("--debug", action="store_true", default=None, help="verbose logging")
    return parser.parse_args(argv)


def load(argv: list[str]) -> Settings:
    flags = parse_flags(argv)
    settings = Settings()
    settings = from_file(settings, flags.config)
    settings = from_env(settings)
    given = {name: value for name, value in vars(flags).items() if value is not None and name != "config"}
    settings = replace(settings, **given)
    if not settings.db_password:
        sys.exit("APP_DB_PASSWORD is not set; refusing to start")
    return settings


if __name__ == "__main__":
    print(load(sys.argv[1:]).masked())
```

## 6. How the other two languages do it

**Go**

```go
port := flag.Int("port", 0, "port to listen on")
flag.Parse()
cfg := defaults()
cfg = fromFile(cfg, "config.json")
if v, ok := os.LookupEnv("APP_PORT"); ok { cfg.Port, _ = strconv.Atoi(v) }
if *port != 0 { cfg.Port = *port }
```

The same four layers; `flag` is the standard library, `os.LookupEnv` returns a second value that
says whether the variable was set at all, and a flag that was not given is its zero value, so the
check is `!= 0` rather than `is not None`.

**C++**

```cpp
CLI::App app{"the users service"};
int port = 0;
app.add_option("--port", port, "port to listen on");
CLI11_PARSE(app, argc, argv);
if (const char* v = std::getenv("APP_PORT")) cfg.port = std::stoi(v);
if (app.count("--port")) cfg.port = port;
```

CLI11 binds a flag to a variable, and `app.count("--port")` is how you ask whether it was given.
`std::getenv` returns a `const char*`, `nullptr` when unset.

**The difference that matters:** Python can say "this flag was not given" with `None`, and a
dataclass with `replace` makes each layer a pure function from settings to settings. In Go and
C++ an integer that was not given is `0`, so "not given" needs either a sentinel you promise never
to use as a real port, or an explicit "was it set" question like `app.count`. Get that wrong and
the flag layer silently resets the port to zero on every run without `--port`.

## 7. The traps

**The near-miss: a default on the flag.**

```python
parser.add_argument("--port", type=int, default=8000, help="port to listen on")
```

Now `flags.port` is `8000` when the flag was not typed, `given` includes it, and it overrides the
file's `9000` and the environment's `9100` on every run. Nothing errors. The precedence order is
broken and the output looks plausible. A flag's default is `None`; the real default lives on the
dataclass.

**The password in the file.** `{"port": 9000, "db_password": "hunter2"}` works perfectly, which
is the problem. The file is committed, pushed, cloned by every developer, kept in every backup,
and visible in the history forever even after you delete the line. The practice sheet has you
write the check that refuses it.

**A bad flag value.** `python main.py --port abc`:

```text
usage: main.py [-h] [--config CONFIG] [--port PORT] [--debug]
main.py: error: argument --port: invalid int value: 'abc'
```

argparse prints usage and exits with status 2. That is the right behaviour.

**A bad environment value.** `APP_PORT=abc python main.py`:

```text
ValueError: invalid literal for int() with base 10: 'abc'
```

A traceback, because `from_env` did a bare `int(value)`. The flag layer validated for you; the
environment layer is yours to validate. The practice sheet makes this a one-line refusal like the
password one.

**A typo in the file.** `{"port": 1, "prot": 2}`:

```text
bad.json: unknown keys ['prot']
```

Without the unknown-key check, `replace(settings, prot=2)` would raise a `TypeError` naming an
unexpected keyword, which is the same information in a worse voice; and a loader that used
`dict.get` for each key would say nothing and run with the wrong port.

**Printing the settings.** `print(settings)` at start-up prints the password into the log,
where it lives in the log aggregator for ninety days. `masked()` exists so there is a safe way
to print that is easier to type than the unsafe one.

**`os.environ["APP_PORT"]` with square brackets.** Raises `KeyError: 'APP_PORT'` when unset.
`.get` for optional variables; square brackets only for one you intend to require, and then
catch it and say so.

## 8. Say it out loud

**How it gets asked**

- Where should a database password come from, and where should it never be?
- What is your configuration precedence order, and why that order?
- How does the same build run on your laptop and in production?
- What happens if a required setting is missing?

**The ninety-second script**

A password comes from the environment, set by whatever launches the process, or from a secrets
manager that the environment tells the process how to reach. It is never in a config file,
because the file is in the repository and the repository is cloned, forked, backed up, and its
history is permanent. It is never a command-line flag, because flags are visible in the process
list and in shell history. And it is never in a log line, so the settings object has a masked
print. The precedence is defaults in the code, then the config file, then environment variables,
then flags, later winning, because that runs from "true everywhere" to "true for this one run".
The same build runs everywhere because only the environment differs; the code and the file are
identical on my laptop and in production. If a required setting is missing, the program refuses
to start with a message naming the variable, at start-up, rather than starting and failing on
the first database call an hour later.

**The follow-ups**

- **Why environment variables and not a secrets file with tight permissions?** *A file on disk
  with mode 600 is acceptable and some systems mount secrets exactly that way. The rule is not
  "environment" as such; it is "not in the repository, not in the process list, not in the logs,
  handed to the process at start". The environment is the simplest thing that meets all four.*
- **What is wrong with `.env` files?** *Nothing, on a laptop, as long as they are in
  `.gitignore`. The failure is committing one. I treat a `.env` as a local convenience that
  populates the environment, never as the source of truth.*
- **How do you rotate a password?** *The process reads it once at start-up, so rotation is: put
  the new one in the secrets manager, restart the processes. That is a reason to keep start-up
  fast and to have the refusal check, so a botched rotation fails loudly at deploy time.*

**A model answer**

"From the environment, or a secrets manager the environment points at; never in a config file
in the repository, never as a flag, never in a log. Precedence is defaults, file, environment,
flags, later wins, merged into one frozen settings object at start-up, and the program refuses
to start if the password is empty. In Python that is `argparse` with `default=None` on every
flag so an absent flag does not override, `os.environ.get` with the `APP_` prefix, `json` for the
file with a check for unknown keys, and `dataclasses.replace` to apply each layer."

## 9. Recall card

- Precedence: defaults in the dataclass, then file, then `APP_*` environment, then flags; later wins. One frozen `Settings`, applied with `replace`.
- Secrets: environment or a secrets manager. Never in the repo's file, never a flag, never printed; `masked()` for the start-up log.
- argparse flags get `default=None` so an absent flag does not override the layers below.
- Refuse to start without a required secret: `sys.exit("APP_DB_PASSWORD is not set")`, at start-up.
- Environment values are strings; convert and validate them yourself. Unknown file keys are an error, not a shrug.
