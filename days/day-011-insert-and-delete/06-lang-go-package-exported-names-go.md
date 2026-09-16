---
day: 11
track: lang-go
title: "package, exported names, go.mod, and internal directories"
theme: "Splitting code across files"
phase: "Languages: every language, every basic"
status: written
---

# Day 011 · Go — package, exported names, go.mod, and internal directories

**Today's theme:** Splitting code across files

**After today you can:** You can split a program into three files in each language and explain what is visible from where.

**The interviewer asks it as:** *What makes a name visible to another file?*

---

## 1. What this is, and why it matters

A **package** is a group of Go source files compiled together, usually in one directory. A **module** is a versioned collection of packages rooted at `go.mod`. A name beginning with an uppercase letter is **exported**: another package may use it.

Today you use splitting code across files to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Meera is arranging dinner for six friends. Until yesterday, everyone asked her everything. Where are the plates? When should the rice go on? Who is buying milk? Her phone kept buzzing while she tried to cook, and she answered the same question three times.

Tonight she divides the work. Arun handles food, Leela handles drinks, and Meera handles the table. Everyone knows who to ask. Arun tells the group when dinner will be ready, but he does not send them every small decision he makes in the kitchen. Leela needs the serving time, not the order in which he washes vegetables.

At seven, a guest asks Leela whether the rice is ready. She asks Arun rather than inventing an answer. Arun remains responsible for that one piece of information. If he changes the meal, he tells the group what has changed at the boundary: dinner is now at eight. The others can adjust without learning his whole recipe.

There is one final rule. Asking Arun about dinner must not cause him to start cooking a second meal. A question and the instruction to begin are different things. Meera sends the instruction once, after everyone arrives.

The arrangement works because each person has a clear job, a clear way to be reached, and a clear distinction between answering a question and starting the evening. Splitting the work helps only when those boundaries remain understandable.

## 3. The idea in plain English

A **package** is a group of Go source files compiled together, usually in one directory. A **module** is a versioned collection of packages rooted at `go.mod`. A name beginning with an uppercase letter is **exported**: another package may use it.

The dinner responsibilities become packages, not individual files. Two files in the same package can use each other's unexported names. A caller in another package imports a path and uses the exported name, such as `calc.Add`. An `internal` directory adds an import restriction: only code within the tree rooted at its parent may import it.

The `main` package supplies the executable's entry function. In this example, `example.com/split` is a local module path; Go does not fetch it from a website because its packages are inside the current module. Keep the module declaration and import path consistent.

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

```go
func Add(left, right int) int { return left + right }
```

Add is exported because it begins with a capital letter. Both calc files declare package calc, so they compile as one package. The entry package imports that package using the module prefix and calls its public names.

Create `main.go` and a `calc` directory containing the other two files. At the root run `go mod init example.com/split` once.

The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
// calc/add.go
package calc

func Add(left, right int) int { return left + right }

// calc/label.go
package calc

import "fmt"

func Label(total int) string { return fmt.Sprintf("total=%d", total) }

// main.go
package main

import (
    "fmt"
    "example.com/split/calc"
)

func main() {
    fmt.Println(calc.Label(calc.Add(2, 3)))
}
```

**Check the result:** Run `go run .` at the module root. It prints `total=5`.

## 6. How the other two languages do it

- **Python** — A module owns a collection of names.
- **Go** — Packages, not files, control Go name visibility.
- **C++** — Headers publish declarations to callers.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** use `go run main.go` when a helper is in another file in the same directory. That command selects the named file; `go run .` selects the package, including its other files.

**Failure to reproduce:** rename `Add` to `add` without changing the caller. A compiler diagnostic includes `undefined: calc.Add`. Changing the call to `calc.add` does not export it. Restore the capital letter or expose a different exported operation. A file boundary inside one package is not a privacy boundary.

## 8. Say it out loud

**How it gets asked:** “What makes a name visible to another file?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A Go file declares its package, but visibility is controlled across packages. Uppercase names are exported. A module gives packages their import-path prefix and dependency versions. I run the package with `go run .`, and use an internal directory when I want the toolchain to restrict which other packages may import an implementation.

**Follow-ups**

1. **Can two files in one package share a lowercase helper?** Yes. The package is the boundary.

2. **Does every package need a go.mod?** No. A module can contain many packages.

3. **What is special about package main?** It builds an executable with a main function rather than an importable library.

**Model answer:** Add is exported because it begins with a capital letter. Both calc files declare package calc, so they compile as one package. The entry package imports that package using the module prefix and calls its public names. Run the package with go run .

## 9. Recall card

- Packages, not files, control Go name visibility.
- Uppercase names are exported to importers.
- go.mod defines the module path and dependencies.
- internal restricts imports to an enclosing tree.
- Run the package with go run .
