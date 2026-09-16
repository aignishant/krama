---
day: 51
track: lang-cpp
title: "CLI11, getenv, and a Config struct"
theme: "Configuration: flags, environment, files"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 051 · C++ — CLI11, getenv, and a Config struct

**Today's theme:** Configuration: flags, environment, files

**After today you can:** You can configure a program from flags, env vars and a file, with a clear precedence order, in each language.

**The interviewer asks it as:** *Where should a database password come from, and where should it never be?*

---

## 1. What this is, and why it matters

Configuration is everything a program needs that is not in its code: the port, the database
host, a debug switch, and the password. It comes from a file with the defaults, from environment
variables set by whoever runs the program, and from flags on the command line, merged in a fixed
order into one `Config` struct that the rest of the program reads. C++ has `std::getenv` in the
standard library and nothing for flags beyond `argv`, so the flags come from CLI11, a header-only
library that binds `--port` to an `int` and generates `--help`; the file is nlohmann/json from
[day 40](../day-040-2d-prefix-sums/README.md).

At work, a C++ service's `config.cpp` is where you learn whether the team has ever leaked a
secret, because the habits that prevent it are visible in ten lines. In interviews the question
is the one in the header, and the C++ follow-up is usually about `getenv`: what it returns when
the variable is missing, and what happens if you hand that to `std::string`.

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

One morning a new helper walked to the board, found nothing pinned there, and read the empty
board out loud anyway: "it says nothing, so, nothing plates". Lakshmi stopped him. An empty board
is not a note that says nothing. It is no note. You look first to see whether there is a piece
of paper, and only then do you read it. He has not made that mistake again.

One thing is on none of them. The key to the store room is not on the card, because the card is
on the wall. It is not on the note, because the board is by the door. The warden hands it to
Lakshmi at the start of her shift and she gives it back at the end. It is not written down
anywhere, and that is the point.

## 3. The idea in plain English

The laminated card is the **config file**: `config.json` next to the binary, in the repository,
parsed with nlohmann and read with `value(key, fallback)`, which returns the fallback when the
key is absent so the defaults survive.

The note is the **environment**: `APP_PORT=9100` set by the shell, the container, or the
deployment system. `std::getenv("APP_PORT")` returns a `const char*` to the value, or `nullptr`
when the variable is not set. The empty board is `nullptr`. Reading it as if it were a note,
`std::string(std::getenv("APP_PORT"))`, is the new helper's mistake, and in C++ it is a crash
rather than a scolding.

What the warden says is a **flag**: `--port 9200`. CLI11 is `CLI::App app{"description"}`, one
`app.add_option("--port", port, "help")` per flag that binds it to a variable, and
`CLI11_PARSE(app, argc, argv)`, a macro that parses and, on `--help` or a bad value, prints and
returns from `main` for you. `app.count("--port")` is how many times the flag appeared, which is
the "was it given" question.

Card, note, room is the **precedence**: defaults in the struct, then file, then environment,
then flags. One **Config struct**, filled in that order, passed by `const&` to everything else.

The store room key is the **secret**. Never in the file, because the repository is cloned and
its history is permanent. Never a flag, because `ps` and shell history show it. From the
environment or a secrets manager, and the program refuses to start without it. And never printed:
the struct's `operator<<` from [day 25](../day-025-pattern-matching/README.md) masks it, so
the easy way to print is the safe way.

## 4. The picture

```text
   defaults            config.json           APP_* environment        --flags
   (in the struct)     (in the repo)         (on the machine)         (this run)
   port = 8000   -->   "port": 9000    -->   APP_PORT=9100     -->    --port 9200
   db_host =           "db_host":                                      
     "localhost" -->     "db.internal" -->   (nullptr)          -->   (count == 0)
   db_password =                                                       
     ""          -->   (never here)    -->   APP_DB_PASSWORD   -->   (never here)
   debug = false -->   (not set)       -->   (nullptr)          -->   --debug

   result:  port=9200  db_host="db.internal"  db_password=***  debug=true
```

Notice `(nullptr)` and `(count == 0)`: the two ways C++ says "there is no note", and both must
leave the row alone.

## 5. The code, built step by step

CLI11 is one header, `CLI/CLI.hpp`; install `libcli11-dev` on Debian and Ubuntu, `cli11` on
Homebrew and vcpkg. nlohmann/json as on day 40.

The struct with its defaults and a safe printer.

```cpp
struct Config {
    int port = 8000;
    std::string db_host = "localhost";
    std::string db_password;
    bool debug = false;
};

std::ostream& operator<<(std::ostream& out, const Config& c) {
    return out << "{port=" << c.port << " db_host=" << c.db_host
               << " db_password=" << (c.db_password.empty() ? "(unset)" : "***")
               << " debug=" << std::boolalpha << c.debug << "}";
}
```

Default member initialisers are the defaults layer. The `operator<<` masks the password, so
`std::cout << cfg` is safe and there is no unsafe way that is easier to type.

The card.

```cpp
Config from_file(Config cfg, const std::filesystem::path& path) {
    if (!std::filesystem::exists(path)) return cfg;
    std::ifstream in(path);
    json data = json::parse(in);
    for (const auto& [key, value] : data.items()) {
        if (key != "port" && key != "db_host" && key != "db_password" && key != "debug") {
            throw std::runtime_error(path.string() + ": unknown key '" + key + "'");
        }
    }
    cfg.port = data.value("port", cfg.port);
    cfg.db_host = data.value("db_host", cfg.db_host);
    cfg.db_password = data.value("db_password", cfg.db_password);
    cfg.debug = data.value("debug", cfg.debug);
    return cfg;
}
```

`cfg` is taken by value, changed, and returned, so each layer is a function from config to
config. `data.value("port", cfg.port)` reads the key if present and falls back to the current
value, which is the layering. The loop over `items()` refuses a typo instead of ignoring it.

The note.

```cpp
std::optional<std::string> env(const char* name) {
    const char* value = std::getenv(name);
    if (value == nullptr) return std::nullopt;
    return std::string(value);
}

Config from_env(Config cfg) {
    if (auto v = env("APP_PORT")) cfg.port = std::stoi(*v);
    if (auto v = env("APP_DB_HOST")) cfg.db_host = *v;
    if (auto v = env("APP_DB_PASSWORD")) cfg.db_password = *v;
    if (auto v = env("APP_DEBUG")) cfg.debug = (*v == "1" || *v == "true");
    return cfg;
}
```

`env` wraps `getenv` so the `nullptr` check happens exactly once, in one place, and everything
else sees a `std::optional<std::string>` from [day 23](../day-023-palindromes/README.md). The
`if (auto v = ...)` tests the optional and binds it in one line. `std::stoi` on a bad value
throws, which section 7 turns into a message.

The room, and the order.

```cpp
int main(int argc, char** argv) {
    CLI::App app{"the users service"};
    std::filesystem::path config_path = "config.json";
    int port = 0;
    bool debug = false;
    app.add_option("--config", config_path, "settings file");
    app.add_option("--port", port, "port to listen on");
    app.add_flag("--debug", debug, "verbose logging");
    CLI11_PARSE(app, argc, argv);
```

Three variables, three bindings. `add_option` takes a value; `add_flag` is a switch. After
`CLI11_PARSE`, the variables hold whatever was typed, or their initial values if nothing was.

```cpp
    try {
        Config cfg = from_env(from_file(Config{}, config_path));
        if (app.count("--port")) cfg.port = port;
        if (app.count("--debug")) cfg.debug = debug;
        if (cfg.db_password.empty()) {
            throw std::runtime_error("APP_DB_PASSWORD is not set; refusing to start");
        }
        std::cout << cfg << '\n';
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
    return 0;
}
```

Defaults inside `Config{}`, then file, then environment, then the two `count` checks apply only
flags that were typed. The `try` turns every failure in the loader, a bad file, a bad number, a
missing password, into one line on standard error and exit code 1.

Save as `main.cpp` with `config.json` beside it:

```json
{"port": 9000, "db_host": "db.internal"}
```

```bash
g++ -Wall -Wextra -std=c++20 main.cpp -o users
./users
APP_DB_PASSWORD=hunter2 ./users
APP_DB_PASSWORD=hunter2 APP_PORT=9100 ./users
APP_DB_PASSWORD=hunter2 APP_PORT=9100 ./users --port 9200 --debug
```

```text
APP_DB_PASSWORD is not set; refusing to start
{port=9000 db_host=db.internal db_password=*** debug=false}
{port=9100 db_host=db.internal db_password=*** debug=false}
{port=9200 db_host=db.internal db_password=*** debug=true}
```

The refusal, then the file over the defaults, the environment over the file, the flags over
everything, with `db_host` still from the file.

Here is the whole program in one piece, `main.cpp`:

```cpp
#include <CLI/CLI.hpp>
#include <nlohmann/json.hpp>

#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <stdexcept>
#include <string>

using json = nlohmann::json;

struct Config {
    int port = 8000;
    std::string db_host = "localhost";
    std::string db_password;
    bool debug = false;
};

std::ostream& operator<<(std::ostream& out, const Config& c) {
    return out << "{port=" << c.port << " db_host=" << c.db_host
               << " db_password=" << (c.db_password.empty() ? "(unset)" : "***")
               << " debug=" << std::boolalpha << c.debug << "}";
}

Config from_file(Config cfg, const std::filesystem::path& path) {
    if (!std::filesystem::exists(path)) return cfg;
    std::ifstream in(path);
    json data = json::parse(in);
    for (const auto& [key, value] : data.items()) {
        if (key != "port" && key != "db_host" && key != "db_password" && key != "debug") {
            throw std::runtime_error(path.string() + ": unknown key '" + key + "'");
        }
    }
    cfg.port = data.value("port", cfg.port);
    cfg.db_host = data.value("db_host", cfg.db_host);
    cfg.db_password = data.value("db_password", cfg.db_password);
    cfg.debug = data.value("debug", cfg.debug);
    return cfg;
}

std::optional<std::string> env(const char* name) {
    const char* value = std::getenv(name);
    if (value == nullptr) return std::nullopt;
    return std::string(value);
}

Config from_env(Config cfg) {
    if (auto v = env("APP_PORT")) {
        try {
            cfg.port = std::stoi(*v);
        } catch (const std::exception&) {
            throw std::runtime_error("APP_PORT: '" + *v + "' is not a number");
        }
    }
    if (auto v = env("APP_DB_HOST")) cfg.db_host = *v;
    if (auto v = env("APP_DB_PASSWORD")) cfg.db_password = *v;
    if (auto v = env("APP_DEBUG")) cfg.debug = (*v == "1" || *v == "true");
    return cfg;
}

int main(int argc, char** argv) {
    CLI::App app{"the users service"};
    std::filesystem::path config_path = "config.json";
    int port = 0;
    bool debug = false;
    app.add_option("--config", config_path, "settings file");
    app.add_option("--port", port, "port to listen on");
    app.add_flag("--debug", debug, "verbose logging");
    CLI11_PARSE(app, argc, argv);

    try {
        Config cfg = from_env(from_file(Config{}, config_path));
        if (app.count("--port")) cfg.port = port;
        if (app.count("--debug")) cfg.debug = debug;
        if (cfg.db_password.empty()) {
            throw std::runtime_error("APP_DB_PASSWORD is not set; refusing to start");
        }
        std::cout << cfg << '\n';
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
    return 0;
}
```

## 6. How the other two languages do it

**Python**

```python
parser.add_argument("--port", type=int, help="port to listen on")   # default None
if value := os.environ.get("APP_PORT"):
    updates["port"] = int(value)
given = {k: v for k, v in vars(flags).items() if v is not None}
```

`os.environ.get` returns `None` for a missing variable and never a pointer; a missing flag is
`None` too. The two "is there a note" questions are the same comparison.

**Go**

```go
if v, ok := os.LookupEnv("APP_PORT"); ok { cfg.Port, _ = strconv.Atoi(v) }
fs.Visit(func(f *flag.Flag) { if f.Name == "port" { cfg.Port = *port } })
```

`LookupEnv`'s second value is the "is there a note" for the environment, and `flag.Visit` is it
for flags.

**The difference that matters:** C++ is the only one where reading a missing environment
variable the obvious way is a crash. `std::string(std::getenv("X"))` with `X` unset constructs a
string from a null pointer, which is undefined behaviour and in practice a segmentation fault.
Python gives `None`, Go gives `""` and `false`. Wrapping `getenv` in one function that returns
`std::optional` is how a C++ codebase makes that mistake impossible to write twice.

## 7. The traps

**The near-miss: reading the empty board.**

```cpp
std::string port = std::getenv("APP_PORT");
```

Compiles. With `APP_PORT` set it works. Without it:

```text
Segmentation fault (core dumped)
```

Or worse, on some platforms, a `std::logic_error: basic_string: construction from null is not
valid`. Never pass `getenv`'s result to anything without checking for `nullptr`; the `env`
helper is the whole fix.

**Applying every flag.**

```cpp
CLI11_PARSE(app, argc, argv);
cfg.port = port;      // port is 0 when --port was not typed
```

`APP_PORT=9100 ./users` prints `port=0`. No error. `app.count("--port")` is the guard, and
without it the environment layer never survives.

**A bad flag value.** `./users --port abc`:

```text
Could not convert: --port=abc
Run with --help for more information.
```

CLI11 printed that and `CLI11_PARSE` returned exit code from `main` for you; nothing after the
macro ran.

**A bad environment value.** Without the `try` around `stoi`, `APP_PORT=abc ./users`:

```text
terminate called after throwing an instance of 'std::invalid_argument'
  what():  stoi
```

With it:

```text
APP_PORT: 'abc' is not a number
```

The variable's name is the difference between a one-minute fix and a ten-minute one.

**A typo in the file.** `{"port": 1, "prot": 2}`:

```text
config.json: unknown key 'prot'
```

Without the loop over `items()`, `value("port", ...)` reads 1 and `prot` is silently ignored.

**`data["port"]` instead of `value`.** On a file without `port`, `data["port"]` on the non-const
`data` inserts a null, and assigning a null to an `int` throws `type_error.302`, from
[day 50](../day-050-binary-search-revision/README.md). `value(key, fallback)` reads without
inserting and never throws for a missing key.

**Forgetting the include.** Use `CLI::App` without `#include <CLI/CLI.hpp>`:

```text
main.cpp:62:5: error: 'CLI' has not been declared
```

## 8. Say it out loud

**How it gets asked**

- Where should a database password come from, and where should it never be?
- What does `getenv` return when the variable is not set, and what do you do about it?
- What is your precedence order, and how do you know a flag was not given?
- What happens at start-up if a required setting is missing?

**The ninety-second script**

The password comes from the environment, or a secrets manager the environment points at. Never
in the config file, because the repository is cloned and its history is permanent. Never a flag,
because the process list and shell history show it. Never printed, so `operator<<` on the config
masks it. Precedence is defaults in the struct, then the file, then `APP_` environment variables,
then flags, later winning, from "true everywhere" to "true for this run", into one `Config` that
everything else takes by `const&`. In C++ `getenv` returns a `const char*` that is `nullptr` when
unset, and constructing a `std::string` from that is a crash, so I wrap it once in a function
that returns `std::optional<std::string>` and never call `getenv` anywhere else. Flags come from
CLI11, bound to variables, and I apply a flag only when `app.count` says it was typed, because
the bound variable holds its initial value otherwise. A missing password throws in the loader
and the process exits 1 at start-up with the variable's name on standard error.

**The follow-ups**

- **Why `optional` and not an empty string for a missing variable?** *`APP_DB_HOST=` set to
  empty and `APP_DB_HOST` unset are different situations, and an empty string cannot represent
  both. The optional keeps "no note" separate from "a note that says nothing".*
- **Where do TOML or YAML come in?** *Same shape, different parser. JSON is the one the course
  already has. For a config file people edit by hand I would pick TOML for the comments, with
  a header-only parser, and the loader's structure does not change.*
- **How would you test the loader?** *`from_file`, `from_env` and the flag block are functions
  from `Config` to `Config`. `from_file` takes a path, so a test writes a temp file. The
  environment is global, so the test sets and unsets variables around the call, or the `env`
  helper takes a lookup function that the test replaces.*

**A model answer**

"Environment or secrets manager; never the repo's file, never a flag, never a log line.
Precedence defaults, file, environment, flags, later wins, into one `Config`. In C++: `getenv`
wrapped once into an `optional` because `nullptr` into `std::string` is a crash; nlohmann
`value(key, fallback)` so missing keys keep the defaults and a loop that rejects unknown keys;
CLI11 bound to variables with `app.count` guarding each override; a `try` in `main` that turns
any loader failure into one line and exit 1, before anything binds a port."

## 9. Recall card

- Precedence: struct defaults, then file, then `APP_*` environment, then flags; later wins; one `Config` passed by `const&`.
- `std::getenv` returns `nullptr` when unset; `std::string(nullptr)` is a crash. Wrap it once into `std::optional<std::string>`.
- CLI11: `CLI::App app{...}`, `add_option("--port", port, ...)`, `add_flag`, `CLI11_PARSE`; apply only if `app.count("--port")`.
- nlohmann `value(key, fallback)` reads without inserting; reject unknown keys with a loop over `items()`.
- Secrets: environment or a secrets manager; never in the file, never a flag; `operator<<` masks; refuse to start if empty.
