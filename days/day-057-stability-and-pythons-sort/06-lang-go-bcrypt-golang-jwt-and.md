---
day: 57
track: lang-go
title: "bcrypt, golang-jwt, and a login flow"
theme: "Authentication: hashing and tokens"
phase: "Languages: networking, HTTP, and data"
status: written
---

# Day 057 · Go — bcrypt, golang-jwt, and a login flow

**Today's theme:** Authentication: hashing and tokens

**After today you can:** You can store a password correctly and issue a signed token in each language.

**The interviewer asks it as:** *How do you store a password?*

---

## 1. What this is, and why it matters

Authentication has two halves, and Go has a standard-ish library for each. `golang.org/x/crypto/bcrypt`
stores a password as a slow, salted **hash**, so a stolen database reveals no passwords.
`golang-jwt` signs a **JWT**, a token a caller presents on every later request to prove they
logged in, without sending the password again. The bcrypt API is two functions,
`GenerateFromPassword` and `CompareHashAndPassword`; the JWT API is build-sign and parse-verify,
and the verify step takes a key function where the one dangerous mistake in JWT lives.

At work, this is the code you are least allowed to get wrong. In interviews, "how do you store a
password" is in nearly every backend round, and the Go-specific detail is the key function on
verify: what it must assert, and what happens when it does not.

## 2. The story

Farah runs a members' club. To become a member you come in once and sign the register in your own
hand. But the club does not keep your signature. That would be dangerous: a thief who broke in and
photographed the register could forge any member's signature forever. Instead, the moment you
sign, a clerk studies the signature closely, notes down a long list of its particular quirks, and
files that description. Your actual signature is destroyed. Nobody at the club can reproduce your
signature from the description; they can only check a new signature against it.

When you come back, you sign again. The clerk compares your new signature to the filed
description. Two things make this safe. The clerk deliberately takes a slow, careful minute over
each comparison, so a thief who somehow got the descriptions and wanted to try a million forged
signatures against them would need a million slow minutes. And every member's description is
salted with a random word the clerk picked when they joined, so that two members who happen to
sign alike still have completely different descriptions on file.

Signing in full every time you want a drink would be tedious, so once you are in for the evening,
Farah gives you a wristband. It says who you are and the time it was issued, and it is stamped
with the club's embossing seal, which only Farah has. At the bar, the barman glances at the
wristband, runs a thumb over the seal to feel it is genuine, and pours. The wristband expires at
midnight. If you alter the name, the seal no longer matches and the barman refuses.

Farah's barman is trained on one thing above all. He does not read off the wristband which kind of
seal to check for and then check for that. A clever forger printed a band that said, in small
letters, "verify me with the plastic stamp, not the metal one", and left the plastic-stamp area
blank, hoping the barman would check the blank area and wave it through. Farah's rule is that the
barman always checks for the one real metal seal, the club's own, no matter what the band says
about itself. A band that asks to be checked a different way is refused on sight.

## 3. The idea in plain English

Destroying the signature and keeping a description is **hashing**: a one-way function from
password to hash. `bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)` computes
it; you store the result. `bcrypt.CompareHashAndPassword(stored, []byte(attempt))` checks a login,
returning `nil` for a match and an error otherwise. You store the hash, never the password.

The clerk's slowness is the **work factor**, `bcrypt.DefaultCost`, which is 10 in this library.
bcrypt is slow on purpose, so a stolen database cannot be brute-forced quickly. The random word
is the **salt**, generated for you and stored inside the hash string, so identical passwords hash
differently and precomputed tables do not work.

The wristband is a **JWT**: JSON claims, `sub` for the subject and `exp` for expiry, signed with
a **secret** only the server has, using HS256, HMAC-SHA256. `jwt.NewWithClaims(...).SignedString(secret)`
makes it; parsing with a key function verifies it.

The barman always checking for the one real seal is the **key function** on verify. When you
parse a token, golang-jwt calls a function you supply to get the key, and passes it the token so
you can inspect it. The one thing that function must do is assert the signing method is what you
expect, `token.Method.(*jwt.SigningMethodHMAC)`, and only then return the secret. If you return
the secret without checking, an attacker can hand you a token that says "verify me with `none`"
or with a different algorithm, and you will. That is the forger's band that names its own weak
seal, and asserting the method is refusing it.

Because the server verifies the seal without a lookup, a JWT is **stateless**. Tampering breaks
the seal, `exp` bounds its life, and the secret never leaving the server is what keeps the seal
un-forgeable, [day 51](../day-051-why-sorting-matters/README.md)'s rule again.

## 4. The picture

```text
  register (once)                         login (each time)

  password "hunter2"                      password "hunter2"
      |  GenerateFromPassword (slow, salted)  |  CompareHashAndPassword(stored, attempt)
      v                                        v
  $2a$10$N9qo8uLO...   <- stored            nil error? yes -> issue a token

  token: {"sub":"meera","exp":...} + HMAC-SHA256(payload, SECRET) = eyJhbGci...
  verify: Parse(token, keyFunc) where keyFunc asserts token.Method is HMAC, then returns SECRET
```

Notice the key function is where you assert the algorithm before returning the secret. Returning
the secret unconditionally is the hole.

## 5. The code, built step by step

The modules:

```bash
go get golang.org/x/crypto/bcrypt github.com/golang-jwt/jwt/v5
```

Registering.

```go
var users = map[string][]byte{}   // username -> bcrypt hash

func register(username, password string) error {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	users[username] = hash
	return nil
}
```

`GenerateFromPassword` returns the hash as bytes, salt and cost baked in. Store that; the
password is gone.

Checking a password.

```go
func checkPassword(username, password string) bool {
	stored, ok := users[username]
	if !ok {
		return false
	}
	return bcrypt.CompareHashAndPassword(stored, []byte(password)) == nil
}
```

`CompareHashAndPassword` reads the salt and cost from `stored`, hashes the attempt, and compares
in constant time. `== nil` is a match; any error, including `ErrMismatchedHashAndPassword`, is
not. You never re-hash and compare with `==` yourself.

Issuing a token.

```go
var secret = []byte(os.Getenv("JWT_SECRET"))   // 32+ random bytes

func issueToken(username string) (string, error) {
	claims := jwt.RegisteredClaims{
		Subject:   username,
		IssuedAt:  jwt.NewNumericDate(time.Now()),
		ExpiresAt: jwt.NewNumericDate(time.Now().Add(15 * time.Minute)),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(secret)
}
```

`jwt.RegisteredClaims` is the standard set, `Subject`, `IssuedAt`, `ExpiresAt`, so you do not
hand-name `sub`, `iat`, `exp`. `SigningMethodHS256` picks HMAC-SHA256, and `SignedString` seals
it with the secret.

Verifying, with the key function that asserts the method.

```go
func verifyToken(tokenString string) (string, error) {
	token, err := jwt.Parse(tokenString, func(t *jwt.Token) (any, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
		}
		return secret, nil
	})
	if err != nil {
		return "", err
	}
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return "", errors.New("invalid token")
	}
	return claims["sub"].(string), nil
}
```

The key function is the barman. It checks `t.Method` is an HMAC method and only then returns the
secret; a token claiming `none` or `RS256` fails here, before any signature is trusted.
`jwt.Parse` also checks `exp`, so an expired token comes back as an error. This is the shape you
must reproduce every time; golang-jwt cannot pin the algorithm for you because you might legitimately
accept several.

Run it:

```bash
JWT_SECRET=a-long-random-secret-of-at-least-32-bytes go run main.go
```

```text
right password: true
wrong password: false
verified as: meera
tampered -> token signature is invalid: signature is invalid
expired -> token has invalid claims: token is expired
wrong secret -> token signature is invalid: signature is invalid
alg none -> unexpected signing method: none
```

The password check passes and fails correctly, the good token verifies, and a tampered token, an
expired one, one signed with a different secret, and a forged `alg: none` token all fail, the last
one caught by the key function's method assertion.

Here is the whole program in one piece, `main.go`:

```go
package main

import (
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

var users = map[string][]byte{}
var secret = []byte(os.Getenv("JWT_SECRET"))

func register(username, password string) error {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	users[username] = hash
	return nil
}

func checkPassword(username, password string) bool {
	stored, ok := users[username]
	if !ok {
		return false
	}
	return bcrypt.CompareHashAndPassword(stored, []byte(password)) == nil
}

func issueToken(username string) (string, error) {
	claims := jwt.RegisteredClaims{
		Subject:   username,
		IssuedAt:  jwt.NewNumericDate(time.Now()),
		ExpiresAt: jwt.NewNumericDate(time.Now().Add(15 * time.Minute)),
	}
	return jwt.NewWithClaims(jwt.SigningMethodHS256, claims).SignedString(secret)
}

func verifyToken(tokenString string) (string, error) {
	token, err := jwt.Parse(tokenString, func(t *jwt.Token) (any, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
		}
		return secret, nil
	})
	if err != nil {
		return "", err
	}
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return "", errors.New("invalid token")
	}
	sub, _ := claims["sub"].(string)
	return sub, nil
}

func report(label string, sub string, err error) {
	if err != nil {
		fmt.Printf("%s -> %v\n", label, err)
	} else {
		fmt.Printf("%s -> %s\n", label, sub)
	}
}

func main() {
	if err := register("meera", "hunter2"); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("right password:", checkPassword("meera", "hunter2"))
	fmt.Println("wrong password:", checkPassword("meera", "wrong"))

	token, _ := issueToken("meera")
	sub, err := verifyToken(token)
	report("verified as", sub, err)

	sub, err = verifyToken(token[:len(token)-3] + "abc")
	report("tampered", sub, err)

	expired := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.RegisteredClaims{
		Subject: "meera", ExpiresAt: jwt.NewNumericDate(time.Now().Add(-time.Second))})
	expiredStr, _ := expired.SignedString(secret)
	sub, err = verifyToken(expiredStr)
	report("expired", sub, err)

	other := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.RegisteredClaims{Subject: "meera"})
	otherStr, _ := other.SignedString([]byte("a-different-secret-of-at-least-32-bytes!"))
	sub, err = verifyToken(otherStr)
	report("wrong secret", sub, err)

	none := jwt.NewWithClaims(jwt.SigningMethodNone, jwt.RegisteredClaims{Subject: "admin"})
	noneStr, _ := none.SignedString(jwt.UnsafeAllowNoneSignatureType)
	sub, err = verifyToken(noneStr)
	report("alg none", sub, err)
}
```

## 6. How the other two languages do it

**Python**

```python
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
bcrypt.checkpw(password.encode(), hashed)          # True / False
jwt.decode(token, SECRET, algorithms=["HS256"])    # algorithms= is the algorithm allow-list
```

Same bcrypt, and PyJWT pins the algorithm with the `algorithms=` argument rather than a key
function. The salt is inside the hash exactly as in Go.

**C++**

```cpp
std::string hash = argon2::hash(password);   // libsodium crypto_pwhash_str
auto verifier = jwt::verify().allow_algorithm(jwt::algorithm::hs256{secret});
```

libsodium's argon2 for the hash, and `jwt-cpp`'s `allow_algorithm` as the allow-list, the same
guard as Go's key function and Python's `algorithms=`.

**The difference that matters:** the algorithm pin is a key function in Go, a keyword argument in
Python, and a builder call in C++. Go's form is the most error-prone, because the key function is
code you write on every verify and can write wrong by simply returning the secret; Python's and
C++'s are one argument you either pass or forget. The defence is the same in all three, and it is
the single most important line in JWT verification: assert the algorithm before you trust the
signature.

## 7. The traps

**The near-miss: a fast hash.**

```go
sum := sha256.Sum256([]byte(password))
users[username] = sum[:]
```

SHA-256 is fast and unsalted, so a stolen database is cracked at billions of guesses a second and
identical passwords collide. A password hash must be slow and salted: bcrypt or argon2, never the
`crypto/sha256` family.

**The key function that does not assert the method.**

```go
token, err := jwt.Parse(tokenString, func(t *jwt.Token) (any, error) {
	return secret, nil   // no method check
})
```

It works for honest tokens and opens the `alg: none` and algorithm-confusion holes: a token that
names `none` is accepted because you never checked. Older golang-jwt would accept it outright;
current versions reject `none` unless you opt in, but algorithm confusion (an attacker signing
with a public key you expose) still needs the method assertion. Always assert
`t.Method.(*jwt.SigningMethodHMAC)`.

**A short or empty secret.** `os.Getenv("JWT_SECRET")` returning `""` because the variable was
not set means every token is signed with the empty key, which anyone can reproduce. Check the
secret is present and long at start-up and refuse to run without it, as on
[day 51](../day-051-why-sorting-matters/README.md).

**Reusing bcrypt's output the wrong way.** `bcrypt.GenerateFromPassword` on the same password
twice gives different hashes, so you cannot store one and compare with `==`; you must use
`CompareHashAndPassword`, which reads the salt from the stored hash. And bcrypt truncates input
past 72 bytes, so very long passphrases silently lose their tail; pre-hash with SHA-256 to bytes
first if you must accept long ones.

**Secrets in the token.** A JWT is signed, not encrypted; the payload is base64, readable by
anyone. Decode `eyJ...` and you see the claims. No password, card number, or private data in it.

**No expiry.** Omit `ExpiresAt` and the token is a permanent credential. Always set it, short,
and use a refresh flow for longer sessions.

**Logging the token or password.** Both are on [day 52](../day-052-quadratic-sorts/README.md)'s
never-log list. A token in a log is a live credential until it expires.

## 8. Say it out loud

**How it gets asked**

- How do you store a password?
- What does the key function in golang-jwt have to do?
- What is a salt and a work factor?
- What is the `alg: none` attack?

**The ninety-second script**

Never store the password; store a slow, salted hash with `bcrypt.GenerateFromPassword`, and on
login use `bcrypt.CompareHashAndPassword`, which reads the salt from the stored hash and compares
in constant time. Slow defeats brute force on a stolen database, because a fast hash like SHA-256
allows billions of guesses a second; the salt, stored inside the hash, means identical passwords
hash differently so precomputed tables fail. Never encrypt a password, because encryption is
reversible. For sessions I issue a JWT: registered claims with a subject and a short expiry,
signed HS256 with a secret only the server holds. Verifying takes a key function, and the one
thing it must do is assert the signing method is HMAC before returning the secret, because a key
function that returns the secret unconditionally accepts a forged `alg: none` token or an
algorithm-confusion token. The secret is long and from the environment, expiry is always set, and
nothing secret goes in the token because it is signed, not encrypted.

**The follow-ups**

- **Why a key function and not a fixed key?** *Because you might accept more than one key, for
  rotation, and golang-jwt gives you the token so you can inspect its `kid` header to pick the
  right one. The price of that flexibility is that pinning the algorithm is your responsibility,
  in that function.*
- **Where does verification live in a service?** *The auth middleware from
  [day 49](../day-049-peak-finding/README.md): read `Authorization: Bearer <token>`,
  `verifyToken`, put the subject on the request context, or 401.*
- **How do you revoke a JWT?** *You cannot directly; that is the cost of stateless. Short
  expiries so a stolen token dies soon, and a server-side deny-list for immediate revocation when
  it matters, which trades some of the statelessness back.*

**A model answer**

"Store a slow salted hash with `bcrypt.GenerateFromPassword`; check with
`CompareHashAndPassword`, which is constant-time and reads the salt from the hash. Slow beats
brute force, salt beats rainbow tables, and never encryption because that is reversible. Sessions
are a JWT: registered claims, short `ExpiresAt`, HS256 signed with an environment secret. On
verify, the key function must assert `t.Method` is HMAC before returning the secret, or the
`alg: none` forgery works. Nothing secret in the token, because it is signed, not encrypted."

## 9. Recall card

- Never store the password: `bcrypt.GenerateFromPassword([]byte(pw), bcrypt.DefaultCost)`; check with `bcrypt.CompareHashAndPassword(stored, attempt) == nil`. Never a fast hash, never encryption.
- Salt (inside the hash) defeats rainbow tables; the work factor makes each guess slow; comparison is constant-time. bcrypt truncates past 72 bytes.
- JWT: `jwt.NewWithClaims(jwt.SigningMethodHS256, claims).SignedString(secret)` with `RegisteredClaims{Subject, ExpiresAt}`.
- Verify with a key function that asserts `t.Method.(*jwt.SigningMethodHMAC)` before returning the secret, or `alg: none` and algorithm confusion get in.
- Signed, not encrypted: no secrets in the payload; always set `ExpiresAt`; secret is long and from the environment.
