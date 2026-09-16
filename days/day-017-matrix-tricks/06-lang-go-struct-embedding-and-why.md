---
day: 17
track: lang-go
title: "Struct embedding, and why Go has no inheritance"
theme: "Composition versus inheritance"
phase: "Languages: advanced features"
status: written
---

# Day 017 · Go — Struct embedding, and why Go has no inheritance

**Today's theme:** Composition versus inheritance

**After today you can:** You can extend a type in each language and say why composition is the usual answer.

**The interviewer asks it as:** *Why is composition preferred over inheritance?*

---

## 1. What this is, and why it matters

Go has no class inheritance. **Embedding** puts a named type inside a struct without a separate field name, allowing eligible fields and methods to be **promoted** for convenient selection. The outer struct still contains an inner value; it does not become that type.

Today you use composition versus inheritance to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Nikhil buys a bicycle for his commute. After a wet journey, he adds a removable rain cover to his bag. The bag has not become a different kind of bicycle, and the bicycle has not become a kind of rain cover. Each item has one job, and they work together when he needs them.

His friend buys a delivery bicycle with a large rear box fixed to it. That is still a bicycle: it can be steered, pedalled, and parked in the same way. The added box changes how much it carries, but it must not invalidate the ordinary expectations of someone borrowing a bicycle.

They test both arrangements on Saturday. Nikhil can lend the bag to his sister while keeping the bicycle. His friend cannot remove the rear box without tools. That is acceptable if the box always belongs there, but inconvenient if every trip needs a different arrangement.

Later, a shop offers Nikhil a complicated vehicle that looks like a bicycle but cannot be pedalled. Calling it a special bicycle does not make it suitable for the same job. His route includes a narrow path where he must pedal slowly, so he declines it.

He now asks two different questions when buying equipment. Is this genuinely a kind of thing I already know how to use? Or is it a separate thing that should work alongside it? Keeping those questions separate helps him choose equipment he can change without replacing everything at once.

## 3. The idea in plain English

Go has no class inheritance. **Embedding** puts a named type inside a struct without a separate field name, allowing eligible fields and methods to be **promoted** for convenient selection. The outer struct still contains an inner value; it does not become that type.

Nikhil's equipment combination resembles composition. `Desk` embeds `Greeter`, so `desk.Greet()` can select the embedded method. A function requiring a Greeter value still cannot accept Desk merely because of embedding. An interface can accept Desk if its resulting method set satisfies the required behaviour.

Promotion is not virtual overriding. If a method on the embedded Greeter calls another Greeter method, it does not dynamically switch to a same-named method on Desk. Prefer an explicitly named field and forwarding method when that makes the ownership and delegation clearer.

## 4. The picture

```text
INHERITANCE                       COMPOSITION
base contract                     outer object
      ^                                | contains
      | must preserve promises         v
derived implementation            collaborator
                                       |
                                       v
                                  delegated work

Go embedding: containment plus promoted selectors, not inheritance.
```

Ask whether the new object can fulfil the base contract, or whether it merely needs another component to do part of its job.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```go
type Desk struct {
    Greeter
    Place string
}
```

Greeter is still an actual field within Desk. Promotion allows desk.Greet() as a shorthand, but a function expecting a Greeter value receives desk.Greeter explicitly. That shows why embedding is containment rather than subclassing.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import "fmt"

type Greeter struct{}
func (Greeter) Greet() string { return "hello" }

type Desk struct {
    Greeter
    Place string
}

func needsGreeter(greeter Greeter) { fmt.Println(greeter.Greet()) }

func main() {
    desk := Desk{Greeter: Greeter{}, Place: "entrance"}
    fmt.Println(desk.Greet(), desk.Place)
    needsGreeter(desk.Greeter)
}
```

**Check the result:** Run `go run main.go`. It prints `hello entrance` and `hello`.

## 6. How the other two languages do it

- **Python** — Inheritance should preserve the base contract.
- **Go** — Go composition stores another value in a struct.
- **C++** — Public inheritance commits to the base's contract.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** replace `needsGreeter(desk.Greeter)` with `needsGreeter(desk)`. A compiler diagnostic contains `cannot use desk` and `as Greeter value`. Embedding does not create a subtype relationship.

**Second trap:** embed two types that both promote the same method name at the same depth. Selecting that name can be ambiguous. Use an explicit field path or define the outer method deliberately. Promotion saves typing but does not decide your application's meaning.

## 8. Say it out loud

**How it gets asked:** “Why is composition preferred over inheritance?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** Go uses composition and interfaces rather than class inheritance. Embedding promotes eligible selectors, but an outer struct is still a distinct type containing the embedded value. I use interfaces for interchangeable behaviour and explicit delegation when promotion would make the call path confusing. Embedded methods do not gain subclass-style virtual calls to outer methods.

**Follow-ups**

1. **Can Desk satisfy a greeting interface?** Yes, if its method set includes the required promoted method.

2. **Is Desk assignable to Greeter?** No. Select its Greeter field explicitly.

3. **When use a named field instead?** When explicit delegation better communicates which component does the work.

**Model answer:** Greeter is still an actual field within Desk. Promotion allows desk.Greet() as a shorthand, but a function expecting a Greeter value receives desk.Greeter explicitly. That shows why embedding is containment rather than subclassing. Use explicit delegation when it makes call paths clearer.

## 9. Recall card

- Go composition stores another value in a struct.
- Embedding can promote methods and fields.
- Promotion does not make the outer type a subtype.
- Interfaces express interchangeable behaviour.
- Use explicit delegation when it makes call paths clearer.
