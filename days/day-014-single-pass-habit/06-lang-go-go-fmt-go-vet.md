---
day: 14
track: lang-go
title: "go fmt, go vet, go mod tidy, and the standard layout"
theme: "Formatters, linters, and a real project layout"
phase: "Languages: every language, every basic"
status: written
---

# Day 014 · Go — go fmt, go vet, go mod tidy, and the standard layout

**Today's theme:** Formatters, linters, and a real project layout

**After today you can:** You can start a new project in each language from an empty folder, with formatting and dependencies working.

**The interviewer asks it as:** *How do you set up a new project so a teammate can build it on day one?*

---

## 1. What this is, and why it matters

Go's standard tools cover building, formatting, dependency declarations, and several static checks. `go.mod` declares the module and requirements. `go.sum` records dependency checksums; it is not simply a copy of another ecosystem's lockfile.

Today you use formatters, linters, and a real project layout to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Farah invites her cousin to help bake a cake. She sends a photo of the finished cake and says it is easy. Her cousin arrives with flour, but the recipe needs a different kind. The measuring cup has no markings. The oven dial has a worn patch where the temperature should be. Farah knows what all these things mean because she uses them every week. Her cousin does not.

The following Saturday, Farah prepares differently. She saves a shopping list on her phone, including the exact sizes of the packets. She puts the bowls together and checks that the scales turn on. She explains which oven setting she uses and where the cake goes after baking. Her cousin can now repeat the work without asking a question at every step.

They also agree on a few small habits. Wash a spoon before using it for another ingredient. Put lids back immediately. Wipe the counter before measuring the next thing. These habits do not guarantee a good cake. They remove preventable confusion so both people can pay attention to the mixture.

At the end, Farah keeps the recipe and shopping list, but throws away the used packaging. Next week she wants the instructions and ingredients, not yesterday's mess. She asks her cousin to try again without help. If the cake only works when Farah stands beside the oven, the instructions are still missing something important.

## 3. The idea in plain English

Go's standard tools cover building, formatting, dependency declarations, and several static checks. `go.mod` declares the module and requirements. `go.sum` records dependency checksums; it is not simply a copy of another ecosystem's lockfile.

Farah's repeatable recipe becomes commands that work at the module root. `go fmt ./...` formats packages. `go vet ./...` checks suspicious constructs, including some format-string mistakes. `go mod tidy` reconciles declared dependencies with imports and tests. `go test ./...` runs package tests; without tests it still checks that packages can be built in the test workflow.

For one executable, start with `go.mod` and `main.go`. There is no mandatory universal directory tree. Add `cmd/tool` for several commands and `internal` for private implementation packages when they solve an actual organisational need. Avoid creating empty layers just to resemble a large repository.

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

```go
func add(left, right int) int {
    return left + right
}
```

The helper stays in the first package because there is no need for another package yet. The documented workflow formats and checks that package before running it. Its lack of external imports beyond fmt keeps dependency setup small.

In an empty directory run `go mod init example.com/krama-tool`, then save the following as `main.go`. The official [dependency-management guide](https://go.dev/doc/modules/managing-dependencies) explains module metadata.

The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import "fmt"

func add(left, right int) int {
    return left + right
}

func main() {
    fmt.Println(add(2, 3))
}
```

**Check the result:** Run `go fmt ./...`, `go vet ./...`, `go mod tidy`, `go test ./...`, and `go run .`. The application prints `5`. With no external dependencies, tidy need not create go.sum.

## 6. How the other two languages do it

- **Python** — Declare project metadata and dependencies in pyproject.toml.
- **Go** — go.mod identifies a module and its requirements.
- **C++** — CMake describes targets and their requirements.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** assume every repository needs `cmd`, `pkg`, and many nested directories. Start with one package and split by responsibility once there is something to split.

**Failure to reproduce:** add `fmt.Printf("%d", "five")`. `go vet` reports a diagnostic including `fmt.Printf format %d has arg "five" of wrong type string`. The program can compile because Printf accepts arbitrary arguments; vet understands the formatting convention. Fix the verb or the argument, not the check.

## 8. Say it out loud

**How it gets asked:** “How do you set up a new project so a teammate can build it on day one?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I initialise a module, keep the first executable in a small package, and document go run and go test commands. I format with the standard formatter, run vet, and reconcile dependencies with tidy. I commit dependency metadata. I use internal directories to express import boundaries and avoid pretending that one directory layout is compulsory for every Go program.

**Follow-ups**

1. **Does go fmt find logical bugs?** No. It changes layout.

2. **Does every module have a go.sum?** Not necessarily; a standard-library-only module may not need one.

3. **What does ./... select?** Packages below the current directory according to Go's package-pattern rules.

**Model answer:** The helper stays in the first package because there is no need for another package yet. The documented workflow formats and checks that package before running it. Its lack of external imports beyond fmt keeps dependency setup small. Start small; there is no mandatory universal project tree.

## 9. Recall card

- go.mod identifies a module and its requirements.
- go fmt standardises source layout.
- go vet checks suspicious constructs.
- go mod tidy reconciles dependency metadata.
- Start small; there is no mandatory universal project tree.
