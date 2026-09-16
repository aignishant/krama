---
day: 51
track: lang-go
title: "flag, cobra, os.Getenv, and a Config struct"
theme: "Configuration: flags, environment, files"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 051 · Go — flag, cobra, os.Getenv, and a Config struct

**Today's theme:** Configuration: flags, environment, files

**After today you can:** You can configure a program from flags, env vars and a file, with a clear precedence order, in each language.

**The interviewer asks it as:** *Where should a database password come from, and where should it never be?*

---

## 1. What this is, and why it matters

Configuration is everything a program needs that is not in its code: the port, the database
host, a debug switch, and the password. It comes from a file with the defaults, from environment
variables set by whoever runs the program, and from flags on the command line, merged in a fixed
order into one `Config` struct that the rest of the program reads. In Go the pieces are the
standard `flag` package, `os.LookupEnv`, `encoding/json` for the file, and a plain struct; `cobra`
is the third-party library you reach for when the program grows subcommands.

At work, Go services almost always start with a `config.go` that looks like today's lesson, and
the difference between a good one and a bad one is whether it can tell "the flag was not given"
from "the flag was given as zero". In interviews the question is the one in the header, and the
Go follow-up is that exact distinction, because Go's zero values make it easy to get wrong.

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

There is one thing she has learnt to ask. Some mornings the note says "plates: 0". That is not
the same as no note. No note means "two hundred, as on the card". Zero means the hostel is closed
and she should not cook at all. Her first week she treated a blank board and a zero the same way
and cooked for two hundred on a holiday. Now she looks at whether there is a note before she
reads what it says.

One thing is on none of them. The key to the store room is not on the card, because the card is
on the wall. It is not on the note, because the board is by the door. The warden hands it to
Lakshmi at the start of her shift and she gives it back at the end. It is not written down
anywhere, and that is the point.

## 3. The idea in plain English

The laminated card is the **config file**: `config.json` next to the binary, checked into the
repository, decoded into the struct with `encoding/json` from
[day 40](../day-040-2d-prefix-sums/README.md). Go's standard library has no TOML or YAML reader;
JSON is the one that is always there, and the shape of the code is the same with any of them.

The note is the **environment**: `APP_PORT=9100` set in the shell, the container, or the
deployment system. `os.Getenv("APP_PORT")` returns the value, or `""` when unset.
`os.LookupEnv("APP_PORT")` returns the value and a `bool`, and the `bool` is whether there was a
note at all. That is the difference Lakshmi learnt to check.

What the warden says is a **flag**: `--port 9200`. The `flag` package declares each one with a
name, a default and a help line, `flag.Parse()` reads `os.Args`, and each flag is a pointer to
its value. `--help` is generated from the declarations.

Card, note, room is the **precedence**: defaults in the code, then file, then environment, then
flags, each layer overriding the last. The program applies them in that order to one **Config
struct**, and every other function takes a `Config` and never calls `os.Getenv` itself.

The blank board versus the zero is the **zero value** problem again, from
[day 50](../day-050-binary-search-revision/README.md). A flag that was not typed has its default,
and if the default is `0`, the flag layer cannot tell "not given" from "given as zero". The
answer is `flag.Visit`, which calls a function for each flag that was actually set on the command
line, so the flag layer only overrides what was said in the room.

The store room key is the **secret**. Never in the file, because the repository is cloned and
its history is permanent. Never a flag, because flags are in the process list and shell history.
From the environment, or a secrets manager the environment points at, and the program refuses to
start without it.

## 4. The picture

```text
   defaults            config.json           APP_* environment        --flags
   (in the code)       (in the repo)         (on the machine)         (this run)
   Port: 8000    -->   "port": 9000    -->   APP_PORT=9100     -->    --port 9200
   DBHost:             "db_host":                                      
     "localhost" -->     "db.internal" -->   (not set)          -->   (not given)
   DBPassword:                                                         
     ""          -->   (never here)    -->   APP_DB_PASSWORD   -->   (never here)
   Debug: false  -->   (not set)       -->   (not set)          -->   --debug

   result:  Port=9200  DBHost="db.internal"  DBPassword=***  Debug=true
```

Notice that "(not given)" in the flags column must leave the row alone. If the flag layer wrote
its default into every row, the third column would never survive.

## 5. The code, built step by step

The struct, with the defaults and a safe printer.

```go
type Config struct {
	Port       int    `json:"port"`
	DBHost     string `json:"db_host"`
	DBPassword string `json:"db_password"`
	Debug      bool   `json:"debug"`
}

func defaults() Config {
	return Config{Port: 8000, DBHost: "localhost"}
}

func (c Config) String() string {
	password := "(unset)"
	if c.DBPassword != "" {
		password = "***"
	}
	return fmt.Sprintf("{Port:%d DBHost:%s DBPassword:%s Debug:%t}", c.Port, c.DBHost, password, c.Debug)
}
```

A `String()` method makes `fmt.Println(cfg)` use it, from
[day 25](../day-025-pattern-matching/README.md), so the password cannot be printed by accident:
the easy way to print is the safe way.

The card.

```go
func fromFile(cfg Config, path string) (Config, error) {
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return cfg, nil
	}
	if err != nil {
		return cfg, err
	}
	decoder := json.NewDecoder(bytes.NewReader(data))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&cfg); err != nil {
		return cfg, fmt.Errorf("%s: %w", path, err)
	}
	return cfg, nil
}
```

Decoding into `cfg`, which already holds the defaults, overwrites only the keys the file has;
keys the file omits keep their values. That is the layering, for free. `DisallowUnknownFields`
from day 50 turns a typo into an error. A missing file is not an error.

The note.

```go
func fromEnv(cfg Config) (Config, error) {
	if v, ok := os.LookupEnv("APP_PORT"); ok {
		port, err := strconv.Atoi(v)
		if err != nil {
			return cfg, fmt.Errorf("APP_PORT: %w", err)
		}
		cfg.Port = port
	}
	if v, ok := os.LookupEnv("APP_DB_HOST"); ok {
		cfg.DBHost = v
	}
	if v, ok := os.LookupEnv("APP_DB_PASSWORD"); ok {
		cfg.DBPassword = v
	}
	if v, ok := os.LookupEnv("APP_DEBUG"); ok {
		cfg.Debug = v == "1" || strings.EqualFold(v, "true")
	}
	return cfg, nil
}
```

`LookupEnv`, not `Getenv`, so an empty string that was deliberately set counts as set.
Environment values are strings; `Atoi` converts and its error is wrapped with the variable's
name so the message says which one was wrong.

The room.

```go
func fromFlags(cfg Config, args []string) (Config, string, error) {
	fs := flag.NewFlagSet("users", flag.ContinueOnError)
	configPath := fs.String("config", "config.json", "settings file")
	port := fs.Int("port", 0, "port to listen on")
	debug := fs.Bool("debug", false, "verbose logging")
	if err := fs.Parse(args); err != nil {
		return cfg, "", err
	}
	fs.Visit(func(f *flag.Flag) {
		switch f.Name {
		case "port":
			cfg.Port = *port
		case "debug":
			cfg.Debug = *debug
		}
	})
	return cfg, *configPath, nil
}
```

A `FlagSet` rather than the package-level `flag.Int`, so the function can take `args` and be
tested. Each declaration returns a pointer. `fs.Visit` runs the function only for flags that
were on the command line, so `--port 0` sets zero and no `--port` leaves the port alone. That is
the whole trick, and it is why the defaults passed to `fs.Int` do not matter.

The order.

```go
func load(args []string) (Config, error) {
	cfg := defaults()
	_, configPath, err := fromFlags(cfg, args)
	if err != nil {
		return cfg, err
	}
	if cfg, err = fromFile(cfg, configPath); err != nil {
		return cfg, err
	}
	if cfg, err = fromEnv(cfg); err != nil {
		return cfg, err
	}
	if cfg, _, err = fromFlags(cfg, args); err != nil {
		return cfg, err
	}
	if cfg.DBPassword == "" {
		return cfg, errors.New("APP_DB_PASSWORD is not set; refusing to start")
	}
	return cfg, nil
}
```

Flags are parsed twice: once early, only to learn `--config`, and once at the end to apply
their overrides on top of everything else. Defaults, file, environment, flags, then the store
room check.

Save as `main.go` with `config.json` beside it:

```json
{"port": 9000, "db_host": "db.internal"}
```

```bash
go run main.go
APP_DB_PASSWORD=hunter2 go run main.go
APP_DB_PASSWORD=hunter2 APP_PORT=9100 go run main.go
APP_DB_PASSWORD=hunter2 APP_PORT=9100 go run main.go --port 9200 --debug
```

```text
APP_DB_PASSWORD is not set; refusing to start
exit status 1
{Port:9000 DBHost:db.internal DBPassword:*** Debug:false}
{Port:9100 DBHost:db.internal DBPassword:*** Debug:false}
{Port:9200 DBHost:db.internal DBPassword:*** Debug:true}
```

The refusal, then the file over the defaults, the environment over the file, and the flags over
everything, with `DBHost` still from the file because nothing later touched it.

**The same flags with cobra.** When a program grows subcommands, `users serve --port 9200` and
`users migrate`, the standard `flag` package runs out; `cobra` is the library nearly every Go
command-line tool uses:

```go
var port int
serveCmd := &cobra.Command{Use: "serve", Short: "run the server", RunE: func(cmd *cobra.Command, args []string) error {
	cfg, err := load(cmd.Flags())
	// ...
}}
serveCmd.Flags().IntVar(&port, "port", 0, "port to listen on")
rootCmd.AddCommand(serveCmd)
```

It gives subcommands, help pages and shell completion. The flags are the same `pflag` shape
underneath, `cmd.Flags().Changed("port")` is the equivalent of `Visit`, and the precedence
logic does not change.

Here is the whole program in one piece, `main.go`:

```go
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Config struct {
	Port       int    `json:"port"`
	DBHost     string `json:"db_host"`
	DBPassword string `json:"db_password"`
	Debug      bool   `json:"debug"`
}

func defaults() Config {
	return Config{Port: 8000, DBHost: "localhost"}
}

func (c Config) String() string {
	password := "(unset)"
	if c.DBPassword != "" {
		password = "***"
	}
	return fmt.Sprintf("{Port:%d DBHost:%s DBPassword:%s Debug:%t}", c.Port, c.DBHost, password, c.Debug)
}

func fromFile(cfg Config, path string) (Config, error) {
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return cfg, nil
	}
	if err != nil {
		return cfg, err
	}
	decoder := json.NewDecoder(bytes.NewReader(data))
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&cfg); err != nil {
		return cfg, fmt.Errorf("%s: %w", path, err)
	}
	return cfg, nil
}

func fromEnv(cfg Config) (Config, error) {
	if v, ok := os.LookupEnv("APP_PORT"); ok {
		port, err := strconv.Atoi(v)
		if err != nil {
			return cfg, fmt.Errorf("APP_PORT: %w", err)
		}
		cfg.Port = port
	}
	if v, ok := os.LookupEnv("APP_DB_HOST"); ok {
		cfg.DBHost = v
	}
	if v, ok := os.LookupEnv("APP_DB_PASSWORD"); ok {
		cfg.DBPassword = v
	}
	if v, ok := os.LookupEnv("APP_DEBUG"); ok {
		cfg.Debug = v == "1" || strings.EqualFold(v, "true")
	}
	return cfg, nil
}

func fromFlags(cfg Config, args []string) (Config, string, error) {
	fs := flag.NewFlagSet("users", flag.ContinueOnError)
	configPath := fs.String("config", "config.json", "settings file")
	port := fs.Int("port", 0, "port to listen on")
	debug := fs.Bool("debug", false, "verbose logging")
	if err := fs.Parse(args); err != nil {
		return cfg, "", err
	}
	fs.Visit(func(f *flag.Flag) {
		switch f.Name {
		case "port":
			cfg.Port = *port
		case "debug":
			cfg.Debug = *debug
		}
	})
	return cfg, *configPath, nil
}

func load(args []string) (Config, error) {
	cfg := defaults()
	_, configPath, err := fromFlags(cfg, args)
	if err != nil {
		return cfg, err
	}
	if cfg, err = fromFile(cfg, configPath); err != nil {
		return cfg, err
	}
	if cfg, err = fromEnv(cfg); err != nil {
		return cfg, err
	}
	if cfg, _, err = fromFlags(cfg, args); err != nil {
		return cfg, err
	}
	if cfg.DBPassword == "" {
		return cfg, errors.New("APP_DB_PASSWORD is not set; refusing to start")
	}
	return cfg, nil
}

func main() {
	cfg, err := load(os.Args[1:])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(cfg)
}
```

## 6. How the other two languages do it

**Python**

```python
parser.add_argument("--port", type=int, help="port to listen on")   # default None
given = {k: v for k, v in vars(flags).items() if v is not None}
settings = replace(settings, **given)
```

An absent flag is `None`, so "was it given" is a comparison. `dataclasses.replace` returns a new
frozen object per layer.

**C++**

```cpp
int port = 0;
app.add_option("--port", port, "port to listen on");
CLI11_PARSE(app, argc, argv);
if (app.count("--port")) cfg.port = port;
```

CLI11 binds the flag to a variable and `app.count` answers "was it given", the same question
`flag.Visit` answers in Go.

**The difference that matters:** Go's `flag` writes its default into the variable whether or
not the flag was typed, and a default of `0` looks exactly like `--port 0`. Python gets `None` for
free; C++ gets `count`. In Go you must use `flag.Visit`, or `cobra`'s `Changed`, or you will
write a config loader that looks correct, prints a sensible port, and quietly ignores the
environment on every run.

## 7. The traps

**The near-miss: applying every flag.**

```go
fs.Parse(args)
cfg.Port = *port
cfg.Debug = *debug
```

Run `APP_PORT=9100 go run main.go` and the port is `0`, because `*port` is the default `0` and
it overwrote the environment's value. No error, no warning; the program tries to listen on port
zero, which the operating system treats as "pick any free port", so it even starts. `fs.Visit`
is the fix.

**`Getenv` instead of `LookupEnv`.** `os.Getenv("APP_DEBUG")` returns `""` for both "unset" and
"set to empty". For a password that is usually fine. For a value where empty means something,
such as "no prefix", it is a bug you find in production.

**A bad flag.** `go run main.go --port abc`:

```text
invalid value "abc" for flag -port: parse error
Usage of users:
  -config string
        settings file (default "config.json")
  -debug
        verbose logging
  -port int
        port to listen on
```

`flag.ContinueOnError` returns that as an error and `main` prints it and exits 1. With the default
`ExitOnError` the package exits 2 for you.

**A bad environment value.** `APP_DB_PASSWORD=x APP_PORT=abc go run main.go`:

```text
APP_PORT: strconv.Atoi: parsing "abc": invalid syntax
```

The `%w` wrap put the variable's name in front, which is the difference between a one-minute fix
and a ten-minute one.

**A typo in the file.** `{"port": 1, "prot": 2}`:

```text
config.json: json: unknown field "prot"
```

Without `DisallowUnknownFields`, `prot` is ignored and the program runs on port 1.

**The password in the file.** `{"db_password": "hunter2"}` decodes without complaint into
`DBPassword`, because the struct has the field so the file can be printed with `%+v`. The
practice sheet has you make that a start-up refusal, and the `String()` method is why `%v` is
safe even before you do.

**Single-dash and double-dash.** Go's `flag` accepts `-port` and `--port` as the same thing. It
does not accept `--port=abc` differently from `--port abc`; both parse. It does not accept
combined short flags like `-vd`. If you need those, that is `cobra` and `pflag`.

## 8. Say it out loud

**How it gets asked**

- Where should a database password come from, and where should it never be?
- What is your precedence order, and how do you know a flag was not given?
- How does the same binary run on your laptop and in production?
- What happens at start-up if a required setting is missing?

**The ninety-second script**

The password comes from the environment, or from a secrets manager that the environment tells
the process how to reach. Never in the config file, because the file is in the repository and the
repository's history is permanent. Never a flag, because flags are in the process list and shell
history. Never printed, so the `Config` type has a `String()` method that masks it. Precedence is
defaults in code, then the file, then `APP_` environment variables, then flags, later winning,
because that goes from "true everywhere" to "true for this run". The same binary runs everywhere
because only the environment differs. In Go the one thing to get right is that a flag's zero
value is not the same as an absent flag, so I apply flags with `flag.Visit`, which only sees flags
that were typed, and I read the environment with `os.LookupEnv` so I can tell unset from empty.
A missing password is an error from `load`, printed at start-up, exit 1, before the server binds
a port.

**The follow-ups**

- **Why parse the flags twice?** *The config file path is itself a flag, and the file must be
  read before the environment and the flags are applied on top. First parse learns the path;
  second parse applies overrides last. A single parse with the overrides stored in a struct and
  applied at the end works too.*
- **Where does `cobra` fit?** *Subcommands and generated help. Same precedence, same
  `Changed` check instead of `Visit`. I would not add it for a program with one command.*
- **Why refuse to start rather than default the password to empty?** *An empty password fails
  on the first database call, which may be minutes after start-up, in a handler, under load. A
  refusal at start-up fails the deploy instead of the users.*

**A model answer**

"Environment or secrets manager; never the repo's config file, never a flag, never a log line.
Precedence defaults, file, environment, flags, later wins, into one `Config` struct that the rest
of the program reads. In Go: `encoding/json` with `DisallowUnknownFields` for the file,
`os.LookupEnv` so unset and empty differ, and `flag.Visit` so only flags that were typed override,
because the default zero of an untyped flag is indistinguishable from `--port 0` otherwise.
Refuse to start without the password, and a `String()` method that masks it."

## 9. Recall card

- Precedence: `defaults()`, then file, then `APP_*` environment, then flags; later wins; one `Config` struct.
- `flag.Visit` applies only flags that were typed; assigning `*port` unconditionally resets the layers below to zero.
- `os.LookupEnv` returns `(value, ok)`; `Getenv` cannot tell unset from empty.
- Secrets: environment or a secrets manager; never in the repo's file, never a flag; a `String()` method that masks.
- Refuse to start on a missing secret, wrap conversion errors with the variable name, and `DisallowUnknownFields` on the file.
