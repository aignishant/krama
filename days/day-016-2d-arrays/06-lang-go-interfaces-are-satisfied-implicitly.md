---
day: 16
track: lang-go
title: "Interfaces are satisfied implicitly; the empty interface; io.Reader"
theme: "Interfaces"
phase: "Languages: advanced features"
status: written
---

# Day 016 · Go — Interfaces are satisfied implicitly; the empty interface; io.Reader

**Today's theme:** Interfaces

**After today you can:** You can define a behaviour without naming a type in each language, and say when the check happens.

**The interviewer asks it as:** *What is an interface, and when does the compiler check it?*

---

## 1. What this is, and why it matters

A Go **interface** describes a set of methods. A concrete type satisfies it implicitly when its method set includes the required signatures. There is no `implements` declaration. A caller can accept the small behaviour it needs without naming every possible concrete type.

Today you use interfaces to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Priya runs a neighbourhood book exchange. At the entrance, every volunteer has one job: welcome a visitor and tell them where to leave a book. Priya does not care whether the volunteer is a teacher, a student, or a retired neighbour. She cares that the visitor receives a clear greeting and the right directions.

On the first morning, Priya asks each person to demonstrate. Arun says hello and points to the table. Leela does the same in another language for visitors who prefer it. Their words differ, but each fulfils the promise. Priya can send the next visitor to either of them without changing the rest of the event.

A new volunteer arrives and offers to carry chairs. That is useful, but it does not prove that he can greet visitors. Priya gives him the directions and asks him to practise before taking a place at the entrance. Being willing to help is not the same as being ready for this particular job.

Later, one visitor needs directions spoken slowly. Priya swaps the greeter without moving the book tables or stopping the exchange. The other volunteers do not need to know the new greeter's whole background. They need to know that the same small promise will still be kept.

By closing time, Priya has learned to describe jobs by what someone must do, rather than by who they are. A narrow promise makes it easier to welcome new helpers and easier to notice when an essential part of the job is missing.

## 3. The idea in plain English

A Go **interface** describes a set of methods. A concrete type satisfies it implicitly when its method set includes the required signatures. There is no `implements` declaration. A caller can accept the small behaviour it needs without naming every possible concrete type.

Priya's greeting role becomes `interface { Greet() string }`. Two unrelated structs can satisfy it. The compiler checks compatibility where a value is assigned or passed as that interface. **Dynamic dispatch** means the concrete value stored in the interface determines which method implementation runs.

Method sets matter: if Greet has a pointer receiver, `*Friend` has that method while `Friend` does not satisfy this interface on that basis. Automatic address-taking for a method call does not change this assignment rule. An interface containing a typed nil pointer is also not itself a nil interface; both the concrete type and stored value matter.

## 4. The picture

```text
                    welcome(greeter)
                            |
                            v
                     greet() -> text
                       /         \
                      v           v
                    Friend     Neighbour
                    hello       namaste
```

The caller needs one operation. Python Protocol and Go interfaces allow structural matching; the C++ example uses an explicitly inherited abstract base.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```go
type Greeter interface { Greet() string }
func welcome(greeter Greeter) { fmt.Println(greeter.Greet()) }
```

The consumer requires one method, including its result type. Friend and Neighbour satisfy the requirement without mentioning the interface. The call dispatches to the concrete value passed to welcome.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import "fmt"

type Greeter interface { Greet() string }
type Friend struct{}
type Neighbour struct{}

func (Friend) Greet() string { return "hello" }
func (Neighbour) Greet() string { return "namaste" }
func welcome(greeter Greeter) { fmt.Println(greeter.Greet()) }

func main() {
    welcome(Friend{})
    welcome(Neighbour{})
}
```

**Check the result:** Run `go run main.go`. The output is `hello` then `namaste`. The compiler verifies that each argument supplies Greet() string.

## 6. How the other two languages do it

- **Python** — Duck typing asks whether an object supports an operation.
- **Go** — An interface lists required methods.
- **C++** — A pure virtual operation defines required behaviour.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** switch Friend.Greet to a pointer receiver and keep `welcome(Friend{})`. A compiler diagnostic includes `method Greet has pointer receiver`. Pass `&Friend{}` if pointer semantics are intended.

**Second trap:** write `var friend *Friend; var greeter Greeter = friend` with a pointer-receiver method. `greeter == nil` is false because it contains a concrete type. Whether calling the method panics depends on what that method does with its nil receiver; do not use interface-nil comparison as a universal object-validity check.

## 8. Say it out loud

**How it gets asked:** “What is an interface, and when does the compiler check it?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A Go interface is a small method contract satisfied implicitly. I usually define it around what the consumer needs. The compiler checks that the supplied concrete type has the required method set, then calls dispatch to its implementation. I pay attention to pointer receivers and typed nil values because call syntax alone can hide those distinctions.

**Follow-ups**

1. **Where should the interface live?** Often near the consumer that knows the minimal required behaviour.

2. **Does a matching name suffice?** The method signature must match too.

3. **Does a pointer-receiver method belong to the value's interface method set?** No. Use the pointer type where that method is required.

**Model answer:** The consumer requires one method, including its result type. Friend and Neighbour satisfy the requirement without mentioning the interface. The call dispatches to the concrete value passed to welcome. A typed nil inside an interface is not a nil interface.

## 9. Recall card

- An interface lists required methods.
- Concrete types satisfy it implicitly.
- Assignment checks the method set at compile time.
- Pointer and value method sets differ.
- A typed nil inside an interface is not a nil interface.
