---
day: 8
track: lang-cpp
title: "struct, class, constructors, and member functions"
theme: "Modelling a thing"
phase: "Languages: every language, every basic"
status: written
---

# Day 008 · C++ — struct, class, constructors, and member functions

**Today's theme:** Modelling a thing

**After today you can:** You can model a bank account in each language with data and behaviour together, and say what is public.

**The interviewer asks it as:** *What is the difference between a struct and a class?*

---

## 1. What this is, and why it matters

In C++ `struct` and `class` are the same feature: a named type with data members and member functions. The only difference is the default: members of a `struct` are public unless you say otherwise, and members of a `class` are private unless you say otherwise. A constructor is a member function with the class's own name that runs when an object is created, and `private:` is enforced by the compiler, so a field marked private cannot be touched from outside, full stop.

At work, the convention is `struct` for plain bundles of data with no rules and `class` for anything with an invariant to protect, and interviewers ask exactly the question in the heading to see whether you know the difference is only the default. They also ask "what is a `const` member function" and "what is the member initialiser list", and both are today.

## 2. The story

Sunita runs a tiffin service from her kitchen. Forty customers, one hot lunch each, delivered by eleven. She used to keep everything in her head. At forty it stopped fitting.

So she sat down one Sunday and worked out what she actually needs to know about each customer. A name. A delivery address. How much money they have paid in advance. That is it. Every customer is those three things, and nothing else about them matters to the business.

Then she worked out what happens to a customer. They top up, usually five hundred or a thousand at a time, and the balance goes up. Every day a tiffin goes out, and the balance goes down by eighty. If a balance would go below zero, the tiffin does not go out; she sends a message instead. And once a month she tells each customer their balance.

Those are the only four things that ever happen. Top up, deduct a tiffin, refuse if there is not enough, and report. Nobody ever does anything else to a customer's account. Sunita wrote the four things on a note in her phone and has not changed the note in two years.

Here is the part that took her longest to decide. Her customers can ask their balance any time, and she tells them straight away. But they cannot change it. Not even the ones she has known for ten years. Mr Rao once asked her to just write down a thousand and he would pay her on Friday. She said no. The number changes when money arrives or a tiffin leaves, and by no other route, ever. That rule is what makes the number trustworthy. If anyone could reach in and change it, she would have to check it every time she read it.

When a new customer joins, Sunita does the same three things every time: gets the name, gets the address, takes the first payment. Nobody starts without all three. A customer with no address is not a customer yet.

And when she describes a customer to her daughter, she says it the same way every time: "Rao, Flat 4B, four hundred and twenty left." Name, address, balance. The description is part of the thing.

## 3. The idea in plain English

A **class** is a named type with **data members**, the fields, and **member functions**, the methods. `class Account { ... };` declares one, and note the semicolon after the closing brace; forgetting it produces a confusing error on the next line.

Inside, **access specifiers** divide the members. `public:` members can be used by any code. `private:` members can be used only by the class's own member functions. That is enforced by the compiler: `rao.balance_ = 5000` from outside is a compile error, not a convention. Sunita's rule, with teeth. The trailing underscore on `balance_` is a common convention for private data members; it is only a name.

A **struct** is exactly the same thing with the default flipped: everything is public until you write `private:`. So `struct` is what you use for a bundle of values with no rules, a delivery of three fields, and `class` is what you use when there is something to protect. The interviewer's question has a one-sentence answer, and the rest of the answer is when you use which.

A **constructor** is a member function named after the class, with no return type, that runs when an object is created: `Account(std::string holder, std::string address, int opening)`. Sunita's three steps. It sets the data members using the **member initialiser list**, the part after the colon: `: holder_(holder), address_(address), balance_(opening)`. That list initialises each member directly, in the order the members are declared, and it is the correct way to set them; assigning inside the braces works but first default-constructs each member and then overwrites it.

A **`const` member function**, with `const` after its parameter list, promises not to change the object: `int balance() const`. Only `const` member functions can be called on an object that is itself `const`, which matters the moment you pass an account to a function by `const` reference, which day 12 makes routine. The rule now: every member function that only reads is marked `const`.

Objects are created without any `new`: `Account rao("Rao", "Flat 4B", 500);` or `Account rao{"Rao", "Flat 4B", 500};`. The object lives in `rao` and is destroyed when `rao` goes out of scope, which is day 13's subject.

## 4. The picture

```
 class Account {                         struct Delivery {
 public:                                     std::string holder;     ← public by default
     Account(...);                           std::string address;
     void deposit(int);                      int tiffins = 1;
     bool charge_tiffin(int);            };
     int balance() const;                the same feature, different default
 private:
     std::string holder_;
     std::string address_;
     int balance_;
 };

 Account rao("Rao", "Flat 4B", 500);
   ┌──────────────────────────┐
   │ holder_   "Rao"          │  private: only Account's own member functions
   │ address_  "Flat 4B"      │  private
   │ balance_  500            │  private
   └──────────────────────────┘
   rao.deposit(500)      ✓ public
   rao.balance()         ✓ public, const
   rao.balance_ = 5000   ✗ compile error
```

*Notice that the class and the struct have identical machinery and differ only in where the line between public and private falls by default. Notice that the last line is refused by the compiler, not by a convention.*

## 5. The code, built step by step

Start `tiffin.cpp` in a `day08` folder. The class, with its public face first.

```cpp
#include <format>
#include <iostream>
#include <string>

class Account {
public:
    Account(std::string holder, std::string address, int opening)
        : holder_(holder), address_(address), balance_(opening) {}
```

The constructor has the class's name and no return type. After the colon is the member initialiser list; the empty braces are its body, which has nothing left to do.

The actions, and the read-only view.

```cpp
    void deposit(int amount) { balance_ += amount; }

    bool charge_tiffin(int price = 80) {
        if (balance_ < price) {
            return false;
        }
        balance_ -= price;
        return true;
    }

    int balance() const { return balance_; }
```

Member functions defined inside the class body are written right there. `balance()` is `const` because it only reads. There is no `set_balance`; that absence is the design.

The description, and the private part.

```cpp
    std::string describe() const {
        return std::format("Account({}, {}, balance={})", holder_, address_, balance_);
    }

private:
    std::string holder_;
    std::string address_;
    int balance_;
};
```

Everything after `private:` is reachable only from the member functions above. The semicolon after `};` is required.

The struct, for the thing with no rules.

```cpp
struct Delivery {
    std::string holder;
    std::string address;
    int tiffins = 1;
};
```

No constructor written, no access specifiers: all public, and `Delivery d{"Rao", "Flat 4B"}` fills the fields in order with `tiffins` defaulting to `1`. Same feature as `class`, default flipped.

Using them.

```cpp
int main() {
    Account rao("Rao", "Flat 4B", 500);
    rao.deposit(500);
    std::cout << rao.describe() << "\n";
    std::cout << std::boolalpha << rao.charge_tiffin() << " " << rao.balance() << "\n";

    Delivery d{"Rao", "Flat 4B"};
    std::cout << d.holder << " " << d.tiffins << "\n";
}
```

```
Account(Rao, Flat 4B, balance=1000)
true 920
Rao 1
```

And Sunita's rule, which does not compile.

```cpp
    rao.balance_ = 5000;
```

```
tiffin.cpp: In function 'int main()':
tiffin.cpp:37:9: error: 'int Account::balance_' is private within this context
   37 |     rao.balance_ = 5000;
      |         ^~~~~~~~
tiffin.cpp:26:9: note: declared private here
   26 |     int balance_;
      |         ^~~~~~~~
```

Python let this through with an underscore convention. Go refused it across packages. C++ refuses it everywhere outside the class.

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra tiffin.cpp -o tiffin
./tiffin
```

```
Account(Rao, Flat 4B, balance=1000)
tiffin sent: true, balance now 920
tiffin sent: true, balance now 840
Account(Iyer, Flat 2A, balance=60)
tiffin sent: false, balance now 60
delivery: Rao, Flat 4B, 1 tiffin
```

And the complete file.

```cpp
// tiffin.cpp — day 8, class with an invariant, struct without one
// Build: g++ -std=c++20 -Wall -Wextra tiffin.cpp -o tiffin
// Run:   ./tiffin
#include <format>
#include <iostream>
#include <string>

// One customer's prepaid balance. balance_ changes only through deposit and charge_tiffin.
class Account {
public:
    Account(std::string holder, std::string address, int opening)
        : holder_(holder), address_(address), balance_(opening) {}

    void deposit(int amount) { balance_ += amount; }

    bool charge_tiffin(int price = 80) {
        if (balance_ < price) {
            return false;
        }
        balance_ -= price;
        return true;
    }

    int balance() const { return balance_; }

    std::string describe() const {
        return std::format("Account({}, {}, balance={})", holder_, address_, balance_);
    }

private:
    std::string holder_;
    std::string address_;
    int balance_;
};

// Three values and no rules, so a struct.
struct Delivery {
    std::string holder;
    std::string address;
    int tiffins = 1;
};

int main() {
    Account rao("Rao", "Flat 4B", 500);
    rao.deposit(500);
    std::cout << rao.describe() << "\n";
    std::cout << std::boolalpha;
    for (int i = 0; i < 2; ++i) {
        bool sent = rao.charge_tiffin();
        std::cout << "tiffin sent: " << sent << ", balance now " << rao.balance() << "\n";
    }

    Account iyer("Iyer", "Flat 2A", 60);
    std::cout << iyer.describe() << "\n";
    bool sent = iyer.charge_tiffin();
    std::cout << "tiffin sent: " << sent << ", balance now " << iyer.balance() << "\n";

    Delivery d{"Rao", "Flat 4B"};
    std::cout << "delivery: " << d.holder << ", " << d.address << ", " << d.tiffins << " tiffin\n";
    return 0;
}
```

Notice `bool sent = rao.charge_tiffin();` on its own line before the print. Writing `charge_tiffin()` and `balance()` in the same `<<` chain would work in C++17 and later, where the chain is evaluated left to right, but separating the call that changes state from the call that reads it is clearer and is the habit to build.

## 6. How the other two languages do it

Python, where methods live inside the class, privacy is a convention, and `@dataclass` plays the role of `struct`:

```python
class Account:
    def __init__(self, holder: str, address: str, opening: int) -> None:
        self._balance = opening         # convention: please do not touch

    def deposit(self, amount: int) -> None:
        self._balance += amount

@dataclass
class Delivery:
    holder: str
    address: str
    tiffins: int = 1
```

Go, where the struct is data only, methods attach from outside, and a lowercase first letter is private to the package:

```go
type Account struct {
	Holder  string
	balance int          // lowercase: this package only
}

func (a *Account) Deposit(amount int) { a.balance += amount }
```

The one line of difference that matters: **C++ and Go both enforce privacy with the compiler; Python does not, and only C++ makes you choose the default with a keyword.** In Go, `struct` is the only option and visibility is per name. In Python, everything is a class and the underscore is a request. In C++, `struct` and `class` are one thing, and the keyword you pick is a message to the reader about whether there are rules inside. The other thing to notice is the constructor: C++ and Python have a real one that runs on creation; Go has a convention, `NewAccount`, and nothing stops you building the struct without it.

## 7. The traps

**The real error: the `const` object and the non-`const` method.** Forget `const` on `balance()`, then read it through a `const` account.

```cpp
    int balance() { return balance_; }           // const forgotten
    ...
    const Account fixed("Rao", "Flat 4B", 500);
    std::cout << fixed.balance() << "\n";
```

```
tiffin.cpp: In function 'int main()':
tiffin.cpp:34:31: error: passing 'const Account' as 'this' argument discards qualifiers [-fpermissive]
   34 |     std::cout << fixed.balance() << "\n";
      |                  ~~~~~~~~~~~~~^~
tiffin.cpp:15:9: note:   in call to 'int Account::balance()'
```

The compiler will not call a method that might change the object on an object that promised not to change. Yesterday you saw this message for `operator[]` on a `const` map; it is the same rule. Mark every reading method `const` from the start.

**The real error: the most vexing parse.** Create an account with no arguments using round brackets.

```cpp
    Account a();
    a.deposit(500);
```

```
tiffin.cpp:33:14: warning: empty parentheses were disambiguated as a function declaration [-Wvexing-parse]
   33 |     Account a();
      |              ^~
tiffin.cpp:34:7: error: request for member 'deposit' in 'a', which is of non-class type 'Account()'
   34 |     a.deposit(500);
      |       ^~~~~~~
```

`Account a();` declares a **function** named `a` that returns an `Account`. It is one of the oldest jokes in the language. Use braces, `Account a{};`, or no brackets at all, `Account a;`, and today's `Account` has no zero-argument constructor anyway, so both would fail with a clearer message.

**The near-miss: the uninitialised member.** Leave `balance_` out of the initialiser list.

```cpp
    Account(std::string holder, std::string address, int opening)
        : holder_(holder), address_(address) {}
```

```
tiffin.cpp:11:60: warning: unused parameter 'opening' [-Wunused-parameter]
```

Only a warning, and only because `opening` went unused. `balance_` now holds whatever bytes were in that memory, and `rao.balance()` prints a random number. Give every member a value, either in the initialiser list or with a default at the declaration, `int balance_ = 0;`. Go would have given you zero; C++ gives you garbage.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between a struct and a class in C++?"
- "What is a `const` member function and why does it matter?"
- "Why use the member initialiser list instead of assigning in the constructor body?"

**What to say out loud, the first ninety seconds**

"In C++ `struct` and `class` are the same construct with one difference: members of a `struct` default to public and members of a `class` default to private; the same applies to inheritance. Everything else, constructors, member functions, access specifiers, is identical. The convention is `struct` for passive aggregates of data with no invariants and `class` for types that protect an invariant behind private members and public member functions.

A constructor is named after the class, has no return type, and initialises members through the initialiser list after the colon; that list directly initialises each member in declaration order, whereas assigning in the body default-constructs first and then assigns, which is wasteful for strings and impossible for `const` or reference members. A member function marked `const` after its parameters promises not to modify the object, and only `const` member functions can be called on a `const` object or through a `const` reference, so every accessor should be `const`. Private access is checked by the compiler; there is no convention involved."

**The follow-ups**

1. *"What does `this` refer to?"* — A pointer to the object the member function was called on. Inside `deposit`, `balance_` is shorthand for `this->balance_`. Day 12 covers pointers.
2. *"What happens if you do not write a constructor?"* — The compiler generates a default one that default-initialises each member, which for built-in types like `int` means indeterminate values unless a default member initialiser is present. That is why `int balance_ = 0;` at the declaration is a good habit.
3. *"Can a `const` member function change anything?"* — Not the object's members, unless a member is declared `mutable`, which is used for things like caches that do not affect the object's logical state.

**A model answer**

"`struct` and `class` are one mechanism differing only in default access: public for `struct`, private for `class`. A constructor is a same-named member without a return type; the member initialiser list initialises members directly in declaration order and is preferred over assignment in the body for efficiency and because `const` and reference members require it. Access specifiers are enforced at compile time. `const` member functions cannot modify the object and are the only ones callable on `const` instances, so accessors are always `const`. Objects are created directly on the stack with braces or parentheses, with `Account a();` being the vexing parse that declares a function. Members without an initialiser hold indeterminate values, so every member gets a default or an entry in the initialiser list."

## 9. Recall card

- `struct` defaults public, `class` defaults private; otherwise identical; `struct` for plain data, `class` when there is a rule to protect; semicolon after `};`.
- Constructor: `Account(std::string h, int opening) : holder_(h), balance_(opening) {}`; the initialiser list initialises in declaration order.
- Mark every reading member function `const`, or a `const` object cannot call it: `discards qualifiers`.
- `private:` is enforced: `rao.balance_ = 5000` is `error: 'int Account::balance_' is private within this context`.
- `Account a();` declares a function; use `Account a{...};`; give every member a value or it holds garbage.
