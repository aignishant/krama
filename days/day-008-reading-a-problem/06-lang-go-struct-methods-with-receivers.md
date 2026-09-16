---
day: 8
track: lang-go
title: "struct, methods with receivers, and constructor functions"
theme: "Modelling a thing"
phase: "Languages: every language, every basic"
status: written
---

# Day 008 · Go — struct, methods with receivers, and constructor functions

**Today's theme:** Modelling a thing

**After today you can:** You can model a bank account in each language with data and behaviour together, and say what is public.

**The interviewer asks it as:** *What is the difference between a struct and a class?*

---

## 1. What this is, and why it matters

Go has no classes. It has structs, which are named bundles of fields, and it lets you attach methods to any named type by writing a function with a receiver in front of its name. What is public is decided by one rule: a name that starts with a capital letter is visible outside its package, and a name that starts with a lowercase letter is not. There is no constructor keyword; you write an ordinary function, conventionally `NewAccount`, that builds and returns the struct.

At work, every Go service is structs with methods on them, and the capital-letter rule is why Go code has `Holder` and `balance` side by side in one struct. Interviewers ask "what is the difference between a struct and a class", "what is the difference between a value receiver and a pointer receiver", and "how do you make a field private in Go", and the third one has a one-word answer: lowercase.

## 2. The story

Sunita runs a tiffin service from her kitchen. Forty customers, one hot lunch each, delivered by eleven. She used to keep everything in her head. At forty it stopped fitting.

So she sat down one Sunday and worked out what she actually needs to know about each customer. A name. A delivery address. How much money they have paid in advance. That is it. Every customer is those three things, and nothing else about them matters to the business.

Then she worked out what happens to a customer. They top up, usually five hundred or a thousand at a time, and the balance goes up. Every day a tiffin goes out, and the balance goes down by eighty. If a balance would go below zero, the tiffin does not go out; she sends a message instead. And once a month she tells each customer their balance.

Those are the only four things that ever happen. Top up, deduct a tiffin, refuse if there is not enough, and report. Nobody ever does anything else to a customer's account. Sunita wrote the four things on a note in her phone and has not changed the note in two years.

Here is the part that took her longest to decide. Her customers can ask their balance any time, and she tells them straight away. But they cannot change it. Not even the ones she has known for ten years. Mr Rao once asked her to just write down a thousand and he would pay her on Friday. She said no. The number changes when money arrives or a tiffin leaves, and by no other route, ever. That rule is what makes the number trustworthy. If anyone could reach in and change it, she would have to check it every time she read it.

When a new customer joins, Sunita does the same three things every time: gets the name, gets the address, takes the first payment. Nobody starts without all three. A customer with no address is not a customer yet.

And when she describes a customer to her daughter, she says it the same way every time: "Rao, Flat 4B, four hundred and twenty left." Name, address, balance. The description is part of the thing.

## 3. The idea in plain English

A **struct** is a named bundle of **fields**, each with a type:

```go
type Account struct {
	Holder  string
	Address string
	balance int
}
```

`type Account struct` declares a new type called `Account`. Each instance has its own three values. You make one with a **struct literal**, `Account{Holder: "Rao", Address: "Flat 4B", balance: 500}`, and read a field with `rao.Holder`.

Now look at the capital letters. `Holder` and `Address` are **exported**: code in any other package can read and write them. `balance` is **unexported**: only code in this package can touch it. That is the whole of Go's privacy system. No `private` keyword, no underscore convention; the first letter decides, and the compiler enforces it. Sunita's rule that nobody outside changes the balance is one lowercase letter.

A **method** is a function with a **receiver**, an extra parameter written before the name: `func (a *Account) Deposit(amount int)`. The receiver `a` is the account the method was called on, the same job as Python's `self`, except you choose its name and its type. You call it as `rao.Deposit(500)`.

The receiver's type is either `Account` or `*Account`. The star means **pointer**, which day 12 covers properly; today, the rule you need is this. With `(a Account)`, a **value receiver**, the method gets a **copy** of the account, and any change it makes is thrown away when it returns. With `(a *Account)`, a **pointer receiver**, the method works on the original. So any method that changes a field must use `*Account`, and by convention, once one method on a type needs a pointer receiver, they all use it.

There is no constructor. The convention is a plain function named `New` plus the type: `func NewAccount(holder, address string, opening int) *Account`. It is where Sunita's three steps live, and it returns a pointer to the new struct so that the methods with pointer receivers work on the one true copy.

A struct also works with no constructor at all: `var a Account` gives you an account with every field at its zero value, `""`, `""`, `0`. Go calls this "making the zero value useful", and designs its standard library around it.

## 4. The picture

```
 type Account struct { Holder string; Address string; balance int }

 rao := NewAccount("Rao", "Flat 4B", 500)        rao is a *Account: it points at the struct

   rao ──► ┌──────────────────────────┐
           │ Holder   "Rao"           │  exported: any package may read or write
           │ Address  "Flat 4B"       │  exported
           │ balance  500             │  unexported: this package only
           └──────────────────────────┘

 func (a *Account) Deposit(n int)     a is rao itself   → a.balance += n changes the struct above
 func (a  Account) Deposit(n int)     a is a COPY       → a.balance += n changes the copy, then it is gone

 Methods are not inside the struct. They are functions with a receiver, declared anywhere in the package.
```

*Notice that the struct is only data, and the methods attach from outside. Notice the difference in the two `Deposit` lines: one star decides whether the change survives.*

## 5. The code, built step by step

Start `tiffin.go` in a `day08` folder. The struct and its constructor.

```go
package main

import "fmt"

type Account struct {
	Holder  string
	Address string
	balance int
}

func NewAccount(holder, address string, opening int) *Account {
	return &Account{Holder: holder, Address: address, balance: opening}
}
```

`&Account{...}` builds the struct and gives back a pointer to it, which is what `*Account` in the return type promises. Read `&` as "the address of", and leave the rest for day 12.

The methods.

```go
func (a *Account) Deposit(amount int) {
	a.balance += amount
}

func (a *Account) ChargeTiffin(price int) bool {
	if a.balance < price {
		return false
	}
	a.balance -= price
	return true
}

func (a *Account) Balance() int {
	return a.balance
}
```

Each is a function with `(a *Account)` before its name. `Balance()` is how the outside world reads the balance, since `balance` itself is unexported. No `Set`; that is Sunita's rule.

The description.

```go
func (a *Account) String() string {
	return fmt.Sprintf("Account{%s, %s, balance=%d}", a.Holder, a.Address, a.balance)
}
```

A method named `String() string` is special: `fmt.Println` and `%v` call it when they print your type. Python's `__repr__` under another name.

Using it.

```go
func main() {
	rao := NewAccount("Rao", "Flat 4B", 500)
	rao.Deposit(500)
	fmt.Println(rao)
	fmt.Println(rao.ChargeTiffin(80), rao.Balance())
}
```

```
Account{Rao, Flat 4B, balance=1000}
true 920
```

Now the zero value and a plain literal, which also work.

```go
	var blank Account
	fmt.Printf("%+v\n", blank)
	iyer := Account{Holder: "Iyer", Address: "Flat 2A", balance: 60}
	fmt.Println(iyer.ChargeTiffin(80), iyer.Balance())
```

```
{Holder: Address: balance:0}
false 60
```

`%+v` prints a struct with its field names. The zero-value account is a real account with nothing in it. `iyer` was built with a literal instead of the constructor, which is allowed inside this package because `balance` is reachable here. Go took the address of `iyer` automatically to call the pointer-receiver methods on it; that is a convenience you will lean on without noticing.

Here is the run and output for the complete program.

```bash
go run tiffin.go
```

```
Account{Rao, Flat 4B, balance=1000}
tiffin sent: true, balance now 920
tiffin sent: true, balance now 840
Account{Iyer, Flat 2A, balance=60}
tiffin sent: false, balance now 60
zero value: {Holder: Address: balance:0}
```

And the complete file.

```go
// tiffin.go — day 8, a struct with methods and one unexported field
// Run:  go run tiffin.go
package main

import "fmt"

// Account is one customer's prepaid balance.
// Holder and Address are exported; balance is not, so it changes only through methods.
type Account struct {
	Holder  string
	Address string
	balance int
}

// NewAccount is the constructor by convention: Sunita's three steps.
func NewAccount(holder, address string, opening int) *Account {
	return &Account{Holder: holder, Address: address, balance: opening}
}

func (a *Account) Deposit(amount int) {
	a.balance += amount
}

func (a *Account) ChargeTiffin(price int) bool {
	if a.balance < price {
		return false
	}
	a.balance -= price
	return true
}

func (a *Account) Balance() int {
	return a.balance
}

func (a *Account) String() string {
	return fmt.Sprintf("Account{%s, %s, balance=%d}", a.Holder, a.Address, a.balance)
}

func main() {
	rao := NewAccount("Rao", "Flat 4B", 500)
	rao.Deposit(500)
	fmt.Println(rao)
	for i := 0; i < 2; i++ {
		fmt.Printf("tiffin sent: %v, balance now %d\n", rao.ChargeTiffin(80), rao.Balance())
	}

	iyer := NewAccount("Iyer", "Flat 2A", 60)
	fmt.Println(iyer)
	fmt.Printf("tiffin sent: %v, balance now %d\n", iyer.ChargeTiffin(80), iyer.Balance())

	var blank Account
	fmt.Printf("zero value: %+v\n", blank)
}
```

## 6. How the other two languages do it

Python, where the methods live inside the class and privacy is a naming convention:

```python
class Account:
    def __init__(self, holder: str, address: str, opening: int) -> None:
        self.holder = holder
        self.address = address
        self._balance = opening      # underscore: please do not touch

    def deposit(self, amount: int) -> None:
        self._balance += amount
```

C++, where `class` and `struct` are one feature with two default visibilities, and `private:` is enforced:

```cpp
class Account {
public:
    Account(std::string holder, std::string address, int opening);
    void deposit(int amount);
private:
    std::string holder_;
    std::string address_;
    int balance_;
};
```

The one line of difference that matters: **Go decides visibility per name by its first letter; Python by convention; C++ by `public:` and `private:` sections.** A Python or C++ programmer arriving in Go looks for the keyword and finds a capital letter instead, and then discovers it applies to functions, types and constants too, not only fields. The second difference: in Go the struct holds only data and methods attach from outside, so "struct or class" is not a choice you make. Every type is a struct, and it has methods or it does not.

## 7. The traps

**The near-miss: the value receiver that changes nothing.** Write `Deposit` with a value receiver.

```go
func (a Account) Deposit(amount int) {
	a.balance += amount
}

rao := Account{Holder: "Rao", balance: 500}
rao.Deposit(500)
fmt.Println(rao.balance)
```

```
500
```

No error, no warning. `Deposit` received a copy, added to the copy, and the copy was thrown away. This is the most common mistake in the first month of Go. Any method that assigns to a field needs `*Account`.

**The real error: touching an unexported field from another package.** Suppose `Account` lives in a package called `bank` and you write, from `main`:

```go
	rao := bank.NewAccount("Rao", "Flat 4B", 500)
	rao.balance = 5000
```

```
./main.go:9:6: rao.balance undefined (cannot refer to unexported field balance)
```

Not a warning, not a convention, a compile error. That is what one lowercase letter buys you. Day 11 splits code across packages so you can see this for real.

**The near-miss: the positional struct literal.** Build an account without field names.

```go
	rao := Account{"Rao", "Flat 4B", 500}
```

It compiles and works today. Tomorrow someone adds a field or reorders two, and every positional literal in the codebase either breaks or, worse, quietly puts the address in the holder. Always name the fields: `Account{Holder: "Rao", Address: "Flat 4B", balance: 500}`. `go vet` flags unkeyed literals for types from other packages for exactly this reason.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between a struct and a class?"
- "When do you use a pointer receiver instead of a value receiver?"
- "How do you make a field private in Go?"

**What to say out loud, the first ninety seconds**

"Go has structs and methods but no classes. A struct is a named collection of fields. A method is a function with a receiver parameter before its name, attached to a named type, and declared separately from the struct; the struct is just data. So the struct-versus-class question does not arise in Go: every type is a struct, and behaviour is added by writing methods.

Visibility is by capitalisation. An identifier starting with an uppercase letter is exported from its package; lowercase is unexported and inaccessible outside the package, enforced by the compiler. A private field is simply a lowercase field, and the package exposes exported methods to read or change it.

Receivers are value or pointer. A value receiver gets a copy, so mutations are lost; a pointer receiver operates on the original. I use pointer receivers for any method that mutates, for large structs to avoid copying, and, for consistency, for all methods on a type once any one of them needs a pointer. There is no constructor syntax; the convention is a `NewT` function returning `*T`, and the zero value of a struct should be usable where possible."

**The follow-ups**

1. *"Can you attach methods to types that are not structs?"* — Yes, to any named type declared in the package: `type Celsius float64` can have methods. Not to built-in types directly, and not to types from other packages.
2. *"Why does Go take the address automatically when calling a pointer method on a value?"* — Convenience: `iyer.ChargeTiffin(80)` on an addressable `Account` variable is rewritten as `(&iyer).ChargeTiffin(80)`. It does not work on values you cannot take the address of, such as a struct returned directly from a function call.
3. *"What is struct embedding?"* — Placing one struct type inside another without a field name, so the outer struct gets the inner one's fields and methods promoted. It is Go's substitute for inheritance, and day 17 covers it.

**A model answer**

"A Go struct is a value type holding named fields; methods are functions with a receiver, declared at package level, so data and behaviour are separate declarations and there is no class construct. Exported identifiers begin with an uppercase letter and are visible across packages; lowercase identifiers are package-private, which is how fields are hidden and invariants protected. Pointer receivers, `(a *Account)`, act on the original and are required for mutation; value receivers copy. Constructors are plain functions by convention, `NewAccount`, returning `*Account`, and idiomatic types make their zero value useful. Keyed struct literals are preferred over positional ones for robustness, and `String() string` on a type is picked up by `fmt` for printing."

## 9. Recall card

- `type Account struct { Holder string; balance int }`; capital first letter is exported, lowercase is package-private, enforced by the compiler.
- Methods are functions with a receiver: `func (a *Account) Deposit(n int)`; the struct is data only.
- `(a *Account)` works on the original; `(a Account)` works on a copy and mutations vanish silently. Mutating methods need the star.
- No constructor keyword: `func NewAccount(...) *Account { return &Account{...} }`; `var a Account` is a usable zero value.
- Name your fields in literals, `Account{Holder: "Rao"}`; `String() string` is what `fmt` prints.
