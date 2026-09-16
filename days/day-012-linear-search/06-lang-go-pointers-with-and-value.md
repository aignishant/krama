---
day: 12
track: lang-go
title: "Pointers with & and *, value receivers versus pointer receivers"
theme: "Pointers, references, and value semantics"
phase: "Languages: every language, every basic"
status: written
---

# Day 012 · Go — Pointers with & and *, value receivers versus pointer receivers

**Today's theme:** Pointers, references, and value semantics

**After today you can:** You can say, for each language, whether a function receives a copy or the original, and prove it with a print.

**The interviewer asks it as:** *Is this passed by value or by reference?*

---

## 1. What this is, and why it matters

Go passes every argument by value. A **pointer** is a value containing an address. `&value` obtains an address and `*pointer` accesses the value at that address. Copying a pointer copies the address, so both copies can access the same object.

Today you use pointers, references, and value semantics to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Ravi and his sister share a shopping basket at the market. Ravi puts two oranges in it. His sister adds a third. When Ravi looks down, he sees three oranges. They have two people talking about one basket, not two baskets that somehow stay in agreement.

At the next stall, the shopkeeper offers his sister a fresh basket. She takes it and puts a mango inside. Ravi's basket still contains three oranges. Changing which basket she carries has not moved the fruit in his basket. Earlier she changed the shared contents. Now she changed what she was holding.

Ravi then asks for a second basket with exactly the same three oranges. He can compare the contents and say the two baskets match. He cannot honestly say they are the very same basket. If one falls, the other remains upright. Equal contents and being the same thing answer different questions.

Before they leave, their mother asks them to carry the heavy shopping upstairs. She can hand Ravi the actual basket, or she can ask him to assemble another basket containing the same purchases. One choice lets him change what everyone will receive; the other gives him something separate to rearrange.

The family avoids confusion by asking two questions before anyone moves anything: which basket are you holding, and are you changing its contents or choosing a different basket? Those questions explain the whole disagreement without blaming anyone for remembering the oranges incorrectly.

## 3. The idea in plain English

Go passes every argument by value. A **pointer** is a value containing an address. `&value` obtains an address and `*pointer` accesses the value at that address. Copying a pointer copies the address, so both copies can access the same object.

Ravi's separate basket corresponds to a struct passed by value. Changing the copy's fields does not change the original. A **value receiver** receives a copy of the receiver. A **pointer receiver** receives a copied pointer and can update the original struct through it.

A slice is different from an array: its copied descriptor still refers to shared backing storage. Changing an existing element can be visible to the caller, but appending may allocate new backing storage and always changes the local descriptor's length. Return the resulting slice when the caller needs the new length. A nil pointer has no object to access.

## 4. The picture

```text
caller --------------------> object A: [1, 2]
                                  ^
local parameter / alias -----------+

mutate A: both paths observe the change
rebind local: local -------------> object B: [99]
             caller still ------> object A
```

This is the shared-object case. In Go it requires a reference-bearing value such as a pointer or slice; a copied struct is different. In C++, compare a reference parameter with a plain value parameter.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```go
func (counter Counter) BumpCopy() { counter.Value++ }
func (counter *Counter) Bump() { counter.Value++ }
```

The first method changes a copied Counter. The second copies an address and changes the Counter at that address. Starting at 2, the caller sees 2 after BumpCopy and 3 after Bump.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import "fmt"

type Counter struct { Value int }

func (counter Counter) BumpCopy() { counter.Value++ }
func (counter *Counter) Bump() { counter.Value++ }

func main() {
    counter := Counter{Value: 2}
    counter.BumpCopy()
    fmt.Println(counter.Value)
    counter.Bump()
    fmt.Println(counter.Value)
    pointer := &counter
    pointer.Value = 8
    fmt.Println((*pointer).Value, counter.Value)
}
```

**Check the result:** Run `go run main.go`. It prints `2`, `3`, and `8 8` on separate lines.

## 6. How the other two languages do it

- **Python** — Assignment binds names to objects; it does not copy.
- **Go** — Every Go argument is passed by value.
- **C++** — A value parameter is independent of its caller's value.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** put a slice in a value-receiver struct and assume all its contents are copied. The slice descriptor is copied, but its elements may still be shared. A value receiver is not a deep-copy operation.

**Failure to reproduce:** `var pointer *Counter; fmt.Println(pointer.Value)` panics with a message containing `runtime error: invalid memory address or nil pointer dereference`. Check nil when absence is permitted, or construct a real Counter before using its address.

## 8. Say it out loud

**How it gets asked:** “Is this passed by value or by reference?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** Go always passes values, including pointers. A pointer receiver lets a method change the original object because the copied pointer still identifies it. A value receiver copies the struct, but reference-bearing fields can still share storage. I separate copying a descriptor from copying all the data it reaches, particularly for slices and maps.

**Follow-ups**

1. **Does Go support pointer arithmetic?** Ordinary Go pointers do not support C++-style pointer arithmetic.

2. **Why does counter.Bump() work without an explicit &?** For an addressable value, method-call syntax can take its address automatically.

3. **Does append update the caller's slice length?** No. Return the new slice descriptor and assign it in the caller.

**Model answer:** The first method changes a copied Counter. The second copies an address and changes the Counter at that address. Starting at 2, the caller sees 2 after BumpCopy and 3 after Bump. Return a slice after append when the caller needs its new length.

## 9. Recall card

- Every Go argument is passed by value.
- Copying a pointer preserves access to one object.
- Pointer receivers can mutate the original struct.
- Slice descriptors can share backing storage.
- Return a slice after append when the caller needs its new length.
